module tb_FA;

wire cout;
wire sum;
reg a;
reg b;
reg c;

initial begin
    $from_myhdl(
        a,
        b,
        c
    );
    $to_myhdl(
        cout,
        sum
    );
end

FA dut(
    cout,
    sum,
    a,
    b,
    c
);

endmodule
