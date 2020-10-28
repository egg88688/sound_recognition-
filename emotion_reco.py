import pickle #pickle模組
import pandas as pd 
import os
import numpy as np
import csv
from sklearn.tree import DecisionTreeClassifier

class emo_reco:
    def __init__(self):
        #設定模型
        self.model = DecisionTreeClassifier(criterion='entropy', 
                        max_depth=8,
                        splitter='random',
                        random_state=0)

        # self.filename = './data/audio.csv'
    def reco(self, filename):
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            # 讀取 CSV 檔案內容
            test = csv.reader(csvfile, delimiter=',')
            test = np.array(list(test))

        # test= pd.read_csv(filename)
            print(np.shape(test))
        #讀取Model
        with open('./data/json/emo.pickle', 'rb') as f:
            self.model = pickle.load(f)
            prd = self.model.predict(test)
            # print(str(prd[0]))
            if str(prd[0]) == '0':
                emotion='happy'
            elif str(prd[0]) == '1':
                emotion='normal'
            elif str(prd[0]) == '2':
                emotion='unhappy'
        return emotion


if __name__ == "__main__":
    emo = emo_reco()
    print(emo.reco('./data/audio.csv'))