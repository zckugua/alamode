import xml.etree.ElementTree as ET

def extract_positions(vasprun_file):
    # 解析 XML 文件
    tree = ET.parse(vasprun_file)
    root = tree.getroot()

    # 存储每个 step 的原子位置
    positions_steps = []

    # 跳过前两个 <varray name="positions"> 标签后的数据
    positions_count = 0  # 计数器，用于跳过前两个数据块
    for varray in root.findall('.//varray[@name="positions"]'):
        if positions_count < 2:
            positions_count += 1  # 跳过前两个 positions 数据块
            continue

        step_positions = []
        for v in varray.findall('v'):
            # 提取原子位置（分数坐标）并转换为浮动类型
            positions = [float(x) for x in v.text.split()]
            step_positions.append(positions)

        positions_steps.append(step_positions)

    # 删除最后一个数据块
    if positions_steps:
        positions_steps.pop()  # 删除最后一个数据块

    return positions_steps

def write_positions_to_file(positions_steps, output_file):
    # 打开文件并写入数据
    with open(output_file, 'w') as f:
        for step in positions_steps:
            for position in step:
                # 每个原子的位置为一行，格式为 x, y, z
                f.write(f"{position[0]:20.15f} {position[1]:20.15f} {position[2]:20.15f}\n")
            f.write("\n")  # 每个 step 之间空一行

# 读取 vasprun.xml 文件并提取所有原子位置数据
vasprun_file = 'vasprun.xml'  # 替换为你的文件路径
positions_steps = extract_positions(vasprun_file)

# 将原子位置写入 pos.dat 文件
output_file = 'pos.dat'
write_positions_to_file(positions_steps, output_file)

print(f"Atomic positions have been written to {output_file}.")

