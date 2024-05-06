import gspread
import gc
import hashlib
import json

def getMigrationList():
    sheet = gc.open(config['sheet'])
    worksheet = sheet.worksheet(config['worksheet'])
    migrationList = worksheet.col_values(config['columnOfMigrationName'])
    migrationList.pop(0)

    return migrationList

def review(config):
    path_target = config['path_target']
    path_source = config['path_source']

    merge = config['merge']
    project_id = merge['project_id']
    merge_request_id = merge['merge_request_id']
    
    comments = []

    gc = gspread.oauth()
    gspread.oauth_from_dict(config['credentials'], config['authorizedUser'])

    if path_source not in getMigrationList():
        comments.append({
                        "id": __generate_md5(path_source),
                        "comment": f"Arquivo {path_source} nao mapeado na tabela de migrations",
                        "position": {
                            "language": "sql",
                            "path": path_source,
                            "startInLine": 1,
                            "endInLine": 1,
                            "snipset": False
                        }
                    })

    return comments

def __generate_md5(string):
    md5_hash = hashlib.md5()
    md5_hash.update(string.encode('utf-8'))
    return md5_hash.hexdigest()