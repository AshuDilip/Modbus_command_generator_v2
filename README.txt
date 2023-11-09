README

command_generator.py 

This file can be used to generate modbus commands. 

modbus_command_generator(slave_id, function_code, register_address, value, byteorder, datatype)
slave_id: between 0 to 255
function_code: 6 or 16 (write single or multiple registers. Writing multiple registers is not supported yet, you guys can implement it later if needed by adding an extra arguement).
register_address: register address between 0 and 65535
value: value to be written (it checks if it is valid for the entered datatype) 
byteorder: 'HL' or 'LH' for high to low or low to high. 
datatype: 4 charecters. First charecter S or U, second and third are numbers (number of bits), third is type. Example: unsigned integer of 16 bits is 'U16I'. Right now only 'U16I','S16I','U32I','S32I' are supported. Those are all we have used so far. You guys can add float if you want. 

calculate_crc(data) 

Calculates CRC based on data inputted. 

print_spaced_command(modbus_command)

Prints the command with spaces after every other charecter so it is easier to read. 

test_for_goodwe_commands.py

Example use case of commands on Goodwe device control page. 