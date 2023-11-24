from pathlib import Path
from multilogging import multilogger
from dicergirl.utils.handlers import get_group_id, get_user_id

import json

current_dir = Path(__file__).resolve().parent
uvdiviner_dir = Path.home() / ".uvdiviner"
data_dir = uvdiviner_dir / "data"
_divination_cachepath = data_dir / "divination.json"

logger = multilogger(name="DicerGirl", payload="diviner")


def init():
    if not uvdiviner_dir.exists():
        logger.info("UVDiviner 文件夹未建立, 建立它.")
        uvdiviner_dir.mkdir()
    if not data_dir.exists():
        logger.info("UVDiviner 数据文件夹未建立, 建立它.")
        data_dir.mkdir()
    if not _divination_cachepath.exists():
        logger.info("UVDiviner 数据存储文件未建立, 建立它.")
        with open(_divination_cachepath, "w", encoding="utf-8") as f:
            f.write("{}")


def load_limit() -> dict:
    data = _divination_cachepath.read_text()
    if data:
        return json.loads(data)
    else:
        return {}


def minus_limit(event):
    datas = load_limit()
    datas[get_group_id(event)][get_user_id(event)]["limit"] -= 1
    file = _divination_cachepath.open(mode="w", encoding="utf-8")
    json.dump(datas, file)


def reset_limit():
    datas: dict = json.loads(_divination_cachepath.read_text(encoding="utf-8"))
    for group, users in datas.items():
        for user in users.keys():
            datas[group][user]["limit"] = 2

    json.dump(datas, _divination_cachepath.open(mode="w", encoding="utf-8"))


def get_limit(event):
    return load_limit()[get_group_id(event)][get_user_id(event)]["limit"]


def has_user(event):
    datas = load_limit()
    if not has_group(event):
        return False

    if get_user_id(event) not in datas.keys():
        return False

    return True


def has_group(event):
    datas = load_limit()
    if get_group_id(event) not in datas.keys():
        return False

    return True


def get_users():
    users = []
    for group in load_limit():
        users += [user for user in group.keys()]

    return users


def get_groups():
    groups = load_limit().keys()
    if len(groups) == 1:
        if groups[0] == "0":
            return False

    return groups


def set_user(event):
    datas = load_limit()
    if not has_group(event):
        datas[get_group_id(event)] = {}

    datas[get_group_id(event)][get_user_id(event)] = {"limit": 3}

    file = open(_divination_cachepath, "w")
    json.dump(datas, file)
