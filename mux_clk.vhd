Library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;

entity mux_clk is

port(
		i_clk0	: in std_logic;
		i_clk1	: in std_logic;
		i_clk2	: in std_logic;
		o_clk:out std_logic);
end entity;

architecture arch_mux_clk of mux_clk is
begin
		o_clk <= i_clk0;
		--o_clk <= i_clk1;
		--o_clk <= i_clk2;
end architecture;