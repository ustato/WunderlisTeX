import yaml
import json
import datetime
from requests_oauthlib import OAuth2Session


class ToDoList:
    """
    WunderListのToDoリストを扱うクラス．
    """

    def __init__(self):
        """
        ToDoリストを取得する．
        """

        self.todolist = {}

        # API tokenを"secret.yaml"から参照する
        yaml_dict = yaml.load(open("./secret.yaml"), Loader=yaml.SafeLoader)
        client_id = yaml_dict['client_id']
        access_token = yaml_dict['access_token']

        # APIからデータを取得
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
                done_tasks = json.loads(
                        wunderlist.get(url, params=params).text)

                params["completed"] = False
                req = wunderlist.get(url, params=params)
                notdone_tasks = json.loads(
                        wunderlist.get(url, params=params).text)

                tasks = done_tasks + notdone_tasks
                completed_task = [
                        task for task in tasks if task["completed"] == True]
                n_tasks = len(tasks)
                n_dones = len(completed_task)

                if (n_tasks != 0):
                    self.todolist[list_["title"]] = {}
                    self.todolist[list_["title"]]["title"] = list_["title"]
                    self.todolist[list_["title"]]["tasks"] = tasks
                    self.todolist[list_["title"]]["n_tasks"] = n_tasks
                    self.todolist[list_["title"]]["n_dones"] = n_dones
                    self.todolist[list_["title"]]["progress"] = (
                            n_dones / n_tasks)
                    self.todolist[list_["title"]]["completed_task"] = (
                            completed_task)


    def get_todotable(self):
        tex_message = ""

        for lists in self.todolist.values():
            if (lists["n_tasks"] != 0):
                tex_message += "\\begin{0}{1}".format(
                        "{myframe}", "{"+lists["title"])
                tex_message += "\\progressbar{0} {1:f} {2}".format(
                        '{', lists["progress"], '}')
                tex_message += "({0:d}\%)".format(
                        int(lists["progress"]*100))
                tex_message += "} \\begin{tabular}{ll}"

                for task in lists["tasks"]:
                    task_title = task["title"]
                    task_star = ''
                    task_mark = "$\\Box$"

                    if (task["starred"]):
                        task_star = "$\\star$"
                    if (task["completed"]):
                        task_mark = "$\\CheckedBox$"

                    tex_message += "{0} & {1}{2} \\\\".format(
                            task_mark, task_star, task_title)

                tex_message += "\\end{tabular}\\end{myframe}"

        return tex_message


    def itemize(process):
        def wrapper(self, *args, **kwargs):
            tex_message = ""

            for lists in self.todolist.values():
                temp_message = process(lists)

                if (temp_message != ""):
                    tex_message += (
                            "\\item "
                            + lists["title"]
                            + "\\begin{itemize}"
                            + temp_message
                            + "\\end{itemize}")

            if (tex_message != ""):
                tex_message = (
                        "\\begin{itemize}"
                        + tex_message
                        + "\\end{itemize}")

            return tex_message
        return wrapper


    @itemize
    def get_completed_task_in_a_week(lists):
        temp_message = ""
        now = datetime.datetime.now()

        if (lists["completed_task"] != []):
            for completed_task in lists["completed_task"]:
                completed_at = datetime.datetime.strptime(
                        completed_task["completed_at"],
                        '%Y-%m-%dT%H:%M:%S.%fZ')

                if (completed_at > (now - datetime.timedelta(days=7))):
                    temp_message += "\\item " + completed_task["title"]

        return temp_message


    @itemize
    def get_starred_task(lists):
        temp_message = ""

        for task in lists["tasks"]:
            if (task["starred"] and (not task["completed"])):
                temp_message += "\\item " + task["title"]

        return temp_message
