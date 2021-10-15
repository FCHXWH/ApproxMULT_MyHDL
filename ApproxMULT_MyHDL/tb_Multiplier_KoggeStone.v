module tb_Multiplier_KoggeStone;

reg [7:0] A;
reg [7:0] B;
wire [15:0] OUTS;

initial begin
    $from_myhdl(
        A,
        B
    );
    $to_myhdl(
        OUTS
    );
end

Multiplier_KoggeStone dut(
    A,
    B,
    OUTS
);

endmodule
