# https://docs.streamlit.io/library/api-reference
# https://platform.openai.com/docs/guides/chat/introduction

### 간단한 채팅 서비스를 구현해봅시다

### openai 연동
import configparser
import openai
import streamlit as st
import sys
import os
from sqlalchemy import create_engine
import pandas as pd

### 현재 스크립트로 작업 폴더 변경

# 현재 실행 중인 파일의 디렉토리 경로 가져오기
dir_path = os.path.dirname(os.path.realpath(__file__))

# 작업 디렉토리 변경
os.chdir(dir_path)

# 변경된 작업 디렉토리 출력
#st.write(os.getcwd())

# 설정 파일 가져오기: openai
config = configparser.ConfigParser()
config.read('config.ini')

secret_key = config.get('DEFAULT', 'SECRET_KEY')
organization = config.get('DEFAULT', 'ORGANIZATION')

openai.organization = organization
openai.api_key = secret_key
openai.Model.list()

# 설정 파일 가져오기: DB
host = config.get('DB', 'HOST')
port = int(config.get('DB', 'PORT'))
username = config.get('DB', 'USERNAME')
password = config.get('DB', 'PASSWORD')
db = config.get('DB', 'SCHEMA')

# 데이터베이스 연동 및 이전 데이터 삭제
# 일반적으로 DB 내용을 실행 시마다 삭제하지 않습니다. 
# 강의 코드 단순화를 위해서 초기화 내용 넣었습니다. 

con = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{db}")

### 사용자 입력을 위한 웹 구현

user = st.text_input('입력하세요')

if user !="":
    
    # 앞의 대화 가져오기
    query = '''select role, content from dialogs '''
    dialogs_df = pd.read_sql(query, con)
    dialogs = []
    if len(dialogs_df)>0:
        dialogs = dialogs_df.to_dict(orient='records')    
    ### chatGPT에 입력   
    
    dialog = {'role':'user', 'content':user}
    query = f'''INSERT INTO dialogs(role, content)
                VALUES('user','{user}'); '''
    con.execute(query)
    
    dialogs.append(dialog)
    st.write(dialogs)
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=dialogs
    )
        
    assistant = response['choices'][0]['message']['content']
    st.write(assistant)
    query = f'''INSERT INTO dialogs(role, content)
                VALUES('assistant','{assistant}'); '''
    con.execute(query)
    
# 대화 초기화 버튼
if st.button('대화 초기화'):
    con.execute('TRUNCATE TABLE dialogs')
    



