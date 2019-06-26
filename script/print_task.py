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

    for list_ in lists:
        url = "https://a.wunderlist.com/api/v1/tasks"
        params = {
                "list_id": list_["id"],
                "completed": True
                }
        done_tasks = json.loads(wunderlist.get(url, params=params).text)

        params["completed"] = False
        req = wunderlist.get(url, params=params)
        notdone_tasks = json.loads(wunderlist.get(url, params=params).text)

        tasks = done_tasks + notdone_tasks

        n_tasks = len(tasks)
        n_dones = len([task for task in tasks if task["completed"]==True])
        if (n_tasks != 0):
            print("{0} ({1:.2f} %)".format(list_["title"], n_dones / n_tasks))

        for task in tasks:
            if (task["completed"]):
                print("- {}: done".format(task["title"]))
            else:
                print("- {}: not done".format(task["title"]))
else:
    print("Error: %d" % req.status_code)
