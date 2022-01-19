# -*- coding: utf-8 -*-
"""
Spyder 编辑器

这是一个临时脚本文件。
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import os
from scipy.signal import savgol_filter

def moving_average(y, windowsize):
    window = np.ones(int(windowsize)) / float(windowsize)
    re = np.convolve(y, window, 'same')
    return re

current_path = os.getcwd()
name = "RMSD.CSV"
title_name = name.split(".")[0]

df = pd.read_csv(f"{current_path}\\{name}")
plt.figure(figsize=(12,8))
x = df["Time (ps)"]
y = df["RMSD (nm)"]
#savgol_filter
#y1 = savgol_filter(y, 9, 1, mode= 'nearest')
#line2, = plt.plot(x,y1, color='black', lw=2.0, ls='-', marker=None, ms=2)

#make_interp_spline
#x1 = np.linspace(x.min(), x.max(), 100)
#y1 = make_interp_spline(x, y)(x1)
#line2, = plt.plot(x1,y1, color='black', lw=2.0, ls='-', marker=None, ms=2)

#邻近平均值
#x1 = [(x[i-1]+x[i])/2 for i in range(1,len(x))]
#y1 = [(y[i-1]+y[i])/2 for i in range(1,len(y))]
#line2, = plt.plot(x1,y1, color='black', lw=2.0, ls='-', marker=None, ms=2)

plt.xlim((0,100000))
plt.ylim((0,1))
plt.xticks(fontproperties = "Times New Roman", size=24, rotation=20)
plt.yticks(fontproperties = "Times New Roman", size=24)

#基于Numpy.convolve实现滑动平均滤波
y1 = moving_average(y,80)
x1 = x[:-50]
y1 = y1[:-50]

line1, = plt.plot(x,y, color='gray', 
                  lw=0.5, ls='-', 
                  marker=None, ms=2)

line2, = plt.plot(x1,y1, color='black', 
                  lw=2.0, ls='-', 
                  marker=None, ms=2)

#plt.xticks(x,index, horizontalalignment='right')
plt.ylabel('RMSD (nm)',fontdict={'family' : 'Times New Roman','size':28})
plt.xlabel('Time (ps)',fontdict={'family' : 'Times New Roman','size':28})
#plt.title('RMSD of backbone', fontdict={'size':24})
plt.savefig(f"{title_name}.png",dpi=500,bbox_inches = 'tight')
plt.show()
