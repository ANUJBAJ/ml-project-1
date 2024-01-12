import streamlit as st
import pandas as pd
import pickle
import json
import numpy as np
import csv
import os
import boto3
from io import StringIO
#from sqlalchemy import create_engine
import mysql.connector

#///////////////////////////////////////////////////////////////////////////////////////////#######################################
#
#engine = create_engine(f"mysql://{os.environ['username']}:{os.environ['password']}@{os.environ['host']}/{os.environ['database']}")

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#
def Logging_Db(lst1):
    values = ()
    conn = mysql.connector.connect(
    host=os.environ['host'],
    port=os.environ['port'],
    database=os.environ['database'],
    user=os.environ['username'],
    password=os.environ['password']
    )  
    cursor = conn.cursor()
    sql_insert_query = """
    INSERT INTO Banking_Customers(Gender , Married , Dependents , Education , Self_Employed , ApplicantIncome ,CoapplicantIncome , LoanAmount , Loan_Amount_Term ,Credit_History,Property_Area) 
    VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s);
     """
    for i in lst1:
        values += (i,)
    cursor.execute(sql_insert_query, values)
    conn.commit()
    cursor.close()
    conn.close()

################/////////////////////////////////////////////////////////////////////////////////####################################
#
# #####################################################################################################################################
# ############PRACTISING BOTO3 #########################################################################################################3
# #//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
def Loan_app_pred(lst_1):
    model_1 = pickle.load(open('finalized_model.sav', 'rb'))
    if model_1.predict(lst_1) == 1:
        return 'Your Loan is approved'
    else :
        return 'Your Loan is not Approved' 
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



if st.button('Save_record'):
    Logging_Db(log_lst)
    


st.write(Loan_app_pred(np.array(inp_lst).reshape(1,-1)))




          


