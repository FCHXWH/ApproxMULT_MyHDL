from myhdl import *
from BasicModule import *
from math import *

@block
def highorderAC(OUTS,INPUTS,width):
    instances_list = [];
    nAC32 = 0; nAC42 = 0; nAC53 = 0; nAC63 = 0;
    out_list = [];
    nOut = int(ceil(float(width)/2));
    out_list = [Signal(intbv(0)[1:]) for j in range(nOut)];
    print("input number is %s" % (width));
    if width <= 6:
        if width == 3:
            AC32_ins = AC32(out_list[0],out_list[1],INPUTS(0),INPUTS(1),INPUTS(2));
            instances_list.append(AC32_ins);
        elif width == 4:
            AC42_ins = AC42(out_list[0],out_list[1],INPUTS(0),INPUTS(1),INPUTS(2),INPUTS(3));
            instances_list.append(AC42_ins);
        elif width == 5:
            AC53_ins = AC53(out_list[0],out_list[1],out_list[2],INPUTS(0),INPUTS(1),INPUTS(2),INPUTS(3),INPUTS(4));
            instances_list.append(AC53_ins);
        elif width == 6:
            AC63_ins = AC63(out_list[0],out_list[1],out_list[2],INPUTS(0),INPUTS(1),INPUTS(2),INPUTS(3),INPUTS(4),INPUTS(5));
            instances_list.append(AC63_ins);
    else: 
        if width%4 is 0:
            nAC42 = width / 4;
        elif width%4 is 1:
            nAC42 = int(floor(float(width)/4)-1);
            nAC53 = 1;
        elif width%4 is 2:
            nAC42 = int(floor(float(width)/4)-1);
            nAC63 = 1;
        else:
            nAC42 = int(floor(float(width)/4));
            nAC32 = 1;
    
        iStartIndex = 0; iEndIndex = nAC32*3;
        oStartIndex = 0; oEndIndex = nAC32*2;
        for i in range(nAC32):
            AC32_ins = AC32(out_list[oStartIndex+2*i],out_list[oStartIndex+2*i+1],INPUTS(iStartIndex+3*i),INPUTS(iStartIndex+3*i+1),INPUTS(iStartIndex+3*i+2));
            instances_list.append(AC32_ins);
        iStartIndex = iEndIndex; iEndIndex = iStartIndex+nAC42*4;
        oStartIndex = oEndIndex; oEndIndex = oStartIndex+nAC42*2;
        for i in range(int(nAC42)):
            AC42_ins = AC42(out_list[oStartIndex+2*i],out_list[oStartIndex+2*i+1],INPUTS(iStartIndex+4*i),INPUTS(iStartIndex+4*i+1),INPUTS(iStartIndex+4*i+2),INPUTS(iStartIndex+4*i+3));
            instances_list.append(AC42_ins);
        iStartIndex = iEndIndex; iEndIndex = iStartIndex+nAC53*5;
        oStartIndex = oEndIndex; oEndIndex = oStartIndex+nAC53*3;
        for i in range(int(nAC53)):
            AC53_ins = AC53(out_list[oStartIndex+3*i],out_list[oStartIndex+3*i+1],out_list[oStartIndex+3*i+2],INPUTS(iStartIndex+5*i),INPUTS(iStartIndex+5*i+1),\
                INPUTS(iStartIndex+5*i+2),INPUTS(iStartIndex+5*i+3),INPUTS(iStartIndex+5*i+4));
            instances_list.append(AC53_ins);
        iStartIndex = iEndIndex; iEndIndex = iStartIndex+nAC63*6;
        oStartIndex = oEndIndex; oEndIndex = oStartIndex+nAC63*3;
        for i in range(int(nAC63)):
            AC63_ins = AC63(out_list[oStartIndex+3*i],out_list[oStartIndex+3*i+1],out_list[oStartIndex+3*i+2],INPUTS(iStartIndex+6*i),INPUTS(iStartIndex+6*i+1),\
                INPUTS(iStartIndex+6*i+2),INPUTS(iStartIndex+6*i+3),INPUTS(iStartIndex+6*i+4),INPUTS(iStartIndex+6*i+5));
            instances_list.append(AC63_ins);
    outs_vec = ConcatSignal(*reversed(out_list));
    @always_comb
    def comb():
        OUTS.next = outs_vec;
    return instances_list,comb;

def convert_highorderAC(hdl):
    width = 8; outWidth = int(ceil(float(width)/2));
    INPUTS= Signal(intbv(0)[width:]);
    OUTS = Signal(intbv(0)[outWidth:]);
    highorderAC_1 = highorderAC(INPUTS,OUTS,width);
    highorderAC_1.convert(hdl);

def HighOrderAC(INPUTS,OUTS):
    instances_list = [];
    width = len(INPUTS);
    nAC32 = 0; nAC42 = 0; nAC53 = 0; nAC63 = 0;
    if width <= 6:
        if width == 3:
            AC32_ins = AC32(OUTS[0],OUTS[1],INPUTS[0],INPUTS[1],INPUTS[2]);
            instances_list.append(AC32_ins);
        elif width == 4:
            AC42_ins = AC42(OUTS[0],OUTS[1],INPUTS[0],INPUTS[1],INPUTS[2],INPUTS[3]);
            instances_list.append(AC42_ins);
        elif width == 5:
            AC53_ins = AC53(OUTS[0],OUTS[1],OUTS[2],INPUTS[0],INPUTS[1],INPUTS[2],INPUTS[3],INPUTS[4]);
            instances_list.append(AC53_ins);
        elif width == 6:
            AC63_ins = AC63(OUTS[0],OUTS[1],OUTS[2],INPUTS[0],INPUTS[1],INPUTS[2],INPUTS[3],INPUTS[4],INPUTS[5]);
            instances_list.append(AC63_ins);
    else: 
        if width%4 is 0:
            nAC42 = width / 4;
        elif width%4 is 1:
            nAC42 = int(floor(float(width)/4)-1);
            nAC53 = 1;
        elif width%4 is 2:
            nAC42 = int(floor(float(width)/4)-1);
            nAC63 = 1;
        else:
            nAC42 = int(floor(float(width)/4));
            nAC32 = 1;
    
        iStartIndex = 0; iEndIndex = nAC32*3;
        oStartIndex = 0; oEndIndex = nAC32*2;
        for i in range(nAC32):
            AC32_ins = AC32(OUTS[oStartIndex+2*i],OUTS[oStartIndex+2*i+1],INPUTS[iStartIndex+3*i],INPUTS[iStartIndex+3*i+1],INPUTS[iStartIndex+3*i+2]);
            instances_list.append(AC32_ins);
        iStartIndex = iEndIndex; iEndIndex = iStartIndex+nAC42*4;
        oStartIndex = oEndIndex; oEndIndex = oStartIndex+nAC42*2;
        for i in range(int(nAC42)):
            AC42_ins = AC42(OUTS[oStartIndex+2*i],OUTS[oStartIndex+2*i+1],INPUTS[iStartIndex+4*i],INPUTS[iStartIndex+4*i+1],INPUTS[iStartIndex+4*i+2],INPUTS[iStartIndex+4*i+3]);
            instances_list.append(AC42_ins);
        iStartIndex = iEndIndex; iEndIndex = iStartIndex+nAC53*5;
        oStartIndex = oEndIndex; oEndIndex = oStartIndex+nAC53*3;
        for i in range(int(nAC53)):
            AC53_ins = AC53(OUTS[oStartIndex+3*i],OUTS[oStartIndex+3*i+1],OUTS[oStartIndex+3*i+2],INPUTS[iStartIndex+5*i],INPUTS[iStartIndex+5*i+1],\
                INPUTS[iStartIndex+5*i+2],INPUTS[iStartIndex+5*i+3],INPUTS[iStartIndex+5*i+4]);
            instances_list.append(AC53_ins);
        iStartIndex = iEndIndex; iEndIndex = iStartIndex+nAC63*6;
        oStartIndex = oEndIndex; oEndIndex = oStartIndex+nAC63*3;
        for i in range(int(nAC63)):
            AC63_ins = AC63(OUTS[oStartIndex+3*i],OUTS[oStartIndex+3*i+1],OUTS[oStartIndex+3*i+2],INPUTS[iStartIndex+6*i],INPUTS[iStartIndex+6*i+1],\
                INPUTS[iStartIndex+6*i+2],INPUTS[iStartIndex+6*i+3],INPUTS[iStartIndex+6*i+4],INPUTS[iStartIndex+6*i+5]);
            instances_list.append(AC63_ins);
    return instances_list;

def check_stop(cols_sig_list):
    flag = 1;
    for i in range(len(cols_sig_list)):
        if len(cols_sig_list[i]) > 2:
            flag = 0;
            return flag;
    return flag;

def check_stop_bm(bm_size):
    flag = 1;
    for i in range(len(bm_size)):
        if bm_size[i] > 2:
            flag = 0;
            return flag;
    return flag;

#@block
#def TCAS18(OUTS,INPUTS,width,height_evolution):
#    cols_sig_list_currentStage = [];
#    cols_sig_list_nextStage = [];
#    instances_list = [];
#    startIndex = 0; endIndex = 0;
#    iStage = 0;
#    for i in range(2*width-1):
#        col_len = width - abs(i-width+1);
#        endIndex = startIndex + col_len;
#        tmp_list = [];
#        for j in range(startIndex,endIndex):
#            tmp_list.append(INPUTS(j));
#        cols_sig_list_currentStage.append(tmp_list);
#        startIndex = endIndex;

#    while not check_stop(cols_sig_list_currentStage):
#        if iStage < 2:
#            # LSP parts
#            for i in range(width):
#                if len(cols_sig_list_currentStage[i]) <= 2:
#                    tmp_list = [Signal(intbv(0)[1:]) for j in range(len(cols_sig_list_currentStage[i]))];
#                    for j in range(len(cols_sig_list_currentStage[i])):
#                        tmp_list[j] = cols_sig_list_currentStage[i][j];
#                    cols_sig_list_nextStage.append(tmp_list);
#                else:
#                    col_len = len(cols_sig_list_currentStage[i]);
#                    col_inputs = cols_sig_list_currentStage[i];
#                    col_inputs_vec = ConcatSignal(*col_inputs);
#                    vInputs = Signal(intbv(0)[col_len:]);
#                    slice_shadower_ins = slice_shadower(vInputs,col_inputs_vec);
#                    col_outputs = Signal(intbv(0)[int(ceil(float(col_len)/2)):]);
#                    AC_ins = highorderAC(col_outputs,vInputs,col_len);
#                    cols_sig_list_nextStage.append([col_outputs(j) for j in range(int(ceil(float(col_len)/2)))]);
#                    instances_list.append(slice_shadower_ins);
#                    instances_list.append(AC_ins);
#            # MSP parts
#            nlastCarry = 0; lastCarry = [];
#            ncurrentCarry = 0; currentCarry = [];
#            for i in range(width,2*width-1):
#                # compute number of all compressors
#                nFA = 0; nHA = 0; nj = 0; nC = 0;
#                h_next = 0;
#                h_nextmax = height_evolution[iStage];
#                tmp_list = [cols_sig_list_currentStage[i][j] for j in range(len(cols_sig_list_currentStage[i]))];
#                h = len(tmp_list);
#                CStar = 0;
#                if h-(h_nextmax-nlastCarry) >= 0:
#                    CStar = int(math.ceil((h-(h_nextmax-nlastCarry))/float(2)));
#                CStarStar = 0;
#                if i < 2*width - 3:
#                    h_left  = len(cols_sig_list_currentStage[i+1]);
#                    h_leftleft = len(cols_sig_list_currentStage[i+2]);
#                    CMax = h_nextmax-int(math.ceil(h_leftleft/float(3)));
#                    CStarStar = 2*CMax - h_left + h_nextmax;
#                    if CStarStar < 0:
#                        CStarStar = 0;
#                else:
#                    CStarStar = float('inf');
#                if CStarStar < CStar:
#                    nC = CStarStar; ncurrentCarry = nC; nFA = nC;
#                    nj = 2*(h-h_nextmax-2*nFA+nlastCarry);
#                    if nj == 2 and h-3*nFA >= 3:
#                        nj = 3;
#                else:
#                    nC = CStar; ncurrentCarry = nC;
#                    if nC > 0:
#                        nFA = int(math.floor((h-h_nextmax+nlastCarry)/float(2)));
#                        nHA = nC - nFA;
#                h_next = h - 2*nFA - nHA - int(math.floor(nj/float(2))) + nlastCarry;
#                print(h_next);
#                # use these compressors
#                if iStage == 0:
#                    allInputs = tmp_list + lastCarry;
#                else:
#                    allInputs = lastCarry + tmp_list;
#                allOutputs = [Signal(intbv(0)[1:]) for j in range(h_next)];
#                currentCarry = [Signal(intbv(0)[1:]) for j in range(ncurrentCarry)];
#                iStartIndex = 0; iEndIndex = 3*nFA; oStartIndex = 0; oEndIndex = nFA;
#                for j in range(nFA):
#                    FA_ins = FA(currentCarry[oStartIndex+j],allOutputs[oStartIndex+j],allInputs[iStartIndex+3*j],\
#                        allInputs[iStartIndex+3*j+1],allInputs[iStartIndex+3*j+2]);
#                    instances_list.append(FA_ins);
#                iStartIndex = iEndIndex; iEndIndex = iStartIndex + 2*nHA; 
#                oStartIndex = oEndIndex; oEndIndex = oStartIndex + nHA;
#                for j in range(nHA):
#                    HA_ins = HA(currentCarry[oStartIndex+j],allOutputs[oStartIndex+j],allInputs[iStartIndex+2*j],allInputs[iStartIndex+2*j+1]);
#                    instances_list.append(HA_ins);
#                # high order approximate compressor's inputs
#                iStartIndex = iEndIndex; iEndIndex = iStartIndex + nj;
#                oStartIndex = oEndIndex; oEndIndex = oStartIndex + int(math.ceil(nj/float(2)));
#                if nj > 0:    
#                    AC_inputs_list = [allInputs[j] for j in range(iStartIndex,iEndIndex)];
#                    vInputs = Signal(intbv(0)[iEndIndex-iStartIndex:]);
#                    slice_shadower_ins = slice_shadower(vInputs,ConcatSignal(*reversed(AC_inputs_list)));
#                    AC_outputs_vec = Signal(intbv(0)[int(math.ceil(nj/float(2))):]);
#                    HighOrderAC_ins = highorderAC(AC_outputs_vec,vInputs,nj);
#                    for j in range(int(math.ceil(nj/float(2)))):
#                        allOutputs[oStartIndex+j] = AC_outputs_vec(j);
#                        print("the %s stage, the %s column, the %s element" % (iStage+1,i,oStartIndex+j));
#                    instances_list.append(slice_shadower_ins);
#                    instances_list.append(HighOrderAC_ins);
#                #remaining bits
#                iStartIndex = iEndIndex; iEndIndex = len(allInputs);
#                oStartIndex = oEndIndex; oEndIndex = h_next;
#                for j in range(iStartIndex,iEndIndex):
#                    index = j - iStartIndex;
#                    allOutputs[index + oStartIndex] = allInputs[j];
#                cols_sig_list_nextStage.append(allOutputs);
#                nlastCarry  = ncurrentCarry;
#                lastCarry = currentCarry;
#        else:
#            nlastCarry = 0; lastCarry = [];
#            ncurrentCarry = 0; currentCarry = [];
#            for i in range(2*width-1):
#                nFA = 0; nHA = 0; nC = 0;
#                h_next = 0; h_nextmax = height_evolution[iStage];
#                tmp_list = [cols_sig_list_currentStage[i][j] for j in range(len(cols_sig_list_currentStage[i]))];
#                h = len(tmp_list);
#                if h-(h_nextmax-nlastCarry) >= 0:
#                    nC = int(math.ceil((h-(h_nextmax-nlastCarry))/float(2)));
#                ncurrentCarry = nC;
#                if nC > 0:
#                    nFA = int(math.floor((h-h_nextmax+nlastCarry)/float(2)));
#                    nHA = nC - nFA;
#                h_next = h - 2*nFA - nHA + nlastCarry;
#                allInputs = tmp_list + lastCarry;
#                allOutputs = [Signal(intbv(0)[1:]) for j in range(h_next)];
#                currentCarry = [Signal(intbv(0)[1:]) for j in range(ncurrentCarry)];
#                iStartIndex = 0; iEndIndex = 3*nFA; oStartIndex = 0; oEndIndex = nFA;
#                for j in range(nFA):
#                    FA_ins = FA(currentCarry[oStartIndex+j],allOutputs[oStartIndex+j],allInputs[iStartIndex+3*j],\
#                        allInputs[iStartIndex+3*j+1],allInputs[iStartIndex+3*j+2]);
#                    instances_list.append(FA_ins);
#                iStartIndex = iEndIndex; iEndIndex = iStartIndex + 2*nHA; 
#                oStartIndex = oEndIndex; oEndIndex = oStartIndex + nHA;
#                for j in range(nHA):
#                    HA_ins = HA(currentCarry[oStartIndex+j],allOutputs[oStartIndex+j],allInputs[iStartIndex+2*j],allInputs[iStartIndex+2*j+1]);
#                    instances_list.append(HA_ins);
#                iStartIndex = iEndIndex; iEndIndex = len(allInputs);
#                oStartIndex = oEndIndex; oEndIndex = h_next;
#                #remaining bits
#                for j in range(iStartIndex,iEndIndex):
#                    index = j - iStartIndex;
#                    allOutputs[index + oStartIndex] = allInputs[j];
#                cols_sig_list_nextStage.append(allOutputs);
#                nlastCarry  = ncurrentCarry;
#                lastCarry = currentCarry;
#        cols_sig_list_currentStage = cols_sig_list_nextStage;
#        cols_sig_list_nextStage = [];
#        iStage += 1;
#    outs_list = [];
#    for i in range(len(cols_sig_list_currentStage)):
#        outs_list += cols_sig_list_currentStage[i];
#    outs_vec = ConcatSignal(*reversed(outs_list));
#    @always_comb
#    def comb():
#        OUTS.next = outs_vec;
#    return instances_list,comb;

@block
def TCAS18(OUTS,INPUTS,width,height_evolution,approx_step_num,is_trunc):
    cols_sig_list_currentStage = [];
    cols_sig_list_nextStage = [];
    instances_list = [];
    startIndex = 0; endIndex = 0;
    iStage = 0;
    for i in range(2*width-1):
        col_len = 0;
        if is_trunc and i < width-1:
            col_len = 0;
        else:
            col_len = width - abs(i-width+1);
        endIndex = startIndex + col_len;
        tmp_list = [];
        for j in range(startIndex,endIndex):
            tmp_list.append(INPUTS(j));
        cols_sig_list_currentStage.append(tmp_list);
        startIndex = endIndex;

    while not check_stop(cols_sig_list_currentStage):
        if iStage < approx_step_num:
            # LSP parts
            for i in range(width):
                if len(cols_sig_list_currentStage[i]) <= 2:
                    tmp_list = [Signal(intbv(0)[1:]) for j in range(len(cols_sig_list_currentStage[i]))];
                    for j in range(len(cols_sig_list_currentStage[i])):
                        tmp_list[j] = cols_sig_list_currentStage[i][j];
                    cols_sig_list_nextStage.append(tmp_list);
                else:
                    col_len = len(cols_sig_list_currentStage[i]);
                    col_inputs = cols_sig_list_currentStage[i];
                    col_inputs_vec = ConcatSignal(*col_inputs);
                    vInputs = Signal(intbv(0)[col_len:]);
                    slice_shadower_ins = slice_shadower(vInputs,col_inputs_vec);
                    col_outputs = Signal(intbv(0)[int(ceil(float(col_len)/2)):]);
                    AC_ins = highorderAC(col_outputs,vInputs,col_len);
                    cols_sig_list_nextStage.append([col_outputs(j) for j in range(int(ceil(float(col_len)/2)))]);
                    instances_list.append(slice_shadower_ins);
                    instances_list.append(AC_ins);
            # MSP parts
            nlastCarry = 0; lastCarry = [];
            ncurrentCarry = 0; currentCarry = [];
            for i in range(width,2*width-1):
                # compute number of all compressors
                nFA = 0; nHA = 0; nj = 0; nC = 0;
                h_next = 0;
                h_nextmax = height_evolution[iStage];
                tmp_list = [cols_sig_list_currentStage[i][j] for j in range(len(cols_sig_list_currentStage[i]))];
                h = len(tmp_list);
                CStar = 0;
                if h-(h_nextmax-nlastCarry) >= 0:
                    CStar = int(math.ceil((h-(h_nextmax-nlastCarry))/float(2)));
                CStarStar = 0;
                if i < 2*width - 3:
                    h_left  = len(cols_sig_list_currentStage[i+1]);
                    h_leftleft = len(cols_sig_list_currentStage[i+2]);
                    CMax = h_nextmax-int(math.ceil(h_leftleft/float(3)));
                    CStarStar = 2*CMax - h_left + h_nextmax;
                    if CStarStar < 0:
                        CStarStar = 0;
                else:
                    CStarStar = float('inf');
                if CStarStar < CStar:
                    nC = CStarStar; ncurrentCarry = nC; nFA = nC;
                    nj = 2*(h-h_nextmax-2*nFA+nlastCarry);
                    if nj == 2 and h-3*nFA >= 3:
                        nj = 3;
                else:
                    nC = CStar; ncurrentCarry = nC;
                    if nC > 0:
                        nFA = int(math.floor((h-h_nextmax+nlastCarry)/float(2)));
                        nHA = nC - nFA;
                h_next = h - 2*nFA - nHA - int(math.floor(nj/float(2))) + nlastCarry;
                print(h_next);
                # use these compressors
                if iStage == 0:
                    allInputs = tmp_list + lastCarry;
                else:
                    allInputs = lastCarry + tmp_list;
                allOutputs = [Signal(intbv(0)[1:]) for j in range(h_next)];
                currentCarry = [Signal(intbv(0)[1:]) for j in range(ncurrentCarry)];
                iStartIndex = 0; iEndIndex = 3*nFA; oStartIndex = 0; oEndIndex = nFA;
                for j in range(nFA):
                    FA_ins = FA(currentCarry[oStartIndex+j],allOutputs[oStartIndex+j],allInputs[iStartIndex+3*j],\
                        allInputs[iStartIndex+3*j+1],allInputs[iStartIndex+3*j+2]);
                    instances_list.append(FA_ins);
                iStartIndex = iEndIndex; iEndIndex = iStartIndex + 2*nHA; 
                oStartIndex = oEndIndex; oEndIndex = oStartIndex + nHA;
                for j in range(nHA):
                    HA_ins = HA(currentCarry[oStartIndex+j],allOutputs[oStartIndex+j],allInputs[iStartIndex+2*j],allInputs[iStartIndex+2*j+1]);
                    instances_list.append(HA_ins);
                # high order approximate compressor's inputs
                iStartIndex = iEndIndex; iEndIndex = iStartIndex + nj;
                oStartIndex = oEndIndex; oEndIndex = oStartIndex + int(math.ceil(nj/float(2)));
                if nj > 0:    
                    AC_inputs_list = [allInputs[j] for j in range(iStartIndex,iEndIndex)];
                    vInputs = Signal(intbv(0)[iEndIndex-iStartIndex:]);
                    slice_shadower_ins = slice_shadower(vInputs,ConcatSignal(*reversed(AC_inputs_list)));
                    AC_outputs_vec = Signal(intbv(0)[int(math.ceil(nj/float(2))):]);
                    HighOrderAC_ins = highorderAC(AC_outputs_vec,vInputs,nj);
                    for j in range(int(math.ceil(nj/float(2)))):
                        allOutputs[oStartIndex+j] = AC_outputs_vec(j);
                        print("the %s stage, the %s column, the %s element" % (iStage+1,i,oStartIndex+j));
                    instances_list.append(slice_shadower_ins);
                    instances_list.append(HighOrderAC_ins);
                #remaining bits
                iStartIndex = iEndIndex; iEndIndex = len(allInputs);
                oStartIndex = oEndIndex; oEndIndex = h_next;
                for j in range(iStartIndex,iEndIndex):
                    index = j - iStartIndex;
                    allOutputs[index + oStartIndex] = allInputs[j];
                cols_sig_list_nextStage.append(allOutputs);
                nlastCarry  = ncurrentCarry;
                lastCarry = currentCarry;
        else:
            nlastCarry = 0; lastCarry = [];
            ncurrentCarry = 0; currentCarry = [];
            for i in range(2*width-1):
                nFA = 0; nHA = 0; nC = 0;
                h_next = 0; h_nextmax = height_evolution[iStage];
                tmp_list = [cols_sig_list_currentStage[i][j] for j in range(len(cols_sig_list_currentStage[i]))];
                h = len(tmp_list);
                if h-(h_nextmax-nlastCarry) >= 0:
                    nC = int(math.ceil((h-(h_nextmax-nlastCarry))/float(2)));
                ncurrentCarry = nC;
                if nC > 0:
                    nFA = int(math.floor((h-h_nextmax+nlastCarry)/float(2)));
                    nHA = nC - nFA;
                h_next = h - 2*nFA - nHA + nlastCarry;
                allInputs = tmp_list + lastCarry;
                allOutputs = [Signal(intbv(0)[1:]) for j in range(h_next)];
                currentCarry = [Signal(intbv(0)[1:]) for j in range(ncurrentCarry)];
                iStartIndex = 0; iEndIndex = 3*nFA; oStartIndex = 0; oEndIndex = nFA;
                for j in range(nFA):
                    FA_ins = FA(currentCarry[oStartIndex+j],allOutputs[oStartIndex+j],allInputs[iStartIndex+3*j],\
                        allInputs[iStartIndex+3*j+1],allInputs[iStartIndex+3*j+2]);
                    instances_list.append(FA_ins);
                iStartIndex = iEndIndex; iEndIndex = iStartIndex + 2*nHA; 
                oStartIndex = oEndIndex; oEndIndex = oStartIndex + nHA;
                for j in range(nHA):
                    HA_ins = HA(currentCarry[oStartIndex+j],allOutputs[oStartIndex+j],allInputs[iStartIndex+2*j],allInputs[iStartIndex+2*j+1]);
                    instances_list.append(HA_ins);
                iStartIndex = iEndIndex; iEndIndex = len(allInputs);
                oStartIndex = oEndIndex; oEndIndex = h_next;
                #remaining bits
                for j in range(iStartIndex,iEndIndex):
                    index = j - iStartIndex;
                    allOutputs[index + oStartIndex] = allInputs[j];
                cols_sig_list_nextStage.append(allOutputs);
                nlastCarry  = ncurrentCarry;
                lastCarry = currentCarry;
        cols_sig_list_currentStage = cols_sig_list_nextStage;
        cols_sig_list_nextStage = [];
        iStage += 1;
    outs_list = [];
    for i in range(len(cols_sig_list_currentStage)):
        if len(cols_sig_list_currentStage[i]) == 0:
            outs_list.append(intbv(0)[1:]);
        else:
            outs_list += cols_sig_list_currentStage[i];
    outs_vec = ConcatSignal(*reversed(outs_list));
    @always_comb
    def comb():
        OUTS.next = outs_vec;
    return instances_list,comb;


@block
def ISCAS18(OUTS,INPUTS,width,truncWidth,height_evolution):
    cols_sig_list_currentStage = [];
    cols_sig_list_nextStage = [];
    instances_list = [];
    startIndex = 0; endIndex = 0;
    for i in range(2*width-1):
        col_len = width - abs(i-width+1);
        endIndex = startIndex + col_len;
        tmp_list = [];
        for j in range(startIndex,endIndex):
            tmp_list.append(INPUTS(j));
        cols_sig_list_currentStage.append(tmp_list);
        startIndex = endIndex;

    h0 = ceil(float(width)/4);
    #stage 1

    #approximation part
    for i in range(truncWidth):
        if len(cols_sig_list_currentStage[i]) <= 2:
            tmp_list = [Signal(intbv(0)[1:]) for j in range(len(cols_sig_list_currentStage[i]))];
            for j in range(len(cols_sig_list_currentStage[i])):
                tmp_list[j] = cols_sig_list_currentStage[i][j];
            cols_sig_list_nextStage.append(tmp_list);
        else:
            col_len = len(cols_sig_list_currentStage[i]);
            col_inputs = cols_sig_list_currentStage[i];
            col_inputs_vec = ConcatSignal(*col_inputs);
            vInputs = Signal(intbv(0)[col_len:]);
            slice_shadower_ins = slice_shadower(vInputs,col_inputs_vec);
            col_outputs = Signal(intbv(0)[int(ceil(float(col_len)/2)):]);
            AC_ins = highorderAC(col_outputs,vInputs,col_len);
            cols_sig_list_nextStage.append([col_outputs(j) for j in range(int(ceil(float(col_len)/2)))]);
            instances_list.append(slice_shadower_ins);
            instances_list.append(AC_ins);
            
    #exact part
    nlastCarry = 0; lastCarry = [];
    ncurrentCarry = 0; currentCarry = [];
    for i in range(truncWidth,2*width-1):
        # get the current column's signals
        tmp_list = [cols_sig_list_currentStage[i][j] for j in range(len(cols_sig_list_currentStage[i]))];
        col_len = len(tmp_list);
        ncurrentCarry = floor(float(col_len+nlastCarry)/3);
        allInSignals = lastCarry + tmp_list;
        #prepare current column's sum and cout signals
        allOutSignals = [Signal(intbv(0)[1:]) for j in range(len(allInSignals) - 2*ncurrentCarry)];
        #allSumSignals = [Signal(intbv(0)[1:]) for j in range(ncurrentCarry)];
        currentCarry = [Signal(intbv(0)[1:]) for j in range(ncurrentCarry)];
        for j in range(ncurrentCarry):
            FA_ins = FA(currentCarry[j],allOutSignals[j],allInSignals[3*j],allInSignals[3*j+1],allInSignals[3*j+2]);
            instances_list.append(FA_ins);
        for j in range(ncurrentCarry,len(allOutSignals)):
            allOutSignals[j] = allInSignals[ncurrentCarry*3+j-ncurrentCarry];
        cols_sig_list_nextStage.append(allOutSignals);
        nlastCarry = ncurrentCarry;
        lastCarry = currentCarry;
    cols_sig_list_currentStage = cols_sig_list_nextStage;
    cols_sig_list_nextStage = [];
    #stage2
    #approximation part
    for i in range(truncWidth):
        if len(cols_sig_list_currentStage[i]) <= 2:
            tmp_list = [Signal(intbv(0)[1:]) for j in range(len(cols_sig_list_currentStage[i]))];
            for j in range(len(cols_sig_list_currentStage[i])):
                tmp_list[j] = cols_sig_list_currentStage[i][j];
            cols_sig_list_nextStage.append(tmp_list);

        else:
            col_len = len(cols_sig_list_currentStage[i]);
            col_inputs = cols_sig_list_currentStage[i];
            col_inputs_vec = ConcatSignal(*reversed(col_inputs));
            vInputs = Signal(intbv(0)[col_len:]);
            slice_shadower_ins = slice_shadower(vInputs,col_inputs_vec);
            col_outputs = Signal(intbv(0)[int(ceil(float(col_len)/2)):]);
            AC_ins = highorderAC(col_outputs,vInputs,col_len);
            cols_sig_list_nextStage.append([col_outputs(j) for j in range(int(ceil(float(col_len)/2)))]);
            instances_list.append(slice_shadower_ins);
            instances_list.append(AC_ins);
            
    #exact part
    nlastCarry = 0; lastCarry = [];
    ncurrentCarry = 0; currentCarry = [];
    ncurrentFACarry = 0;
    ncurrentHACarry = 0;
    for i in range(truncWidth,2*width-1):
        # get the current column's signals
        tmp_list = [cols_sig_list_currentStage[i][j] for j in range(len(cols_sig_list_currentStage[i]))];
        col_len = len(tmp_list);
        if col_len+nlastCarry > h0:
            if width <= 8:
                ncurrentFACarry = floor(float(col_len+nlastCarry-h0)/2);
                ncurrentHACarry = floor(float(col_len+nlastCarry-3*ncurrentFACarry)/2);
                ncurrentCarry = ncurrentFACarry + ncurrentHACarry;
            else:
                ncurrentCarry = ceil(float(col_len+nlastCarry-h0)/2);
                ncurrentFACarry = floor(float(col_len+nlastCarry-h0)/2);
                ncurrentHACarry = ncurrentCarry - ncurrentFACarry;
        else:
            ncurrentCarry = 0;
            ncurrentFACarry = 0;
            ncurrentHACarry = 0;
        allInSignals = lastCarry + tmp_list;
        #prepare current column's sum and cout signals
        allOutSignals = [Signal(intbv(0)[1:]) for j in range(len(allInSignals) - 2*ncurrentFACarry - ncurrentHACarry)];
        currentCarry = [Signal(intbv(0)[1:]) for j in range(ncurrentCarry)];
        for j in range(ncurrentFACarry):
            FA_ins = FA(currentCarry[j],allOutSignals[j],allInSignals[3*j],allInSignals[3*j+1],allInSignals[3*j+2]);
            instances_list.append(FA_ins);
        startIndex = 3*ncurrentFACarry;
        for j in range(ncurrentHACarry):
            HA_ins = HA(currentCarry[ncurrentFACarry+j],allOutSignals[ncurrentFACarry+j],allInSignals[startIndex+2*j],allInSignals[startIndex+2*j+1]);
            instances_list.append(HA_ins);
        startIndex += 2*ncurrentHACarry;
        for j in range(ncurrentCarry,len(allOutSignals)):
            allOutSignals[j] = allInSignals[startIndex+j-ncurrentCarry];
        cols_sig_list_nextStage.append(allOutSignals);
        nlastCarry = ncurrentCarry;
        lastCarry = currentCarry;
    cols_sig_list_currentStage = cols_sig_list_nextStage;
    cols_sig_list_nextStage = [];

    # remaining all exact compressors
    iStage = 0;
    while not check_stop(cols_sig_list_currentStage):
        nlastCarry = 0; lastCarry = [];
        ncurrentCarry = 0; currentCarry = [];
        for i in range(2*width-1):
            nFA = 0; nHA = 0; nC = 0;
            h_next = 0; h_nextmax = height_evolution[iStage];
            tmp_list = [cols_sig_list_currentStage[i][j] for j in range(len(cols_sig_list_currentStage[i]))];
            h = len(tmp_list);
            if h-(h_nextmax-nlastCarry) >= 0:
                nC = int(math.ceil((h-(h_nextmax-nlastCarry))/float(2)));
            ncurrentCarry = nC;
            if nC > 0:
                nFA = int(math.floor((h-h_nextmax+nlastCarry)/float(2)));
                nHA = nC - nFA;
            h_next = h - 2*nFA - nHA + nlastCarry;
            allInputs = tmp_list + lastCarry;
            allOutputs = [Signal(intbv(0)[1:]) for j in range(h_next)];
            currentCarry = [Signal(intbv(0)[1:]) for j in range(ncurrentCarry)];
            iStartIndex = 0; iEndIndex = 3*nFA; oStartIndex = 0; oEndIndex = nFA;
            for j in range(nFA):
                FA_ins = FA(currentCarry[oStartIndex+j],allOutputs[oStartIndex+j],allInputs[iStartIndex+3*j],\
                    allInputs[iStartIndex+3*j+1],allInputs[iStartIndex+3*j+2]);
                instances_list.append(FA_ins);
            iStartIndex = iEndIndex; iEndIndex = iStartIndex + 2*nHA; 
            oStartIndex = oEndIndex; oEndIndex = oStartIndex + nHA;
            for j in range(nHA):
                HA_ins = HA(currentCarry[oStartIndex+j],allOutputs[oStartIndex+j],allInputs[iStartIndex+2*j],allInputs[iStartIndex+2*j+1]);
                instances_list.append(HA_ins);
            iStartIndex = iEndIndex; iEndIndex = len(allInputs);
            oStartIndex = oEndIndex; oEndIndex = h_next;
            #remaining bits
            for j in range(iStartIndex,iEndIndex):
                index = j - iStartIndex;
                allOutputs[index + oStartIndex] = allInputs[j];
            cols_sig_list_nextStage.append(allOutputs);
            nlastCarry  = ncurrentCarry;
            lastCarry = currentCarry;
        cols_sig_list_currentStage = cols_sig_list_nextStage;
        cols_sig_list_nextStage = [];
        iStage += 1;
    outs_list = [];
    for i in range(len(cols_sig_list_currentStage)):
        outs_list += cols_sig_list_currentStage[i];
    outs_vec = ConcatSignal(*reversed(outs_list));
    @always_comb
    def comb():
        OUTS.next = outs_vec;
    return instances_list,comb;

#def tcas_finalstage_size(width,height_evolution):
#    bm = []; bm_next = [];
#    for i in range(2*width-1):
#        col_len = width - abs(i-width+1);
#        bm.append(col_len);
#    iStage = 0;
#    while not check_stop_bm(bm):
#        if iStage < 2:
#            # LSB
#            for i in range(width):
#                if bm[i] <= 2:
#                    bm_next.append(bm[i]);
#                else:
#                    bm_next.append(int(math.ceil(bm[i]/float(2))));
#            # MSB
#            nlastCarry = 0; ncurrentCarry = 0;
#            for i in range(width,2*width-1):
#                # compute number of all compressors
#                nFA = 0; nHA = 0; nj = 0; nC = 0;
#                h_next = 0;
#                h_nextmax = height_evolution[iStage];
                
#                h = bm[i];
#                CStar = 0;
#                if h-(h_nextmax-nlastCarry) >= 0:
#                    CStar = int(math.ceil((h-(h_nextmax-nlastCarry))/float(2)));
#                CStarStar = 0;
#                if i < 2*width - 3:
#                    h_left  = bm[i+1];
#                    h_leftleft = bm[i+2];
#                    CMax = h_nextmax-int(math.ceil(h_leftleft/float(3)));
#                    CStarStar = 2*CMax - h_left + h_nextmax;
#                    if CStarStar < 0:
#                        CStarStar = 0;
#                else:
#                    CStarStar = float('inf');
#                if CStarStar < CStar:
#                    nC = CStarStar; ncurrentCarry = nC; nFA = nC;
#                    nj = 2*(h-h_nextmax-2*nFA+nlastCarry);
#                    if nj == 2 and h-3*nFA >= 3:
#                        nj = 3;
#                else:
#                    nC = CStar; ncurrentCarry = nC;
#                    if nC > 0:
#                        nFA = int(math.floor((h-h_nextmax+nlastCarry)/float(2)));
#                        nHA = nC - nFA;
#                h_next = h - 2*nFA - nHA - int(math.floor(nj/float(2))) + nlastCarry;
#                bm_next.append(h_next);
#                nlastCarry  = ncurrentCarry;
#        else:
#            nlastCarry = 0; ncurrentCarry = 0;
#            for i in range(2*width-1):
#                nFA = 0; nHA = 0; nC = 0;
#                h_next = 0; h_nextmax = height_evolution[iStage];
#                h = bm[i];
#                if h-(h_nextmax-nlastCarry) >= 0:
#                    nC = int(math.ceil((h-(h_nextmax-nlastCarry))/float(2)));
#                ncurrentCarry = nC;
#                if nC > 0:
#                    nFA = int(math.floor((h-h_nextmax+nlastCarry)/float(2)));
#                    nHA = nC - nFA;
#                h_next = h - 2*nFA - nHA + nlastCarry;
#                bm_next.append(h_next);
#                nlastCarry  = ncurrentCarry;
#        bm = bm_next; bm_next = [];
#        print(bm);
#        iStage += 1;
#    return bm;

def tcas_finalstage_size(width,height_evolution,approx_step_num,is_trunc):
    bm = []; bm_next = [];
    for i in range(2*width-1):
        col_len = 0;
        if i < width-1 and is_trunc:
            col_len = 0;
        else:
            col_len = width - abs(i-width+1);
        bm.append(col_len);
    iStage = 0;
    while not check_stop_bm(bm):
        if iStage < approx_step_num:
            # LSB
            for i in range(width):
                if bm[i] <= 2:
                    bm_next.append(bm[i]);
                else:
                    bm_next.append(int(math.ceil(bm[i]/float(2))));
            # MSB
            nlastCarry = 0; ncurrentCarry = 0;
            for i in range(width,2*width-1):
                # compute number of all compressors
                nFA = 0; nHA = 0; nj = 0; nC = 0;
                h_next = 0;
                h_nextmax = height_evolution[iStage];
                
                h = bm[i];
                CStar = 0;
                if h-(h_nextmax-nlastCarry) >= 0:
                    CStar = int(math.ceil((h-(h_nextmax-nlastCarry))/float(2)));
                CStarStar = 0;
                if i < 2*width - 3:
                    h_left  = bm[i+1];
                    h_leftleft = bm[i+2];
                    CMax = h_nextmax-int(math.ceil(h_leftleft/float(3)));
                    CStarStar = 2*CMax - h_left + h_nextmax;
                    if CStarStar < 0:
                        CStarStar = 0;
                else:
                    CStarStar = float('inf');
                if CStarStar < CStar:
                    nC = CStarStar; ncurrentCarry = nC; nFA = nC;
                    nj = 2*(h-h_nextmax-2*nFA+nlastCarry);
                    if nj == 2 and h-3*nFA >= 3:
                        nj = 3;
                else:
                    nC = CStar; ncurrentCarry = nC;
                    if nC > 0:
                        nFA = int(math.floor((h-h_nextmax+nlastCarry)/float(2)));
                        nHA = nC - nFA;
                h_next = h - 2*nFA - nHA - int(math.floor(nj/float(2))) + nlastCarry;
                bm_next.append(h_next);
                nlastCarry  = ncurrentCarry;
        else:
            nlastCarry = 0; ncurrentCarry = 0;
            for i in range(2*width-1):
                nFA = 0; nHA = 0; nC = 0;
                h_next = 0; h_nextmax = height_evolution[iStage];
                h = bm[i];
                if h-(h_nextmax-nlastCarry) >= 0:
                    nC = int(math.ceil((h-(h_nextmax-nlastCarry))/float(2)));
                ncurrentCarry = nC;
                if nC > 0:
                    nFA = int(math.floor((h-h_nextmax+nlastCarry)/float(2)));
                    nHA = nC - nFA;
                h_next = h - 2*nFA - nHA + nlastCarry;
                bm_next.append(h_next);
                nlastCarry  = ncurrentCarry;
        bm = bm_next; bm_next = [];
        print(bm);
        iStage += 1;
    return bm;

def get_finalstage_size(width,truncWidth,height_evolution):
    #initialize bit matrix
    bm = [];
    for i in range(2*width-1):
        col_len = width - abs(i-width+1);
        bm.append(col_len);
    #stage 1
    bm_next = [];
    for i in range(truncWidth):
        if bm[i] <= 2:
            bm_next.append(bm[i]);
        else:
            bm_next.append(ceil(float(bm[i])/2));
    nlastCarry = 0;
    for i in range(truncWidth,2*width-1):
        ncurrentCarry = floor(float(bm[i]+nlastCarry)/3);
        bm_next.append(bm[i]+nlastCarry-2*ncurrentCarry);
        nlastCarry = ncurrentCarry;
    
    #stage 2
    bm = bm_next;
    bm_next = []; h0 = ceil(float(width)/4);
    for i in range(truncWidth):
        if bm[i] <= 2:
            bm_next.append(bm[i]);
        else:
            bm_next.append(ceil(float(bm[i])/2));
    nlastCarry = 0;
    ncurrentFACarry = 0;
    ncurrentHACarry = 0;
    for i in range(truncWidth,2*width-1):
        if bm[i]+nlastCarry > h0:
            if width <= 8:
                ncurrentFACarry = floor(float(bm[i]+nlastCarry-h0)/2);
                ncurrentHACarry = floor(float(bm[i]+nlastCarry-3*ncurrentFACarry)/2);
                ncurrentCarry = ncurrentFACarry + ncurrentHACarry;
                bm_next.append(bm[i]+nlastCarry-2*ncurrentFACarry-ncurrentHACarry);
            else:
                ncurrentCarry = ceil(float(bm[i]+nlastCarry-h0)/2);
                ncurrentFACarry = floor(float(bm[i]+nlastCarry-h0)/2);
                ncurrentHACarry = ncurrentCarry - ncurrentFACarry;
                bm_next.append(bm[i]+nlastCarry-2*ncurrentFACarry-ncurrentHACarry);
        else:
            ncurrentCarry = 0;
            ncurrentFACarry = 0;
            ncurrentHACarry = 0;
            bm_next.append(bm[i]+nlastCarry-2*ncurrentFACarry-ncurrentHACarry);
        #ncurrentcarry = ceil(float(bm[i]+nlastcarry-h0)/2);
        #ncurrentFAcarry = floor(float(bm[i]+nlastcarry-h0)/2);
        #ncurrentHAcarry = ncurrentcarry - ncurrentFAcarry;
        nlastCarry = ncurrentCarry;
    bm = bm_next;
    bm_next = [];
    # remaining all exact compressors
    # remaining all exact compressors
    iStage = 0;
    while not check_stop_bm(bm):
        nlastCarry = 0;
        ncurrentCarry = 0;
        for i in range(2*width-1):
            nFA = 0; nHA = 0; nC = 0;
            h_next = 0; h_nextmax = height_evolution[iStage];
            h = bm[i];
            if h-(h_nextmax-nlastCarry) >= 0:
                nC = int(math.ceil((h-(h_nextmax-nlastCarry))/float(2)));
            ncurrentCarry = nC;
            if nC > 0:
                nFA = int(math.floor((h-h_nextmax+nlastCarry)/float(2)));
                nHA = nC - nFA;
            h_next = h - 2*nFA - nHA + nlastCarry;
            bm_next.append(h_next);
            nlastCarry  = ncurrentCarry;
        bm = bm_next;
        bm_next = [];
        iStage += 1;
    return bm;

#def convert_ISCAS18(hdl):
#    width = 8;
#    nInBits = width*width;
#    INPUTS = Signal(intbv(0)[nInBits:]);
#    nOutBits = 0;
#    last_bm_size = get_finalstage_size(width,10);
#    nOutBits = 0;
#    for i in range(len(last_bm_size)):
#        nOutBits += last_bm_size[i];
#    OUTS = Signal(intbv(0)[nOutBits:]);
#    iscas_ins = ISCAS18(INPUTS,OUTS,width,10);
#    iscas_ins.convert(hdl);

def convert_ISCAS18(hdl):
    width = 8;
    truncWidth = 10;
    INPUTS = Signal(intbv(0)[width*width:]);
    #stages = ParseJson("CompressorTree.json");
    last_bm_size = get_finalstage_size(width,truncWidth);
    nOutBits = 0;
    for i in range(len(last_bm_size)):
        nOutBits += last_bm_size[i];
    OUTS = Signal(intbv(0)[nOutBits:])
    iscas_ins = ISCAS18(OUTS,INPUTS,width,truncWidth);
    iscas_ins.convert(hdl);

def convert_TCAS18(hdl):
    width = 8;    
    INPUTS = Signal(intbv(0)[width*width:]);
    #stages = ParseJson("CompressorTree.json");
    last_bm_size = tcas_finalstage_size(width,[4,2]);
    nOutBits = 0;
    for i in range(len(last_bm_size)):
        nOutBits += last_bm_size[i];
    OUTS = Signal(intbv(0)[nOutBits:])
    tcas_ins = TCAS18(OUTS,INPUTS,width,[4,2]);
    tcas_ins.convert(hdl);