import math

import numpy as np
import xlrd
from scipy.optimize import curve_fit


def Instant_AmpOmega_Extraction_Sliding(t, u, Omeg_Mean, Slide_Ratio, N_Period, Para0):
    N_t = len(t)
    Win_Width = N_Period * 2 * math.pi / Omeg_Mean
    N_Win = round(Win_Width / (t[1] - t[0]))
    N_Slide_Ratio = round(N_Win * Slide_Ratio)
    N_T = math.floor((N_t - N_Win) / N_Slide_Ratio)
    # T=np.zeros(N_t)
    # A_Inst=np.zeros(N_t)
    # V_Inst=np.zeros(N_t)
    # Omega_Inst=np.zeros(N_t)
    # Stream=np.zeros(N_t)
    T = [0] * N_T
    A_Inst = [0] * N_T
    V_Inst = [0] * N_T
    Omega_Inst = [0] * N_T
    Stream = [0] * N_T

    LB = [Para0[0] * 0.8, 0.1 * Para0[1], Para0[2] * 0.8, Para0[3] - math.pi, -0.1, -0.1]
    UB = [Para0[0] * 1.5, 2 * Para0[1], Para0[2] * 1.2, Para0[3] + math.pi, 0.1, 0.1]

    for n in range(1, N_T - 1):
        var1 = t[n * N_Slide_Ratio:N_Win + n * N_Slide_Ratio]
        var2 = u[n * N_Slide_Ratio:N_Win + n * N_Slide_Ratio]

        popt, pcov = curve_fit(Fun_for_Fit, var1, var2, p0=Para0, bounds=(LB, UB))

        Para0 = popt

        LB = [Para0[0] * 0.8, 0.1 * Para0[1], Para0[2] * 0.8, Para0[3] - math.pi, -0.1, -0.1]
        UB = [Para0[0] * 1.5, 2 * Para0[1], Para0[2] * 1.2, Para0[3] + math.pi, 0.1, 0.1]

        T[n] = (t[(n - 0) * N_Slide_Ratio + 0] + t[(n - 0) * N_Slide_Ratio + N_Win - 1]) / 2
        Omega_Inst[n] = popt[2]
        A_Inst[n] = abs(popt[0] * math.exp(-popt[1] * T[n]))
        V_Inst[n] = -popt[1] * A_Inst[n]
        Stream[n] = popt[4] * math.exp(-popt[5] * T[n])
    return T, A_Inst, V_Inst, Omega_Inst


def Fun_for_Fit(t, *x):
    A0 = x[0]
    zeta = x[1]
    Omeg0 = x[2]
    Phi = x[3]
    Drift = x[4]
    mu = x[5]
    result = Drift * np.exp(-mu * t) + (A0 * np.exp(-zeta * t)) * np.cos(Omeg0 * t + Phi)
    # A0 * np.exp(-zeta * t)
    #    .dot(np.cos(Omeg0 * t + Phi))
    # Drift * np.exp(-mu * t) +
    return result


def excel_read():  # 定义了一个读取excel的函数
    wb = xlrd.open_workbook(r'C:\Users\Student-16\Desktop\java\Backbone Experiment\1.11 - 2.xlsx')  # 打开Excel文件
    sheet = wb.sheets()[0]  # 通过excel表格名称(rank)获取工作表
    ts = []  # 创建空list，用来保存人物名称一列
    us = []  # 保存id数据
    for a in range(sheet.nrows):  # 循环读取表格内容（每次读取一行数据）
        cells = sheet.row_values(a)  # 每行数据赋值给cells
        t = cells[0]
        u = cells[1]
        ts.append(t)
        us.append(u)
    return ts, us


if __name__ == '__main__':
    a = excel_read()
    para = [0.8, 4, 2.4, 4.4894, 0.0299, -0.0592]
    A_Inst, V_Inst = Instant_AmpOmega_Extraction_Sliding(a[0], a[1], 3, 0.1, 5, para)
    print(A_Inst)
