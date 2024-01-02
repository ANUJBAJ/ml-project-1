import streamlit as st
import pandas as pd
import pickle
import json
import numpy as np
import csv
import os
import boto3
from io import StringIO
################/////////////////////////////////////////////////////////////////////////////////####################################
def upload_to_s3():
    global aws_access_key_id,aws_secret_access_key,bucket_name,csv_file_key
    local_file_path = '/home/anuj/Documents/ANUJ_Project/ml-project-1/Df_User_Inp_Data.csv'
    # Create an S3 client
    
    s3 = boto3.client('s3',aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    

    try:
        # Upload the file
        s3.upload_file(local_file_path, bucket_name, csv_file_key)
        #print(f"File '{local_file_path}' uploaded to '{bucket_name}/{s3_file_name}'.")
        

    except FileNotFoundError:
        print(f"The file '{local_file_path}' was not found.")
#####################################################################################################################################
############PRACTISING BOTO3 #########################################################################################################3
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
def Loan_app_pred(lst_1):
    model_1 = pickle.load(open('finalized_model.sav', 'rb'))
    if model_1.predict(lst_1) == 1:
        return 'Your Loan is approved'
    else :
        return 'Your Loan is not Approved' 
# #####################################################################################################################################
# #////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
def Reading_file(Inp_Cols):
        global csv_file_key
       # pd.DataFrame(columns = Inp_Cols).to_csv(csv_file_key)
        with open(csv_file_key,'a') as log_file:
            st.write('I am creating file locally')
            fl_wrt = csv.writer(log_file)
            fl_wrt.writerow(Inp_Cols)
        upload_to_s3()
        return None  
# #####################################################################################################################################
# #////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
# def Logging_Db(lg_ls):
#     with open('Df_User_Inp_Data.csv','a') as log_file:
#         fl_wrt = csv.writer(log_file)
#         fl_wrt.writerow(lg_ls)
#//////////////////////S3 BUCKET VERSION FOR THE SAME LOGGING DB//////////////////////////////////////////////////////////////////////////
# def Logging_Db(lg_ls):
#     global aws_access_key_id,aws_secret_access_key,bucket_name,csv_file_key
#     obj = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,)
#     response = obj.get_object(Bucket=bucket_name, Key=csv_file_key)
#     csv_content = response['Body'].read().decode('utf-8')
#     csv_reader = csv.reader(StringIO(csv_content ))
#     csv_data = list(csv_reader)
#     st.write(csv_data)
#     # csv_data.append(lg_ls)
   
#     # csv_buffer = StringIO()
#     # csv_writer = csv.writer(csv_buffer)
#     # csv_writer.writerows(csv_data)

#     #updated_csv_data = csv_writer.getvalue()
#     #obj.put_object(bucket_name = bucket_name,key =  csv_file_key,data = csv_buffer.getvalue())

# # #####################################################################################################################################
def Logging_Db(lg_ls):
    global aws_access_key_id,aws_secret_access_key,bucket_name,csv_file_key
    obj = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,)
    response = obj.get_object(Bucket=bucket_name, Key=csv_file_key)
    csv_content = response['Body'].read().decode('utf-8')
    df_lgdb = pd.read_csv(StringIO(csv_content))
    shp1 = df_lgdb.shape
    df_lgdb.loc[shp1[0],:] = lg_ls
    df_lgdb.to_csv(csv_file_key,index = False)
    upload_to_s3()

# #////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
aws_access_key_id = st.text_input('Enter your aws_access_key_id = ')
aws_secret_access_key = st.text_input('Enter your aws_secret_access_key = ')
bucket_name = 'anuj-placement-practise'
csv_file_key = 'Df_User_Inp_Data.csv'
df_proc = pd.read_csv('Df_train_mvr.csv') 
#s3 = boto3.client('s3',aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
with open('sample.json') as user_file:     
     dictionary = json.load(user_file)
df_proc.drop(columns = ['Loan_Status'],inplace =True)
Inp_Cols = df_proc.columns
st.title('Loan Approver app')
st.header('Few Entries and know wheteher your loan will be approved or not ')
inp_lst = []
log_lst = []

for cols in Inp_Cols:
     tmp_nm = f'{cols}'
     if df_proc[cols].dtypes == 'object' and cols  != 'Credit_History':
       tmp_lst = []
       tmp_1 = df_proc[cols].unique()
       for i in tmp_1:
           tmp_lst.append(i)
       
       option = st.selectbox(tmp_nm,tmp_lst)
       for opts in dictionary[cols].keys():
           if opts ==  option:
               inp_lst.append((dictionary[cols][opts]))
               log_lst.append(opts)
               
     else :
        if cols  == 'Credit_History':
             option = st.selectbox(tmp_nm,[0,1])
             inp_lst.append(option)
             log_lst.append(option)
            
        else :
              option = st.slider(f'{cols}',min_value = 0.0, max_value = float(df_proc[cols].max()))
              inp_lst.append(option)
              log_lst.append(option)
       
st.button("Writing_Csv")
if st.button('Save_record'):
    # try:
        
    #     s3.head_object(Bucket=bucket_name, Key=csv_file_key)
    #     Logging_Db(log_lst)
    # except :
    #    Reading_file(Inp_Cols)
    #    st.write('keying records to the database for the first time')
    #    Logging_Db(log_lst)
    if os.path.exists('/home/anuj/Documents/ANUJ_Project/ml-project-1/Df_User_Inp_Data.csv'):
        Logging_Db(log_lst)
    else:
        Reading_file(Inp_Cols)
        st.write('keying records to the database for the first time')
        Logging_Db(log_lst)


st.write(Loan_app_pred(np.array(inp_lst).reshape(1,-1)))




          


