module tb_KoggeStone;

wire [8:0] OUTS;
reg [15:0] INPUTS;

initial begin
    $from_myhdl(
        INPUTS
    );
    $to_myhdl(
        OUTS
    );
end

KoggeStone dut(
    OUTS,
    INPUTS
);

endmodule
