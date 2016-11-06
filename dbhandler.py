from flask.ext import shelve

def getPassword(username):
    db = shelve.get_shelve('c')
    try:
        value = str(db[str(username)])
    except Exception:
        value = ""
    return value

def setPassword(username, password):
    db = shelve.get_shelve('c')
    db[str(username)] = password
    try:
        value = (password == str(db[str(username)]))
    except Exception:
        value = false
    return value
