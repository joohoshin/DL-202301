# https://docs.streamlit.io/library/api-reference
# https://platform.openai.com/docs/guides/chat/introduction

### 간단한 채팅 서비스를 구현해봅시다



### openai 연동
import configparser
import openai
import streamlit as st
import sys
import os

# 현재 실행 중인 파일의 디렉토리 경로 가져오기
dir_path = os.path.dirname(os.path.realpath(__file__))

# 작업 디렉토리 변경
os.chdir(dir_path)

# 변경된 작업 디렉토리 출력
#st.write(os.getcwd())

config = configparser.ConfigParser()
config.read('config.ini')

secret_key = config.get('DEFAULT', 'SECRET_KEY')
organization = config.get('DEFAULT', 'ORGANIZATION')

openai.organization = organization
openai.api_key = secret_key
openai.Model.list()

### 사용자 입력을 위한 웹 구현


# streamlit에서 데이터 누적이 안되는 문제가 있음. 
# DB 또는 파일 연동 필요 (여기서는 반영하지 않음)
dialogs = []   
user = st.text_input('입력하세요')
st.write(user)
if user !="":
    ### chatGPT에 입력   
    dialogs.append({'role':'user', 'content':user}) 
    st.write(dialogs)
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=dialogs
    )
        
    assistant = response['choices'][0]['message']['content']
    dialogs.append({'role':'assistant', 'content':assistant})
    
    st.write(assistant)    
    st.write(dialogs)


