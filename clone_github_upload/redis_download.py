import logging
import os

import redis
import requests
from tqdm import tqdm

from requests_toolbelt import MultipartEncoder
import glob

logging.basicConfig(filename='log.log', filemode='a', format='[%(levelname)s]-[%(asctime)s]-%(filename)s-%(message)s',
                    level=logging.INFO)


class Redis(object):
    def __init__(self, host, port, password, db):
        try:
            self.redis = redis.Redis(host=host, port=port, password=password, db=db, decode_responses=True)
        except Exception as e:
            logging.error('网络错误数据库连接失败,失败原因：%s' % e)

    def push(self, key, value):
        try:
            self.redis.lpush(key, value)
        except Exception as e:
            logging.error('向%s队列中写入%s失败，失败原因：%s' % (key, value, e))

    def pop(self, key):
        try:
            return self.redis.rpop(key)

        except Exception as e:
            logging.error('取出队列失败，失败原因：%s' % e)

    def len(self, key):
        try:
            return self.redis.llen(key)
        except Exception as e:
            logging.error('获取队列长度失败，失败原因：%s' % e)


def download(url, dir, filename):
    if not os.path.exists(dir):
        os.makedirs(dir)
    try:
        r = requests.get(url, stream=True)
        total_size = int(r.headers.get('content-length', 0))
        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, colour='#32CD32', position=0)
        progress_bar.set_description('%s文件下载中，当前进度：' % filename)
    except Exception as e:
        logging.error('请求下载地址失败，失败原因：%s' % e)
    if r.status_code == 200:
        try:
            with open(dir + '/' + filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    progress_bar.update(len(chunk))
                    f.write(chunk)
                progress_bar.close()
            logging.info('下载文件%s成功' % filename)
        except Exception as e:
            logging.error('下载文件失败，失败原因：%s' % e)
    else:
        logging.error('网络请求失败：%s' % r.text)


def clone(url, dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
