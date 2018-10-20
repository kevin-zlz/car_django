import datetime
import jwt
SECRECT_KEY="orsp"
def jwtEncoding(some, aud='webkit'):
    datetimeInt = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
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
    # if decoded:
    #     return {
    #         "telphone":decoded
    #     }
    # else:
    #     return ''
    return decoded
'''

'''
# token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJqb2JhcHAuY29tIiwiZXhwIjoxNTQwMDAwMjg0LCJhdWQiOiJ3ZWJraXQiLCJzb21lIjoiMTU3NzY1NTQ2MTIifQ.FoPQ-r78b9l91nAFPsBRJmy2J3OOFmiJZFLES4izQs4"
# jwt.decode(token, SECRECT_KEY, audience='webkit', algorithms=['HS256'])