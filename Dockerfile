FROM python:3.10-slim-bullseye

RUN apt update && apt install -y git make gcc nano sudo  build-essential curl wget libpcap-dev

## MASSCAN INSTALLATION
WORKDIR /tmp/masscan
RUN git clone https://github.com/robertdavidgraham/masscan.git
RUN cd masscan && make install

WORKDIR /usr/
COPY mc/ /usr/app/
RUN sudo pip3 install -r /usr/app/requirements.txt

CMD ["sudo", "python3", "/usr/app/main.py"]
