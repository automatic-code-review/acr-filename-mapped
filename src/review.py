def review(config):
    path_target = config['path_target']
    path_source = config['path_source']

    merge = config['merge']
    project_id = merge['project_id']
    merge_request_id = merge['merge_request_id']
    
    comments = []
    
    # TODO IMPLEMENTAR EXTENSION
    #  O OBJETO DE COMENTARIO DEVE POSSUIR O SEGUINTE FORMATO
    #  {
    #      "id": "",
    #      "comment": "",
    #      "position": {
    #          "language": "",
    #          "path': "",
    #          "startInLine": 0,
    #          "endInLine": 0
    #    }
    #  }

    return comments
