module tb_Multiplier;

reg [7:0] A;
reg [7:0] B;
wire [28:0] OUTS;

initial begin
    $from_myhdl(
        A,
        B
    );
    $to_myhdl(
        OUTS
    );
end

Multiplier dut(
    A,
    B,
    OUTS
);

endmodule
