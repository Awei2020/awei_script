from redis_download import download, Redis
import re
import concurrent.futures

if __name__ == '__main__':
    r = Redis('118.31.8.73', 26379, 'zzhaoAI888', 0)
    max_threads = 5
    with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
        while r.len('apk') > 0:
            url = r.pop('apk')
            # 提交任务给线程池，每个任务都会在可用线程上并行执行
            executor.submit(download, url, 'E:/test', re.search(r"[^/]+?\.apk", url).group())
