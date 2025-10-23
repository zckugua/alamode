import xml.etree.ElementTree as ET

def extract_forces(vasprun_file):
    tree = ET.parse(vasprun_file)
    root = tree.getroot()
    forces_steps = []

    for varray in root.findall('.//varray[@name="forces"]'):
        step_forces = []
        for v in varray.findall('v'):
            forces = [float(x) for x in v.text.split()]
            step_forces.append(forces)

        forces_steps.append(step_forces)

    return forces_steps

def write_forces_to_file(forces_steps, output_file):
    with open(output_file, 'w') as f:
        for step in forces_steps:
            for force in step:
                f.write(f"{force[0]:20.15f} {force[1]:20.15f} {force[2]:20.15f}\n")
            f.write("\n")

vasprun_file = 'vasprun.xml'
forces_steps = extract_forces(vasprun_file)

output_file = 'forces.dat'
write_forces_to_file(forces_steps, output_file)

print(f"Atomic forces have been written to {output_file}.")

