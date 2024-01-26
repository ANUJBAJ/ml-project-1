import streamlit as st
import pandas as pd
import pickle
import json    
import numpy as np
import csv
import os
import boto3
from io import StringIO
import string
import random
import mysql.connector
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def Id_generator():
     chars = string.ascii_uppercase + string.digits
     random_id = ''.join(random.choice(chars) for _ in range(8))
     return(random_id)
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def get_parameters():
    ssm = boto3.client('ssm', aws_access_key_id=os.getenv('access_key_id'), aws_secret_access_key=os.getenv('secret_access_key'),region_name = 'us-east-1')
    dct1 ={}
    response = ssm.get_parameters(
    Names=['mysql-host','mysql-port','mysql-database','mysql-user','mysql-password'])#,WithDecryption=True
    for parameter in response['Parameters']:
        if parameter['Name'] =='mysql-host':
               dct1['host'] = parameter['Value']
        if parameter['Name'] =='mysql-database':
               dct1['database'] = parameter['Value']
        if parameter['Name'] =='mysql-password':
               dct1['password'] = parameter['Value']
        if parameter['Name'] =='mysql-port':
               dct1['port'] = parameter['Value']
        if parameter['Name'] =='mysql-user':
               dct1['user'] = parameter['Value']
        
    return (dct1)
        
#///////////////////////////////////////////////////////////////////////////////////////////#######################################
def Logging_Db(lst1):
    dct2 = get_parameters()
    values = ()
    conn = mysql.connector.connect(
    host=dct2['host'],
    port=dct2['port'],
    database=dct2['database'],
    user=dct2['user'],
    password=dct2['password']
    )  
    cursor = conn.cursor()
    sql_insert_query = """
    INSERT INTO Banking_Customers(Id,Gender , Married , Dependents , Education , Self_Employed , ApplicantIncome ,CoapplicantIncome , LoanAmount , Loan_Amount_Term ,Credit_History,Property_Area,Loan_Status) 
    VALUES (%s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s,%s);
     """
    for i in lst1:
        values += (i,)
    cursor.execute(sql_insert_query, values)
    conn.commit()
    cursor.close()
    conn.close()
# # #####################################################################################################################################
# ############PRACTISING parameter store #########################################################################################################3
# #//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
def Loan_app_pred(lst_1):
    model_1 = pickle.load(open('finalized_model.sav', 'rb'))
    if model_1.predict(lst_1) == 1:
        return 'Yes'
    else :
        return 'No' 
# # #####################################################################################################################################
#
# # #////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
df_proc = pd.read_csv('Df_train_mvr.csv') 
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

log_lst.insert(0,Id_generator())
st.write(log_lst)
if st.button('Submit'):
   if (Loan_app_pred(np.array(inp_lst).reshape(1,-1)))=='Yes':
        log_lst.append('Yes')
        Logging_Db(log_lst)
        st.write('Your Loan is approved')
   else :
         log_lst.append('No')
         Logging_Db(log_lst)
         st.write('Your Loan is not approved')
        
        
        
        
        
    


          


