module tb_CMP_Multiplier;

wire [44:0] OUTS;
reg [11:0] A;
reg [11:0] B;

initial begin
    $from_myhdl(
        A,
        B
    );
    $to_myhdl(
        OUTS
    );
end

CMP_Multiplier dut(
    OUTS,
    A,
    B
);

endmodule
