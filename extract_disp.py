import numpy as np

def read_poscar(file_name):
    """
    从 POSCAR 文件中读取初始原子位置和晶格矢量
    """
    with open(file_name, 'r') as f:
        lines = f.readlines()

    # 读取晶格矢量
    latt = np.array([list(map(float, lines[i].split())) for i in range(2, 5)])

    # 读取原子种类（跳过第一行和第二行）
    atom_counts = list(map(int, lines[6].split()))
    n_atoms = sum(atom_counts)  # 计算总原子数

    # 读取初始原子位置（跳过前 8 行）
    pos0 = []
    for i in range(8, 8 + n_atoms):
        pos0.append(list(map(float, lines[i].split())))
    pos0 = np.array(pos0)

    return latt, pos0

def read_positions(file_name, n_atoms):
    """
    从 pos.dat 文件中读取每个时间步的原子位置
    """
    positions_steps = []
    with open(file_name, 'r') as f:
        lines = f.readlines()
        step_positions = []
        for i, line in enumerate(lines):
            if i % (n_atoms + 1) == 0:  # 每个时间步的数据以空行隔开
                if step_positions:
                    positions_steps.append(np.array(step_positions))
                step_positions = []
            if line.strip() and len(step_positions) < n_atoms:
                step_positions.append(list(map(float, line.split())))
        if step_positions:
            positions_steps.append(np.array(step_positions))  # 追加最后一个时间步
    return positions_steps

def _refold(x):
    """
    折叠原子位置，使其保持在 [-0.5, 0.5) 区间内
    """
    if x >= 0.5:
        return x - 1.0
    elif x < -0.5:
        return x + 1.0
    else:
        return x

def calculate_displacements(positions_steps, latt, pos0):
    """
    计算每个时间步的原子位移
    """
    displacements_steps = []

    # 计算每一步的位移，都是相对于初始坐标 pos0 计算
    for step_idx in range(len(positions_steps)):
        current_step_pos = positions_steps[step_idx]
        displacement = current_step_pos - pos0  # 相对于初始坐标的位移

        # 折叠超出晶胞范围的位移
        for i in range(len(displacement)):
            for j in range(3):
                displacement[i][j] = _refold(displacement[i][j])
        
        displacement = displacement @ latt.T
        displacements_steps.append(displacement)

    return displacements_steps

def write_displacements_to_file(displacements, output_file):
    """
    将位移数据写入文件
    """
    with open(output_file, 'w') as f:
        for step in displacements:
            for disp in step:
                # 每个原子的位移为一行，格式为 x, y, z
                f.write(f"{disp[0]:20.15f} {disp[1]:20.15f} {disp[2]:20.15f}\n")
            f.write("\n")  # 每个 step 之间空一行

# 读取 POSCAR 文件中的晶格矢量和初始位置
latt, pos0 = read_poscar('POSCAR')  # 读取 POSCAR 文件

# 读取 pos.dat 文件中的每个时间步的位置
n_atoms = 40  # 原子数
positions_steps = read_positions('pos.dat', n_atoms)  # 读取位置数据

# 计算每个时间步的原子位移
displacements_steps = calculate_displacements(positions_steps, latt, pos0)

# 将位移数据写入 disp.dat 文件
write_displacements_to_file(displacements_steps, 'disp.dat')

print("Atomic displacements have been written to disp.dat.")

