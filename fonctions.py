import os
import requests
import math
import time
import pandas as pd
from tqdm import tqdm
from pathlib import Path
import openpyxl

class colors:
    END = "\033[0m"

basedir = os.getcwd()

def horloge():
    timestamp = time.ctime()
    timestamp = str(pd.to_datetime(timestamp))
    timestamp = timestamp[8:10] + "_" + timestamp[5:7] + "_" + timestamp[:4] + "_" + timestamp[11:13] + "H_" + timestamp[14:16] + "M_" + timestamp[17:] + "S"
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

    for i in tqdm(range(1, nbr_pages+1), desc= f"{colors.END}~ Téléchargements des données "):
        url = f"https://www.justice.gov/multimedia-search?keys={recherche}&page={i}"
        headers = {"User-Agent": "Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12H321 [FBAN/FBIOS;FBAV/38.0.0.6.79;FBBV/14316658;FBDV/iPad4,1;FBMD/iPad;FBSN/iPhone OS;FBSV/8.4.1;FBSS/2; FBCR/;FBID/tablet;FBLC/en_US;FBOP/1]"}
        req = requests.get(url, headers=headers)
        req = req.json()
        req = req["hits"]["hits"]

        for x in range(len(req)):
            # Keys
            document_id = req[x]["_source"]["documentId"]
            document_key = req[x]["_source"]["key"]

            # Document
            start_page = req[x]["_source"]["startPage"]
            end_page = req[x]["_source"]["endPage"]
            mots = req[x]["_source"]["totalWords"]
            caractere = req[x]["_source"]["totalCharacters"]
            strings = req[x]["highlight"]["content"]
            strings = " -//- ".join(strings)
            recap_document = strings.replace("\n", " ").replace("<em>", "").replace("</em>", "")

            # Dates, source.
            preparation = req[x]["_source"]["processedAt"]
            indexation = req[x]["_source"]["indexedAt"]
            bucket = req[x]["_source"]["bucket"]
            source = req[x]["_source"]["source"]

            # File tag.
            pdf_tag = req[x]["_source"]["ORIGIN_FILE_URI"][0:45]+"%20"+req[x]["_source"]["ORIGIN_FILE_URI"][46:]
            
            # Bypass age verification.
            cookies = {"justiceGovAgeVerified": "true"}

            try:
                response = requests.get(pdf_tag, headers=headers, cookies=cookies)
                file_path = os.path.join(path, os.path.basename(pdf_tag))
                with open(file_path, "wb") as f:
                    f.write(response.content)
            except (requests.exceptions.HTTPError, requests.exceptions.SSLError):
                pass
            timestamp = horloge()
            global_df.append({"date_recuperation": timestamp,
                              "id_document": document_id,
                              "cle_document": document_key,
                              "page_debut": start_page,
                              "page_fin": end_page,
                              "nb_mots": mots,
                              "nb_caracteres": caractere,
                              "recap_document": recap_document,
                              "date_preparation": preparation,
                              "date_indexation": indexation,
                              "bucket": bucket,
                              "source": source})
        
    global_df = pd.DataFrame(global_df)
    timestamp = horloge()
    global_df.to_excel(path + fr"/{timestamp}_data_{recherche}_recap.xlsx", index_label=False)
    return nbr_fichier

def global_bdd_append(timestamp, recherche, occurences):
    base = os.getcwd()
    path = Path(base + "/base_de_donnees_globale.xlsx")
    df = pd.read_excel(path, usecols=["date_recuperation", "champ_recherche", "nombre_occurence"])
    data = []
    to_append = {
            "date_recuperation": timestamp,
            "champ_recherche": recherche,
            "nombre_occurence": occurences
        }
    data.append(to_append)
    data = pd.DataFrame(data)
    df = pd.concat([df, data])
    df.to_excel("base_de_donnees_globale.xlsx", index=False)
    return None