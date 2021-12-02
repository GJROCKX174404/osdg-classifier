import pandas as pd
import streamlit as st
import pickle
import numpy as np
import pdfplumber
from pdfminer.high_level import extract_text


model=pickle.load(open("Clf.pickle","rb"))
	

def Prediction(File):

	text =[]
	text.append(File)
	pb = model.predict_proba(text)
	result = pb.tolist()
	test_res = result[0]
	sdg_goals = ["1-No Poverty","2-Zero Hunger","3-Good Healthand Well Being","4-Quality Education"
            ,"5-Gender Equality","6-Clean Water and Sanitation","7-Affordable  and Clean Energy"
            ,"8-Decent Work and Economic Growth","9-Industry,Innovation and Infrastructure"
            ,"10-Reduced Inequalites","11-Sustainable Cities and Communities",
            "12-Responsible Consumption and Production","13-Climate Action","14-Life Below Water","15-Life On Land"]
            
	data_fuse =zip(sdg_goals,test_res)
	df_ForPred = pd.DataFrame(data_fuse,columns=["OSDG","Score"])   
	df_fin= df_ForPred.sort_values("Score", ascending = [False])
	return((df_fin))


############ 	Header Section
header = st.title('SDG Classifier')    
st.image('SDG.png')
Raw_input=""
  


####### Sample section  
sample=st.selectbox('Select a sample file For Demo',
                             ('HDFC_Bank_CSR.txt','BAJAJ_Auto_CSR.txt','COAL_India_CSR.txt','None'), index=3)


st.sidebar.title('File Manager')

if sample != 'None':
        file = open(sample, "r", encoding='utf-8')
        #st.write(file)
        Raw_input = file.read()
        
        
        
###SideBar Section        
st.sidebar.header('Upload File')
File=st.sidebar.file_uploader("Upload",type=["txt","pdf"])   
	
if(File):
	sample='None'
	if(File.type =="application/pdf"):
		try:
			with pdfplumber.open(File) as pdf:
				pages = pdf.pages[0]
				Raw_input=str(pages.extract_text())
				
		except:
			st.write("None")
	else:
		Raw_input = str(File.read())
		
#Classification Result Section 
if st.button('Check out Prediction'):

	if Raw_input == "":
		st.header('No text Entered')
		st.write('Please enter text or upload a file to see the Classification')
	else:
		#classification of the dcoument into SDG is done here
		Result=Prediction(Raw_input)
		st.title('SDG Classification')
		df1=st.dataframe(Result)
		csv=Result.to_csv().encode('utf-8')
		st.download_button('click here to Download Output csv file',data=csv,file_name='SDG_Classified.csv')
		
		df2 = pd.DataFrame(Result, columns = ["Score"])
		st.bar_chart(df2)

#Displays the input Document 
if(Raw_input!=""):
	expand = st.expander("See Orginal Report")
	with expand:
		st.write(Raw_input)



