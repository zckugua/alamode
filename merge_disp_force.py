import numpy as np

def read_data(file_name, n_atoms):
    """
    读取数据文件，每 40 行表示一个时间步，每行有 6 个数字（3 个位移，3 个受力），
    每 40 行之间有一个空行需要跳过。
    """
    data = []
    with open(file_name, 'r') as f:
        lines = f.readlines()
        step_data = []
        for i, line in enumerate(lines):
            if line.strip():  # 跳过空行
                values = list(map(float, line.split()))  # 将每行数据转换为浮动类型
                step_data.append(values)
            
            # 每 40 行（对应 n_atoms 个原子）加一个空行
            if len(step_data) == n_atoms:
                data.append(np.array(step_data))
                step_data = []  # 重置当前步的数据
    return np.array(data)

def write_merged_data(disp_data, force_data, output_file):
    """
    将位移数据和受力数据合并并写入输出文件
    """
    # 确保 `f` 是文件对象
    with open(output_file, 'w') as f:
        for disp, force in zip(disp_data, force_data):
            # 合并位移数据和受力数据，格式：disp_x disp_y disp_z force_x force_y force_z
            for d, f_ in zip(disp, force):
                f.write(f"{d[0]:20.15f} {d[1]:20.15f} {d[2]:20.15f} "
                        f"{f_[0]:20.15f} {f_[1]:20.15f} {f_[2]:20.15f}\n")

# 设置原子数
n_atoms = 40

# 读取数据文件
disp_data = read_data('disp.dat', n_atoms)  # 读取位移数据
force_data = read_data('forces.dat', n_atoms)  # 读取受力数据

# 确保两个数据文件的行数一致
if len(disp_data) != len(force_data):
    raise ValueError("The number of steps in disp.dat and forces.dat do not match.")

# 将位移和受力数据合并并写入新文件
write_merged_data(disp_data, force_data, 'DFSET')

print("Data has been merged and written to DFSET.")

