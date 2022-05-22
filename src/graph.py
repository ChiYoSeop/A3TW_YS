import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np
from numpy import exp
from lmfit import Model
from sklearn.metrics import r2_score
import time
import pandas as pd
import sys
import os
from pathlib import Path

h = ((os.path.dirname(os.path.abspath(__file__))).replace("\\","/")).replace("src","results/jpgs")
# hi = 'C:\\Users\\user\\PycharmProjects\\A3TW_YS\\dat\\D08\\20190526_082853\\HY202103_D08_(0,2)_LION1_DCM_LMZO.xml'


def figname(a):
    a = a.replace("\\","/")
    b = a.split("/")
    c = b[-1].split(".")
    d = c[0]
    e = h+"/"+d+".jpg"
    return e

# print(figname(hi))

def eq(x, a, b, c, d, e):
    return a * (x**4) + b * (x**3) + c * (x**2) + d * x + e

def IV(x, Is, q, n, k):
    return Is * (exp((q * x) / (n * k)) - 1)

def grph(v,i,wvl,itst,lgds,show,save,figname):
    plt.figure(figsize = (12, 8))
    plt.subplot(2, 3, 4)
    plt.plot(v, i, 'o', label = 'I-V curve')
    plt.title("IV analysis")
    plt.xlabel("Voltage [V]")
    plt.ylabel("Current [A]")
    plt.yscale('logit')
    plt.legend(loc = 'best')

    plt.subplot(2,3,5)
    plt.plot(v, i, 'o', label = 'I-V curve')

    v1 = v[:10]
    v2 = v[9:]

    i1 = i[:10]
    i2 = i[9:]

    start_time1 = time.time()
    lmodel = Model(eq)
    params1 = lmodel.make_params(a=1, b=1, c=1, d=1, e=1)
    result1 = lmodel.fit(i1, params1, x = v1)
    plt.plot(v1, result1.best_fit, '--', label = 'Fit-L')
    end_time1 = time.time()
    # print(f'left fitting time : {end_time1 - start_time1}')

    start_time2 = time.time()
    rmodel = Model(IV)
    params2 = rmodel.make_params(Is=1, q=1, n=1, k=1)
    result2 = rmodel.fit(i2, params2, x = v2)
    plt.plot(v2, result2.best_fit, '--', label = 'Fit-R')
    end_time2 = time.time()
    # print(f'right fitting time : {end_time2 - start_time2}')

    plt.title("IV analysis")
    plt.xlabel("Voltage [V]")
    plt.ylabel("Current [A]")
    plt.yscale('logit')
    plt.legend(loc='best')
    LR2IV = r2_score(i1, result1.best_fit)
    RR2IV = r2_score(i2, result2.best_fit)
    # print(f'Left R Squared : {LR2IV}')
    # print(f'Right R Squared: {RR2IV}')


    plt.subplot(2, 3, 1)
    for n in range(len(wvl)):
        plt.title("Transmission spectra-as measured")
        plt.xlabel("Wavelength [nm]")
        plt.ylabel("Measured transmission [dB]")
        plt.rc("legend", fontsize=7)
        if n == 6:
            plt.plot(wvl[6], itst[6], label = 'DCBias = REF')
            plt.rc("legend", fontsize=5)
        else:
            plt.plot(wvl[n], itst[n], label = f'DCBias = {lgds[n]}V')
        plt.legend(loc = 'best', ncol = 3)

    # Fitting
    plt.subplot(2, 3, 2)
    for n in range(len(wvl)):
        if n == 6:
            plt.plot(wvl[n], itst[n], label="REF")
        else:
            continue
    for b in range(2,7):
        dp1 = np.polyfit(wvl[6], itst[6], b)
        f1 = np.poly1d(dp1)
        plt.plot(wvl[6], f1(wvl[6]), 'r--', label = f'{b} th R^2:{round(r2_score(itst[6], f1(wvl[6])),4)}')
        plt.rc("legend", fontsize=8)
        # print(f'I-IL R Squared {b}th : {r2_score((itst[6]),f1(wvl[6]))}') # 피팅 제곱의 값 즉, 1에 가까울 수록 정확하다.
    plt.xlabel('Wavelength[nm]')
    plt.ylabel('Transmissions[dB]')
    plt.title('Transmission spectra - fitted')
    plt.legend(loc='best')
    max_ref = max(f1(wvl[6]))

    plt.subplot(2, 3, 3)
    for k in range(len(wvl)-1):
        plt.title("Fitting Function")
        plt.xlabel("Wavelength [nm]")
        plt.ylabel("Measured transmission [dB]")
        plt.plot(wvl[k], itst[k] - f1(wvl[k]), label = f'DCBias = {lgds[k]}V')
        plt.legend(loc = 'best', ncol = 3)
        plt.rc("legend", fontsize=5)
        # 각 DC Bias에서 빛의 세기의 최대값
        # print(f'Max intensity[dB] at DCBias = {lgds[k]} :{max(itst[k] - f1(wvl[k]))}')
        # # 빛의 세기가 최대일 때 파장
        # print(f'at {wvl[k][(np.argmax(itst[k] - f1(wvl[k])))]}nm')
        # # 각 DC Bias에서 빛의 세기의 최소값
        # print(f'Min intensity[dB] at DCBias = {lgds[k]} :{min(itst[k] - f1(wvl[k]))}')
        # # 빛의 세기가 최소일 때 파장
        # print(f'at {wvl[k][(np.argmin(itst[k] - f1(wvl[k])))]}nm')
    plt.tight_layout()
    if show == True:
        plt.show()
    if save == True:
        plt.savefig(figname, dpi=300, bbox_inches='tight')



# print(f'max :{max(itst[k]-f1(wvl[k]))}')


# fit1i = result1.best_fit
# fit2i = result2.best_fit
# h = [-2.0,-1.5,-1,-0.5,0.0]
# for t in range(len(fiti)):
#     print(f'{}: {fiti[t]}')

# # 좌측 best_fit일 때의 parameters 값
# print(f'Left best Parameters: {result1.best_values}')
# # 좌측 best_fit일 때의 Current 값들
# print(f'Left best Currents[A]: {fit1i}')
# # 우측 best_fit일 때의 parameters 값
# print(f'Right best Parameters: {result2.best_values}')
# # 우측 best_fit일 때의 Current 값들
# print(f'Right best Currents[A]: {fit2i}')







