module tb_Multiplier_BrentKung;

reg [11:0] A;
reg [11:0] B;
wire [23:0] OUTS;

initial begin
    $from_myhdl(
        A,
        B
    );
    $to_myhdl(
        OUTS
    );
end

Multiplier_BrentKung dut(
    A,
    B,
    OUTS
);

endmodule
