import librosa
import matplotlib.pyplot as plt
import numpy as np
import librosa.display
from python_speech_features import logfbank
from PIL import Image
import IPython.display as ipd
import os
import csv


class sound:
    def __init__(self):
        self.audioPath = "./data/audio/"
        self.csvPath = "./data/CSV/"
        
    def soundUp(self, audio_path, audio_Name):
        global y_ps
        global sr
        y_ps, sr = librosa.load( audio_path+audio_Name, sr=None, duration=5.0) #sr=每秒被分割的頻寬  duration=讀取的秒數
            # librosa.output.write_wav('file_trim_5s.wav', y, sr)
        # y_ps = librosa.effects.pitch_shift(y, sr, n_steps =-6)   # n_steps =要上移幾個半音，6為三個音(六個半音)
            # plt.plot(y_ps)
            # plt.title('Pitch Shift transformed waveform')
        # get mfcc
        mfccs = librosa.feature.mfcc(y_ps, sr=sr, n_mfcc=24) #n_mfcc要返回的MFCC数量 
        librosa.display.specshow(mfccs, sr=sr, x_axis='time')    
        # plt.show()

    def writeToCsv(self, audio_path, csv_path):
        b =[]
        b =np.array(b)
        # get MFCCs for every .wav file in our specified directory 
        for filename in os.listdir(audio_path):
            if filename.endswith('.wav'): # 抓取要改成csv的.wav
                b =[] 
                # print(os.path.splitext(filename)[0])
                self.soundUp(audio_path, os.path.splitext(filename)[0]+'.wav')
                # get filterbank energies
                fbank_feat = logfbank(y_ps, sr)
                rows = np.array(list(fbank_feat))
                rows =np.ravel(rows) #將多維降成一維
                b =np.concatenate([b,rows])
                print(np.shape(b))
                b= b.reshape(1, 12974)
                # create a file to save our results in
                outputFile = csv_path+ os.path.splitext(filename)[0] + ".csv"
                file = open(outputFile, 'w+') # make file/over write existing file
                if audio_path =="./data/audio/":
                    np.savetxt(file, b, delimiter=",") #save MFCCs as .csv
                else:
                    np.savetxt(file, b, delimiter=",") #save MFCCs as .csv
                    # np.savetxt(file, b, delimiter=",", header ='1,2,3') #save MFCCs as .csv
                    # print("success save MFCCs as .csv")
                file.close() # close file

    

    def openCsv(self):
        person_list = os.listdir(self.csvPath)
        person_num_list = []
        a =[]
        a =np.array(a)
        features_cap_arr = []
        e_distance_list = []
        for person in person_list:
            person_num_list.append(str(person)) #將資料夾名稱(person)讀入person_num_list
            person_cnt = max(person_num_list) #取最後一個資料夾名稱
            print("person_num_list = " + str(person_num_list))
        # 開啟 CSV 檔案
        for filename in os.listdir(self.csvPath):
            if filename.endswith('.csv'):
                outputFile = self.csvPath + os.path.splitext(filename)[0] + ".csv"
                print("讀取到" + outputFile)  
                with open(outputFile, 'r', newline='', encoding='utf-8') as csvfile:
                    # 讀取 CSV 檔案內容
                    rows = csv.reader(csvfile, delimiter=',')
                    rows = np.array(list(rows))
                    rows =np.ravel(rows) #將多維降成一維
                    a =np.concatenate([a,rows])
                    # print(rows)
                    print(np.shape(a))
                    print(len(person_num_list))
        with open("features_all.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            a= a.reshape(len(person_num_list), len(rows))
            writer.writerows(a)
            print("寫入features_all.csv成功")



if __name__ == "__main__":
    sd = sound()
    sd.writeToCsv("./data/", "./data/")
    # sd.openCsv()