import numpy as np
import wave
import math
from numpy import ceil, log2
from collections import deque
import librosa
import matplotlib.pyplot as plt

class reduce_no:
    def __init__(self):
        return

    def nextpow2(self,x):
        res = ceil(log2(x))
        return res.astype('int')  #we want integer values only but ceil gives float
    # Noise magnitude calculations - assuming that the first 5 frames is noise/silence

    def reduce(self, inputFile):
        f = wave.open(inputFile)
        # 讀取格式信息
        params = f.getparams()
        nchannels, sampwidth, framerate, nframes = params[:4]
        fs = framerate
        # 讀取波形數據
        str_data = f.readframes(nframes)
        f.close()
        # 將波形數據轉換為數組
        x = np.fromstring(str_data, dtype=np.short)
        # 計算參數
        len_ = 20 * fs // 1000
        PERC = 50
        len1 = len_ * PERC // 100
        len2 = len_ - len1
        # 設置默認參數
        Thres = 3
        Expnt = 2.0
        beta = 0.002
        G = 0.9
        # 初始化漢明窗
        win = np.hamming(len_)
        # normalization gain for overlap+add with 50% overlap
        winGain = len2 / sum(win)
        nFFT = 2 * 2 ** (self.nextpow2(len_))
        noise_mean = np.zeros(nFFT)
        j = 0
        for k in range(1, 6):
            noise_mean = noise_mean + abs(np.fft.fft(win * x[j:j + len_], nFFT))
            j = j + len_
        noise_mu = noise_mean / 5
        # --- allocate memory and initialize various variables
        k = 1
        img = 1j
        x_old = np.zeros(len1)
        Nframes = len(x) // len2 - 1
        xfinal = np.zeros(Nframes * len2)
        # ========================= Start Processing ===============================
        for n in range(0, Nframes):
            # Windowing
            insign = win * x[k-1:k + len_ - 1]
            # compute fourier transform of a frame
            spec = np.fft.fft(insign, nFFT)
            # compute the magnitude
            sig = abs(spec)

            # save the noisy phase information
            theta = np.angle(spec)
            SNRseg = 10 * np.log10(np.linalg.norm(sig, 2) ** 2 / np.linalg.norm(noise_mu, 2) ** 2)

            def berouti(SNR):
                if -5.0 <= SNR <= 20.0:
                    a = 4 - SNR * 3 / 20
                else:
                    if SNR < -5.0:
                        a = 5
                    if SNR > 20:
                        a = 1
                return a

            def berouti1(SNR):
                if -5.0 <= SNR <= 20.0:
                    a = 3 - SNR * 2 / 20
                else:
                    if SNR < -5.0:
                        a = 4
                    if SNR > 20:
                        a = 1
                return a

            if Expnt == 1.0:  # 幅度譜
                alpha = berouti1(SNRseg)
            else:  # 功率譜
                alpha = berouti(SNRseg)
            #############
            sub_speech = sig ** Expnt - alpha * noise_mu ** Expnt
            # 當純凈信號小於噪聲信號的功率時
            diffw = sub_speech - beta * noise_mu ** Expnt
            # beta negative components

            def find_index(x_list):
                index_list = []
                for i in range(len(x_list)):
                    if x_list[i] < 0:
                        index_list.append(i)
                return index_list


            z = find_index(diffw)
            if len(z) > 0:
                # 用估計出來的噪聲信號表示下限值
                sub_speech[z] = beta * noise_mu[z] ** Expnt
                # --- implement a simple VAD detector --------------
                if SNRseg < Thres:  # Update noise spectrum
                    noise_temp = G * noise_mu ** Expnt + (1 - G) * sig **Expnt  # 平滑處理噪聲功率譜
                    noise_mu = noise_temp ** (1 / Expnt)  # 新的噪聲幅度譜
                # flipud函數實現矩陣的上下翻轉，是以矩陣的“水平中線”為對稱軸
                # 交換上下對稱元素
                sub_speech[nFFT // 2 + 1:nFFT] = np.flipud(sub_speech[1:nFFT // 2])
                x_phase = (sub_speech ** (1 / Expnt)) * (np.array([math.cos(x) for x in theta]) + img * (np.array([math.sin(x) for x in theta])))
                # take the IFFT


                xi = np.fft.ifft(x_phase).real
                # --- Overlap and add ---------------
                xfinal[k-1:k + len2 - 1] = x_old + xi[0:len1]
                x_old = xi[0 + len1:len_]
                k = k + len2

        # 保存文件
        wf = wave.open(inputFile, 'wb')
        # 設置參數
        wf.setparams(params)
        # 設置波形文件 .tostring()將array轉換為data
        wave_data = (winGain * xfinal).astype(np.short)
        wf.writeframes(wave_data.tostring())
        wf.close()

    


    

# y_ps, sr = librosa.load( 'outfile.wav', sr=None, duration=5.0)
# plt.plot(y_ps)
# plt.title('Pitch Shift transformed waveform')
# plt.show()

if __name__ == "__main__":
    rn= reduce_no()
    rn.reduce('./data/Peggy.wav')
    # y_ps, sr = librosa.load('./data/Peggy.wav', sr=None, duration=5.0)
    # plt.plot(y_ps)
    # plt.title('Pitch Shift transformed waveform')
    # plt.show()