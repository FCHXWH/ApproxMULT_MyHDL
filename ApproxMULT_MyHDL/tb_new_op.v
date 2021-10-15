module tb_new_op;

wire [1:0] out;
reg [0:0] a;
reg [0:0] b;
reg [0:0] c;
reg [0:0] d;

initial begin
    $from_myhdl(
        a,
        b,
        c,
        d
    );
    $to_myhdl(
        out
    );
end

new_op dut(
    out,
    a,
    b,
    c,
    d
);

endmodule
