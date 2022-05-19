import scipy.io
from matplotlib import pyplot as plt

from Input_And_Output.Matlab_FFT import Matlab_FFT

mat = scipy.io.loadmat(r'C:\Users\Student-16\Desktop\MatlabAlgorithm\Data.mat')
print(mat)
t=mat['t'][0]
x=mat['x'][0]
y=mat['y'][:,0]
print(y)
fs=1/(t[1]-t[0])
X,Freq=Matlab_FFT(x,fs)
Y,Freq2=Matlab_FFT(y,fs)
print(Freq)
plt.semilogy(Freq,abs(Y/X))
plt.xlim(0,1)
plt.show()
