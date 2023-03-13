import re
import pandas as pd
import sqlite3 as sql3
import numpy as np
import matplotlib.pyplot as plt

from flask import Flask, jsonify, request
from flasgger import Swagger, LazyString, LazyJSONEncoder, swag_from
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# create stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

app = Flask(__name__)

app.json_encoder = LazyJSONEncoder
# app.json = LazyJSONEncoder
swagger_template = dict(
info = {
    'title': LazyString(lambda:'API Documentation for Data Processing and Modeling'),
    'version' : LazyString(lambda: '2.0.0'),
    'description' : LazyString(lambda: 'Dokumentasi API untuk Data Processing dan Modeling'),
    },
    host = LazyString(lambda: request.host)
)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json'
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger = Swagger(app,template = swagger_template, config = swagger_config)

UPLOAD_FOLDER = 'data/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def Hallo():
    return "Hallo Ari Angga"

@swag_from("docs/Text_Processing.yml", methods=['POST'])
@app.route('/Proses-Text', methods=['POST'])
def text():
    teks_input = request.form.get('text')
    teks_output = cleansing(teks_input)
     
    json_respon = {
        'input' : teks_input,
        'output' : teks_output,
    }
    response_data = jsonify(json_respon)
   
    return response_data

@swag_from("docs/File_Processing.yml", methods=['POST'])
@app.route('/Proses-File', methods=['POST'])
def uploadfile():
    # upload file data.csv
    # load data abusive
    # load data alay
    # looping isi tweet di data.csv
        # cek satu per satu tweet ada atau tidak abusive, jika ada maka hapus abusive
        # cek satu per satu tweet ada atau tidak alay, jika ada maka ganti dengan text baku
        # simpan tweet yang sudah di cleansing sebagai new_tweet

    # upload file data.csv
    uploadfile = request.files['file']
    df_csv = pd.read_csv(uploadfile,encoding='latin-1')
    df_csv = df_csv['Tweet']
    df_csv = df_csv.drop_duplicates()

    all_new_tweet = []
    # looping isi tweet di data.csv
    for tweet in df_csv:
        new_tweet = cleansing(tweet)
        new_tweet = stemmer.stem(new_tweet)
        all_new_tweet.append(new_tweet)

    return str(all_new_tweet)

    
# proses ambil data di database ke dataframe
conn = sql3.connect("data/abusive_challenge.db", check_same_thread=False)

def removeVowels(str):
    vowels = 'aeiou'
    for ele in vowels:
        str = str.replace(ele, "x")
    return str

def case_folding(teks):
    # proses cleansing
    # 1. jadikan teks agar lowercase
    teks = teks.lower()
    # 2. hanya menerima alfabet text
    teks = re.sub(r'[^\w\d\s]+',' ', teks)
    # menghapus whitespace di awal dan di akhir kalimat
    teks = teks.strip()
    return teks

# ubah kata alay menjadi kata baku
def normalization_alay(teks):
    df_alay = pd.read_sql_query('select * from ALAY', conn)
    dict_alay = dict(zip(df_alay['teks_alay'],df_alay['teks_baku']))
    teks = teks.split()
    teks_normal = ''
    for str in teks:
        if(bool(str in dict_alay)):
            teks_normal = teks_normal + ' ' + dict_alay[str]
        else:
            teks_normal = teks_normal + ' ' + str
    teks_normal = teks_normal.strip()
    return teks_normal

# fungsi untuk sensor kata-kata abusive
def normalization_abusive(teks):
    df_abusive = pd.read_sql_query("select * from ABUSIVE", conn)
    dict_abusive = dict(zip(df_abusive['teks'],df_abusive['teks']))
    teks = teks.split()
    teks_normal = ''
    for str in teks:
        if(bool(str in dict_abusive)):
            str = removeVowels(str)
            teks_normal = teks_normal + ' ' + str
        else:
            teks_normal = teks_normal + ' ' + str  
    teks_normal = teks_normal.strip()
    return teks_normal
   
def cleansing(teks):
    teks = case_folding(teks)
    teks = normalization_alay(teks)
    teks = normalization_abusive(teks)
    
    return teks

if __name__ == '__main__' :
    app.run(debug=True)