import os
import gspread
import re
import gc
import hashlib
import json
from google.oauth2.service_account import Credentials

def getDataFromMappedFiles(config):
    data = config['data']
    creds = Credentials.from_service_account_info(data['credentials'], scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'])
    client = gspread.authorize(creds)
    sheet = client.open_by_key(data['sheetId'])
    worksheet = sheet.worksheet(config['merge']['project_name'])

    __HEADER_LINE = 0

    #TODO buscar apenas a coluna do nome dos arquivos
    data = worksheet.get_all_values()
    data.pop(__HEADER_LINE)

    return data

def getFileName(filePath):
    match = re.search(r'V', filePath)
    if match:
        return filePath[match.start():]

    return filePath

def review(config):
    path_source = config['path_source']

    merge = config['merge']
    changes = merge['changes']

    comments = []

    regex_list = config['regexFile']

    filesByRegex = []
    for change in changes:
        fileName = getFileName(change.get('new_path'))

        #TODO ajustar esse metodo para validar a lista toda caso sejam implementados novos regex
        if re.match(regex_list[0], fileName):
            filesByRegex.append(fileName)

    if len(filesByRegex) > 0:
        mappedFiles = getDataFromMappedFiles(config)

        for file in filesByRegex:
            if file not in mappedFiles:
                comments.append({
                    "id": __generate_md5(path_source),
                    "comment": f"Arquivo {file} nao mapeado na tabela de migrations",
                    "position": {
                        "language": "sql",
                        "path": path_source,
                        "startInLine": 1,
                        "endInLine": 1,
                        "snipset": False
                    }
                })

    print(comments)
    return comments


def __generate_md5(string):
    md5_hash = hashlib.md5()
    md5_hash.update(string.encode('utf-8'))
    return md5_hash.hexdigest()
