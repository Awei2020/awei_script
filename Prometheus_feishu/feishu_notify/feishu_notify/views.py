# 设置webhook路由
# Path: feishu_notify\feishu_notify\views.py
import datetime
import json
import os

import requests
from django.http import HttpResponse

feishu_webhook_url = os.environ.get('FEISHU_WEBHOOK_URL')
print(feishu_webhook_url)
headers = {"Content-Type": "application/json;charset=utf-8"}


def webhook(request):
    if request.method == 'POST':
        date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = json.loads(request.body.decode('utf-8'))["alerts"]
        title = data[0]["labels"]["instance"] + "发生异常"
        msg = "异常信息：" + data[0]["labels"]["alertname"] + "\n" + "异常级别：" + data[0]["labels"][
            "severity"] + "\n" + "异常描述：" + data[0]["annotations"]["description"] + "\n" + "异常时间：" + date_time
        print(title, msg)
        msg_body = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": title,
                        "content": [
                            [{
                                "tag": "text",
                                "text": msg
                            }
                            ]
                        ]
                    }
                }
            }
        }
        requests.post(url=feishu_webhook_url, headers=headers, data=json.dumps(msg_body))
        return HttpResponse(status=200, content=json.dumps({'msg': 'ok'}))
    else:
        return HttpResponse(status=403)
