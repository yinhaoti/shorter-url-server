# Ubuntu 16.04
# 配置基础容器 python-dev-base
FROM python:3.5
MAINTAINER yinhaotian hautienyin@qq.com

# 更新Debian源
RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak && \
echo "deb http://mirrors.163.com/debian/ jessie main non-free contrib" >/etc/apt/sources.list && \
echo "deb http://mirrors.163.com/debian/ jessie-proposed-updates main non-free contrib" >>/etc/apt/sources.list && \
echo "deb-src http://mirrors.163.com/debian/ jessie main non-free contrib" >>/etc/apt/sources.list && \
echo "deb-src http://mirrors.163.com/debian/ jessie-proposed-updates main non-free contrib" >>/etc/apt/sources.list

# 安装自定义package
RUN apt-get update -y && apt-get install -y nano git curl
    # vim

# initDocker 是文件 initDocker/ 是文件夹
ADD ./requirements.txt /yinhaotian/shorter-url-server/
WORKDIR /yinhaotian/shorter-url-server/

RUN pip install -r /yinhaotian/shorter-url-server/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

CMD "echo" "shorter-url-server docker build sucess!"

# docker build -t yinhaoti/shorter-url-server .
# 即删即用
# docker run --rm -it  -p 80:1888 -v $(pwd):/yinhaotian/shorter-url-server/ --name shorturl yinhaoti/shorter-url-server /bin/bash
# 自动重启/后台运行
# docker run -d --restart=always -v $(pwd):/yinhaotian/wtf_chat_robot/ --name chatbot yinhaoti/chatbot /bin/bash -c 'python3 -u ./WSGI_Debian_wechat.py'
# 查看输出日志
# docker logs -f chatbot

