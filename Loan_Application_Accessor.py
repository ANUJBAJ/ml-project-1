import streamlit as st
import pandas as pd
df_tr = pd.read_csv('/home/anuj/Documents/ANUJ_Project/RADHA_My_frst_project_preplaced/Loan_pred/Training Dataset.csv')
#df_tr.drop(columns = ['Loan_Status','Loan_ID'_],inplace = True)
df_tr.drop(columns = ['Loan_ID','Loan_Status'],inplace =True)

Inp_Cols = df_tr.columns
st.title('Loan Approver app')
st.header('Few Entries and know wheteher your loan will be approved or not ')
#print(df_tr['Loan_Status'].unique()[0])
inp_lst = []
for cols in Inp_Cols:
     tmp_nm = f'{cols}'
     inp_lst.append(tmp_nm)
     if df_tr[cols].dtypes == 'object':
       tmp_lst = []
       tmp_1 = df_tr[cols].unique()
       for i in tmp_1:
           tmp_lst.append(i)
       
       option = st.selectbox(tmp_nm,tmp_lst[0:-1])
     else :
        tmp_nm = st.slider(f'{cols}',min_value = 0.0, max_value = float(df_tr[cols].max()))

          


