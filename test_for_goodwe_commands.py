import command_generator as cgen

commands_required=[
    [1,6,47000,3,'HL','U16I'],
    [1,6,47518,65407,'HL','U16I'],
    [1,6,47515,0,'HL','U16I'],
    [1,6,47516,5947,'HL','U16I'],
    [1,6,47517,-100,'HL','S16I'],
    [1,6,47517,100,'HL','S16I'],
    [1,6,47517,-1,'HL','S16I'],
    [1,6,47517,0,'HL','S16I'],
]

commands_required_reading=[
    [1,3,35187,1]]


for i in commands_required:
    try:
        modbus_command = cgen.modbus_command_generator(*i)
        cgen.print_spaced_command(modbus_command)
    except ValueError as e:
        print(f"Error: {e}")

print('\n')

for i in commands_required_reading:
    try:
        modbus_command = cgen.modbus_reading_command_generator(*i)
        cgen.print_spaced_command(modbus_command)
    except ValueError as e:
        print(f"Error: {e}")

