from dotenv import load_dotenv
import os
import json
import base64
from requests import post
import os
import spotipy.util as utilimport
from urllib.parse import urlencode

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_url = "https://localhost/"



# credentials
# user = 'username'
# desired_scope = 'playlist-modify-private'
# id = os.environ.get('SPOT_CLIENT')
# secret = os.environ.get('SPOT_SECRET')
# uri = 'https://localhost'
# token = util.prompt_for_user_token(username=user,
#                                    scope=desired_scope,
#                                    client_id=id,
#                                    client_secret=secret,
#                                    redirect_uri=uri)

def get_auth_code():
    
    auth_params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_url,
        'scope': 'playlist-modify-private playlist-modify-public user-modify-playback-state',
    }

    auth_url = 'https://accounts.spotify.com/authorize?' + urlencode(auth_params)
    print(f"Please navigate to this URL to authorize your application: {auth_url}"+"\n--------")
    response_url = input("Paste the URL you were redirected to here: ")
    response_params = dict(pair.split('=') for pair in response_url.split('&'))
    auth_code = response_params['https://localhost/?code']
    return auth_code

def get_token(auth_code):

    # url = "https://accounts.spotify.com/api/token"

    # headers = {
    #     "Authorization": "Basic " + auth_base64,
    #     "Content-Type": "application/x-www-form-urlencoded",
    # }
    # data = {"grant_type": "client_credentials"}
    # result = post(url, headers=headers, data=data)
    # json_result = json.loads(result.content)
    # print(json_result)
    # token = json_result["access_token"]
    # return token

    token_url = 'https://accounts.spotify.com/api/token'
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    token_params = {
        'code': auth_code,
        'redirect_uri': redirect_url,
        'grant_type': 'authorization_code',
    }
    token_headers = {
        'Authorization': 'Basic ' + auth_base64,
        
    }
    result = post(token_url, data=token_params, headers=token_headers)
    token_data = json.loads(result.content)
    token = token_data["access_token"]
    return token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}