Library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;

entity phase_increment_PLL_Test is
generic(NumOfBits : integer := 20);
port(
		check : in std_logic;
		--check : in std_logic_vector(1 downto 0);
		increment :out std_logic_vector(numOfBits-1 downto 0));
end entity;

architecture arch_phase_increment_PLL_Test of phase_increment_PLL_Test is
begin
--increment <= 				 conv_std_logic_vector(104858,numOfBits); -- 1.25M
increment <= --conv_std_logic_vector(26214,numOfBits) when check = '0' else
				 --conv_std_logic_vector(2*209715,numOfBits) when check = '1' else
				 conv_std_logic_vector(104858,numOfBits); -- 1.25M when sig = 50M
				 --conv_std_logic_vector(262144,numOfBits); -- 1.25M when sig = 50M

	
end architecture;