import hashlib
import os
import re

import gspread
from google.oauth2.service_account import Credentials


def get_data_from_mapped_files(config, project_name):
    data = config['data']
    creds = Credentials.from_service_account_info(data['credentials'],
                                                  scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'])
    client = gspread.authorize(creds)
    sheet = client.open_by_key(data['sheetId'])
    worksheet = sheet.worksheet(project_name)

    __HEADER_LINE = 0
    if 'column' in data:
        __VALUE_COLUMN = data['column']
    else:
        __VALUE_COLUMN = 1

    data = worksheet.col_values(__VALUE_COLUMN)
    data.pop(__HEADER_LINE)

    return data


def get_file_name(file_path):
    return os.path.basename(file_path)


def review(config):
    merge = config['merge']
    changes = merge['changes']
    project_name = merge['project_name']

    comments = []

    if 'configs' in config:
        configs = config['configs']
    else:
        configs = [config]

    for obj_config in configs:
        comments.extend(review_by_config(obj_config, changes, project_name, config))

    return comments


def review_by_config(config, changes, project_name, config_root):
    comments = []
    regex_list = config['regexFile']

    files_by_regex = []
    for change in changes:
        file_name = get_file_name(change.get('new_path'))

        # TODO ajustar esse metodo para validar a lista toda caso sejam implementados novos regex
        if re.match(regex_list[0], file_name):
            files_by_regex.append({
                "basename": file_name,
                "absolutePath": change.get('new_path')
            })

    if len(files_by_regex) > 0:
        mapped_files = get_data_from_mapped_files(config, project_name)

        for file in files_by_regex:
            if file['basename'] not in mapped_files:
                comment = {
                    "id": __generate_md5(file['absolutePath']),
                    "comment": config['message'].replace("${FILE_NAME}", file['basename']),
                    "position": {
                        "language": "",
                        "path": file['absolutePath'],
                        "startInLine": 1,
                        "endInLine": 1,
                        "snipset": False
                    }
                }

                if 'processorArgs' in config_root:
                    comment['processorArgs'] = config_root['processorArgs']

                comments.append(comment)

    return comments


def __generate_md5(string):
    md5_hash = hashlib.md5()
    md5_hash.update(string.encode('utf-8'))
    return md5_hash.hexdigest()
