from myhdl import *
from BasicModule import *
from Interface import *
from ComparisonApproxMult import *
from KoggeStoneAdder import *
from BrentKungAdder import *
import sys
@block
def PPG(OUTS,A,B,width):
    startIndex = 0; endIndex = 0;
    instances_list = [];
    outs = [];
    for i in range(2*width-1):
        col_len = width - abs(i-width+1);
        endIndex += col_len;
        col_sigs_list = [Signal(intbv(0)[1:]) for j in range(col_len)];
        #col_sigs = ConcatSignal(*reversed(col_sigs_list));
        for j in range(col_len):
            #out_tmp = Signal(intbv(0)[1:]);
            if i <= width-1:
                AND_1 = AND(col_sigs_list[j],A(i-j),B(j)); # instances' output can't be parts of a bit vector
                #print("%s %s %s" % (startIndex + j,i-j,j));
                #print("%s*%s " % (i-j,j))
            else:
                AND_1 = AND(col_sigs_list[j],A(width-1-j),B(i+j+1-width));
                #print("%s*%s " % (width-1-j,i+j+1-width));
                #print("%s %s %s" % (startIndex + j,width-1-j,i+j+1-width));
            instances_list.append(AND_1);
        #print("------------")
        outs += list(reversed(col_sigs_list));
        #outs += col_sigs_list;
        startIndex = endIndex;
    outs_vec = ConcatSignal(*reversed(outs));  # can't be put into alway_comb section
                                               # in converted verilog files, the concat signals are the same ones in sig list
    @always_comb
    def comb():
        OUTS.next = outs_vec;
    return instances_list,comb;

def convert_PPG(hdl):
    width = 8;
    A= Signal(intbv(0)[width:]);
    B = Signal(intbv(0)[width:]);
    total_nOUTbits = width*width;
    OUTS = Signal(intbv(0)[total_nOUTbits:]);
    PPG_1 = PPG(OUTS,A,B,width);
    PPG_1.convert(hdl);

@block
def test_PPG():
    width = 8;
    A= Signal(intbv(0)[width:]);
    B = Signal(intbv(0)[width:]);
    total_nOUTbits = width*width;
    OUTS = Signal(intbv(0)[total_nOUTbits:]);
    PPG_1 = PPG(OUTS,A,B,width);
    @instance
    def simu():
        print("A B OUT_SIMU OUT_EXACT");
        #for i in range(12):
        #a = random.randint(0,pow(2,width)-1); b = random.randint(0,pow(2,width)-1);
        A.next = intbv(255)[width:];
        B.next = intbv(7)[width:];
        yield delay(10);
        mult = 0;
        startIndex = 0; endIndex = 0;
        print(OUTS);
        for i in range(2*width-1):
            col_len = width - abs(i-width+1);
            endIndex = startIndex + col_len;
            sum_col = 0;
            for j in range(startIndex,endIndex):
                sum_col += OUTS[j];
                print(OUTS[j])
            print("---------");
            mult += pow(2,i)*sum_col;
            startIndex = endIndex;
            
        #print("%s %s  %s  %s" % (a,b,mult,a*b));
    return instances();

@block
def CompressorTree(OUTS,INPUTS,width,stages):
    cols_sig_list_currentStage = [];
    cols_sig_list_nextStage = [];
    instances_list = [];
    # initialize
    startIndex = 0; endIndex = 0;
    for i in range(len(stages[0])):
        col_len = stages[0][i].col_len;
        endIndex += col_len;
        tmp_list = [];
        for j in range(startIndex,endIndex):
            tmp_list.append(INPUTS(j));
        startIndex = endIndex;
        cols_sig_list_currentStage.append(tmp_list);
    for i in range(len(stages)-1):
        # remaining bits, AC42, AC32, f, h, fc, hc
        cols_sig_list_nextStage = [];
        for j in range(len(stages[i+1])):
            total_bits = stages[i+1][j].col_len;
            cols_sig_list_nextStage.append([Signal(intbv(0)[1:]) for k in range(total_bits)]);
        for j in range(len(stages[i])):
            # current stage
            # indexs of corresponding input bits in current column
            iRbs_list = stages[i][j].rbs; 
            iAC42_list = stages[i][j].ac42;
            iAC32_list = stages[i][j].ac32;
            iF_list = stages[i][j].f;
            iH_list = stages[i][j].h;
            # next stage
            # the number of corresponding output signals in next stage's column
            nRbs_out = stages[i+1][j].nRbs_out;
            nAC42_out = stages[i+1][j].nAC42_out;
            nAC32_out = stages[i+1][j].nAC32_out;
            nF_out = stages[i+1][j].nF_out;
            nH_out = stages[i+1][j].nH_out;
            nFC_out = stages[i+1][j].nFC_out;
            nHC_out = stages[i+1][j].nHC_out;
            if j != len(stages[i])-1:
                nRbs_lout = stages[i+1][j+1].nRbs_out;
                nAC42_lout = stages[i+1][j+1].nAC42_out;
                nAC32_lout = stages[i+1][j+1].nAC32_out;
                nF_lout = stages[i+1][j+1].nF_out;
                nH_lout = stages[i+1][j+1].nH_out;
                nFC_lout = stages[i+1][j+1].nFC_out;
                nHC_lout = stages[i+1][j+1].nHC_out;

            # connect remaining bits
            startIndex = 0; endIndex = startIndex + nRbs_out - 1;
            for k in range(len(iRbs_list)):
                cols_sig_list_nextStage[j][startIndex+k] = cols_sig_list_currentStage[j][iRbs_list[k]];
            # connect AC42 output bits
            startIndex = endIndex + 1; endIndex = startIndex + nAC42_out - 1;
            for k in range(len(iAC42_list)):
                AC42_ins = AC42(cols_sig_list_nextStage[j][startIndex+k*2],cols_sig_list_nextStage[j][startIndex+k*2+1],\
                    cols_sig_list_currentStage[j][iAC42_list[k][0]],cols_sig_list_currentStage[j][iAC42_list[k][1]],\
                    cols_sig_list_currentStage[j][iAC42_list[k][2]],cols_sig_list_currentStage[j][iAC42_list[k][3]]);
                instances_list.append(AC42_ins);
            # connect AC32 output bits
            startIndex = endIndex + 1; endIndex = startIndex + nAC32_out - 1;
            for k in range(len(iAC32_list)):
                AC32_ins = AC32(cols_sig_list_nextStage[j][startIndex+k*2],cols_sig_list_nextStage[j][startIndex+k*2+1],\
                    cols_sig_list_currentStage[j][iAC32_list[k][0]],cols_sig_list_currentStage[j][iAC32_list[k][1]],\
                    cols_sig_list_currentStage[j][iAC32_list[k][2]]);
                instances_list.append(AC32_ins);
            # connect FA output bits
            startIndex = endIndex + 1; endIndex = startIndex + nF_out - 1;
            startIndex_l = nRbs_lout + nAC42_lout + nAC32_lout + nF_lout + nH_lout; endIndex_l = startIndex_l + nFC_lout - 1;
            for k in range(len(iF_list)):
                F_ins = FA(cols_sig_list_nextStage[j+1][startIndex_l+k],cols_sig_list_nextStage[j][startIndex+k],\
                    cols_sig_list_currentStage[j][iF_list[k][0]],cols_sig_list_currentStage[j][iF_list[k][1]],\
                    cols_sig_list_currentStage[j][iF_list[k][2]]);
                #print("FA cout: %s %s %s; sum: %s %s %s" % (i+1,j+1,startIndex_l+k,i+1,j,startIndex+k));
                instances_list.append(F_ins);
            # connect HA output bits
            startIndex = endIndex + 1; endIndex = startIndex + nH_out - 1;
            startIndex_l = endIndex_l + 1; endIndex_l = startIndex_l + nHC_lout - 1;
            for k in range(len(iH_list)):
                H_ins = HA(cols_sig_list_nextStage[j+1][startIndex_l+k],cols_sig_list_nextStage[j][startIndex+k],\
                    cols_sig_list_currentStage[j][iH_list[k][0]],cols_sig_list_currentStage[j][iH_list[k][1]]);
                #print("HA cout: %s %s %s; sum: %s %s %s" % (i+1,j+1,startIndex_l+k,i+1,j,startIndex+k));
                instances_list.append(H_ins);
        cols_sig_list_currentStage = cols_sig_list_nextStage;
    outs_list = [];
    for i in range(len(cols_sig_list_currentStage)):
        outs_list += cols_sig_list_currentStage[i];
    outs_vec = ConcatSignal(*reversed(outs_list));  # can't be put into alway_comb section
                                               # in converted verilog files, the concat signals are the same ones in sig list
    @always_comb
    def comb():
        OUTS.next = outs_vec;
    return instances_list,comb;

def convert_CT(hdl,stages):
    width = 8;
    nInBits = width*width;
    INPUTS = Signal(intbv(0)[nInBits:]);
    last_stage = stages[len(stages)-1];
    nOutBits = 0;
    for i in range(len(last_stage)-1):
        nOutBits += last_stage[i].col_len;
    OUTS = Signal(intbv(0)[nOutBits:]);
    CT1 = CompressorTree(OUTS,INPUTS,width,stages);
    CT1.convert(hdl);

@block
def Multiplier(A,B,OUTS,width,stages):
    nOutBits_ppg = width*width;
    OutBits_ppg = Signal(intbv(0)[nOutBits_ppg:]);
    PPG_1 = PPG(OutBits_ppg,A,B,width);
    CT_1 = CompressorTree(OUTS,OutBits_ppg,width,stages);
    return instances();

@block
def Multiplier_KoggeStone(A,B,OUTS,stages,width):
    last_stage = stages[len(stages)-1];
    inputs_len = 0;
    columns = [];
    for i in range(len(last_stage)):
        if last_stage[i].col_len != 0:
            columns.append(last_stage[i].col_len);
            inputs_len += last_stage[i].col_len;
    OutBits_ct = Signal(intbv(0)[inputs_len:]);
    Multiplier_ins = Multiplier(A,B,OutBits_ct,width,stages);
    KoggeStone_ins = KoggeStone(OUTS,OutBits_ct,columns);
    return instances();

@block
def Multiplier_BrentKung(A,B,OUTS,stages,width):
    last_stage = stages[len(stages)-1];
    inputs_len = 0;
    columns = [];
    for i in range(len(last_stage)):
        if last_stage[i].col_len != 0:
            columns.append(last_stage[i].col_len);
            inputs_len += last_stage[i].col_len;
    OutBits_ct = Signal(intbv(0)[inputs_len:]);
    Multiplier_ins = Multiplier(A,B,OutBits_ct,width,stages);
    BrentKung_ins = BrentKung(OUTS,OutBits_ct,columns);
    return instances();

def convert_Multiplier(hdl,stages,width):
    A= Signal(intbv(0)[width:]);
    B = Signal(intbv(0)[width:]);
    #stages = ParseJson("CompressorTree.json");
    nOutBits = 0;
    last_stage = stages[len(stages)-1];
    for i in range(len(last_stage)):
        nOutBits += last_stage[i].col_len;
    OUTS = Signal(intbv(0)[nOutBits:]);
    Multiplier_1 = Multiplier(A,B,OUTS,width,stages);
    Multiplier_1.convert(hdl);

def convert_Multiplier_KoggeStone(hdl,stages,width):
    A= Signal(intbv(0)[width:]);
    B = Signal(intbv(0)[width:]);
    last_stage = stages[len(stages)-1];
    outputs_len = 0;
    for i in range(len(last_stage)):
        if last_stage[i].col_len != 0:
            outputs_len += 1;
    outputs_len += 1;
    OUTS = Signal(intbv(0)[outputs_len:]);
    Multiplier_KoggeStone_ins = Multiplier_KoggeStone(A,B,OUTS,stages,width);
    Multiplier_KoggeStone_ins.convert(hdl);

def convert_Multiplier_BrentKung(hdl,stages,width):
    A= Signal(intbv(0)[width:]);
    B = Signal(intbv(0)[width:]);
    last_stage = stages[len(stages)-1];
    outputs_len = 0;
    for i in range(len(last_stage)):
        if last_stage[i].col_len != 0:
            outputs_len += 1;
    outputs_len += 1;
    OUTS = Signal(intbv(0)[outputs_len:]);
    Multiplier_BrentKung_ins = Multiplier_BrentKung(A,B,OUTS,stages,width);
    Multiplier_BrentKung_ins.convert(hdl);


@block
def test_Multiplier_KoggeStone(stages,width):
    A= Signal(intbv(0)[width:]);
    B = Signal(intbv(0)[width:]);
    #stages = ParseJson("CompressorTree.json");
    last_stage = stages[len(stages)-1];
    nOutBits = 0;
    for i in range(len(last_stage)):
        if last_stage[i].col_len != 0:
            nOutBits += 1;
    nOutBits += 1;
    OUTS = Signal(intbv(0)[nOutBits:]);
    Multiplier_KoggeStone_ins = Multiplier_KoggeStone(A,B,OUTS,stages,width);
    @instance
    def simu():
        print("A B OUT_SIMU OUT_EXACT");
        f = open(sys.argv[3],mode='a+')
        #print("test!!!!!!!!!",file = f);
        error_times = 0; test_times = 0; error_sum = 0; error_normalized_sum = 0;
        for i in range(int(pow(2,width)-1),-1,-1):
            for j in range(int(pow(2,width))):
                #a = random.randint(0,pow(2,width)-1); b = random.randint(0,pow(2,width)-1);
                A.next = intbv(i)[width:];
                B.next = intbv(j)[width:];
                yield delay(10);
                mult = 0;
                test_times += 1;
                for k in range(nOutBits):
                    mult += pow(2,k)*OUTS[k];
                print("%s %s  %s  %s" % (i,j,mult,i*j));
                if mult != i*j:
                    error_times += 1;
                    error_sum += int(math.fabs(mult-i*j));
                    error_normalized_sum += math.fabs(mult-i*j)/(i*j);
                    print("Error distance is %s" % (int(math.fabs(mult-i*j))));
                    #print("Error distance is %s" % (int(math.fabs(mult-i*j))),file = f);
                    print("The total wrong times is %s" % (error_times));
                    #print("The total wrong times is %s" % (error_times),file = f);
                    print("The error rate is %s" % (float(error_times)/test_times));
                    #print("The error rate is %s" % (float(error_times)/test_times),file = f);
        print("The final MED is %s" % (float(error_sum)/test_times));
        print("The sum of error distance is %s" % (error_sum),file = f);
        print("The final MED is %s" % (float(error_sum)/test_times),file = f);
        print("The final error rate is %s" % (float(error_times)/test_times));
        print("The total error time is %s" % (error_times),file=f);
        print("The final error rate is %s" % (float(error_times)/test_times),file = f);
        print("The final normalized MED is %s" % (float(error_normalized_sum)/test_times));
        print("The final normalized MED is %s" % (float(error_normalized_sum)/test_times),file = f);
        f.close();
    return instances();

@block
def test_Multiplier(stages,width):
    A= Signal(intbv(0)[width:]);
    B = Signal(intbv(0)[width:]);
    #stages = ParseJson("CompressorTree.json");
    nOutBits = 0;
    last_stage = stages[len(stages)-1];
    for i in range(len(last_stage)):
        nOutBits += last_stage[i].col_len;
    OUTS = Signal(intbv(0)[nOutBits:]);
    Multiplier_1 = Multiplier(A,B,OUTS,width,stages);
    @instance
    def simu():
        print("A B OUT_SIMU OUT_EXACT");
        f = open(sys.argv[3],mode='a+')
        #print("test!!!!!!!!!",file = f);
        error_times = 0; test_times = 0; error_sum = 0; error_normalized_sum = 0;
        for i in range(int(pow(2,width)-1),-1,-1):
            for j in range(int(pow(2,width))):
                #a = random.randint(0,pow(2,width)-1); b = random.randint(0,pow(2,width)-1);
                A.next = intbv(i)[width:];
                B.next = intbv(j)[width:];
                yield delay(10);
                mult = 0;
                startIndex = 0; endIndex = 0;
                last_stage = stages[len(stages)-1];
                test_times += 1;
                for k in range(len(last_stage)):
                    col_len = last_stage[k].col_len;
                    endIndex = startIndex + col_len;
                    sum_col = 0;
                    for l in range(startIndex,endIndex):
                        sum_col += OUTS[l];  # OUTS()->Signal; OUTS[]->Signal's value
                    mult += pow(2,k)*sum_col;
                    startIndex = endIndex;
                print("%s %s  %s  %s" % (i,j,mult,i*j));
                if mult != i*j:
                    error_times += 1;
                    error_sum += int(math.fabs(mult-i*j));
                    error_normalized_sum += math.fabs(mult-i*j)/(i*j);
                    print("Error distance is %s" % (int(math.fabs(mult-i*j))));
                    #print("Error distance is %s" % (int(math.fabs(mult-i*j))),file = f);
                    print("The total wrong times is %s" % (error_times));
                    #print("The total wrong times is %s" % (error_times),file = f);
                    print("The error rate is %s" % (float(error_times)/test_times));
                    #print("The error rate is %s" % (float(error_times)/test_times),file = f);
        print("The final MED is %s" % (float(error_sum)/test_times));
        print("The sum of error distance is %s" % (error_sum),file = f);
        print("The final MED is %s" % (float(error_sum)/test_times),file = f);
        print("The final error rate is %s" % (float(error_times)/test_times));
        print("The total error time is %s" % (error_times),file=f);
        print("The final error rate is %s" % (float(error_times)/test_times),file = f);
        print("The final normalized MED is %s" % (float(error_normalized_sum)/test_times));
        print("The final normalized MED is %s" % (float(error_normalized_sum)/test_times),file = f);
        f.close();
                #print(OUTS);
    return instances();

@block
def test_CMP_Multiplier_KoggeStone(width,truncWidth,height_evolution):
    A= Signal(intbv(0)[width:]);
    B = Signal(intbv(0)[width:]);
    nOutBits = 0;
    last_bm_size = get_finalstage_size(width,truncWidth,height_evolution);
    for i in range(len(last_bm_size)):
        if last_bm_size[i] != 0:
            nOutBits += 1;
    nOutBits += 1;
    OUTS = Signal(intbv(0)[nOutBits:]);
    CMP_Multiplier_KoggeStone_ins = CMP_Multiplier_KoggeStone(OUTS,A,B,width,truncWidth,height_evolution);
    @instance
    def simu():
        print("A B OUT_SIMU OUT_EXACT");
        file = 'CMP_multiplier_simu_'+str(width)+'.txt';
        f = open(file,mode='w')
        #print("test!!!!!!!!!",file = f);
        error_times = 0; test_times = 0; error_sum = 0; error_normalized_sum = 0;
        for i in range(int(pow(2,width)-1),-1,-1):
            for j in range(int(pow(2,width))):
                #a = random.randint(0,pow(2,width)-1); b = random.randint(0,pow(2,width)-1);
                A.next = intbv(i)[width:];
                B.next = intbv(j)[width:];
                yield delay(10);
                mult = 0;
                test_times += 1;
                for k in range(nOutBits):
                    mult += pow(2,k)*OUTS[k];
                print("%s %s  %s  %s" % (i,j,mult,i*j));
                if mult != i*j:
                    error_times += 1;
                    error_sum += int(math.fabs(mult-i*j));
                    error_normalized_sum += math.fabs(mult-i*j)/(i*j);
                    print("Error distance is %s" % (int(math.fabs(mult-i*j))));
                    #print("Error distance is %s" % (int(math.fabs(mult-i*j))),file = f);
                    print("The total wrong times is %s" % (error_times));
                    #print("The total wrong times is %s" % (error_times),file = f);
                    print("The error rate is %s" % (float(error_times)/test_times));
                    #print("The error rate is %s" % (float(error_times)/test_times),file = f);
        print("The final MED is %s" % (float(error_sum)/test_times));
        print("The sum of error distance is %s" % (error_sum),file = f);
        print("The final MED is %s" % (float(error_sum)/test_times),file = f);
        print("The final error rate is %s" % (float(error_times)/test_times));
        print("The total error time is %s" % (error_times),file=f);
        print("The final error rate is %s" % (float(error_times)/test_times),file = f);
        print("The final normalized MED is %s" % (float(error_normalized_sum)/test_times));
        print("The final normalized MED is %s" % (float(error_normalized_sum)/test_times),file = f);
        f.close();
    return instances();

@block
def test_CMP_Multiplier(width,truncWidth,height_evolution):
    #width = 8;
    #truncWidth = 10;
    A= Signal(intbv(0)[width:]);
    B = Signal(intbv(0)[width:]);
    nOutBits = 0;
    last_bm_size = get_finalstage_size(width,truncWidth,height_evolution);
    for i in range(len(last_bm_size)):
        nOutBits += last_bm_size[i];
    OUTS = Signal(intbv(0)[nOutBits:]);
    CMP_Multiplier_ins = CMP_Multiplier(OUTS,A,B,width,truncWidth,height_evolution);
    @instance
    def simu():
        file = 'ISCAS_CMP_multiplier_simu_'+str(width)+'.txt';
        f = open(file,'w')
        error_times = 0; test_times = 0; error_sum = 0;
        for i in range(int(pow(2,width)-1),-1,-1):
            for j in range(int(pow(2,width))):
                #a = random.randint(0,pow(2,width)-1); b = random.randint(0,pow(2,width)-1);
                A.next = intbv(i)[width:];
                B.next = intbv(j)[width:];
                yield delay(10);
                mult = 0;
                startIndex = 0; endIndex = 0;
                test_times += 1;
                for k in range(len(last_bm_size)):
                    col_len = last_bm_size[k];
                    endIndex = startIndex + col_len;
                    sum_col = 0;
                    for l in range(startIndex,endIndex):
                        sum_col += OUTS[l];  # OUTS()->Signal; OUTS[]->Signal's value
                    mult += pow(2,k)*sum_col;
                    startIndex = endIndex;
                print("%s %s  %s  %s" % (i,j,mult,i*j));
                if mult != i*j:
                    error_times += 1;
                    error_sum += int(math.fabs(mult-i*j));
                    print("Error distance is %s" % (int(math.fabs(mult-i*j))));
                    #print("Error distance is %s" % (int(math.fabs(mult-i*j))),file = f);
                    print("The total wrong times is %s" % (error_times));
                    #print("The total wrong times is %s" % (error_times),file = f);
                    print("The error rate is %s" % (float(error_times)/test_times));
                    #print("The error rate is %s" % (float(error_times)/test_times),file = f);
        print("The final MED is %s" % (float(error_sum)/test_times));
        print("The sum of error distance is %s" % (error_sum),file = f);
        print("The final MED is %s" % (float(error_sum)/test_times),file = f);
        print("The final error rate is %s" % (float(error_times)/test_times));
        print("The total error time is %s" % (error_times),file=f);
        print("The final error rate is %s" % (float(error_times)/test_times),file = f);
        f.close();
    return instances();

@block
def CMP_Multiplier(OUTS,A,B,width,truncWidth,height_evolution):
    nOutBits_ppg = width*width;
    OutBits_ppg = Signal(intbv(0)[nOutBits_ppg:]);
    PPG_1 = PPG(OutBits_ppg,A,B,width);
    #last_bm_size = get_finalstage_size(width,truncWidth);
    #nOutBits = 0;
    #for i in range(len(last_bm_size)):
    #    nOutBits += last_bm_size[i];
    iscas_ins = ISCAS18(OUTS,OutBits_ppg,width,truncWidth,height_evolution);
    return instances();

@block
def CMP_Multiplier_KoggeStone(OUTS,A,B,width,truncWidth,height_evolution):
    last_bm_size = get_finalstage_size(width,truncWidth,height_evolution);
    nOutBits = 0;
    columns = [];
    for i in range(len(last_bm_size)):
        if last_bm_size[i] != 0:
            nOutBits += last_bm_size[i];
            columns.append(last_bm_size[i]);
    CT_OUTS = Signal(intbv(0)[nOutBits:]);
    CMP_Multiplier_ins = CMP_Multiplier(CT_OUTS,A,B,width,truncWidth,height_evolution);
    KoggeStone_ins = KoggeStone(OUTS,CT_OUTS,columns);
    return instances();

def convert_CMP_Multiplier_KoggeStone(hdl,width,truncWidth,height_evolution):
    A= Signal(intbv(0)[width:]);
    B = Signal(intbv(0)[width:]);
    last_bm_size = get_finalstage_size(width,truncWidth,height_evolution);
    nOutBits = 0;
    for i in range(len(last_bm_size)):
        if last_bm_size[i] != 0:
            nOutBits += 1;
    nOutBits += 1;
    OUTS = Signal(intbv(0)[nOutBits:]);
    CMP_Multiplier_KoggeStone_ins = CMP_Multiplier_KoggeStone(OUTS,A,B,width,truncWidth,height_evolution);
    CMP_Multiplier_KoggeStone_ins.convert(hdl);

def convert_CMP_Multiplier(hdl,width,truncWidth,height_evolution):
    #width = 8;
    #truncWidth = 10;
    A= Signal(intbv(0)[width:]);
    B = Signal(intbv(0)[width:]);
    #stages = ParseJson("CompressorTree.json");
    last_bm_size = get_finalstage_size(width,truncWidth,height_evolution);
    nOutBits = 0;
    for i in range(len(last_bm_size)):
        nOutBits += last_bm_size[i];
    OUTS = Signal(intbv(0)[nOutBits:]);
    CMP_Multiplier_1 = CMP_Multiplier(OUTS,A,B,width,truncWidth,height_evolution);
    CMP_Multiplier_1.convert(hdl);

@block
def TCAS_CMP_Multiplier(OUTS,A,B,width,evol_stages):
    nOutBits_ppg = width*width;
    OutBits_ppg = Signal(intbv(0)[nOutBits_ppg:]);
    PPG_1 = PPG(OutBits_ppg,A,B,width);
    tcas_ins = TCAS18(OUTS,OutBits_ppg,width,evol_stages);
    return instances();

@block
def TCAS_CMP_Multiplier_KoggeStone(OUTS,A,B,width,evol_stages):
    last_bm_size = tcas_finalstage_size(width,evol_stages);
    nOutBits = 0; columns = [];
    for i in range(len(last_bm_size)):
        if last_bm_size[i] != 0:
            nOutBits += last_bm_size[i];
            columns.append(last_bm_size[i]);
    CT_OUTS = Signal(intbv(0)[nOutBits:]);
    TCAS_CMP_Multiplier_ins = TCAS_CMP_Multiplier(CT_OUTS,A,B,width,evol_stages);
    KoggeStone_ins_ins = KoggeStone(OUTS,CT_OUTS,columns);
    return instances();

def convert_TCAS_CMP_Multiplier(hdl,width,evol_stages):
    #width = 12;
    A= Signal(intbv(0)[width:]);
    B = Signal(intbv(0)[width:]);
    #stages = ParseJson("CompressorTree.json");
    last_bm_size = tcas_finalstage_size(width,evol_stages);
    nOutBits = 0;
    for i in range(len(last_bm_size)):
        nOutBits += last_bm_size[i];
    OUTS = Signal(intbv(0)[nOutBits:]);
    tcas_ins = TCAS_CMP_Multiplier(OUTS,A,B,width,evol_stages);
    tcas_ins.convert(hdl);

def convert_TCAS_CMP_Multiplier_KoggeStone(hdl,width,evol_stages):
    A= Signal(intbv(0)[width:]);
    B = Signal(intbv(0)[width:]);
    #stages = ParseJson("CompressorTree.json");
    nOutBits = 0;
    last_bm_size = tcas_finalstage_size(width,evol_stages);
    for i in range(len(last_bm_size)):
        if last_bm_size[i] != 0:
            nOutBits += 1;
    nOutBits += 1;
    OUTS = Signal(intbv(0)[nOutBits:]);
    TCAS_CMP_Multiplier_KoggeStone_ins = TCAS_CMP_Multiplier_KoggeStone(OUTS,A,B,width,evol_stages);
    TCAS_CMP_Multiplier_KoggeStone_ins.convert(hdl);

@block
def test_TCAS_CMP_Multiplier(width,evol_stages):
    #width = 12;
    A= Signal(intbv(0)[width:]);
    B = Signal(intbv(0)[width:]);
    nOutBits = 0;
    last_bm_size = tcas_finalstage_size(width,evol_stages);
    for i in range(len(last_bm_size)):
        nOutBits += last_bm_size[i];
    OUTS = Signal(intbv(0)[nOutBits:]);
    tcas_ins = TCAS_CMP_Multiplier(OUTS,A,B,width,evol_stages);
    @instance
    def simu():
        print("A B OUT_SIMU OUT_EXACT");
        file = 'TCAS_CMP_multiplier_simu_'+str(width)+'.txt';
        f = open(file,'w')
        error_times = 0; test_times = 0; error_sum = 0; error_normalized_sum = 0;
        for i in range(int(pow(2,width)-1),-1,-1):
            for j in range(int(pow(2,width))):
                #a = random.randint(0,pow(2,width)-1); b = random.randint(0,pow(2,width)-1);
                A.next = intbv(i)[width:];
                B.next = intbv(j)[width:];
                yield delay(10);
                mult = 0;
                startIndex = 0; endIndex = 0;
                test_times += 1;
                for k in range(len(last_bm_size)):
                    col_len = last_bm_size[k];
                    endIndex = startIndex + col_len;
                    sum_col = 0;
                    for l in range(startIndex,endIndex):
                        sum_col += OUTS[l];  # OUTS()->Signal; OUTS[]->Signal's value
                    mult += pow(2,k)*sum_col;
                    startIndex = endIndex;
                print("%s %s  %s  %s" % (i,j,mult,i*j));
                if mult != i*j:
                    error_times += 1;
                    error_sum += int(math.fabs(mult-i*j));
                    error_normalized_sum += math.fabs(mult-i*j)/(i*j);
                    print("Error distance is %s" % (int(math.fabs(mult-i*j))));
                    #print("Error distance is %s" % (int(math.fabs(mult-i*j))),file = f);
                    print("The total wrong times is %s" % (error_times));
                    #print("The total wrong times is %s" % (error_times),file = f);
                    print("The error rate is %s" % (float(error_times)/test_times));
                    #print("The error rate is %s" % (float(error_times)/test_times),file = f);
        print("The final MED is %s" % (float(error_sum)/test_times));
        print("The sum of error distance is %s" % (error_sum),file = f);
        print("The final MED is %s" % (float(error_sum)/test_times),file = f);
        print("The final error rate is %s" % (float(error_times)/test_times));
        print("The total error time is %s" % (error_times),file=f);
        print("The final error rate is %s" % (float(error_times)/test_times),file = f);
        print("The final normalized MED is %s" % (float(error_normalized_sum)/test_times));
        print("The final normalized MED is %s" % (float(error_normalized_sum)/test_times),file = f);

        f.close();
    return instances();

@block
def test_TCAS_CMP_Multiplier_KoggeStone(width,evol_stages):
    A= Signal(intbv(0)[width:]);
    B = Signal(intbv(0)[width:]);
    nOutBits = 0;
    last_bm_size = tcas_finalstage_size(width,evol_stages);
    for i in range(len(last_bm_size)):
        if last_bm_size[i] != 0:
            nOutBits += 1;
    nOutBits += 1;
    OUTS = Signal(intbv(0)[nOutBits:]);
    TCAS_CMP_Multiplier_KoggeStone_ins = TCAS_CMP_Multiplier_KoggeStone(OUTS,A,B,width,evol_stages);
    @instance
    def simu():
        print("A B OUT_SIMU OUT_EXACT");
        file = 'TCAS_CMP_multiplier_simu_'+str(width)+'.txt';
        f = open(file,'w')
        #print("test!!!!!!!!!",file = f);
        error_times = 0; test_times = 0; error_sum = 0; error_normalized_sum = 0;
        for i in range(int(pow(2,width)-1),-1,-1):
            for j in range(int(pow(2,width))):
                #a = random.randint(0,pow(2,width)-1); b = random.randint(0,pow(2,width)-1);
                A.next = intbv(i)[width:];
                B.next = intbv(j)[width:];
                yield delay(10);
                mult = 0;
                test_times += 1;
                for k in range(nOutBits):
                    mult += pow(2,k)*OUTS[k];
                print("%s %s  %s  %s" % (i,j,mult,i*j));
                if mult != i*j:
                    error_times += 1;
                    error_sum += int(math.fabs(mult-i*j));
                    error_normalized_sum += math.fabs(mult-i*j)/(i*j);
                    print("Error distance is %s" % (int(math.fabs(mult-i*j))));
                    #print("Error distance is %s" % (int(math.fabs(mult-i*j))),file = f);
                    print("The total wrong times is %s" % (error_times));
                    #print("The total wrong times is %s" % (error_times),file = f);
                    print("The error rate is %s" % (float(error_times)/test_times));
                    #print("The error rate is %s" % (float(error_times)/test_times),file = f);
        print("The final MED is %s" % (float(error_sum)/test_times));
        print("The sum of error distance is %s" % (error_sum),file = f);
        print("The final MED is %s" % (float(error_sum)/test_times),file = f);
        print("The final error rate is %s" % (float(error_times)/test_times));
        print("The total error time is %s" % (error_times),file=f);
        print("The final error rate is %s" % (float(error_times)/test_times),file = f);
        print("The final normalized MED is %s" % (float(error_normalized_sum)/test_times));
        print("The final normalized MED is %s" % (float(error_normalized_sum)/test_times),file = f);
        f.close();
    return instances();

#test_FA1= test_FA();
#test_FA1.run_sim();
#test_HA1 = test_HA();
#test_HA1.run_sim();
#test_AC42_1 = test_AC42();
#test_AC42_1.run_sim();
#test_AC32_1 = test_AC32();
#test_AC32_1.run_sim();

#convert_highorderAC("verilog");
#convert_ISCAS18("verilog");
#convert_CMP_Multiplier("verilog");
#test_CMP_Multiplier_ins = test_CMP_Multiplier();
#test_CMP_Multiplier_ins.run_sim();
#convert_PPG("verilog")
#test_PPG1 = test_PPG();
#test_PPG1.run_sim();




if __name__ == '__main__':
    #print("Test kogge stone");
    #width = 12; columns = [];
    #for i in range(width):
    #    columns.append(2);
    ##convert_KoggeStone("verilog",columns);
    #convert_BrentKung("verilog",columns);
    ##test_KoggeStone_ins = test_KoggeStone(columns);
    ##test_KoggeStone_ins.run_sim();
    #test_BrentKung_ins = test_BrentKung(columns);
    #test_BrentKung_ins.run_sim();

    if sys.argv[2] == 'ILP_ApproxMult':
        stages = ParseJson(sys.argv[1]);
        width = int(sys.argv[4]);
        #convert_Multiplier("verilog",stages,width); 
        #convert_Multiplier_KoggeStone("verilog",stages,width);
        convert_Multiplier_BrentKung("verilog",stages,width);
        #test_Multiplier1 = test_Multiplier(stages,width);
        #test_Multiplier_KoggeStone_ins = test_Multiplier_KoggeStone(stages,width);
        #test_Multiplier_BrentKung_ins = test_Multiplier_BrentKung(stages,width);
        #test_Multiplier1.run_sim();
        if int(sys.argv[5]) == 0:
            test_Multiplier_KoggeStone_ins.run_sim();
    elif sys.argv[2] == 'TCAS18':
        #width = 12; evol_stages = [6,3,2];
        #width = 16; evol_stages = [8,4,3,2];
        width = 20; evol_stages = [10,5,4,3,2];
        #width = 8; evol_stages = [4,2];
        convert_TCAS_CMP_Multiplier_KoggeStone("verilog",width,evol_stages);
        test_TCAS_CMP_Multiplier_KoggeStone_ins = test_TCAS_CMP_Multiplier_KoggeStone(width,evol_stages);
        #test_TCAS_CMP_Multiplier_KoggeStone_ins.run_sim();
        #convert_TCAS_CMP_Multiplier("verilog",width,evol_stages);
        #test_TCAS_Multiplier1 = test_TCAS_CMP_Multiplier(width,evol_stages);
        ##test_TCAS_Multiplier1.config_sim();
        #test_TCAS_Multiplier1.run_sim();
    elif sys.argv[2] == 'ISCAS20':
        #width = 12; truncWidth = 16; height_evolution = [2];
        #width = 16; truncWidth = 21; height_evolution = [3,2];
        width = 20; truncWidth = 28; height_evolution = [4,3,2];
        convert_CMP_Multiplier_KoggeStone("verilog",width,truncWidth,height_evolution);
        test_CMP_Multiplier_KoggeStone_ins = test_CMP_Multiplier_KoggeStone(width,truncWidth,height_evolution);
        #test_CMP_Multiplier_KoggeStone_ins.run_sim();
        #convert_CMP_Multiplier("verilog",width,truncWidth,height_evolution);
        #test_ISCAS_Multiplier1 = test_CMP_Multiplier(width,truncWidth,height_evolution);
        #test_ISCAS_Multiplier1.run_sim();



