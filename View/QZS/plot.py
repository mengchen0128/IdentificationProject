import numpy as np
from matplotlib import pyplot as plt


class plot_para():

    def __init__(self, iter, para, *args, **kwargs):
        super(plot_para, self).__init__(*args, **kwargs)
        self.Iter=iter
        self.Mu=para

    def plot(self):
        Iteration = np.arange(1, self.Iter + 1)

        fig1 = plt.figure('fig1')
        plt.scatter(Iteration, self.Mu[1:len(self.Mu), 0].flatten(), s=20)

        fig1 = plt.figure('fig1')
        plt.plot(np.arange(0, len(self.Mu - 2)), [0.04] * len(self.Mu - 1), '--', linewidth=2, color='k')
        plt.xlabel("Iteration step")
        plt.ylabel(r"$\zeta$")
        plt.xlim([0, len(self.Mu)])
        plt.ylim([0, 0.08])
        plt.show()

