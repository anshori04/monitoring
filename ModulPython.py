#Modul Python
import pandas as pd                 # digunakan untuk pengolahan data frames, data tabels, data array. data pivot
#import seaborn as sns               # digunakan untuk menampilkan plot atau distribusi, fungsinya sama dengan matplotlib namun seaborn lebih pendistribusianya
#import time as ts
#from datetime import time
import psycopg2                     #ini modul database opc
from psycopg2 import Error
import warnings             
warnings.filterwarnings('ignore')
import numpy as np

import streamlit as st

col1, col2, col3 = st.columns([1,1,1])

#Koneksi Modul
try:
    connection = psycopg2.connect(user="opc",password="opc12345",host="10.7.19.140",port="5432",database="opc")
    print("****************")
    print("OPC UJKT ................... Koneksi Tersambung")
    print("****************")
except (Exception, Error) as error:
    print("Error cek koneksi dan pastikan satu Jaringan Kantor", error)

#List Taglist DCS
lst=[]

B1A = 'KALTIM_0.SIGNAL.AI.10HFA10CL101'
B1B = 'KALTIM_0.SIGNAL.AI.10HFA20CL101'
B1C = 'KALTIM_0.SIGNAL.AI.10HFA30CL101'
B1D = 'KALTIM_0.SIGNAL.AI.10HFA40CL101'
B1E = 'KALTIM_0.SIGNAL.AI.10HFA50CL101'
B1F = 'KALTIM_0.SIGNAL.AI.10HFA60CL101'
B2A = 'KALTIM_0.SIGNAL.AI.20HFA10CL101'
B2B = 'KALTIM_0.SIGNAL.AI.20HFA20CL101'
B2C = 'KALTIM_0.SIGNAL.AI.20HFA30CL101'
B2D = 'KALTIM_0.SIGNAL.AI.20HFA40CL101'
B2E = 'KALTIM_0.SIGNAL.AI.20HFA50CL101'
B2F = 'KALTIM_0.SIGNAL.AI.20HFA60CL101'

C1A = 'KALTIM1.SIGNAL.AI.10HFB10AF001XQ02'
C1B = 'KALTIM1.SIGNAL.AI.10HFB20AF001XQ02'
C1C = 'KALTIM1.SIGNAL.AI.10HFB30AF001XQ02'
C1D = 'KALTIM1.SIGNAL.AI.10HFB40AF001XQ02'
C1E = 'KALTIM1.SIGNAL.AI.10HFB50AF001XQ02'
C1F = 'KALTIM1.SIGNAL.AI.10HFB60AF001XQ02'
C2A = 'KALTIM2.SIGNAL.AI.20HFB10AF001XQ02'
C2B = 'KALTIM2.SIGNAL.AI.20HFB20AF001XQ02'
C2C = 'KALTIM2.SIGNAL.AI.20HFB30AF001XQ02'
C2D = 'KALTIM2.SIGNAL.AI.20HFB40AF001XQ02'
C2E = 'KALTIM2.SIGNAL.AI.20HFB50AF001XQ02'
C2F = 'KALTIM2.SIGNAL.AI.20HFB60AF001XQ02'

st.sidebar.header('Input Tanggal')
tglstart = st.sidebar.date_input("Masukkan tanggal mulai")
tmstart = st.sidebar.time_input("Masukkan waktu mulai")
tglover = st.sidebar.date_input("Masukkan tanggal berakhir")
tmover = st.sidebar.time_input("Masukkan waktu berakhir")

start = "'" + str(tglstart) + " " + str(tmstart) + "'"
finish = "'" + str(tglover) + " " + str(tmover) + "'"

#Data yang akan dipanggil
lst=[]
list = [B1A, B1B, B1C,B1D, B1E, B1F, B2A, B2B, B2C, B2D, B2E, B2F, C1A, C1B, C1C, C1D, C1E, C1F, C2A, C2B, C2C, C2D, C2E, C2F]
tglin = start
tglout = finish
menit="0,15,30,45"

#Resume
print("*****************")
print('Tanggal Tarikan OPC dari',tglin,"Sampai",tglout)
print("Input Tag DCS berjumlah",len(list),"Item Tag")
print("*****************")

#query
print("Tarikan OPC Loading.....")
print("Tanggal Tarikan dari",tglin,"Sampai",tglout)
sql= connection.cursor()
query="select a.date_rec as tanggal_penarikan,b.address_no,b.description, round(a.value,2) as nilai_operasi,b.satuan from history a,address b where a.address_no="
func=" and a.address_no=b.address_no "
dat="and a.date_rec >= timestamp "+tglin+" and a.date_rec <= timestamp "+tglout+" "
ext="and extract (minute from a.date_rec) in ("+menit+") order by a.date_rec"
#tag disesuaikan dengan taglis, silahkan tambahkan sesuaikan dengan keinginan 
#loop Query
if menit=="0":
    for lop in list:
        var=query + "'" + lop + "'" + func + dat + ext
        sql.execute(var)
        lst.extend(sql.fetchall())
else:
    for lop in list:
        var=query + "'" + lop + "'" + func + dat + ext
        sql.execute(var.replace('KALTIM_0','KALTIM 0'))
        lst.extend(sql.fetchall())
df = pd.DataFrame.from_records(lst, columns=[x[0] for x in sql.description])

#Pivot of DataFrame Query SQL
data=df.pivot(index='tanggal_penarikan',columns='description',values='nilai_operasi').astype(float)

st.markdown("""
# Skripsi iOT

Anshori
197030717

""")

st.write(data)

col1.area_chart(data['Bunker 1A'], width = 100, height = 200)
col2.area_chart(data['Bunker 1B'], width = 100, height = 200)
col3.area_chart(data['Bunker 1C'], width = 100, height = 200)
col1.area_chart(data['Bunker 1D'], width = 100, height = 200)
col2.area_chart(data['Bunker 1E'], width = 100, height = 200)
col3.area_chart(data['Bunker 1F'], width = 100, height = 200)
col1.area_chart(data['Bunker 2A'], width = 100, height = 200)
col2.area_chart(data['Bunker 2B'], width = 100, height = 200)
col3.area_chart(data['Bunker 2C'], width = 100, height = 200)
col1.area_chart(data['Bunker 2D'], width = 100, height = 200)
col2.area_chart(data['Bunker 2E'], width = 100, height = 200)
col3.area_chart(data['Bunker 2F'], width = 100, height = 200)

st.area_chart(data['Unit#1 - A coal feeder flow feedback'], width = 100, height = 200)
st.area_chart(data['Unit#1 - B coal feeder flow feedback'], width = 100, height = 200)
st.area_chart(data['Unit#1 - C coal feeder flow feedback'], width = 100, height = 200)
st.area_chart(data['Unit#1 - D coal feeder flow feedback'], width = 100, height = 200)
st.area_chart(data['Unit#1 - E coal feeder flow feedback'], width = 100, height = 200)
st.area_chart(data['Unit#1 - F coal feeder flow feedback'], width = 100, height = 200)
st.area_chart(data['Unit#2 - A coal feeder flow feedback'], width = 100, height = 200)
st.area_chart(data['Unit#2 - B coal feeder flow feedback'], width = 100, height = 200)
st.area_chart(data['Unit#2 - C coal feeder flow feedback'], width = 100, height = 200)
st.area_chart(data['Unit#2 - D coal feeder flow feedback'], width = 100, height = 200)
st.area_chart(data['Unit#2 - E coal feeder flow feedback'], width = 100, height = 200)
st.area_chart(data['Unit#2 - F coal feeder flow feedback'], width = 100, height = 200)