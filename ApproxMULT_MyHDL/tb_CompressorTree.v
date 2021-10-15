module tb_CompressorTree;

wire [28:0] OUTS;
reg [63:0] INPUTS;

initial begin
    $from_myhdl(
        INPUTS
    );
    $to_myhdl(
        OUTS
    );
end

CompressorTree dut(
    OUTS,
    INPUTS
);

endmodule
