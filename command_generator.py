import struct
import binascii


def print_spaced_command(modbus_command):
    spaced_command = ' '.join(modbus_command[i:i+2] for i in range(0, len(modbus_command), 2))
    print(spaced_command)

def calculate_crc(data):
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc.to_bytes(2, byteorder='little')

def modbus_command_generator(slave_id, function_code, register_address, value_array, byteorder, datatype):
    #check if single value is entered or multiple
    try:
        x = len(value_array)
    except:
        value_array = [value_array]
    # Validate slave ID
    if not (0 <= slave_id <= 255):
        raise ValueError("Slave ID must be in the range 0 to 255.")

    # Validate function code
    if function_code not in {6, 16}:
        raise ValueError("Function code must be 6 (Write Single Register), 16 (Write Multiple Registers).")

    if function_code == 6 and len(value_array)>1:
        raise ValueError("Function code must 16 when writing multiple registers.")

    # Validate register address
    if not (0 <= register_address <= 65535):
        raise ValueError("Register address must be in the range 0 to 65535.")

    # Validate byte order
    if byteorder not in {'HL', 'LH'}:
        raise ValueError("Byte order must be 'HL' (High to Low) or 'LH' (Low to High).")

    #Pack struct according to byteorder
    if byteorder=='HL':
        pack_sign='>'
    else:
        pack_sign='<'

    # Validate data type
    valid_data_types = {'S16I', 'U16I', 'S32I', 'U32I', 'S32F', 'U32F', 'S64F', 'U64F', 'S64I', 'U64I'}
    if datatype not in valid_data_types:
        raise ValueError("Invalid data type.")

    # Convert register address and value to bytes
    register_address_bytes = register_address.to_bytes(2, byteorder='big')

    message = bytearray([
        slave_id,
        function_code,
        *register_address_bytes,
    ])

    for value in value_array:

        if datatype[0] == 'U' and value < 0:
            raise ValueError("Unsigned data type cannot have a negative value.")

        if datatype[3] == 'I':
            if datatype[0] == 'S' and not (-2 ** (int(datatype[1:3]) - 1) <= value <= 2 ** (int(datatype[1:3]) - 1) - 1):
                 raise ValueError(f"Value out of range for signed {datatype} data type.")

            if datatype[0] == 'U' and not (0 <= value <= 2 ** (int(datatype[1:3])) - 1):
                 raise ValueError(f"Value out of range for unsigned {datatype} data type.")

            if [datatype[1],datatype[2]] == ['1','6']:
                if datatype[0] == 'S':
                    value_bytes = struct.pack(pack_sign+'h', value)  # Signed 16-bit integer (short)
                elif datatype[0] == 'U':
                    value_bytes = struct.pack(pack_sign+'H', value)  # Unsigned 16-bit integer (unsigned short)
                else:
                    raise ValueError("Datatype and bytesize mismatch")
            elif [datatype[1],datatype[2]] == ['3','2']:
                if datatype[0] == 'S':
                    value_bytes = struct.pack(pack_sign+'i', value)  # Signed 32-bit integer (int)
                elif datatype[0] == 'U':
                    value_bytes = struct.pack(pack_sign+'I', value)  # Unsigned 32-bit integer (unsigned int)
                else:
                    raise ValueError("Datatype and bytesize mismatch")
            elif [datatype[1],datatype[2]] == ['6','4']:
                if datatype[0] == 'S':
                    value_bytes = struct.pack(pack_sign+'q', value)  # Signed 64-bit integer (long long)
                elif datatype[0] == 'U':
                    value_bytes = struct.pack(pack_sign+'Q', value)  # Unsigned 64-bit integer (unsigned long long)
                else:
                    raise ValueError("Datatype and bytesize mismatch")
            else:
                raise ValueError("Invalid datatype")

        elif datatype[3]=='F':
            if [datatype[1], datatype[2]] == ['3', '2']:
                value_bytes = struct.pack(pack_sign+'f', value)  # Float32 (float)
            elif [datatype[1], datatype[2]] == ['6', '4']:
                value_bytes = struct.pack(pack_sign+'d', value)  # Float64 (double)
            else:
                raise ValueError("Datatype and bytesize mismatch")
        else:
            raise ValueError("Invalid datatype")

        # Combine all parts to form the message
        message.extend(bytearray([*value_bytes]))

    # Calculate CRC and append it to the message
    crc = calculate_crc(message)
    message += crc

    # Convert the entire message to hexadecimal
    hex_message = binascii.hexlify(message).decode('utf-8').upper()

    return hex_message

def modbus_reading_command_generator(slave_id, function_code, register_address, number_of_regs):
    # Validate slave ID
    if not (0 <= slave_id <= 255):
        raise ValueError("Slave ID must be in the range 0 to 255.")

    # Validate function code
    if function_code not in {3, 4}:
        raise ValueError("Function code must be 3 (Read Holding Register), 4 (Read Input Registers).")

    # Validate register address
    if not (0 <= register_address <= 65535):
        raise ValueError("Register address must be in the range 0 to 65535.")

    if not (1 <= number_of_regs <= 65535):
        raise ValueError("Number of registers must be in the range 1 to 65535.")

    # Convert register address and value to bytes
    register_address_bytes = register_address.to_bytes(2, byteorder='big')

    number_of_regs_bytes=number_of_regs.to_bytes(2, byteorder='big')

    message = bytearray([
        slave_id,
        function_code,
        *register_address_bytes,
        *number_of_regs_bytes,
    ])

    # Calculate CRC and append it to the message
    crc = calculate_crc(message)
    message += crc

    # Convert the entire message to hexadecimal
    hex_message = binascii.hexlify(message).decode('utf-8').upper()

    return hex_message




