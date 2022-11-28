FROM python:3.9.15
COPY ./ /code
WORKDIR /code
RUN apt update && apt install sqlite3
RUN mkdir db && pip3 install -U pip && pip3 install -r requirements.txt  
#&& unzip /srv/sqlite.zip -d /srv && mv /srv/sqlite* /usr/bin/ 
CMD python3 bot.py
