import hashlib
import json
import os
import random
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from zhipuai import ZhipuAI

ans_dict = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3
}
shareId = os.getenv("shareId")
fid = os.getenv("fid")
ai_key = os.getenv("ai_key")
did = os.getenv("did")
proxy_time = os.getenv("proxy_time")

activity_token_dict = {

    "AN_TOy81hLg": {"region": "湖北", "interface": "hubei", "share_subBiz": "JIMU_ERXYLGLCOC", "shareObjectId": "JIMU_ERXylgLc"},
    "AN_XHfJRWxM": {"region": "河北", "interface": "hebei", "share_subBiz": "JIMU_EIVDQFCOGB", "shareObjectId": "JIMU_eIVdqfcO"},
    "AN_MNsDC77M": {"region": "新疆", "interface": "xinjiang", "share_subBiz": "JIMU_AYKCUTERJK", "shareObjectId": "JIMU_AykCUtEr"},

    "AN_MUTZGdaC": {"region": "东北", "interface": "northeast", "share_subBiz": "JIMU_EUWBAWEAEG", "shareObjectId": "JIMU_eUwbaWEa"},

    "AN_JiYEYkvm": {"region": "北京", "interface": "beijing", "share_subBiz": "JIMU_AYUQQVXHEB", "shareObjectId": "JIMU_aYuqqvxH"},
    "AN_KsABBloa": {"region": "福建", "interface": "fujian", "share_subBiz": "JIMU_RFAZQVXUMI", "shareObjectId": "JIMU_RFazQvxu"},

    "AN_cStt133b": {"region": "广东", "interface": "guangdong", "share_subBiz": "JIMU_ZCXFBERCIA", "shareObjectId": "JIMU_Zcxfberc"},
    "AN_9aTdJQPN": {"region": "山东", "interface": "shandong", "share_subBiz": "JIMU_OTAXTENOEB", "shareObjectId": "JIMU_oTaxtenO"},
    "AN_A5rSerYn": {"region": "广西", "interface": "guangxi", "share_subBiz": "JIMU_VZUCFNBOAB", "shareObjectId": "JIMU_vzucfnbO"},

    "AN_iUH3j1lC": {"region": "川渝", "interface": "sichuan", "share_subBiz": "JIMU_FREOGKGTHD", "shareObjectId": "JIMU_fREOgkGT"},

    "AN_OvZbv3mB": {"region": "河南", "interface": "henan", "share_subBiz": "JIMU_AXGGTDEDDO", "shareObjectId": "JIMU_axGGTDEd"},

    "AN_u0rAmUj4": {"region": "江浙", "interface": "zhejiang", "share_subBiz": "JIMU_PMGGWMHZEM", "shareObjectId": "JIMU_pMggWMhz"},
    "AN_9H9DZjsG": {"region": "云贵", "interface": "yunnan", "share_subBiz": "JIMU_WYWRCQAICB", "shareObjectId": "JIMU_wyWrcqaI"},
    "AN_ZRutfXeK": {"region": "西北", "interface": "northwest", "share_subBiz": "JIMU_IYPAJVUYCI", "shareObjectId": "JIMU_iyPaJvuy"},
    "AN_DHvs1D1E": {"region": "安徽", "interface": "anhui", "share_subBiz": "JIMU_RLWVRBAGDO", "shareObjectId": "JIMU_rlWVRBAg"},
    "AN_eqw4t8bF": {"region": "湖南", "interface": "hunan", "share_subBiz": "JIMU_UARQCPGSJC", "shareObjectId": "JIMU_UarQcpGs"},
}


def find_ipaddr():
    url = "https://uutool.cn/ip/"

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        'Accept-Encoding': "gzip, deflate, br, zstd",
        'cache-control': "max-age=0",
        'sec-ch-ua': "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': "\"Windows\"",
        'dnt': "1",
        'upgrade-insecure-requests': "1",
        'sec-fetch-site': "cross-site",
        'sec-fetch-mode': "navigate",
        'sec-fetch-user': "?1",
        'sec-fetch-dest': "document",
        'referer': "https://cn.bing.com/",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        'priority': "u=0, i",
        'Cookie': "userId=cbc519d7299471a15007"
    }

    response = requests.get(url, headers=headers, proxies=proxies)

    # print(response.text)

    ip_addr = re.findall("var ip = (.*?);", response.text)[0]
    ip_addr = ip_addr.strip('\'')
    # print(ip_addr)
    time.sleep(1)

    url = "https://api.ip77.net/ip2/v4/"

    payload = {
        'ip': ip_addr
    }
    # print(payload)
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'Accept-Encoding': "gzip, deflate, br, zstd",
        'sec-ch-ua-platform': "\"Windows\"",
        'sec-ch-ua': "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        'dnt': "1",
        'sec-ch-ua-mobile': "?0",
        'origin': "https://uutool.cn",
        'sec-fetch-site': "cross-site",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://uutool.cn/",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        'priority': "u=1, i"
    }

    response = requests.post(url, data=payload, headers=headers, proxies=proxies)

    print(response.json())


def get_proxy_ip(time_minutes, _region):
    _proxy_ip = None
    _proxy_port = None
    url = f"https://api.douyadaili.com/proxy/?service=GetIp&authkey=0GaLAqirDTVSCJM7PPQE&num=1&lifetime={time_minutes}&region={_region}&format=json&distinct=2&detail=1"

    while _proxy_ip is None or _proxy_port is None:

        res = requests.get(url)

        if res.status_code == 200:
            # print(res.json())
            if res.json()["ret"] == 200:
                if "data" in res.json() and len(res.json()["data"]):

                    if "ip" in res.json()["data"][0] and "port" in res.json()["data"][0]:
                        _proxy_ip = res.json()["data"][0]["ip"]
                        _proxy_port = res.json()["data"][0]["port"]
                        # print(_proxy_ip, _proxy_port)
                        if _proxy_ip and _proxy_port:
                            break
        time.sleep(1)
    return _proxy_ip, _proxy_port


def add_error_ques(_ques_id, _option_index):
    url = "http://118.31.69.17:12345/add_error_ques"

    payload = {
        "ques_id": _ques_id,
        "option_index": _option_index
    }

    headers = {
        'Content-Type': "application/json"
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers)


def find_error_ques(ques_id):
    params = {
        'ques_id': str(ques_id)
    }

    response = requests.get("http://118.31.69.17:12345/find_error_ques", params=params)

    return response.json()["data"]


def delete_ques(ques_index):
    url = f"http://118.31.69.17:12345/delete_ques/{ques_index}"

    response = requests.post(url)


def find_ques(ques_index):
    url = f"http://118.31.69.17:12345/find_ques/{ques_index}"

    response = requests.get(url)

    if response.json()["code"] == 0:
        return None
    else:
        return response.json()["ans_index"]


def add_ques(ques_index, ques, ans_index):
    url = "http://118.31.69.17:12345/add_ques"

    payload = {
        "ques_index": ques_index,
        "ques": ques,
        "ans_index": ans_index
    }

    headers = {
        'Content-Type': "application/json"
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers)


def zhipu_gpt(linkUrl, question_str, ans_list, url_type):
    type_dict = {
        "-1": {"model": "glm-4-air", "content": [{"type": "text", "text": f"{question_str}{ans_list}只需回答字母"}]},
        "1": {"model": "glm-4-plus", "content": [{"type": "image_url", "image_url": {"url": linkUrl}}, {"type": "text", "text": f"{question_str}{ans_list}只需回答字母"}]},
        "2": {"model": "glm-4-air", "content": [{"type": "video_url", "video_url": {"url": linkUrl}}, {"type": "text", "text": f"{question_str}{ans_list}只需回答字母"}]}
    }
    try:
        response = zhipu_client.chat.completions.create(
            model=type_dict[url_type]["model"],  # 填写需要调用的模型名称
            messages=[
                {
                    "role": "user",
                    "content": type_dict[url_type]["content"]
                }
            ],
            temperature=0.3,
            timeout=9
        )
        # print(response.choices[0])
        ai_response = response.choices[0].message.content[0]
        # print(ai_response)
        # print(f"gpt回答：{ai_response}")
        if ai_response in ["A", "B", "C", "D"]:
            index = ans_dict[ai_response]
            # print(response.choices[0].message.content[0])
            return index
        else:
            # 随机返回一个答案
            return random.randint(0, len(ans_list) - 1)
    except:
        print("gpt异常，随机一个答案")
        return random.randint(0, len(ans_list) - 1)


class KS:

    # 'PGID': "33F56DAD-63C3-41FA-A095-DDCC6C346224",
    def __init__(self, _user, _region, _cookie, _user_agent):
        self.question_list = []
        self.examId = None
        self.user = _user
        self.ua = _user_agent
        self.cookie = _cookie
        self.region = _region
        self.headers = {
            'User-Agent': self.ua,
            'Accept': "application/json, text/plain, */*",
            'Content-Type': "application/json",
            'ZYCK': "jimu",
            'X-Requested-With': "XMLHttpRequest",
            'Accept-Language': "en-US,en;q=0.9",
            'Origin': "https://ppg.viviv.com",
            'Cookie': self.cookie
        }

    def query_chance(self, activityToken):
        url = "https://ppg.viviv.com/rest/doodle/activity/answer/online/barrier/query-chance"

        payload = json.dumps({
            "answerActivityToken": activityToken
        })

        response = requests.post(url, data=payload, headers=self.headers, proxies=proxies)
        # print(response.json())
        if response.status_code == 200:
            json_data = response.json()
            if json_data["result"] == 1:
                return json_data["data"]["chance"]
            else:
                return 0
        else:
            return 0

    def answer_question(self, activityToken, questionId, answerOptionId_list, index):
        url = "https://ppg.viviv.com/rest/doodle/activity/answer/online/barrier/answer"

        payload = json.dumps({
            "answerActivityToken": activityToken,
            "examId": self.examId,
            "answerInfo": {
                "questionId": questionId,
                "answerOptionIds": answerOptionId_list
            }
        })
        try:
            response = requests.post(url, data=payload, headers=self.headers, timeout=5, proxies=proxies)
            if response.status_code == 200:
                json_data = response.json()
                # print(json_data)
                if json_data["result"]:
                    correct = json_data["data"]["correct"]
                    if index == 5:
                        allRightTimes = json_data["data"]["allRightTimes"]
                        print(f"【账号{self.user}】共完成次数{allRightTimes}")
                    return correct
                else:
                    return 0
            else:
                return 0
        except:
            return 0

    def start_exam(self, activityToken):
        url = "https://ppg.viviv.com/rest/doodle/activity/answer/online/barrier/begin-answer"
        payload = json.dumps({
            "answerActivityToken": activityToken
        })
        response = requests.post(url, data=payload, headers=self.headers, proxies=proxies)

        if response.status_code == 200:
            json_data = response.json()
            # print(json_data)
            if json_data["result"] == 1:
                self.examId = json_data["data"]["examId"]
                self.question_list = json_data["data"]["examQuestions"]

    def share(self, share_subBiz, shareObjectId):
        # print(_cookie)
        # print(share_subBiz)
        # print(shareObjectId)
        url = "https://api.kuaishouzt.com/rest/zt/share/any"

        param_dict = {}
        params = {}
        cookie_param_list = self.cookie.split(";")
        for param in cookie_param_list:
            if "=" in param:
                key, value = param.split("=")
                param_dict[key.strip()] = value

        params["gid"] = param_dict["egid"]
        params["mod"] = param_dict["mod"]
        params["appver"] = param_dict["appver"]
        params["appver"] = param_dict["appver"]
        params["language"] = "zh-cn"
        params["sys"] = param_dict["sys"]
        params["mcc"] = "46003"
        params["did_tag"] = "0"
        params["countryCode"] = "cn"
        params["net"] = param_dict["net"]
        if "socName" in param_dict:
            params["socName"] = param_dict["socName"]
        params["kpf"] = param_dict["kpf"]
        params["ver"] = param_dict["ver"]
        params["c"] = param_dict["c"]
        params["oDid"] = param_dict["oDid"]
        if "android_os" in param_dict:
            params["android_os"] = param_dict["android_os"]
        params["os"] = "android" if "ANDROID" in param_dict["kpf"] else "ios"
        if "boardPlatform" in param_dict:
            params["boardPlatform"] = param_dict["boardPlatform"]
        params["ftt"] = param_dict["ftt"]
        params["kpn"] = param_dict["kpn"]
        params["subBiz"] = str(share_subBiz)
        if "androidApiLevel" in param_dict:
            params["androidApiLevel"] = param_dict["androidApiLevel"]
        if "abi" in param_dict:
            params["abi"] = param_dict["abi"]
        if "device_abi" in param_dict:
            params["device_abi"] = param_dict["device_abi"]
        params["userId"] = param_dict["userId"]
        if params["os"] == "android":
            params["memoryTotalSize"] = "5634"
        params["rdid"] = param_dict["rdid"]
        params["did"] = param_dict["did"]
        ks_api_st = param_dict["kuaishou.api_st"]
        if "token" in param_dict:
            ks_token = param_dict["token"]
        _kpf = param_dict["kpf"]

        payload = {
            'kpf': "_kpf",
            'subBiz': share_subBiz,
            'kpn': params["kpn"],
            'shareResourceType': "",
            'extTransientParams': "{\"ztShareSDKExtParams\":\"{\\\"sharePanelId\\\":\\\"998790857923\\\"}\"}",
            'extRecoParams': "{}",
            'shareChannelId': "COPY_LINK",
            'shareChannel': "copyLink",
            'sdkVersion': "1.14.0.4",
            'theme': "light",
            'kuaishou.api_st': ks_api_st,
            'shareObjectId': shareObjectId,
            'extInnerSdkParams': "{}",
            'extTokenStoreParams': "{\"JIMU_PARAMS\":\"\",\"JIMU_PARAMS_ENCODED\":\"\"}",
        }

        headers = {
            'User-Agent': self.ua,
            'Accept-Encoding': "gzip",
            'Content-Type': "application/x-www-form-urlencoded",
            'Accept-Language': "zh-cn",
            'X-REQUESTID': str(int(time.time() * 1000)),
            'Cookie': f"__NSWJ=null; kuaishou.api_st={ks_api_st};"
        }

        response = requests.post(url, params=params, data=payload, headers=headers, proxies=proxies)

        # print(response.text)

        json_data = response.json()
        if json_data["result"]:
            print("分享成功")

    def exec(self, account_index):

        # print(self.user)
        time.sleep(random.uniform(0, 3))
        print(f"开始账号{self.user}")
        activity_token_list = list(activity_token_dict.keys())
        activity_token_list = random.sample(activity_token_list, len(activity_token_list))
        for activity_token in activity_token_list:
            cur_region = activity_token_dict[activity_token]["region"]
            cur_interface = activity_token_dict[activity_token]["interface"]
            if cur_interface == self.region:
                for i in range(10):
                    timeStamp = int(time.time() * 1000)
                    share_subBiz = activity_token_dict[activity_token]["share_subBiz"]
                    shareObjectId = activity_token_dict[activity_token]["shareObjectId"]
                    _temp = re.findall("JIMU_(.*?)$", shareObjectId)[0]

                    self.headers["Jimu-Token"] = _temp
                    self.headers["ResourceTag"] = _temp
                    self.headers[
                        "referer"] = f"https://ppg.viviv.com/doodle/{_temp}.html?fid={fid}&cc=share_im&shareMode=APP&followRefer=151&originShareId={shareId}&shareMethod=CARD&kpn=KUAISHOU&subBiz={share_subBiz}&shareId={shareId}&shareObjectId={shareObjectId}&shareUrlOpened=0&timestamp={timeStamp}&hyId=jimu&bizId=jimu_{_temp}&noBackNavi=true&uni_src=share&layoutType=4"

                    question_list = []
                    for i in range(2):
                        self.share(share_subBiz, shareObjectId)
                        time.sleep(random.uniform(2, 3))
                    count = self.query_chance(activity_token)
                    if count == 0:
                        print(f"【账号{self.user}】分享不增加次数了，结束答题")
                        return
                    for i in range(random.randint(7, 11)):
                        self.share(share_subBiz, shareObjectId)
                        time.sleep(random.uniform(2, 3))
                    count = self.query_chance(activity_token)
                    print(f"【账号{self.user}】【{cur_region}地区】 答题剩余次数：{count}")
                    _exec_count = min(random.randint(7, 11), count)
                    print(f"本次答题次数: {_exec_count}")

                    while _exec_count > 0:
                        self.start_exam(activity_token)

                        if len(self.question_list):
                            for index, item in enumerate(self.question_list, start=1):
                                print(f"================== 第 {index} 道题 ======================= ")
                                ques_id = item["id"]
                                question = item["content"]["text"]

                                linkUrl = ""
                                resources = item["content"]["resources"]
                                _type = -1
                                if len(resources):
                                    if "linkUrl" in item["content"]["resources"][0]:
                                        _type = item["content"]["resources"][0]["type"]
                                        linkUrl = item["content"]["resources"][0]["linkUrl"]

                                ai_answer_list = []
                                database_answer_list = []
                                for row in item["options"]:
                                    ai_answer_list.append(row["text"].strip("'").replace(" ", ""))
                                    database_answer_list.append(row["text"][1:].strip(".").strip())
                                # print(f"【账号{self.user}】[第{index}道题]id:{ques_id}")
                                print(f"【账号{self.user}】[第{index}道题]问题：{question}")
                                print(f"【账号{self.user}】[第{index}道题]答案：{ai_answer_list}")
                                # print(linkUrl)
                                ans_option_list = []
                                exist_ques = False

                                database_ans_index = find_ques(ques_id)  # 从零开始

                                if database_ans_index is None:
                                    print(f"【账号{self.user}】数据库不存在该题目,查询gpt")
                                    ans_index = zhipu_gpt(linkUrl, question, ai_answer_list, str(_type))

                                    error_option_index_list = find_error_ques(ques_id)
                                    # print(f"gpt回答: {ans_index}")

                                    if ans_index in error_option_index_list:
                                        # print("错误数据库存在该选项")
                                        ans_index = 0
                                        for ans_index in range(len(ai_answer_list)):
                                            if ans_index not in error_option_index_list:
                                                break
                                    print(f"【账号{self.user}】最后选项: {ans_index}")

                                else:
                                    print(f"【账号{self.user}】数据库存在题目")
                                    exist_ques = True
                                    ans_index = database_ans_index
                                time.sleep(1)
                                ans_option_list.append(ans_index + 1)
                                ans_status = self.answer_question(activity_token, ques_id, ans_option_list, index)
                                if ans_status:
                                    print(f"【账号{self.user}】回答正确")
                                    if exist_ques is False:
                                        add_ques(ques_id, question, ans_index)
                                else:
                                    add_error_ques(ques_id, ans_index)
                                    time.sleep(0.5)
                                    print(f"【账号{self.user}】回答错误，结束答题")

                                    break
                                if index != 5:
                                    time.sleep(random.uniform(2, 2))
                                else:
                                    print(f"【账号{self.user}】全答对了✌️")
                        _exec_count -= 1
                        time.sleep(random.uniform(5, 10))

                    time.sleep(random.uniform(15, 20))


def create_and_execute_objects(values):
    objects = [KS(_key, _value["region"], _value["cookie"], _value["ua"]) for _key, _value in values.items()]
    results = []

    with ThreadPoolExecutor(max_workers=4) as executor:
        # 创建一个字典来保存Future对象和对应的index
        future_to_index = {executor.submit(obj.exec, _index): _index for _index, obj in enumerate(objects, start=1)}
        for future in as_completed(future_to_index):
            _index = future_to_index[future]
            result = future.result()
            results.append((_index, result))
    return results


if __name__ == "__main__":

    uname_str = subprocess.run(['uname', '-a'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout.strip()
    print(uname_str)
    if did != hashlib.md5(("you" + uname_str + "my" + uname_str).encode()).hexdigest():
        exit(0)

    region_str = sys.argv[1].strip()
    cookies_str = os.getenv(region_str)

    cookies_list = cookies_str.split("&")

    print(f"共{len(cookies_list)}个")

    zhipu_client = ZhipuAI(api_key=ai_key)  # 填写您自己的APIKey

    if region_str == "none":
        proxies = None
    else:
        proxy_ip, proxy_port = get_proxy_ip(int(proxy_time), region_str)
        proxies = {
            'http': f'http://{proxy_ip}:{proxy_port}',  # 这里替换为你的HTTP代理服务器地址
            'https': f'http://{proxy_ip}:{proxy_port}',  # 这里替换为你的HTTPS代理服务器地址
        }
    find_ipaddr()
    account_json_data = {}
    for cookie in cookies_list:
        region, _cookie, _user_agent = cookie.split("#")
        _userid = re.findall("userId=(.*?);", _cookie)[0]

        account_json_data[_userid] = {"region": region, "cookie": _cookie, "ua": _user_agent}

    results = create_and_execute_objects(account_json_data)
