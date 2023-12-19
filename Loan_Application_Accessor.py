import streamlit as st
import pandas as pd
import pickle
import json
import numpy as np
def Loan_app_pred(lst_1):
    model_1 = pickle.load(open('finalized_model.sav', 'rb'))
    if model_1.predict(lst_1) == 0:
        return 'Your Loan is approved'
    else :
        return 'Your Loan is not Approved' 
#df_tr = pd.read_csv('/home/anuj/Documents/ANUJ_Project/RADHA_My_frst_project_preplaced/Loan_pred/Training Dataset.csv')
df_proc = pd.read_csv('/home/anuj/Documents/ANUJ_Project/RADHA_My_frst_project_preplaced/Df_train_mvr.csv') 
#dictionary = json.loads('/home/anuj/Documents/ANUJ_Project/RADHA_My_frst_project_preplaced/sample.json')
with open('/home/anuj/Documents/ANUJ_Project/RADHA_My_frst_project_preplaced/sample.json') as user_file:
     dictionary = json.load(user_file)
#print(dictionary)
df_proc.drop(columns = ['Unnamed: 0','Loan_Status'],inplace =True)
Inp_Cols = df_proc.columns
st.title('Loan Approver app')
st.header('Few Entries and know wheteher your loan will be approved or not ')
#print(df_proc['Loan_Status'].unique()[0])
inp_lst = []
for cols in Inp_Cols:
     tmp_nm = f'{cols}'
     if df_proc[cols].dtypes == 'object':
       tmp_lst = []
       tmp_1 = df_proc[cols].unique()
       for i in tmp_1:
           tmp_lst.append(i)
       option = st.selectbox(tmp_nm,tmp_lst)
       for opts in dictionary[cols].keys():
           if opts ==  option:
               inp_lst.append(dictionary[cols][opts])
               
     else :
        option = st.slider(f'{cols}',min_value = 0.0, max_value = float(df_proc[cols].max()))
        inp_lst.append(option)
inp_lst = np.array(inp_lst).reshape(1,-1)
st.write(Loan_app_pred(inp_lst))
          


