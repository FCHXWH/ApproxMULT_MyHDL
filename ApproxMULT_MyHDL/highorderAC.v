// File: highorderAC.v
// Generated by MyHDL 0.11
// Date: Sun Aug 15 15:32:51 2021


`timescale 1ns/10ps

module highorderAC (
    OUTS,
    INPUTS
);


output [7:0] OUTS;
wire [7:0] OUTS;
input [3:0] INPUTS;

wire [3:0] outs_vec;
wire [0:0] AC421_out1;
wire [0:0] AC421_out2;
wire [0:0] AC422_out1;
wire [0:0] AC422_out2;

assign outs_vec[3] = AC422_out2[0];
assign outs_vec[2] = AC422_out1[0];
assign outs_vec[1] = AC421_out2[0];
assign outs_vec[0] = AC421_out1[0];



assign AC421_out2 = (((INPUTS[0] & INPUTS[1]) | INPUTS[2]) | INPUTS[3]);
assign AC421_out1 = (((INPUTS[2] & INPUTS[3]) | INPUTS[0]) | INPUTS[1]);



assign AC422_out2 = (((INPUTS[4] & INPUTS[5]) | INPUTS[6]) | INPUTS[7]);
assign AC422_out1 = (((INPUTS[6] & INPUTS[7]) | INPUTS[4]) | INPUTS[5]);



assign OUTS = outs_vec;

endmodule