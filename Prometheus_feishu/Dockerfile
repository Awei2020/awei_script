FROM python:3.9
COPY ./feishu_notify /feishu_notify
WORKDIR /feishu_notify
RUN pip install django requests -i https://pypi.tuna.tsinghua.edu.cn/simple
CMD python manage.py runserver 0.0.0.0:8000
