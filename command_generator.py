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


def modbus_command_generator(slave_id, function_code, register_address, value, byteorder, datatype):
    # Validate slave ID
    if not (0 <= slave_id <= 255):
        raise ValueError("Slave ID must be in the range 0 to 255.")

    # Validate function code
    if function_code not in {6, 16}:
        raise ValueError("Function code must be 6 (Write Single Register) or 16 (Write Multiple Registers).")

    # Validate register address
    if not (0 <= register_address <= 65535):
        raise ValueError("Register address must be in the range 0 to 65535.")

    # Validate byte order
    if byteorder not in {'HL', 'LH'}:
        raise ValueError("Byte order must be 'HL' (High to Low) or 'LH' (Low to High).")

    # Validate data type
    valid_data_types = {'S', 'U'}
    if not (datatype[0] in valid_data_types and datatype[1:3].isdigit() and datatype[-1] == 'I'):
        raise ValueError("Invalid data type.")

    if datatype[0] == 'U' and value < 0:
        raise ValueError("Unsigned data type cannot have a negative value.")

    if datatype[0] == 'S' and not (-2 ** (int(datatype[1:3]) - 1) <= value <= 2 ** (int(datatype[1:3]) - 1) - 1):
        raise ValueError(f"Value out of range for signed {datatype} data type.")

    if datatype[0] == 'U' and not (0 <= value <= 2 ** (int(datatype[1:3])) - 1):
        raise ValueError(f"Value out of range for unsigned {datatype} data type.")

    # Convert register address and value to bytes
    register_address_bytes = register_address.to_bytes(2, byteorder='big')

    if isinstance(value, int):
        if datatype[0] == 'S':
            value_bytes = struct.pack('>h', value)  # Signed 16-bit integer
        elif datatype[0] == 'U':
            value_bytes = struct.pack('>H', value)  # Unsigned 16-bit integer
        else:
            raise ValueError("Invalid datatype")
    else:
        raise ValueError("Invalid value type or datatype mismatch.")

    # Combine all parts to form the message
    message = bytearray([
        slave_id,
        function_code,
        *register_address_bytes,
        *value_bytes
    ])

    # Calculate CRC and append it to the message
    crc = calculate_crc(message)
    message += crc

    # Convert the entire message to hexadecimal
    hex_message = binascii.hexlify(message).decode('utf-8').upper()

    return hex_message

