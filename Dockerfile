FROM python:3.10-slim-bullseye
LABEL maintainer="13508023081@163.com"
LABEL description="[blog-backend] python:3.10-slim-bullseye"
ADD . /root
WORKDIR /root
RUN chmod 765 ./start.sh

RUN sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN sed -i s@/security.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list

ENV TZ=Asia/Shanghai
ENV LANG=C.UTF-8
ENV dpip3="/usr/local/bin/python -m pip install"
ENV by_aliyun="-i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com"

RUN apt-get update \
    && apt-get install -y tzdata vim procps \
    && apt-get clean \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone

RUN $dpip3 --upgrade pip $by_aliyun
RUN $dpip3 -r requirements.txt $by_aliyun

EXPOSE 5856
COPY . .
CMD ["supervisord", "-c", "deploy/supervisord.conf", "-n"]