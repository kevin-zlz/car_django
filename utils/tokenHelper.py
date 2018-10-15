import datetime
import jwt
SECRECT_KEY="orsp"
def jwtEncoding(some, aud='webkit'):
    datetimeInt = datetime.datetime.utcnow() + datetime.timedelta(seconds=180)
    option = {
        'iss': 'jobapp.com',
        'exp': datetimeInt,
        'aud': 'webkit',
        'some': some
    }
    encoded2 = jwt.encode(option, SECRECT_KEY, algorithm='HS256')
    # print(encoded2.decode())
    return encoded2.decode()

def jwtDecoding(token):
    decoded = jwt.decode(token, SECRECT_KEY, audience='webkit', algorithms=['HS256'])
    if decoded:
        return True
    else:
        return False
