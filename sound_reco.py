import sound_up
import os
import csv
import numpy as np
import pandas as pd 
import librosa
from python_speech_features import logfbank
import pickle #pickle模組

class sound_reco:
    def __init__(self):
        self.audioPath = "./data/audio/"
        self.audioPath2 ="./data/"
        self.csvPath = "./data/CSV/"

    # 計算兩個128D向量間的歐式距離
    def return_euclidean_distance(self,feature_1, feature_2):
        feature_1 = np.array(feature_1) #原本的
        feature_2 = np.array(feature_2) #後來的
        dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
        return dist

    def sd_reco(self):
        toCSV = sound_up.sound()
        # toCSV.writeToCsv(self.audioPath, self.csvPath)
        # toCSV.openCsv()
        a =[]
        
        if os.path.exists("features_all.csv"):
            path_features_known_csv = "features_all.csv"
            csv_rd = pd.read_csv(path_features_known_csv, header=None)
            # 存放camera讀入的特徵向量
            features_known_arr = []
            #已知身分
            person_list = os.listdir(self.csvPath)
            person_num_list = []
            for person in person_list:
                person_num_list.append(str(person))

            # 2. 讀取已知數據
            for i in range(csv_rd.shape[0]):
                features_someone_arr = []
                for j in range(0, len(csv_rd.iloc[i])):
                    features_someone_arr.append(csv_rd.iloc[i][j])
                features_known_arr.append(features_someone_arr)
            print(features_someone_arr[0])
            print("Faces in Database：", np.shape(np.array(features_known_arr)))
            

            #如果有新的聲音檔拿來做處理
            for filename in os.listdir(self.audioPath2):
                if filename.endswith('.wav'):
                    print(self.audioPath2, os.path.splitext(filename)[0]+'.wav')
                    # toCSV.soundUp(self.audioPath2, os.path.splitext(filename)[0]+'.wav') #資料前處理
                    # toCSV.writeToCsv(self.audioPath2, self.audioPath2)
                    
                    # 讀取未知的特徵向量
                    features_cap_arr = []
                    outputFile = self.audioPath2 +os.path.splitext(filename)[0]+'.csv'
                    features_cap_arr = pd.read_csv(outputFile, header=None, encoding = 'utf-8')
                    features_cap_arr = np.array(features_cap_arr)
                    features_cap_arr =np.ravel(features_cap_arr)
                    print(np.shape(features_cap_arr))
                    

                    e_distance_list = []
                    for i in range(len(features_known_arr)):
                        # 如果 person_X 数据不为空
                        if str(features_known_arr) != '0.0':
                            print("with person", str(i + 1), "the e distance: ", end='')
                            e_distance_tmp = self.return_euclidean_distance(features_cap_arr, features_known_arr[i])
                            print( e_distance_tmp) #準確率
                            e_distance_list.append(e_distance_tmp)
                        else:
                        # 空数据 person_X
                            e_distance_list.append(999999999)
                    similar_person_num = e_distance_list.index(min(e_distance_list))
                    print("Minimum e distance with person", int(similar_person_num)+1)
                    
        else:
            print("失敗")
        return str(person_num_list [int(similar_person_num)]) #回傳身分者名稱
                    # if min(e_distance_list) < 0.4:
                    #     ####### 在这里修改 person_1, person_2 ... 的名字 ########
                    #     # 可以在这里改称 Jack, Tom and others
                    #            # name_namelist[k] = "person" + str(int(similar_person_num)+1)
                    #     name_namelist[k] =person_num_list[int(similar_person_num)]
                    #     print("May be person "+str(int(similar_person_num)+1))

                    # else:
                    #     print("Unknown person")
    
    # def emo_reco(self):
        

if __name__ == "__main__":
    reco = sound_reco()
    reco.sd_reco()