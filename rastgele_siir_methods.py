from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import urllib.request
import logging
from telegram.ext import Updater, CommandHandler
from time import gmtime, strftime, sleep
import telebot
import pymongo
from telegram.error import Unauthorized
from random import randint
import enum_file
from telegram.error import (TelegramError, Unauthorized, BadRequest, 
                            TimedOut, ChatMigrated, NetworkError)


myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient['sairler']

class Sair:
    def __init__(self, name):
        self.name = name

#Ali Lidar
ali_lidar_column = mydb['ali-lidar']

#Hasan Hüseyin Korkmazgil
hasan_huseyin_korkmazgil_column = mydb['hasan-huseyin-korkmazgil']

#Cemal Süreya
cemal_sureya_column = mydb['cemal-sureya']

#Didem Madak
didem_madak_column = mydb['didem-madak']

#Turgut Uyar
turgut_uyar_column = mydb['turgut-uyar']

#Özdemir Asaf
ozdemir_asaf_column = mydb['ozdemir-asaf']

#Ah Muhsin Ünlü
ah_muhsin_unlu_column = mydb['ah-muhsin-unlu']

#Atilla İlhan
attila_ilhan_column = mydb['attila-ilhan']

#Nazım Hikmet Ran
nazim_hikmet_ran_column = mydb['nazim-hikmet-ran']

#Edip Cansever
edip_cansever_column = mydb['edip-cansever']

#Ece Ayhan
ece_ayhan_column = mydb['ece-ayhan']

#Orhan Veli Kanık
orhan_veli_kanik_column = mydb['orhan-veli-kanik']

#Cahit Sıtkı Tarancı
cahit_sitki_taranci_column = mydb['cahit-sitki-taranci']

#Yilmaz Güney
yilmaz_guney_column = mydb['yilmaz-guney']

#Yilmaz Erdogan
yilmaz_erdogan_column = mydb['yilmaz-erdogan']

#Tevfik Fikret
tevfik_fikret_column = mydb['tevfik-fikret']

api_key = "<Telegram bot api key>"

bot = telebot.TeleBot(api_key)

#check for new messages --> polling
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

@bot.message_handler(commands = ["start"])
def start(message):
    #databaseye baglan
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    mydb = myclient["sairler"]

    #tableye geçis yap
    mycol = mydb['telegram-users']

    chat_id = message.chat.id

    data = mycol.find_one({"chatId": chat_id})
    if(data == None):
        mycol.insert_one({"chatId": chat_id})
        print("ilk defa giris yapti, databaseye kaydedildi")
    else:
        print("zaten databasede, kaydedilmedi")
    bot.send_message(chat_id,"Hosgeldin.\n/siir: Rastgele bir şairden şiir almak bu methodu kullan\n/sair: Belli bir şairden rastgele şiir almak için bu methodu kullan.\n/sairler: Varolan sairleri bu komut ile görebilirsin.")

@bot.message_handler(commands = ['siir'])
def getPoem(message):
    try:
        myArray = getPoet()
        myColumn = myArray[0]
        myPoemCount = myArray[1]
        myPoet = myArray[2]
        randSiir = randint(1,myPoemCount)
        print("Number: ",randSiir)
        print("Column: ", myColumn)
        print("\n\n\n")
        data = myColumn.find_one({"Number": str(randSiir)})
        string = "Şair: "+ myPoet + "\nBaşlık: " + str(data['Title']) + "\nŞiir: " + str(data['Poem'])
        bot.send_message(message.chat.id, string)
    except BadRequest as b:
        bot.send_message("Error occured: ", b)
    
@bot.message_handler(commands = ['sairler'])
def getPoets(message):
    bot.send_message(message.chat.id,"1: Ali Lidar\n2: Hasan Hüseyin Korkmazgil\n3: Cemal Süreya\n4: Didem Madak\n5: Turgut Uyar\n6: Özdemir Asaf\n7: Ah Muhsin Ünlü\n8: Attila İlhan\n9: Nazım Hikmet Ran\n10: Edip Cansever\n11: Ece Ayhan\n12: Orhan Veli\n13: Cahit Sıtkı Tarancı\n14: Yılmaz Güney\n15: Yılmaz Erdoğan\n16: Tevfik Fikret")
    
@bot.message_handler(commands = ["sair"])
def getOnePoetsPoem(message):
    msg = bot.reply_to(message, "Hangi şairden rastgele şiir almak istersin?")
    bot.register_next_step_handler(msg, getPoemOfPoet)

def getPoemOfPoet(message):
    try:
        myArray = getOnePoetsPoemMethod(message.text.lower())
        myColumn = myArray[0]
        myPoemCount = myArray[1]
        myPoet = myArray[2]
        randSiir = randint(1,myPoemCount)
        print("Number: ",randSiir)
        print("Column: ", myColumn)
        print("\n\n\n")
        data = myColumn.find_one({"Number": str(randSiir)})
        string = "Poet is: "+ myPoet + "\nTitle is: " + str(data['Title']) + "\nPoem is: " + str(data['Poem'])
        bot.send_message(message.chat.id, string)  
    except Exception as e:
        bot.reply_to(message, 'Siir getirilemedi. Belkide şair adını yanlış girdin? /help komutu ile varolan şairleri görebilirsin.')


def getPoet():
    whichPoet = randint(0,15)
    if whichPoet == 0:
        myColumn = ali_lidar_column
        siirSayisi = enum_file.SairlerinSiirSayisi.ali_lidar
        poet = "Ali Lidar"
    elif whichPoet == 1:
        myColumn = hasan_huseyin_korkmazgil_column
        siirSayisi = enum_file.SairlerinSiirSayisi.hasan_huseyin_korkmazgil
        poet = "Hasan Hüseyin Korkmazgil"
    elif whichPoet == 2:
        myColumn = cemal_sureya_column
        siirSayisi = enum_file.SairlerinSiirSayisi.cemal_sureya
        poet = "Cemal Süreya"
    elif whichPoet == 3:
        myColumn = didem_madak_column
        siirSayisi = enum_file.SairlerinSiirSayisi.didem_madak
        poet = "Didem Madak"
    elif whichPoet == 4:
        myColumn = turgut_uyar_column
        siirSayisi = enum_file.SairlerinSiirSayisi.turgut_uyar
        poet = "Turgut Uyar"
    elif whichPoet == 5:
        myColumn = ozdemir_asaf_column
        siirSayisi = enum_file.SairlerinSiirSayisi.ozdemir_asaf
        poet = "Özdemir Asaf"
    elif whichPoet == 6:
        myColumn = ah_muhsin_unlu_column
        siirSayisi = enum_file.SairlerinSiirSayisi.ah_muhsin_unlu
        poet = "Ah Muhsin Ünlü"
    elif whichPoet == 7:
        myColumn = attila_ilhan_column
        siirSayisi = enum_file.SairlerinSiirSayisi.attila_ilhan
        poet = "Attila İlhan"
    elif whichPoet == 8:
        myColumn = nazim_hikmet_ran_column
        siirSayisi = enum_file.SairlerinSiirSayisi.nazim_hikmet_ran
        poet = "Nazım Hikmet Ran"
    elif whichPoet == 9:
        myColumn = edip_cansever_column
        siirSayisi = enum_file.SairlerinSiirSayisi.edip_cansever
        poet = "Edip Cansever"
    elif whichPoet == 10:
        myColumn = ece_ayhan_column
        siirSayisi = enum_file.SairlerinSiirSayisi.ece_ayhan
        poet = "Ece Ayhan"
    elif whichPoet == 11:
        myColumn = orhan_veli_kanik_column
        siirSayisi = enum_file.SairlerinSiirSayisi.orhan_veli
        poet = "Orhan Veli"
    elif whichPoet == 12:
        myColumn = cahit_sitki_taranci_column
        siirSayisi = enum_file.SairlerinSiirSayisi.cahit_sitki
        poet = "Cahit Sıtkı Tarancı"
    elif whichPoet == 13:
        myColumn = yilmaz_erdogan_column
        siirSayisi = enum_file.SairlerinSiirSayisi.yilmaz_erdogan
        poet = "Yılmaz Erdoğan"
    elif whichPoet == 14:
        myColumn = yilmaz_erdogan_column
        siirSayisi = enum_file.SairlerinSiirSayisi.yilmaz_guney
        poet = "Yılmaz Güney"
    elif whichPoet == 15:
        myColumn = tevfik_fikret_column
        siirSayisi = enum_file.SairlerinSiirSayisi.tevfik_fikret
        poet = "Tevfik Fikret"
    return [myColumn,siirSayisi,poet]

def getOnePoetsPoemMethod(poet):
    if poet == "Ali Lidar".lower():
        myColumn = ali_lidar_column
        siirSayisi = enum_file.SairlerinSiirSayisi.ali_lidar
    elif poet == "Hasan Hüseyin Korkmazgil".lower():
        myColumn = hasan_huseyin_korkmazgil_column
        siirSayisi = enum_file.SairlerinSiirSayisi.hasan_huseyin_korkmazgil
    elif poet == "Cemal Süreya".lower():
        myColumn = cemal_sureya_column
        siirSayisi = enum_file.SairlerinSiirSayisi.cemal_sureya
    elif poet == "Didem Madak".lower():
        myColumn = didem_madak_column
        siirSayisi = enum_file.SairlerinSiirSayisi.didem_madak
    elif poet == "Turgut Uyar".lower():
        myColumn = turgut_uyar_column
        siirSayisi = enum_file.SairlerinSiirSayisi.turgut_uyar
    elif poet == "Özdemir Asaf".lower():
        myColumn = ozdemir_asaf_column
        siirSayisi = enum_file.SairlerinSiirSayisi.ozdemir_asaf
    elif poet == "Ah Muhsin Ünlü".lower():
        myColumn = ah_muhsin_unlu_column
        siirSayisi = enum_file.SairlerinSiirSayisi.ah_muhsin_unlu
    elif poet == "Attila İlhan".lower():
        myColumn = attila_ilhan_column
        siirSayisi = enum_file.SairlerinSiirSayisi.attila_ilhan
    elif poet == "Nazım Hikmet Ran".lower():
        myColumn = nazim_hikmet_ran_column
        siirSayisi = enum_file.SairlerinSiirSayisi.nazim_hikmet_ran
    elif poet == "Edip Cansever".lower():
        myColumn = edip_cansever_column
        siirSayisi = enum_file.SairlerinSiirSayisi.edip_cansever
    elif poet == "Ece Ayhan".lower():
        myColumn = ece_ayhan_column
        siirSayisi = enum_file.SairlerinSiirSayisi.ece_ayhan
    elif poet == "Orhan Veli".lower():
        myColumn = orhan_veli_kanik_column
        siirSayisi = enum_file.SairlerinSiirSayisi.orhan_veli
    elif poet == "Cahit Sıtkı Tarancı".lower():
        myColumn = cahit_sitki_taranci_column
        siirSayisi = enum_file.SairlerinSiirSayisi.cahit_sitki
    elif poet == "Yılmaz Erdoğan".lower():
        myColumn = yilmaz_erdogan_column
        siirSayisi = enum_file.SairlerinSiirSayisi.yilmaz_erdogan
    elif poet == "Yılmaz Güney".lower():
        myColumn = yilmaz_erdogan_column
        siirSayisi = enum_file.SairlerinSiirSayisi.yilmaz_guney
    elif poet == "Tevfik Fikret".lower():
        myColumn = tevfik_fikret_column
        siirSayisi = enum_file.SairlerinSiirSayisi.tevfik_fikret
    return [myColumn,siirSayisi,poet]

bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
#bot.load_next_step_handlers()

bot.polling()
