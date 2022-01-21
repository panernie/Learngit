import pandas as pd
import numpy as np
import os
import math
import argparse
import time
from tqdm import tqdm


def ring_cm(atom_list_id, df):
    C1, C2, C3, C4, C5, C6 = [[] for i in range(1, 7)]
    C_list = [C1, C2, C3, C4, C5, C6]
    for x, y in enumerate(atom_list_id):
        for i in df.index:
            if int(df.loc[i, "atom_nums"]) == int(y):
                C_list[x].append(
                    np.array(
                        [
                            float(df.loc[i, "x"]),
                            float(df.loc[i, "y"]),
                            float(df.loc[i, "z"]),
                        ]
                    )
                )
                # atom_id2name.append(df.loc[i,"atom_names"])
    dft = pd.DataFrame(C_list)
    ring_cm_xyz = dft.sum(axis=0) / 6
    return ring_cm_xyz, C1, C2, C3, C4, C5, C6, C_list


class point(object):  # 定义空间点类
    """docstring for point"""

    def __init__(self, x, y, z, name):
        self.x = x
        self.y = y
        self.z = z
        self.name = name


class plane(object):  # 定义平面类
    """docstring for plane"""

    def __init__(self, A, B, C, name):
        self.points = [A, B, C]  # 一个平面三个点
        self.points_name = [A.name, B.name, C.name]  # 点的名字
        self.name = name  # 平面的名字
        self.n = []  # 平面的法向量

    def isplane(self):  # 判断这三个点是否能构成平面
        coors = [[], [], []]  # 三个点的xyz坐标分别放在同一个列表用来比较
        for _point in self.points:  # 对于每个点
            coors[0].append(_point.x)
            coors[1].append(_point.y)
            coors[2].append(_point.z)
        for coor in coors:
            if coor[0] == coor[1] == coor[2]:  # 如果三个点的x或y或z坐标相等 则不能构成平面
                return print('Points:', *self.points_name, 'cannot form a plane')

    def normal(self):  # 获得该平面的法向量
        self.isplane()  # 获得该平面的法向量前提是能构成平面
        A, B, C = self.points  # 对应三个点
        AB = [B.x - A.x, B.y - A.y, B.z - A.z]  # 向量AB
        AC = [C.x - A.x, C.y - A.y, C.z - A.z]  # 向量AC
        B1, B2, B3 = AB  # 向量AB的xyz坐标
        C1, C2, C3 = AC  # 向量AC的xyz坐标
        self.n = [
            B2 * C3 - C2 * B3,
            B3 * C1 - C3 * B1,
            B1 * C2 - C1 * B2,
        ]  # 已知该平面的两个向量,求该平面的法向量的叉乘公式

    def angle(self, P2):  # 两个平面的夹角
        x1, y1, z1 = self.n  # 该平面的法向量的xyz坐标
        x2, y2, z2 = P2.n  # 另一个平面的法向量的xyz坐标
        cosθ = ((x1 * x2) + (y1 * y2) + (z1 * z2)) / (
            ((x1 ** 2 + y1 ** 2 + z1 ** 2) ** 0.5)
            * ((x2 ** 2 + y2 ** 2 + z2 ** 2) ** 0.5)
        )  # 平面向量的二面角公式
        degree = math.degrees(math.acos(cosθ))
        if degree > 90:  # 二面角∈[0°,180°] 但两个平面的夹角∈[0°,90°]
            degree = 180 - degree
            # print('平面',self.name,P2.name,'的夹角为'+str(round(degree,5))+'°')
        return degree
        # round(数值,四舍五入位数) math.degrees(弧度)将弧度转换为角度 math.acos(数值)返回该数值的反余弦弧度值


def main():
    """https://github.com/CharlesHahn/DuIvy/blob/master/sources/pipi_dist_ang/pipi_dist_ang.py"""
    print("计算两个5元或6元环的距离和角度")
    parser = argparse.ArgumentParser(description="计算环的距离和角度")
    parser.add_argument(
        "-n",
        "--index",
        help="index file which contains two groups of rings",
        required=True,
    )
    parser.add_argument(
        "-f",
        "--input",
        help="gro file",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output",
        default="output.xvg",
        help="可以保存为xvg或者csv文件，the results data, default output.xvg",
    )
    args = parser.parse_args()
    # print(args)
    start_time = time.time()
    path = os.getcwd()
    file_name = os.path.join(path, args.input)
    file_indx = os.path.join(path, args.index)
    output_file = args.output
    with open(file_indx, "r") as f:
        ring1, ring2, x1, x2 = "", "", "", ""
        # x1,x2 = [],[]
        lines = f.readlines()
        i = 0
        for line in lines:
            line = line.strip()
            i += 1
            if i == 1:
                ring1 = "ring1"
            elif i == 2:
                x1 = line.split()
            elif i == 3:
                ring2 = "ring2"
            else:
                x2 = line.split()
    with open(file_name, "r") as f:
        lines = f.readlines()
        add_lines = []
        run_time = []
        for line in lines:
            line = line.strip()
            if "t=" in line.split():
                list_line = line.split()
                run_time.append(list_line[list_line.index("t=") + 1])
            if len(line.split()) == 6:
                add_lines.append(line.split())
    df_columns = ["res_names", "atom_names", "atom_nums", "x", "y", "z"]
    df = pd.DataFrame(add_lines, columns=df_columns)
    ring1_cm_xyz, r1C1, r1C2, r1C3, r1C4, r1C5, r1C6, C_list1 = ring_cm(x1, df)
    ring2_cm_xyz, r2C1, r2C2, r2C3, r2C4, r2C5, r2C6, C_list2 = ring_cm(x2, df)
    distance_cm_xyz = (ring2_cm_xyz - ring1_cm_xyz) ** 2
    distance = []
    for i in distance_cm_xyz:
        distance.append(np.sqrt(np.sum(i)))
    df_distance = pd.DataFrame(run_time, columns=["Time"])
    df_distance["distance "] = distance
    angle = []
    print("正在计算每一帧的环与环之间的角度")
    for i in tqdm(range(len(run_time))):
        A = point(r1C1[i][0], r1C1[i][1], r1C1[i][2], 'A')  # 六个点
        B = point(r1C3[i][0], r1C3[i][1], r1C3[i][2], 'B')
        C = point(r1C5[i][0], r1C5[i][1], r1C5[i][2], 'C')
        P1 = plane(A, B, C, 'P1')  # p1平面
        D = point(r2C1[i][0], r2C1[i][1], r2C1[i][2], 'D')
        E = point(r2C3[i][0], r2C3[i][1], r2C3[i][2], 'E')
        F = point(r2C5[i][0], r2C5[i][1], r2C5[i][2], 'F')
        P2 = plane(D, E, F, 'P2')  # p2平面
        P1.normal()  # 求平面p1 p2的法向量
        P2.normal()
        angle.append(P1.angle(P2))  # 求平面p1 p2的夹角
    df_distance["angle"] = angle
    df_distance.to_csv(
        f"{path}\\{output_file}", sep="\t", index=None, float_format='%.3f'
    )
    df_distance.to_csv(f"{path}\\output.csv", index=None, float_format='%.3f')
    elapsed = time.time() - start_time
    print(f"已完成计算工作,共用时{elapsed}s")


if __name__ == "__main__":
    main()
