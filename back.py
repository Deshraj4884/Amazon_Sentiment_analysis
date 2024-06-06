from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pandas as pd
import plotly.express as px
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
mymodel=SentimentIntensityAnalyzer()
#permission
f=InstalledAppFlow.from_client_secrets_file('key.json',['https://www.googleapis.com/auth/spreadsheets'])
cred=f.run_local_server(port=0)
#creat a service
service=build('Sheets','v4',credentials=cred).spreadsheets().values()
# Retrieve data from google sheets.
d=service.get(spreadsheetId='1jFJb7cNMdcA9RnN94SwN-C_jvXQL_Ej8gL2PYUptibQ',range='A1:O').execute()
print(d['values'])
mycolumns=d['values'][0]
mydata=d['values'][1:]
df=pd.DataFrame(data=mydata,columns=mycolumns)
pos=0
neg=0
neu=0
for i in range(0,len(df)):
    p=df._get_value(i,'Feedback' )
    pred=mymodel.polarity_scores(p)
    if (pred['compound']>0.5):
        pos=pos+1
    elif(pred['compound']<-0.5):
        neg=neg+1
    else:
        neu=neu+1
posper=(pos/len(df))*100
negper=(neg/len(df))*100
neuper=(neu/len(df))*100
print('Posetive:',posper)
print('Nagetive:',negper)
print('Neutral:',neuper)
fig=px.pie(values=[posper,negper,neuper],names=['Posetive','Negative','Neutral'])
fig.show()
