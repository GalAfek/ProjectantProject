module DAC_Module(clk, dac_a,sigin,sigin_FM, DAC_WRT_A, DAC_WRT_B, DAC_MODE, DAC_CLK_A, DAC_CLK_B, DAC_B, ADC_DA, ADC_OEB_A, ADC_CLK_A, adc_out); 

output [13:0] dac_a; // GPIO Connection 0
			// GPIO Connection 1
			output [13:0] adc_out;
			input [13:0] ADC_DA;
			output ADC_OEB_A;
			output ADC_CLK_A;


input [13:0] sigin;
input [13:0] sigin_FM;
input clk;
output DAC_CLK_A;
output DAC_CLK_B;
output DAC_MODE;
output DAC_WRT_A;
output DAC_WRT_B;
output [13:0] DAC_B;





assign DAC_WRT_A = clk; //Input write signal for PORT A
assign DAC_WRT_B = clk; //Input write signal for PORT B 

assign DAC_MODE = 1; //Mode select. 1 = dual port, 0 interleaved.


assign DAC_CLK_A = clk; //PLL clock to DAC A
assign DAC_CLK_B = clk; //PLL Clock to DAC B 


assign DAC_B = {~sigin[13],sigin[12:0]};
assign dac_a = {~sigin_FM[13],sigin_FM[12:0]};


assign ADC_CLK_A = clk;//PLL clock to ADC_A

assign ADC_OEB_A = 0;//ADC_OEA

assign adc_out = {ADC_DA [13], ADC_DA[12:0]};


endmodule