#聊天套件
import dialogflow
from google.api_core.exceptions import InvalidArgument
from google.oauth2 import service_account
import os
#傳輸套件
import pyrebase
import firebase_admin
from time import sleep
import speech_recognition as stt_reco
from os import path
import sound_up
import sound_reco
import pcmToWAV
from os.path import basename
import reduce_noise
import emotion_reco
#-------------------firebase初始化-開始---------------------------------
firebaseConfig = {
    'apiKey': "AIzaSyCag0-hQq5SYmAu-Pzf0qCY0ScPPizmr2w",
    'authDomain': "fir-crud-example-e19c3.firebaseapp.com",
    'databaseURL': "https://fir-crud-example-e19c3.firebaseio.com",
    'projectId': "fir-crud-example-e19c3",
    'storageBucket': "fir-crud-example-e19c3.appspot.com",
    'messagingSenderId': "972578164970",
    'appId': "1:972578164970:web:5006750e806c8d5a84c793",
    'measurementId': "G-LSE15JMRBY"
  }
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
auth = firebase.auth()
storage = firebase.storage()
#Authentication
email = "server@mail.com"
password = "123456"
auth.sign_in_with_email_and_password(email,password)
#-------------------firebase初始化-結尾---------------------------------
downloadPath ='data/audio/'
filename = "Audio/audio.pcm"#聊天更新的檔案名
new_filename="new_Audio/new_audio.pcm"#新增使用者身分的
audioPath ="./data/"
csvPath = "./data/CSV/"
# user = db.child("User").child("audio").get() #得到User資料
# newUserName = db.child("New").child("new_name").get() 
# newUserAUDIO = db.child("New").child("new_audio").get() 
# newUserSTATUS = db.child("New").child("new_status").get() 
toCSV = sound_up.sound()
reco = sound_reco.sound_reco()
pcm2wav = pcmToWAV.pcm2wav()
rn= reduce_noise.reduce_no()
emotionReco = emotion_reco.emo_reco()
# for userdata in user.each():
#   print(userdata.key() + ": " + userdata.val() ) 
def dialog(emotion):
    #設定dialogflow初始化(文本串接)
    global projectID,language_code,GOOGLE_APPLICATION,session_client,session,sessionID

    if emotion =='happy':
        projectID = 'happy-hgcqxf' 
        GOOGLE_APPLICATION = service_account.Credentials.from_service_account_file('./data/json/happy-hgcqxf-4c3313d8cf79.json')
        sessionID = '4c3313d8cf793ae12a8fd512932a1baf9caba8c9' #金鑰
    elif emotion =='normal':
        projectID = 'newagent-jwivja' 
        GOOGLE_APPLICATION = service_account.Credentials.from_service_account_file('./data/json/newagent-jwivja-47205338a626.json')
        sessionID ='47205338a6260d576145f640420e24bc976da929'
    elif emotion =='unhappy':
        projectID = 'unhappy-ahgt' 
        GOOGLE_APPLICATION = service_account.Credentials.from_service_account_file('./data/json/unhappy-ahgt-5641234aeb76.json')
        sessionID = '5641234aeb76f06cb0eecefcce7f1e5da780cfd8'
    language_code = 'Chinese (Traditional) — zh-TW'
    session_client = dialogflow.SessionsClient(credentials=GOOGLE_APPLICATION)
    session = session_client.session_path(projectID, sessionID)

def stt():
    # newUserName = db.child("New").child("new_name").get() 
    sound = 'data/audio.wav'
    r = stt_reco.Recognizer()
    global text
    #STT
    with stt_reco.AudioFile(sound) as sound:
        print("Please wait. Calibrating microphone...")
        r.adjust_for_ambient_noise(sound)
        audio=r.listen(sound) #讀入音檔(只能使用.wav)
        text=r.recognize_google(audio, language='zh-TW')

print("running start")
while 1:
    
    newUserAUDIO = db.child("New").child("new_audio").get() 
    newUserSTATUS = db.child("New").child("new_status").get() 
    userAUDIO = db.child("User").child("status").get() #得到User資料
    user = db.child("User").child("audio").get()  #初始化
    newUserName = db.child("New").child("new_name").get() #新增使用者名稱

    # pcm2wav.pcm2wav
    #新增使用者身分
    if newUserSTATUS.val() == 'true':
        if newUserAUDIO.val() =='true':
            print("新增使用者"+newUserName.val())
            storage.child(new_filename).download(downloadPath + newUserName.val()+'.pcm') #child(要下載的storage路徑).download(下載到本機哪的路徑)
            pcm2wav.pcm2wav(downloadPath + newUserName.val() +'.pcm', downloadPath + newUserName.val() + '.wav')
            rn.reduce(downloadPath + newUserName.val() + '.wav')
            toCSV.writeToCsv('./' + downloadPath, csvPath)
            toCSV.openCsv() #把身份寫進去feture_all.csv
            data = {'new_audio':"false", 'new_name':newUserName.val(), 'new_status':"false"}
            db.child("New").update(data)
            print("新增使用者"+newUserName.val()+"成功")


    #與使用者聊天
    if user.val() == 'true':
        if userAUDIO.val() =='true':

            storage.child(filename).download('data/audio.pcm')
            pcm2wav.pcm2wav('data/audio.pcm', 'data/audio.wav')
            rn.reduce('data/audio.wav')
            durations = pcm2wav.duration('data/audio.wav')
            print("錄音長度:" + str(durations))
            #資料前處理
            toCSV.soundUp(audioPath, 'audio.wav') 
            toCSV.writeToCsv(audioPath, audioPath)
            recoName = path.splitext(reco.sd_reco())[0] #身分辨識
            emo= emotionReco.reco('./data/audio.csv')
            #------------------聊天處理-----------------------------------------------------------------------
            stt()
            
            dialog(emo)
            text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
            query_input = dialogflow.types.QueryInput(text=text_input)
            try:
                response = session_client.detect_intent(session=session, query_input=query_input)
            except InvalidArgument:
                raise
                    
            print(recoName+ '=> ' + text +'\t 情緒為:' + emo) 
            print('chatbot => ',recoName + response.query_result.fulfillment_text)
            chatbotTalk = recoName + response.query_result.fulfillment_text #輸出的文字回應
            #------------------聊天處理-----------------------------------------------------------------------
            data = {'audio':"false", 'status':"false", 'uid':"Mfm8zY7Nf7WrsaSt6PwrdbpJi2o2"}
            db.child("User").update(data)
            data = {'emo':emo, 'res_text':chatbotTalk, 'status':"true", 'uid':"IKrj3vr8ExeUwVDqbgx3j4uQU8j1", 'user_name':recoName}
            db.child("Bot").update(data)


