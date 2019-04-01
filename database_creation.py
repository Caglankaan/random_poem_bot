import pymongo
from bs4 import BeautifulSoup as BS
import re
import urllib.request
from urllib.error import HTTPError

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient['sairler']

#Ali Lidar
ali_lidar_column = mydb['ali-lidar']
ali_lidar_page = 20
ali_lidar = "ali-lidar"

#Hasan Hüseyin Korkmazgil
hasan_huseyin_korkmazgil_column = mydb['hasan-huseyin-korkmazgil']
hasan_huseyin_page = 3
hasan_huseyin_korkmazgil = "hasan-huseyin-korkmazgil"

#Cemal Süreya
cemal_sureya_column = mydb['cemal-sureya']
cemal_sureya_page = 6
cemal_sureya = "cemal-sureya"

#Didem Madak
didem_madak_column = mydb['didem-madak']
didem_madak_page = 1
didem_madak = "didem-madak"

#Turgut Uyar
turgut_uyar_column = mydb['turgut-uyar']
turgut_uyar_page = 2
turgut_uyar = "turgut-uyar"

#Özdemir Asaf
ozdemir_asaf_column = mydb['ozdemir-asaf']
ozdemir_asaf_page = 12
ozdemir_asaf = "ozdemir-asaf"

#Ah Muhsin Ünlü
ah_muhsin_unlu_column = mydb['ah-muhsin-unlu']
ah_muhsin_unlu_page = 2
ah_muhsin_unlu = "ah-muhsin-unlu"

#Atilla İlhan
attila_ilhan_column = mydb['attila-ilhan']
attila_ilhan_page = 7
attila_ilhan = "attila-ilhan"

#Nazım Hikmet Ran
nazim_hikmet_column = mydb['nazim-hikmet-ran']
nazim_hikmet_ran_page = 9
nazim_hikmet = "nazim-hikmet"

#Edip Cansever
edip_cansever_column = mydb['edip-cansever']
edip_cansever_page = 7
edip_cansever = "edip-cansever"

#Ece Ayhan
ece_ayhan_column = mydb['ece-ayhan']
ece_ayhan_page = 2
ece_ayhan = "ece-ayhan"

#Orhan Veli
orhan_veli_kanik_column = mydb['orhan-veli-kanik']
orhan_veli_kanik_page = 5
orhan_veli_kanik = "orhan-veli-kanik"

#Cahit Sıtkı Tarancı
cahit_sitki_taranci_column = mydb['cahit-sitki-taranci']
cahit_sitki_taranci = "cahit-sitki-taranci"

#Yilmaz Güney
yilmaz_guney_column = mydb['yilmaz-guney']
yilmaz_guney = "yilmaz-guney"

#Yilmaz Erdogan
yilmaz_erdogan_column = mydb['yilmaz-erdogan']
yilmaz_erdogan = "yilmaz-erdogan"

#Tevfik Fikret
tevfik_fikret_column = mydb['tevfik-fikret']
tevfik_fikret = "tevfik-fikret"




def table_creation(db_column, page_count, poet_name,current_page, index):
    for i in range(0,page_count):
        string = "sayfa-"+str(current_page)+"/"
        page = "https://www.antoloji.com/"+poet_name+"/siirleri/ara-/sirala-/"+string
        html = urllib.request.urlopen(page).read()
        soup = BS(html, features="lxml")
        div = soup.find("div", {"class": "list-content poemListBox"})
        rows = div.find_all('a')
        isOdd = False
        for row in rows:
            if isOdd:
                link = "https://www.antoloji.com"+str(row.get('href'))
                mydict = { "Title": str(row.get('title')), "Link":str(link), "Poem":"", "Number":str(index)}
                x = db_column.insert_one(mydict)
                isOdd = False
                index = index+1
            else:
                isOdd = True
        print(current_page,". Sayfa tamamlandı.")
        current_page += 1
    i = 0
    for col in db_column.find():
        print(col['Poem'])
        if col['Poem'] == "":
            page = col['Link']
            html = urllib.request.urlopen(page).read()
            soup = BS(html, features="lxml")
            div = soup.find("div", {"class": "pd-text"})
            rows = div.find_all('p')
            a = str(rows)
            a = a.replace('<br/>',"")
            a = a.replace('<p>',"")
            a = a.replace('</p>',"")
            a = a.replace('  ',"")
            a = a.replace('[',"")
            a = a.replace(']',"")
            #aliLidar[i].append(a)
            my_query = {"Number": str(i+1)}
            new_values = {"$set": {"Poem":str(a)}} 
            db_column.update_one(my_query, new_values)
            print(col['Number'],". Siir eklendi. Title : ", col['Title']," Poet: ", poet_name)

            i +=1
        else:
            print("yapilmis")

def table_creation_another_website(db_column, poet_name, index):
    page = "http://siir.sitesi.web.tr/"+poet_name+"/"
    html = urllib.request.urlopen(page).read()
    soup = BS(html, features="lxml")
    div = soup.find("div", {"class": "text"})
    rows = div.find_all("a")
    a = False
    for row in rows:
        if a:
            #print("text is: ",row.text
            href_tags = row.get('href')
            #print("link is: ",href_tags)
            #print('text is: ',row.text)
            mydict = { "Title": str(row.text), "Link":str(href_tags), "Poem":"", "Number":str(index)}
            x = db_column.insert_one(mydict)
            index = index+1
        else:
            a = True
            
    i = 1
    for col in db_column.find():    
        #if col['Poem'] == "":
        page = col['Link']
        html = urllib.request.urlopen(page).read()
        soup = BS(html, features="lxml")
        div = soup.find("div", {"class": "text"})
        rows = div.find_all('p')
        a = str(rows)
        a = a.replace('<br/>',"")
        a = a.replace('<p>',"")
        a = a.replace('</p>',"")
        a = a.replace('  ',"")
        a = a.replace('[',"")
        a = a.replace(']',"")
        my_query = {"Number": str(i)}
        new_values = {"$set": {"Poem":str(a)}} 
        db_column.update_one(my_query, new_values)
        print(col['Number'],". Siir eklendi. Title : ", col['Title']," Poet: ", poet_name)
        i = i+1
        #else:
            #print("yapilmis")
            
def main():
    current_page = 1
    index = 1
    table_creation(ali_lidar_column,ali_lidar_page,ali_lidar, current_page, index)
    table_creation(didem_madak_column,didem_madak_page,didem_madak,current_page,index)
    table_creation(cemal_sureya_column,cemal_sureya_page,cemal_sureya, current_page,index)
    table_creation(hasan_huseyin_korkmazgil_column,hasan_huseyin_page,hasan_huseyin_korkmazgil, current_page, index)
    table_creation(ozdemir_asaf_column,ozdemir_asaf_page,ozdemir_asaf,current_page,index)
    table_creation(ah_muhsin_unlu_column,ah_muhsin_unlu_page,ah_muhsin_unlu,current_page,index)
    table_creation_another_website(cemal_sureya_column,cemal_sureya,index)
    table_creation_another_website(attila_ilhan_column,attila_ilhan,index)
    table_creation_another_website(ece_ayhan_column,ece_ayhan,index)
    table_creation_another_website(edip_cansever_column,edip_cansever,index)
    table_creation_another_website(nazim_hikmet_column,nazim_hikmet,index)
    table_creation_another_website(orhan_veli_kanik_column,orhan_veli_kanik,index)
    table_creation_another_website(turgut_uyar_column,turgut_uyar,index)
    table_creation_another_website(cahit_sitki_taranci_column,cahit_sitki_taranci,index)
    
    table_creation_another_website(yilmaz_erdogan_column,yilmaz_erdogan,index)
    table_creation_another_website(yilmaz_guney_column,yilmaz_guney,index)
    table_creation_another_website(tevfik_fikret_column,tevfik_fikret,index)


main()