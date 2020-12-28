import re
from urllib import request


site = 'https://coinmarketcap.com/'
all_coins = open("all_coins.txt", "w", encoding="utf-8")

def get_html(site):
    print('Делаем запрос к ' + site)
    try:
        resp = request.urlopen(site)
        print('Запрос был удачным!')
    except:
        print('Отсутствует соединение с интернетом!')
        exit()
    html = resp.read().decode('utf-8')
    return html

pages = 42

to_write = "["

for page in range(1,pages+1):
    html = get_html(site+str(page)+'/')
    names = re.findall('''"name":"[^"]+''',html)
    for i in range(1,len(names)):
        to_write += names[i][7:].replace("\\u0026","and") + '",'

to_write += "];"


start = False


all_coins.write(to_write)

print("Операция завершена!")
all_coins.close()
