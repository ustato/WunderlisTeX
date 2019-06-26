# -*- coding: utf-8 -*-
import yaml
import json
from requests_oauthlib import OAuth2Session

# API tokenを'secret.yaml'から参照する
yaml_dict = yaml.load(open('./secret.yaml'), Loader=yaml.SafeLoader)
client_id = yaml_dict['client_id']
access_token = yaml_dict['access_token']

url = "https://a.wunderlist.com/api/v1/lists"
params = {}

wunderlist = OAuth2Session()
wunderlist.headers['X-Client-ID'] = client_id
wunderlist.headers['X-Access-Token'] = access_token
req = wunderlist.get(url, params=params)

if req.status_code == 200:
    lists = json.loads(req.text)
    for list in lists:
        print (list["id"], list["title"])
else:
    print ("Error: %d" % req.status_code)
