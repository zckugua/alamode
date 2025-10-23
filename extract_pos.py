import xml.etree.ElementTree as ET

def extract_positions(vasprun_file):
    tree = ET.parse(vasprun_file)
    root = tree.getroot()
    positions_steps = []
    positions_count = 0 
    for varray in root.findall('.//varray[@name="positions"]'):
        if positions_count < 2:
            positions_count += 1
            continue
        step_positions = []
        for v in varray.findall('v'):
            positions = [float(x) for x in v.text.split()]
            step_positions.append(positions)
        positions_steps.append(step_positions)
    if positions_steps:
        positions_steps.pop()
    return positions_steps

def write_positions_to_file(positions_steps, output_file):
    with open(output_file, 'w') as f:
        for step in positions_steps:
            for position in step:
                f.write(f"{position[0]:20.15f} {position[1]:20.15f} {position[2]:20.15f}\n")
            f.write("\n")
            
vasprun_file = 'vasprun.xml'
positions_steps = extract_positions(vasprun_file)
output_file = 'pos.dat'
write_positions_to_file(positions_steps, output_file)
print(f"Atomic positions have been written to {output_file}.")

