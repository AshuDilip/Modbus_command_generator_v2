# README

## command_generator.py 

This file can be used to generate modbus commands. 

> modbus_command_generator(slave_id, function_code, register_address, value_array, byteorder, datatype)

- slave_id: between 0 to 255
- function_code: 6 or 16 (write single or multiple registers. Writing multiple registers is dony by using a list with the inputs as [value1,value2,value3] etc)
- register_address: register address between 0 and 65535
- value: value to be written (it checks if it is valid for the entered datatype) 
- byteorder: 'HL' or 'LH' for high to low or low to high. 
-datatype: 4 charecters. First charecter S or U, second and third are numbers (number of bits), third is type. Example: unsigned integer of 16 bits is 'U16I'. Right now only {'S16I', 'U16I', 'S32I', 'U32I', 'S32F', 'U32F', 'S64F', 'U64F', 'S64I', 'U64I'} are supported. 'U32F' and 'U64F' are not a real datatype, so if you enter that then the code will just treat it as a 'S32F' or 'S64F'. But it will not let you write negative numbers, so best not to use this.  

> calculate_crc(data)

 Calculates CRC based on data inputted. 

> print_spaced_command(modbus_command)

 Prints the command with spaces after every other charecter so it is easier to read. 

> modbus_reading_command_generator(slave_id, function_code, register_address, number_of_regs)

- slave_id: between 0 to 255
- function_code: 3 or 4 (read holding or input register)
- register_address: register address between 0 and 65535
- number_of_regs: number of registers to be read 

> test_for_goodwe_commands.py

Example use case of commands on Goodwe device control page. 
