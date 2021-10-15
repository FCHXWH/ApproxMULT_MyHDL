from myhdl import block,always_comb,Signal
from myhdl import instances, Signal, intbv, delay
from myhdl import *
import random
# module : no need of width specification for input ports;
#          need of width specification for internal output ports;
#          better to specify the width in paramters of function (especially, hierarchical designs).
# convert :need of width specification for input ports;
# simulate : need of width specification for input ports;
@block
def mux(z,a,b,sel):
    @always_comb
    def comb():
        if sel==1:
            z.next = a;
        else:
            z.next = b;
    return comb;

@block
def FA(cout,sum,a,b,c):
    @always_comb # generator function
    def comb():
        sum.next = a^b^c;
        cout.next = a&b | a&c | b&c;
    return comb;

def convert_mux(hdl):
    a = Signal(bool(0));
    b = Signal(bool(0));
    sel = Signal(bool(0));
    z = Signal(bool(0));
    mux_1 = mux(z,a,b,sel);
    mux_1.convert(hdl);

def convert_FA(hdl):
    a = Signal(bool(0));
    b = Signal(bool(0));
    c = Signal(bool(0));
    sum = Signal(bool(0));
    cout = Signal(bool(0));
    FA_1 = FA(cout,sum,a,b,c);
    FA_1.convert(hdl);

random.seed(5);
randrange = random.randrange;

@block
def test_mux():
    z,a,b,sel = [Signal(intbv(0)) for i in range(4)];
    mux_1 = mux(z,a,b,sel); #instance

    @instance
    def stimulus():
        print("z a b sel")
        for i in range(12):
            a.next,b.next,sel.next = randrange(2),randrange(2),randrange(4);
            yield delay(10);
            print("%s %s %s %s" % (z, a, b, sel))
    return mux_1,stimulus;

@block
def test_FA():
    cout,sum,a,b,c = [Signal(intbv(0)) for i in range(5)];
    FA_1 = FA(cout,sum,a,b,c); #instance

    @instance
    def stimulus():
        print("cout sum a b c")
        for i in range(12):
            a.next,b.next,c.next = randrange(2),randrange(2),randrange(2);
            yield delay(10);
            print("%s %s %s %s %s" % (cout,sum, a, b, c))
    return FA_1,stimulus;

@block
def new_op(out,a,b,c,d,width):
    sum1,cout1,sum2,cout2 = [Signal(intbv(0)[width:]) for i in range(4)];
    FA_1 = FA(cout1,sum1,a,b,c);
    FA_2 = FA(cout2,sum2,a,b,c);
    sum1_list = [sum1(i) for i in range(width)]; cout1_list = [cout1(i) for i in range(width)];
    list1 = sum1_list + cout1_list;
    sum2_list = [sum2(i) for i in range(width)]; cout2_list = [cout2(i) for i in range(width)];
    list2 = sum2_list + cout2_list;
    input1 = ConcatSignal(*reversed(list1)); input2 = ConcatSignal(*reversed(list2));
    mux_1 = mux(out,input1,input2,d);
    return instances();

def convert_new_op(hdl):
    out = Signal(intbv(0)[2:]);
    a = Signal(intbv(0)[1:]);
    b = Signal(intbv(0)[1:]);
    c = Signal(intbv(0)[1:]);
    d = Signal(intbv(0)[1:]);
    new_op_1 = new_op(out,a,b,c,d,1);
    new_op_1.convert(hdl);

@block
def test_new_op():
    #out = Signal(intbv(0)[2:]);
    #a = Signal(bool(0));
    #b = Signal(bool(0));
    #c = Signal(bool(0));
    #d = Signal(bool(0));
    a,b,c,d = [Signal(intbv(0)[1:]) for i in range(4)];
    out = Signal(intbv(0)[2:]);
    new_op_1 = new_op(out,a,b,c,d,1);
    @instance
    def stimulus():
        print("out a b c d");
        for i in range(12):
            a.next,b.next,c.next,d.next = [randrange(2) for j in range(4)];
            yield delay(10);
            print("%s %s %s %s %s" % (out, a, b, c, d));
    return instances();
tb = test_mux();
tb.run_sim();
tb1 = test_FA();
tb1.run_sim();
tb2 = test_new_op();
tb2.run_sim();
convert_mux("verilog");
convert_FA("verilog");
convert_new_op("verilog");

