def response(code:int, message:str, data = []):
    return {
        "code" : code,
        "message" : message,
        "data" : list(data)
    }