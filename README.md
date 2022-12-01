# Как использовать
![](https://s1.hostingkartinok.com/uploads/images/2022/11/4cb7437d6ce1cb90934917052108f583.jpg)

# Как разворачивать
1. В ./conf.py указать список участников (уже указан, но есть возможность добавить/убрать при необходимости)
2. В ./conf.py указать токен бота
3. pip3 install -U pip && pip3 install -r requirements.txt && python3 bot.py  
4. Написать боту команду /zapuskator

# Как разворачивать в Docker
1. docker build -t santa_bot .
2. docker run -d -v /srv/santa_db:/code/db --name santa_bot -e TOKEN="5893178612:AAGhJeMhLXm3wMWWA7zNRLcE_DbSqeyuGoc" --restart always santa_bot 
