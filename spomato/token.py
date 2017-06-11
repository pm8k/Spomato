import os
import pandas as pd
import spotipy
from spotipy import oauth2
from splinter import Browser
import requests
import base64
import six
import time


file_path = os.path.expanduser('~')+'/'

def get_token(username=None,password=None,login='facebook'):

    if os.path.isfile(file_path+'token_info.csv'):
        token_info = pd.Series.from_csv(file_path+'token_info.csv')
        token = token_info['access_token']
        # print 'reading token from csv'
        if int(token_info['expires_at'])-int(time.time()) <= 0:
            # print 'token expired, create new token'
            token,token_info = get_new_token(username,password,login)
            token_info.to_csv(file_path+'token_info.csv')

    else:
        # print 'generate first token'
        token,token_info = get_new_token(username,password,login)
        token_info.to_csv(file_path+'token_info.csv')

    return token,token_info

def get_new_token(username=None,password=None,login='facebook'):

    OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'

    client_id = os.getenv('SPOTIPY_CLIENT_ID')
    client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
    redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
    username = os.getenv('SPOMATO_USERNAME')
    password = os.getenv('SPOMATO_PASSWORD')
    # username='astromars42@gmail.com'


    read_scope = 'playlist-read-private'
    modify_scope = 'playlist-modify-private'
    scope = read_scope + ' ' + modify_scope
    norm_scope = _normalize_scope(scope)

    sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri,
            scope=norm_scope, cache_path=".cache-" + username )
    auth_url = sp_oauth.get_authorize_url()

    code = get_url_code(auth_url,username,password,login)

    payload = {'redirect_uri': redirect_uri,
                   'code': code,
                   'grant_type': 'authorization_code',
                   'scope':norm_scope}

    headers = _make_authorization_headers(client_id,client_secret)

    response = requests.post(OAUTH_TOKEN_URL, data=payload,
            headers=headers, verify=True, proxies=None)

    token_info = response.json()

    token_info = _add_custom_values_to_token_info(token_info, norm_scope)

    mytoken = token_info['access_token']

    token_info = pd.Series(token_info)

    return mytoken,token_info

def get_url_code(auth_url,username,password,login='facebook'):
    b = Browser(driver_name='chrome')
    b.visit(auth_url)
    b.click_link_by_partial_href("/en/login")
    if login=='facebook':
        b.click_link_by_partial_href("https://www.facebook.com")
        b.fill_form({'email':username,'pass':password})
        b.click_link_by_id('loginbutton')
    elif login=='spotify':
        b.fill_form({'username':username,'password':password})
        loginbutton=b.find_by_text('Log In')[0]
        loginbutton.click()
    b.visit(auth_url)
    codeurl = b.url
    code = codeurl.split("?code=")[1].split('&')[0]
    b.quit()

    return code

def _make_authorization_headers(client_id, client_secret):
    auth_header = base64.b64encode(six.text_type(client_id + ':' + client_secret).encode('ascii'))
    return {'Authorization': 'Basic %s' % auth_header.decode('ascii')}

def _normalize_scope(scope):
    if scope:
        scopes = scope.split()
        scopes.sort()
        return ' '.join(scopes)
    else:
        return None

def _add_custom_values_to_token_info(token_info, scope):
    '''
    Store some values that aren't directly provided by a Web API
    response.
    '''
    token_info['expires_at'] = int(time.time()) + token_info['expires_in']
    token_info['scope'] = scope
    return token_info
