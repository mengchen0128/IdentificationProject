# This is a sample Python script.

import math

import matplotlib.pyplot as plt
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np
import xlrd
from scipy import interpolate


def Instant_AmpOmega_Extraction(t, u):
    # Use a breakpoint in the code line below to debug your script.
    # Press Ctrl+F8 to toggle the breakpoint.
    NT = len(t)
    U_Env = []
    Ut_Env = []
    L_Env = []
    Lt_Env = []
    Omeg_T = []
    Omeg_T1 = []
    Omeg_T2 = []
    Cross_P = []
    Cross_T = []
    e = []
    for n in range(20, NT - 19):
        if u[n] == max(u[-20 + n:19 + n]):
            Ut_Env.append(t[n])
            U_Env.append(u[n])
        elif u[n] == min(u[-20 + n:19 + n]):
            Lt_Env.append(t[n])
            L_Env.append(u[n])

    tck = interpolate.splrep(Ut_Env, U_Env, s=0)
    U_A = interpolate.splev(t, tck, der=0)
    tck1 = interpolate.splrep(Lt_Env, L_Env, s=0)
    L_A = interpolate.splev(t, tck1, der=0)

    A_Inst = (U_A - L_A) / 2

    V_Inst = (A_Inst[1:-1] - A_Inst[0:len(A_Inst) - 2]) / (t[1] - t[0])

    u = u - (U_A + L_A) / 2

    for n in range(1, NT - 1):
        if u[n - 1] * u[n] <= 0:
            Cross_T = t[n - 1] + abs(u[n - 1]) / (abs(u[n - 1]) + abs(u[n])) * (t[n] - t[n - 1]);
            if not Cross_P:
                Cross_P = Cross_T
            else:
                # Omeg_T = [Omeg_T, [(Cross_P + Cross_T) / 2;pi / (Cross_T - Cross_P)]];
                Omeg_T1.append((Cross_P + Cross_T) / 2)
                Omeg_T2.append(math.pi / (Cross_T - Cross_P))
                Cross_P = Cross_T
    T = Omeg_T1
    Omega_Inst = np.array(Omeg_T2)
    tck2 = interpolate.splrep(t, A_Inst, s=0)

    A_Inst = interpolate.splev(T, tck2, der=0)

    x1 = list_add(t[1:-1], t[0:len(t) - 2])
    tck3 = interpolate.splrep([e / 2 for e in x1], V_Inst, s=0)
    V_Inst = interpolate.splev(T, tck3, der=0)
    return T, A_Inst, V_Inst, Omega_Inst


def list_add(a, b):
    c = []
    for i in range(len(a)):
        c.append(a[i] + b[i])
    return c


def excel_read():  # 定义了一个读取excel的函数
    wb = xlrd.open_workbook(r'C:\Users\Student-16\Desktop\java\Backbone Experiment\1.11 - 3.xlsx')  # 打开Excel文件
    sheet = wb.sheets()[0]  # 通过excel表格名称(rank)获取工作表
    ts = []
    us = []
    for a in range(sheet.nrows):  # 循环读取表格内容（每次读取一行数据）
        cells = sheet.row_values(a)  # 每行数据赋值给cells
        t = cells[0]
        u = cells[1]
        ts.append(t)
        us.append(u)
    return ts, us


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    a = excel_read()
    Omega_Inst, A_Inst = Instant_AmpOmega_Extraction(a[0], a[1])
    plt.title("Matplotlib demo")
    plt.xlabel("omega(t)")
    plt.xlim(xmax=50, xmin=0)
    plt.ylabel("a(t)")

    # plt.plot(Omega_Inst, A_Inst,linestyle='', marker='.')
    plt.plot(Omega_Inst, A_Inst)
    # plt.scatter(Omega_Inst, A_Inst, marker='o')
    plt.show()
