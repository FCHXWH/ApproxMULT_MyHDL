// File: CompressorTree.v
// Generated by MyHDL 0.11
// Date: Tue Aug 10 11:35:08 2021


`timescale 1ns/10ps

module CompressorTree (
    OUTS,
    INPUTS
);


output [28:0] OUTS;
wire [28:0] OUTS;
input [63:0] INPUTS;

wire [28:0] outs_vec;
wire [0:0] AC320_0_out1;
wire [0:0] AC320_0_out2;
wire [0:0] AC321_out1;
wire [0:0] AC321_out2;
wire [0:0] AC322_out1;
wire [0:0] AC322_out2;
wire [0:0] AC323_out1;
wire [0:0] AC323_out2;
wire [0:0] AC324_out1;
wire [0:0] AC324_out2;
wire [0:0] AC325_out1;
wire [0:0] AC325_out2;
wire [0:0] FA0_0_cout;
wire [0:0] FA0_0_sum;
wire [0:0] FA1_cout;
wire [0:0] FA1_sum;
wire [0:0] FA2_cout;
wire [0:0] FA2_sum;
wire [0:0] FA3_cout;
wire [0:0] FA3_sum;
wire [0:0] FA4_cout;
wire [0:0] FA4_sum;
wire [0:0] FA5_cout;
wire [0:0] FA5_sum;
wire [0:0] FA6_cout;
wire [0:0] FA6_sum;
wire [0:0] FA7_cout;
wire [0:0] FA7_sum;
wire [0:0] FA8_cout;
wire [0:0] FA8_sum;
wire [0:0] AC326_out1;
wire [0:0] AC326_out2;
wire [0:0] AC327_out1;
wire [0:0] AC327_out2;
wire [0:0] AC328_out1;
wire [0:0] AC328_out2;
wire [0:0] FA9_cout;
wire [0:0] FA9_sum;
wire [0:0] AC329_out1;
wire [0:0] AC329_out2;
wire [0:0] FA10_cout;
wire [0:0] FA10_sum;
wire [0:0] FA11_cout;
wire [0:0] FA11_sum;
wire [0:0] FA12_cout;
wire [0:0] FA12_sum;
wire [0:0] HA0_0_cout;
wire [0:0] HA0_0_sum;
wire [0:0] FA13_cout;
wire [0:0] FA13_sum;
wire [0:0] AC3210_out1;
wire [0:0] AC3210_out2;
wire [0:0] AC3211_out1;
wire [0:0] AC3211_out2;
wire [0:0] AC3212_out1;
wire [0:0] AC3212_out2;
wire [0:0] AC3213_out1;
wire [0:0] AC3213_out2;
wire [0:0] FA14_cout;
wire [0:0] FA14_sum;
wire [0:0] FA15_cout;
wire [0:0] FA15_sum;
wire [0:0] FA16_cout;
wire [0:0] FA16_sum;
wire [0:0] FA17_cout;
wire [0:0] FA17_sum;
wire [0:0] FA18_cout;
wire [0:0] FA18_sum;
wire [0:0] FA19_cout;
wire [0:0] FA19_sum;
wire [0:0] FA20_cout;
wire [0:0] FA20_sum;

assign outs_vec[28] = FA20_cout[0];
assign outs_vec[27] = INPUTS[63];
assign outs_vec[26] = FA19_cout[0];
assign outs_vec[25] = FA20_sum[0];
assign outs_vec[24] = FA18_cout[0];
assign outs_vec[23] = FA19_sum[0];
assign outs_vec[22] = FA17_cout[0];
assign outs_vec[21] = FA18_sum[0];
assign outs_vec[20] = FA16_cout[0];
assign outs_vec[19] = FA17_sum[0];
assign outs_vec[18] = FA15_cout[0];
assign outs_vec[17] = FA16_sum[0];
assign outs_vec[16] = FA14_cout[0];
assign outs_vec[15] = FA15_sum[0];
assign outs_vec[14] = FA14_sum[0];
assign outs_vec[13] = FA1_sum[0];
assign outs_vec[12] = AC3213_out2[0];
assign outs_vec[11] = AC3213_out1[0];
assign outs_vec[10] = AC3212_out2[0];
assign outs_vec[9] = AC3212_out1[0];
assign outs_vec[8] = AC3211_out2[0];
assign outs_vec[7] = AC3211_out1[0];
assign outs_vec[6] = AC326_out1[0];
assign outs_vec[5] = AC326_out2[0];
assign outs_vec[4] = AC3210_out2[0];
assign outs_vec[3] = AC3210_out1[0];
assign outs_vec[2] = INPUTS[2];
assign outs_vec[1] = INPUTS[1];
assign outs_vec[0] = INPUTS[0];



assign AC320_0_out2 = ((INPUTS[7] & INPUTS[8]) | INPUTS[9]);
assign AC320_0_out1 = (INPUTS[7] | INPUTS[8]);



assign AC321_out2 = ((INPUTS[12] & INPUTS[13]) | INPUTS[14]);
assign AC321_out1 = (INPUTS[12] | INPUTS[13]);



assign AC322_out2 = ((INPUTS[15] & INPUTS[16]) | INPUTS[17]);
assign AC322_out1 = (INPUTS[15] | INPUTS[16]);



assign AC323_out2 = ((INPUTS[18] & INPUTS[19]) | INPUTS[20]);
assign AC323_out1 = (INPUTS[18] | INPUTS[19]);



assign AC324_out2 = ((INPUTS[22] & INPUTS[23]) | INPUTS[24]);
assign AC324_out1 = (INPUTS[22] | INPUTS[23]);



assign AC325_out2 = ((INPUTS[25] & INPUTS[26]) | INPUTS[27]);
assign AC325_out1 = (INPUTS[25] | INPUTS[26]);



assign FA0_0_sum = ((INPUTS[30] ^ INPUTS[31]) ^ INPUTS[32]);
assign FA0_0_cout = (((INPUTS[30] & INPUTS[31]) | (INPUTS[30] & INPUTS[32])) | (INPUTS[31] & INPUTS[32]));



assign FA1_sum = ((INPUTS[33] ^ INPUTS[34]) ^ INPUTS[35]);
assign FA1_cout = (((INPUTS[33] & INPUTS[34]) | (INPUTS[33] & INPUTS[35])) | (INPUTS[34] & INPUTS[35]));



assign FA2_sum = ((INPUTS[37] ^ INPUTS[38]) ^ INPUTS[39]);
assign FA2_cout = (((INPUTS[37] & INPUTS[38]) | (INPUTS[37] & INPUTS[39])) | (INPUTS[38] & INPUTS[39]));



assign FA3_sum = ((INPUTS[40] ^ INPUTS[41]) ^ INPUTS[42]);
assign FA3_cout = (((INPUTS[40] & INPUTS[41]) | (INPUTS[40] & INPUTS[42])) | (INPUTS[41] & INPUTS[42]));



assign FA4_sum = ((INPUTS[43] ^ INPUTS[44]) ^ INPUTS[45]);
assign FA4_cout = (((INPUTS[43] & INPUTS[44]) | (INPUTS[43] & INPUTS[45])) | (INPUTS[44] & INPUTS[45]));



assign FA5_sum = ((INPUTS[46] ^ INPUTS[47]) ^ INPUTS[48]);
assign FA5_cout = (((INPUTS[46] & INPUTS[47]) | (INPUTS[46] & INPUTS[48])) | (INPUTS[47] & INPUTS[48]));



assign FA6_sum = ((INPUTS[51] ^ INPUTS[52]) ^ INPUTS[53]);
assign FA6_cout = (((INPUTS[51] & INPUTS[52]) | (INPUTS[51] & INPUTS[53])) | (INPUTS[52] & INPUTS[53]));



assign FA7_sum = ((INPUTS[55] ^ INPUTS[56]) ^ INPUTS[57]);
assign FA7_cout = (((INPUTS[55] & INPUTS[56]) | (INPUTS[55] & INPUTS[57])) | (INPUTS[56] & INPUTS[57]));



assign FA8_sum = ((INPUTS[58] ^ INPUTS[59]) ^ INPUTS[60]);
assign FA8_cout = (((INPUTS[58] & INPUTS[59]) | (INPUTS[58] & INPUTS[60])) | (INPUTS[59] & INPUTS[60]));



assign AC326_out2 = ((AC320_0_out1 & AC320_0_out2) | INPUTS[6]);
assign AC326_out1 = (AC320_0_out1 | AC320_0_out2);



assign AC327_out2 = ((INPUTS[10] & AC321_out2) | INPUTS[11]);
assign AC327_out1 = (INPUTS[10] | AC321_out2);



assign AC328_out2 = ((AC323_out1 & AC323_out2) | AC322_out2);
assign AC328_out1 = (AC323_out1 | AC323_out2);



assign FA9_sum = ((AC324_out2 ^ AC324_out1) ^ AC325_out1);
assign FA9_cout = (((AC324_out2 & AC324_out1) | (AC324_out2 & AC325_out1)) | (AC324_out1 & AC325_out1));



assign AC329_out2 = ((INPUTS[29] & INPUTS[28]) | FA0_0_sum);
assign AC329_out1 = (INPUTS[29] | INPUTS[28]);



assign FA10_sum = ((FA1_cout ^ FA0_0_cout) ^ FA2_sum);
assign FA10_cout = (((FA1_cout & FA0_0_cout) | (FA1_cout & FA2_sum)) | (FA0_0_cout & FA2_sum));



assign FA11_sum = ((FA5_sum ^ FA2_cout) ^ FA3_cout);
assign FA11_cout = (((FA5_sum & FA2_cout) | (FA5_sum & FA3_cout)) | (FA2_cout & FA3_cout));



assign FA12_sum = ((INPUTS[49] ^ INPUTS[50]) ^ FA6_sum);
assign FA12_cout = (((INPUTS[49] & INPUTS[50]) | (INPUTS[49] & FA6_sum)) | (INPUTS[50] & FA6_sum));



assign HA0_0_sum = (FA5_cout ^ FA4_cout);
assign HA0_0_cout = (FA5_cout & FA4_cout);



assign FA13_sum = ((INPUTS[54] ^ FA6_cout) ^ FA7_sum);
assign FA13_cout = (((INPUTS[54] & FA6_cout) | (INPUTS[54] & FA7_sum)) | (FA6_cout & FA7_sum));



assign AC3210_out2 = ((INPUTS[4] & INPUTS[3]) | INPUTS[5]);
assign AC3210_out1 = (INPUTS[4] | INPUTS[3]);



assign AC3211_out2 = ((AC321_out1 & AC327_out1) | AC327_out2);
assign AC3211_out1 = (AC321_out1 | AC327_out1);



assign AC3212_out2 = ((AC328_out2 & AC322_out1) | AC328_out1);
assign AC3212_out1 = (AC328_out2 | AC322_out1);



assign AC3213_out2 = ((AC325_out2 & INPUTS[21]) | FA9_sum);
assign AC3213_out1 = (AC325_out2 | INPUTS[21]);



assign FA14_sum = ((AC329_out1 ^ AC329_out2) ^ FA9_cout);
assign FA14_cout = (((AC329_out1 & AC329_out2) | (AC329_out1 & FA9_cout)) | (AC329_out2 & FA9_cout));



assign FA15_sum = ((FA10_sum ^ INPUTS[36]) ^ FA3_sum);
assign FA15_cout = (((FA10_sum & INPUTS[36]) | (FA10_sum & FA3_sum)) | (INPUTS[36] & FA3_sum));



assign FA16_sum = ((FA10_cout ^ FA11_sum) ^ FA4_sum);
assign FA16_cout = (((FA10_cout & FA11_sum) | (FA10_cout & FA4_sum)) | (FA11_sum & FA4_sum));



assign FA17_sum = ((HA0_0_sum ^ FA12_sum) ^ FA11_cout);
assign FA17_cout = (((HA0_0_sum & FA12_sum) | (HA0_0_sum & FA11_cout)) | (FA12_sum & FA11_cout));



assign FA18_sum = ((HA0_0_cout ^ FA13_sum) ^ FA12_cout);
assign FA18_cout = (((HA0_0_cout & FA13_sum) | (HA0_0_cout & FA12_cout)) | (FA13_sum & FA12_cout));



assign FA19_sum = ((FA8_sum ^ FA7_cout) ^ FA13_cout);
assign FA19_cout = (((FA8_sum & FA7_cout) | (FA8_sum & FA13_cout)) | (FA7_cout & FA13_cout));



assign FA20_sum = ((FA8_cout ^ INPUTS[62]) ^ INPUTS[61]);
assign FA20_cout = (((FA8_cout & INPUTS[62]) | (FA8_cout & INPUTS[61])) | (INPUTS[62] & INPUTS[61]));



assign OUTS = outs_vec;

endmodule