# 此脚本判断当前目录下是否有指定文件，如果有进行拷贝，如果没有则不进行拷贝
# 用于自动化打包时，拷贝指定文件到指定目录
# 用法：python auto_package.py semi/whole 来区分是半私有还是全私有打包
import sys
import os
import shutil
import argparse
import subprocess
import time
from colorama import Fore, Back, Style

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--type', type=str, default='')
parser.add_argument('--path', type=str, default='')
args = parser.parse_args()
path = args.path
if args.type == "" or args.path == "":
    print("参数不完整")
    sys.exit(1)
copy_file_dict = {
    "package/task_assistant": path + "/msca/besrv/app/task_assistant/",
    "package/message": path + "/msca/besrv/app/message/",
    "package/user": path + "/msca/besrv/app/user/",
    "package/platform": path + "/msca/besrv/app/platform/",
    "package/rc": path + "/msca/besrv/app/rc/",
    "package/snowflake": path + "/msca/besrv/app/snowflake/",
    "package/msca_update.sql": path + "/msca/mysql/update_sql/",
    "package/detector": path + "/msca/detector/",
    "package/swagger.json": path + "/msca/nginx/html/openapi/v3/",
    "package/scanner-all.jar": path + "/msca/scae/app/",
    "package/LIBLOOM.jar": path + "/msca/scae/app/",
    "package/core-all.jar": path + "/codesimilarity/app/",
    "package/server.jar": path + "/msca/admin/",
    "package/html.zip": path + "/msca/nginx/html/html/",
    "package/console.zip": path + "/msca/nginx/html/v3-html/",
    "package/docs.zip": path + "/msca/nginx/html/docs/",
    "package/admin.zip": path + "/msca/nginx/html/admin-html/",
}


def copy_file(src_file, dst_file):
    if os.path.exists(src_file):
        if not os.path.exists(dst_file):
            os.makedirs(dst_file)
        print(Fore.GREEN + "拷贝" + Style.RESET_ALL + "    %s -> %s" % (src_file, dst_file))
        shutil.copy2(src_file, dst_file)
        # 判断文件不是jar包，给文件添加可执行权限
        if file_end not in ["jar", "sql", "json"]:
            subprocess.run(["chmod", "+x", value + src_file.split('/')[-1]])
            print(Fore.GREEN + "给文件添加可执行权限" + Style.RESET_ALL + "     %s" % (value + src_file.split('/')[-1]))
        time.sleep(1)


for key, value in copy_file_dict.items():
    file_end = key.split('/')[-1].split('.')[-1]
    if key == "package/detector" and args.type != "whole":
        continue
    elif file_end in ["zip"] :
        if os.path.exists(key):
            if not os.path.exists(value):
                os.makedirs(value)
            print(Fore.GREEN + "强制解压" + Style.RESET_ALL + "     %s -> %s" % (key, value))
            subprocess.run(["unzip", "-o", key, "-d", value])
            time.sleep(1)
    else:
        copy_file(key, value)

# 实现对zip包在Linux上强制解压缩功能
