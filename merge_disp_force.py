import numpy as np

def read_data(file_name, n_atoms):
    data = []
    with open(file_name, 'r') as f:
        lines = f.readlines()
        step_data = []
        for i, line in enumerate(lines):
            if line.strip():
                values = list(map(float, line.split()))
                step_data.append(values)
            if len(step_data) == n_atoms:
                data.append(np.array(step_data))
                step_data = []
    return np.array(data)

def write_merged_data(disp_data, force_data, output_file):
    with open(output_file, 'w') as f:
        for disp, force in zip(disp_data, force_data):
            for d, f_ in zip(disp, force):
                f.write(f"{d[0]:20.15f} {d[1]:20.15f} {d[2]:20.15f} "
                        f"{f_[0]:20.15f} {f_[1]:20.15f} {f_[2]:20.15f}\n")

n_atoms = 40
disp_data = read_data('disp.dat', n_atoms)
force_data = read_data('forces.dat', n_atoms)
if len(disp_data) != len(force_data):
    raise ValueError("The number of steps in disp.dat and forces.dat do not match.")
write_merged_data(disp_data, force_data, 'DFSET')
print("Data has been merged and written to DFSET.")

