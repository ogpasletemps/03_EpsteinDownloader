import os
import requests
import math
import time
import pandas as pd
from tqdm import tqdm
import openpyxl

basedir = os.getcwd()

def horloge():
    timestamp = time.ctime()
    timestamp = str(pd.to_datetime(timestamp))
    timestamp = timestamp[:4] + "_" + timestamp[5:7] + "_" + timestamp[8:10] + "_"  + timestamp[11:13] + "_" + timestamp[14:16] + "_" + timestamp[17:]
    return timestamp

def create_dir(name):
    parent_path = os.getcwd()
    mode = 0o755
    path = os.path.join(parent_path, name)
    os.mkdir(path, mode)
    return path

def download_data(recherche):
    timestamp = horloge()
    path = create_dir(f"{recherche}_{timestamp}")
    url = f"https://www.justice.gov/multimedia-search?keys={recherche}&page=1"
    headers = {"User-Agent": "Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12H321 [FBAN/FBIOS;FBAV/38.0.0.6.79;FBBV/14316658;FBDV/iPad4,1;FBMD/iPad;FBSN/iPhone OS;FBSV/8.4.1;FBSS/2; FBCR/;FBID/tablet;FBLC/en_US;FBOP/1]"}
    req = requests.get(url, headers=headers)
    req = req.json()
    nbr_fichier = req["hits"]["total"]["value"]
    nbr_pages = math.ceil(nbr_fichier/10)
    global_df = []

    for i in tqdm(range(1, nbr_pages+1), desc= "Downloading data :"):
        url = f"https://www.justice.gov/multimedia-search?keys={recherche}&page={i}"
        headers = {"User-Agent": "Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12H321 [FBAN/FBIOS;FBAV/38.0.0.6.79;FBBV/14316658;FBDV/iPad4,1;FBMD/iPad;FBSN/iPhone OS;FBSV/8.4.1;FBSS/2; FBCR/;FBID/tablet;FBLC/en_US;FBOP/1]"}
        req = requests.get(url, headers=headers)
        req = req.json()
        req = req["hits"]["hits"]

        for x in range(len(req)):
            document_id = req[x]["_source"]["documentId"]
            document_key = req[x]["_source"]["key"]
            start_page = req[x]["_source"]["startPage"]
            end_page = req[x]["_source"]["endPage"]
            mots = req[x]["_source"]["totalWords"]
            date = req[x]["_source"]["processedAt"]
            source = req[x]["_source"]["source"]
            pdf_tag = req[x]["_source"]["ORIGIN_FILE_URI"][0:45]+"%20"+req[x]["_source"]["ORIGIN_FILE_URI"][46:]
            cookies = {"justiceGovAgeVerified": "true"}
            try:
                response = requests.get(pdf_tag, headers=headers, cookies=cookies)
                file_path = os.path.join(path, os.path.basename(pdf_tag))
                with open(file_path, "wb") as f:
                    f.write(response.content)
            except (requests.exceptions.HTTPError, requests.exceptions.SS):
                pass
            timestamp = horloge()
            global_df.append({"date_recuperation": timestamp,
                              "id_document": document_id,
                              "cle_document": document_key,
                              "page_debut": start_page,
                              "page_fin": end_page,
                              "nb_mots": mots,
                              "date_preparation": date,
                              "source": source})
        
    global_df = pd.DataFrame(global_df)
    timestamp = horloge()
    global_df.to_excel(path + fr"/{timestamp}_data_{recherche}_recap.xlsx", index_label=False)
    return None