module tb_CMP_Multiplier_KoggeStone;

wire [39:0] OUTS;
reg [19:0] A;
reg [19:0] B;

initial begin
    $from_myhdl(
        A,
        B
    );
    $to_myhdl(
        OUTS
    );
end

CMP_Multiplier_KoggeStone dut(
    OUTS,
    A,
    B
);

endmodule
