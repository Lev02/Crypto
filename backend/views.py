from django.shortcuts import render
from django.http import HttpResponse
from .forms import CoinNameForm, LanguageEnForm, LanguageRuForm
import datetime
import urllib
import re
##
def get_html(site):
    print('Making request to ' + site)
    try:
        resp = urllib.request.urlopen(site)
        print('Request was succesful!')
        html = resp.read().decode('utf-8')
        return html
    except:
        return None

#divide number into list of triple digits so that it is easier to read
def divide_number(number):
    output = ""
    n = len(number)
    is_float = False
    for i in range(n):
        if number[i] == '.':
            is_float = True
            break
    if is_float:
        n = number.index(".")
        output += number[n:n+4]
        output = output[::-1]
    for i in range(n):
        output += number[n-i-1]
        if (i+1) % 3 == 0:
            output += " "
    return output[::-1]

def get_coin(request):
    if request.method == "POST":
        coin_name = request.POST.get("coin_name")
        languageRU = request.POST.get("languageRU")

        print(languageRU)

        langEN = False
        langRU = False

        if languageRU == "on":
            langRU = True
        else:
            langEN = True

        site_url = 'https://coinmarketcap.com/currencies/' + coin_name.lower().replace(" ","-") + '/'

        html = get_html(site_url)
        if html != None:
            if re.search("<h2>Sorry, we couldn&#x27;t find your page</h2>",html) == None:
                price = re.findall('''"price":\d+.?\d*''',html)[-1][8:]
                print("price: ", price)

                position = re.findall('''Rank #?\d+''',html)[-1][5:]
                position.replace("#","")
                print("position: ", position)

                change24h = re.findall('''"percent_change_24h":-?\d+.?\d*''',html)[-1][21:]
                print("change24h: ", change24h)

                marketcap = re.findall('''"market_cap":\d+.?\d*''',html)[-1][13:]
                marketcap = divide_number(marketcap)
                print("marketcap: ", marketcap)

                if marketcap == '0,':
                    marketcap = '?'

                exception = ""
                date = datetime.datetime.now()
                context = {"coincost": price, "coin_name": coin_name, "date": date, "change24h":change24h, "marketcap":marketcap, "position":position,"languageRU":LanguageRuForm(), "languageEN":LanguageEnForm(), "langEN":langEN, "langRU":langRU}
                print("context: ", context)
                return render(request, "printcoin.html", context)
            else:
                exception = 'Error, coin "{0}" wasn\'t found!'.format(coin_name)
                context={"coin_name": CoinNameForm(), "exc":exception,"languageRU":LanguageRuForm(), "languageEN":LanguageEnForm()}
                print("context: ", context)
                return render(request, "index.html", context)
        else:
            exception = "Error, no internet connection!"
            context={"coin_name": CoinNameForm(), "exc":exception, "languageRU":LanguageRuForm(), "languageEN":LanguageEnForm()}
            print("context: ", context)
            return render(request, "index.html", context)

    else:
        context={"coin_name": CoinNameForm(), "languageRU":LanguageRuForm(), "languageEN":LanguageEnForm()}
        print("context: ", context)
        return render(request, "index.html", context)
