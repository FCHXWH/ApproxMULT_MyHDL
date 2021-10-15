module tb_BrentKung;

wire [12:0] OUTS;
reg [23:0] INPUTS;

initial begin
    $from_myhdl(
        INPUTS
    );
    $to_myhdl(
        OUTS
    );
end

BrentKung dut(
    OUTS,
    INPUTS
);

endmodule
