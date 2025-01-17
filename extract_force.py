import xml.etree.ElementTree as ET

def extract_forces(vasprun_file):
    # 解析 XML 文件
    tree = ET.parse(vasprun_file)
    root = tree.getroot()

    # 存储每个 step 的原子受力数据
    forces_steps = []

    # 不跳过任何数据块，直接读取所有 <varray name="forces"> 数据
    for varray in root.findall('.//varray[@name="forces"]'):
        step_forces = []
        for v in varray.findall('v'):
            # 提取原子受力数据（x, y, z 方向的力）
            forces = [float(x) for x in v.text.split()]
            step_forces.append(forces)

        forces_steps.append(step_forces)

    return forces_steps

def write_forces_to_file(forces_steps, output_file):
    # 打开文件并写入数据
    with open(output_file, 'w') as f:
        for step in forces_steps:
            for force in step:
                # 每个原子的受力数据为一行，格式为 x, y, z
                f.write(f"{force[0]:20.15f} {force[1]:20.15f} {force[2]:20.15f}\n")
            f.write("\n")  # 每个 step 之间空一行

# 读取 vasprun.xml 文件并提取所有原子受力数据
vasprun_file = 'vasprun.xml'  # 替换为你的文件路径
forces_steps = extract_forces(vasprun_file)

# 将原子受力数据写入 forces.dat 文件
output_file = 'forces.dat'
write_forces_to_file(forces_steps, output_file)

print(f"Atomic forces have been written to {output_file}.")

