from requests_html import HTMLSession
import datetime
import time
import locale
import telegram


bot = telegram.Bot(token='') # Inserir token
session = HTMLSession()
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def getCasasBahia():
    try:
        r = session.get("https://pdp-api.casasbahia.com.br/api/v2/sku/55026525/price/source/CB?utm_medium=Cpc")
        dados = r.json()
    except:
        return "Link inválido!"

    try:
        preco = dados['paymentMethodDiscount']['sellPriceWithDiscount']
        return preco
    except:
        return "Produto indisponível!"


def getPontoFrio():
    try:
        r = session.get("https://pdp-api.pontofrio.com.br/api/v2/sku/55026525/price/source/PF?utm_medium=cpc")
        dados = r.json()
    except:
        return "Link inválido!"

    try:
        preco = dados['paymentMethodDiscount']['sellPriceWithDiscount']
        return preco
    except:
        return "Produto indisponível!"


def getFastShop():
    try:
        r = session.get("https://price-management.fastshop.com.br/api/v1/price-promotion/price?store=fastshop&channel=webapp&skus=LGOLED55C1PSA_PRD")
        dados = r.json()
    except:
        return "Link inválido!"

    try:
        preco = dados['result'][0]['products'][0]['skus'][0]['promotions'][0]['value']
        return preco
    except:
        return "Produto indisponível!"


def getKabum():
    try:
        r = session.get("https://www.kabum.com.br/produto/158925/smart-tv-lg-55-4k-oled55c1-120hz-g-sync-freesync-4x-hdmi-2-1-intelig-ncia-artificial-thinq-google-alexa-oled55c1psa")
    except:
        return "Link inválido!"

    try:
        preco = r.html.xpath("//*[@id=\"blocoValores\"]/div[2]/div/h4", first=True).text
        preco = locale.atof(preco.split()[-1])
        return preco
    except:
        return "Produto indisponível!"


def getMagazineLuiza():
    try:
        r = session.get("https://www.magazineluiza.com.br/smart-tv-55-4k-uhd-oled-lg-oled55c1psa-120hz-wi-fi-e-bluetooth-alexa-4-hdmi-3-usb/p/228862200/et/tves/?&force=2&seller_id=magazineluiza")
    except:
        return "Link inválido!"

    try:
        preco = r.html.xpath("/html/body/div[3]/div[5]/div[1]/div[3]/div[2]/div[4]/div/div[2]/div/span[2]", first=True).text
        preco = locale.atof(preco.split()[-1])
        return preco
    except:
        return "Produto indisponível!"


def getNagem():
    try:
        r = session.get("https://www.nagem.com.br/produto/detalhes/537918/Smart+TV+LG+55%22+55C1+4K+OLED+Inteligencia+Artificial+ThinQ+AI+Google+Assistente+Alexa+Built+In")
    except:
        return "Link inválido!"

    try:
        preco = r.html.xpath("/html/body/div[2]/div[2]/div/section/div/div[2]/section[2]/div[2]/div[2]/span[2]", first=True).text
        preco = locale.atof(preco.split()[-1])
        return preco
    except:
        return "Produto indisponível!"


# def getAmericanas():
#     try:
#         r = session.get("https://www.americanas.com.br/produto/3280458357?opn=YSMESP&sellerid=02")
#     except:
#         return "Link inválido!"
#
#     try:
#         preco = r.html.xpath("//*[@id='rsyswpsdk']/div/main/div[2]/div[2]/div[1]/div[2]/div/text()[2]", first=True).text
#         preco = locale.atof(preco.split()[-1])
#         return preco
#     except:
#         return "Produto indisponível!"


def getFormattedPrice(preco, loja):
    store_price = f"{datetime.datetime.now().replace(microsecond=0)} - {loja}: {preco}"
    print(store_price)
    if preco <= 5100:
        print("########################### !!!!!!!!ALERTA!!!!!!!! ###########################")
        try:
            if canSendMessage == True:
                sendMessage(store_price)
                messageSent = True
        except:
            print("A mensagem não pôde ser enviada!")


def sendMessage(message):
    bot.send_message(text=message, chat_id=) # Inserir ID do chat

canSendMessage = True
messageSent = False
timeSent = []

while True:
    getFormattedPrice(getCasasBahia(), "Casas Bahia")
    getFormattedPrice(getPontoFrio(), "Ponto Frio")
    getFormattedPrice(getFastShop(), "Fast Shop")
    getFormattedPrice(getKabum(), "Kabum")
    getFormattedPrice(getMagazineLuiza(), "Magazine Luiza")
    getFormattedPrice(getNagem(), "Nagem")
    # getFormattedPrice(getAmericanas(), "Americanas")

    if messageSent:
        timeSent.append(datetime.datetime.now())
        messageSent = False
        canSendMessage = False

    print("--------------------------------------------------")
    time.sleep(30)

    if not canSendMessage:
        if (datetime.datetime.now() - timeSent[-1]).total_seconds() > 30*60:
            canSendMessage = True

