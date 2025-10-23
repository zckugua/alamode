import numpy as np

def read_poscar(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()
    latt = np.array([list(map(float, lines[i].split())) for i in range(2, 5)])
    atom_counts = list(map(int, lines[6].split()))
    n_atoms = sum(atom_counts)
    pos0 = []
    for i in range(8, 8 + n_atoms):
        pos0.append(list(map(float, lines[i].split())))
    pos0 = np.array(pos0)
    return latt, pos0

def read_positions(file_name, n_atoms):
    positions_steps = []
    with open(file_name, 'r') as f:
        lines = f.readlines()
        step_positions = []
        for i, line in enumerate(lines):
            if i % (n_atoms + 1) == 0:
                if step_positions:
                    positions_steps.append(np.array(step_positions))
                step_positions = []
            if line.strip() and len(step_positions) < n_atoms:
                step_positions.append(list(map(float, line.split())))
        if step_positions:
            positions_steps.append(np.array(step_positions))
    return positions_steps

def _refold(x):
    if x >= 0.5:
        return x - 1.0
    elif x < -0.5:
        return x + 1.0
    else:
        return x

def calculate_displacements(positions_steps, latt, pos0):
    displacements_steps = []
    for step_idx in range(len(positions_steps)):
        current_step_pos = positions_steps[step_idx]
        displacement = current_step_pos - pos0
        for i in range(len(displacement)):
            for j in range(3):
                displacement[i][j] = _refold(displacement[i][j])
        displacement = displacement @ latt.T
        displacements_steps.append(displacement)
    return displacements_steps

def write_displacements_to_file(displacements, output_file):
    with open(output_file, 'w') as f:
        for step in displacements:
            for disp in step:
                f.write(f"{disp[0]:20.15f} {disp[1]:20.15f} {disp[2]:20.15f}\n")
            f.write("\n")

latt, pos0 = read_poscar('POSCAR')
n_atoms = 40
positions_steps = read_positions('pos.dat', n_atoms)
displacements_steps = calculate_displacements(positions_steps, latt, pos0)
write_displacements_to_file(displacements_steps, 'disp.dat')
print("Atomic displacements have been written to disp.dat.")

