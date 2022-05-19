from scipy.signal import buttord, butter


class Example_Signal_Filter:
    def Example_Signal_Filter(self):
        fs = 1024
        f_pass = 20
        f_stop = 50
        alpha_pass = 3
        alpha_stop = 60
        [n, Wn] = buttord(f_pass / (fs / 2), f_stop / (fs / 2), alpha_pass, alpha_stop)
        [b, a] = butter(n, Wn)