import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import argparse


def file_xvg(xvg_fname):
    with open(xvg_fname, "r") as f:
        x, y = [], []
        title, xaxis, yaxis = "", "", ""
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith("#"):
                continue
            if "title" in line.split():
                title = line.split()[2]
                title = title.split('"')[1]
            elif "xaxis" in line.split():
                xaxis = line.split()[3] + " " + line.split()[4]
                xaxis = xaxis.split('"')[1]
            elif "yaxis" in line.split():
                yaxis = line.split()[3] + " " + line.split()[4]
                yaxis = yaxis.split('"')[1]
            elif line.startswith("@"):
                continue
            else:
                x.append(line.split()[0])
                y.append(line.split()[1])
        return title, xaxis, yaxis, x, y


def csv_file(csv_fname):
    df = pd.read_csv(csv_fname)
    return df


def moving_average(y, windowsize):
    window = np.ones(int(windowsize)) / float(windowsize)
    re = np.convolve(y, window, 'same')
    return re


def plot(path, df, title_name):
    colunm_name = [column for column in df]
    plt.figure(figsize=(12, 8))
    x = df[colunm_name[0]]
    y = df[colunm_name[1]]
    plt.xlim((0, 100000))
    plt.ylim((0, 1))
    plt.xticks(fontproperties="Times New Roman", size=24, rotation=20)
    plt.yticks(fontproperties="Times New Roman", size=24)

    # 基于Numpy.convolve实现滑动平均滤波
    y1 = moving_average(y, 80)
    x1 = x[:-50]
    y1 = y1[:-50]

    (line1,) = plt.plot(x, y, color='gray', lw=0.5, ls='-', marker=None, ms=2)

    (line2,) = plt.plot(x1, y1, color='black', lw=2.0, ls='-', marker=None, ms=2)

    # plt.xticks(x,index, horizontalalignment='right')
    plt.ylabel(colunm_name[0], fontdict={'family': 'Times New Roman', 'size': 28})
    plt.xlabel(colunm_name[1], fontdict={'family': 'Times New Roman', 'size': 28})
    # plt.title('RMSD of backbone', fontdict={'size':24})
    plt.savefig(f"{path}\\{title_name}.png", dpi=500, bbox_inches='tight')
    plt.show()


def main():
    """这是一个自动绘制xvg和csv文件折线图的工具，目前仅支持单因素折线图"""
    parser = argparse.ArgumentParser(
        description="自动绘制xvg和csv文件折线图的工具，仅支持单因素折线图，请输入完整文件名（xxx.xvg/csv）："
    )
    parser.add_argument(
        "-in",
        "--inputfile",
        type=str,
        help="请输入完整文件名（xxx.xvg/csv）",
        required=True,
    )
    args = parser.parse_args()
    print(args)

    file_name = args.inputfile
    path = os.getcwd()
    file_path = os.path.join(path, file_name)
    title_name = file_name.split(".")[0]
    file_format = file_name.split(".")[1]
    if file_format == "xvg":
        title, xaxis, yaxis, x, y = file_xvg(file_path)
        df = pd.DataFrame(x, columns=[xaxis])
        df[yaxis] = y
        df.to_csv(f"{path}\\{title}.csv", index=0)
        judge_plot = input("是否绘制xvg图像并保存：(yes/no)")
        if judge_plot == "yes":
            df = pd.read_csv(f"{path}\\{title}.csv")
            plot(path, df, title_name)
            print(f"图片已保存在{path}\{title_name}.png")
    elif file_format == "csv":
        title_name = file_name.split(".")[0]
        df = pd.read_csv(file_path)
        judge_plot = input("是否绘制xvg图像并保存：(yes/no)")
        if judge_plot == "yes":
            plot(path, df, title_name)
            print(f"图片已保存在{path}\{title_name}.png")
    else:
        print("Sorry,目前仅支持xvg和csv文件格式")


if __name__ == "__main__":
    main()
