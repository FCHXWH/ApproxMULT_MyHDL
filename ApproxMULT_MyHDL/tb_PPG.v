module tb_PPG;

wire [63:0] OUTS;
reg [7:0] A;
reg [7:0] B;

initial begin
    $from_myhdl(
        A,
        B
    );
    $to_myhdl(
        OUTS
    );
end

PPG dut(
    OUTS,
    A,
    B
);

endmodule
