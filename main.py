import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pandas as pd
import plotly.express as px
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
mymodel=SentimentIntensityAnalyzer()
st.title('AMAZON SENTIMENT ANALYSIS SYSTEM')
st.sidebar.image('https://sellermobile.com/wp-content/uploads/2022/04/3rd-Party-Reviews.jpg.webp')
choice=st.sidebar.selectbox('My Menu',('HOME','Analyze Sentiment','CSV File','visualize the Results'))
if(choice=='HOME'):
    st.image('https://i.ytimg.com/vi/nZpmKWX7GwE/maxresdefault.jpg')
    st.write('Happy to service 😃😄😎')
elif(choice=='Analyze Sentiment'):
    url=st.text_input('Enter Google sheet URL')
    r=st.text_input("Enter range")
    btn=st.button('Analyze')
    if btn:
        if 'cred' not in st.session_state:
            f=InstalledAppFlow.from_client_secrets_file('key.json',['https://www.googleapis.com/auth/spreadsheets'])
            st.session_state['cred']=f.run_local_server(port=0)
        service=build('Sheets','v4',credentials=st.session_state['cred']).spreadsheets().values()
        d=service.get(spreadsheetId=url,range=r).execute()
        mycolumns=d['values'][0]
        mydata=d['values'][1:]
        df=pd.DataFrame(data=mydata,columns=mycolumns)
        l=[]
        for i in range(0,len(df)):
            p=df._get_value(i,'Feedback' )
            pred=mymodel.polarity_scores(p)
            if (pred['compound']>0.5):
                l.append('Posetive')
            elif(pred['compound']<-0.5):
                l.append('Negative')
            else:
                 l.append('Neutral')
        df['Sentiment']=l
        st.dataframe(df)
        df.to_csv(' Review.csv',index=False)
        st.header('This data has been saved by the name of Review.csv')


elif(choice=='CSV File'):
    path=st.text_input('Enter File Path')
    c=st.text_input('Enter Column')
    btn=st.button('Analyze')
    if btn:
        if 'cred'not in st.session_state:
            f=InstalledAppFlow.from_client_secrets_file('key.json',['https://www.googleapis.com/auth/spreadsheets'])
            st.session_state['cred']=f.run_local_server(port=0)
        mymodel=SentimentIntensityAnalyzer()
        df=pd.read_csv(path)
        l=[]
        for i in range(0,len(df)):
            p=df._get_value(i,c)
            pred=mymodel.polarity_scores(p)
            if (pred['compound']>0.5):
                l.append('Posetive')
            elif(pred['compound']<-0.5):
                l.append('Negative')
            else:
                l.append('Neutral')
        df['Sentiment']=l
        st.dataframe(df)
        df.to_csv('Review.csv',index=False)
        st.header('This data has been saved by the name of review.csv')

elif(choice=='visualize the Results'):
    choice2=st.selectbox('Choose Visualization',('None','Pie','Histogram'))
    if(choice2=='Pie'):
        df=pd.read_csv('Review.csv')
        posper=(len(df[df['Sentiment']=='Posetive'])/len(df))*100
        negper=(len(df[df['Sentiment']=='Negative'])/len(df))*100
        neuper=(len(df[df['Sentiment']=='Neutral'])/len(df))*100
        fig=px.pie(values=[posper,negper,neuper],names=['Posetive','Negative','Neutral'])
        st.plotly_chart(fig)
    elif(choice2=='Histogram'):
        t=st.text_input('Choose any Categorical Column')
        if t:
            df=pd.read_csv('Review.csv')
            fig=px.histogram(x=df['Sentiment'],color=df[t])
            st.plotly_chart(fig)





























