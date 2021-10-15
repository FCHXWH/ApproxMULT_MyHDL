module tb_mux;

wire z;
reg a;
reg b;
reg sel;

initial begin
    $from_myhdl(
        a,
        b,
        sel
    );
    $to_myhdl(
        z
    );
end

mux dut(
    z,
    a,
    b,
    sel
);

endmodule
