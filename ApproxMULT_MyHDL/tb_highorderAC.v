module tb_highorderAC;

wire [7:0] OUTS;
reg [3:0] INPUTS;

initial begin
    $from_myhdl(
        INPUTS
    );
    $to_myhdl(
        OUTS
    );
end

highorderAC dut(
    OUTS,
    INPUTS
);

endmodule
