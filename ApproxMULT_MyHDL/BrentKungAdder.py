from myhdl import *
from BasicModule import *
import sys
import math
@block
def BrentKung(OUTS,INPUTS,columns):
    width = len(columns);
    inputs_list = [];
    instances_list = [];
    startIndex = 0; endIndex = 0;
    # initialize all inputs
    for i in range(len(columns)):
        col_len = columns[i];
        endIndex = startIndex+col_len;
        tmp_list = [];
        for j in range(startIndex,endIndex):
            tmp_list.append(INPUTS(j));
        inputs_list.append(tmp_list);
        startIndex = endIndex;
    # initial stage: geneate and propagate signals
    dict_init = {};
    for i in range(width):
        GP_Pair = [Signal(intbv(0)[1:]),Signal(intbv(0)[1:])]; # [g,p]
        if len(inputs_list[i]) == 1:
            PG_Generator0_ins = PG_Generator0(GP_Pair[0],GP_Pair[1],inputs_list[i][0]);
            instances_list.append(PG_Generator0_ins);
        else:
            PG_Generator1_ins = PG_Generator1(GP_Pair[0],GP_Pair[1],inputs_list[i][0],inputs_list[i][1]);
            instances_list.append(PG_Generator1_ins);
        key = (i,i);
        dict_init[key] = GP_Pair;
    # prefex tree    
    remainLen = width;
    allSegsLen = [];
    while remainLen != 0:
        npow = int(math.floor(math.log2(remainLen)));
        allSegsLen.append(int(pow(2,npow)));
        remainLen=remainLen-int(pow(2,npow));
    # prepare all segments
    startIndex = 0; endIndex=0;
    for i in range(len(allSegsLen)):
        endIndex = startIndex+allSegsLen[i];
        nStages = int(math.log2(allSegsLen[i]));
        for j in range(0,nStages):
            SegSize = int(pow(2,j+1)); #connect continuous 2^(j+1) bits
            for k in range(0,int(allSegsLen[i]/(SegSize))):
                start= startIndex+k*SegSize; end = start+SegSize-1;
                start_low = start; end_low = start_low + int(SegSize/2) - 1;
                start_high = end_low + 1; end_high = end;
                GP_Pair_high = dict_init[(start_high,end_high)];
                GP_Pair_low = dict_init[(start_low,end_low)];
                if start != 0:
                    GP_Pair = [Signal(intbv(0)[1:]),Signal(intbv(0)[1:])];
                    BlackCircle_ins = BlackCircle(GP_Pair[0],GP_Pair[1],GP_Pair_high[0],GP_Pair_high[1],GP_Pair_low[0],GP_Pair_low[1]);
                    dict_init[(start,end)] = GP_Pair;
                    instances_list.append(BlackCircle_ins);
                else:
                    GP_Pair = [Signal(intbv(0)[1:])];
                    #GrayCircle_ins = GrayCircle(GP_Pair[0],GP_Pair_high[0],GP_Pair_high[1],GP_Pair_low[0],GP_Pair_low[1]);
                    GrayCircle_ins = GrayCircle(GP_Pair[0],GP_Pair_high[0],GP_Pair_high[1],GP_Pair_low[0]);
                    dict_init[(start,end)] = GP_Pair;
                    instances_list.append(GrayCircle_ins);
        startIndex = endIndex;
    # start prefix connection
    dict_out = {};
    for i in range(width):
        remainLen = i+1;
        subSegsLen = [];
        while remainLen != 0:
            npow = int(math.floor(math.log2(remainLen)));
            subSegsLen.append(int(pow(2,npow)));
            remainLen=remainLen-int(pow(2,npow));
        if len(subSegsLen)==1: #just final output
            dict_out[(0,subSegsLen[0]-1)]=dict_init[(0,subSegsLen[0]-1)];
        else:
            start= 0; end = i;
            start_low = start; end_low = i-subSegsLen[len(subSegsLen)-1];
            start_high = end_low + 1; end_high = end;
            GP_Pair_high = dict_init[(start_high,end_high)];
            GP_Pair_low = dict_out[(start_low,end_low)];
            GP_Pair = [Signal(intbv(0)[1:])];
            #GrayCircle_ins = GrayCircle(GP_Pair[0],GP_Pair_high[0],GP_Pair_high[1],GP_Pair_low[0],GP_Pair_low[1]);
            GrayCircle_ins = GrayCircle(GP_Pair[0],GP_Pair_high[0],GP_Pair_high[1],GP_Pair_low[0]);
            dict_out[(start,end)] = GP_Pair;
            instances_list.append(GrayCircle_ins);
    #final sum
    outs_list = [];
    first_sum = dict_init[(0,0)][1];
    outs_list.append(first_sum);
    for i in range(1,width):
        sum = Signal(intbv(0)[1:]);
        FinalSum_ins = FinalSum(sum,dict_init[(i,i)][1],dict_out[(0,i-1)][0]);
        outs_list.append(sum);
        instances_list.append(FinalSum_ins);
    outs_list.append(dict_out[(0,width-1)][0]);
    outs_vec = ConcatSignal(*reversed(outs_list));
    @always_comb
    def comb():
        OUTS.next = outs_vec;
    return instances_list,comb;

def convert_BrentKung(hdl,columns):
    width = len(columns);
    Inputs_len = 0;
    for i in range(len(columns)):
        Inputs_len += columns[i];
    INPUTS = Signal(intbv(0)[Inputs_len:]);
    OUTS = Signal(intbv(0)[width+1:]);
    BrentKung_ins = BrentKung(OUTS,INPUTS,columns);
    BrentKung_ins.convert(hdl);

@block
def test_BrentKung(columns):
    width = len(columns);
    Inputs_len = 0;
    for i in range(len(columns)):
        Inputs_len += columns[i];
    INPUTS = Signal(intbv(0)[Inputs_len:]);
    OUTS = Signal(intbv(0)[width+1:]);
    BrentKung_ins = BrentKung(OUTS,INPUTS,columns);
    @instance
    def simu():
        times = 0;
        for i in range(pow(2,Inputs_len)):
            INPUTS.next = intbv(i)[Inputs_len:];
            yield delay(10);
            add_real = 0; add_compute = 0; wrongtime = 0;
            startIndex = 0; endIndex = 0;
            times += 1;
            for j in range(len(columns)):
                endIndex = startIndex + columns[j];
                if columns[j] == 1:
                    add_real += INPUTS[startIndex]*int(pow(2,j));
                else:
                    add_real += (INPUTS[startIndex]+INPUTS[startIndex+1])*int(pow(2,j));
                add_compute += int(pow(2,j))*OUTS[j];
                startIndex = endIndex;
            add_compute += int(pow(2,width))*OUTS[width];
            print("Real sum , Computed sum : %s , %s" % (add_real,add_compute));
            if add_real == add_compute:
                print("Correct!!!");
            else:
                print("Wrong!!!");
                wrongtime += 1;
        print("Total wrong times is %s" % (wrongtime));
        print("Total test times is %s" % (times));
    return instances();
