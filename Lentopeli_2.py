#importit
import mysql.connector
import time
import json
import random

#muodostetaan yhteys
yhteys = mysql.connector.connect(
    host='localhost',
    database='lentopeli',
    user='username',
    password='salasana',
    autocommit=True,
    collation = 'utf8mb4_unicode_ci'
)


#intro
def intro(text):
    for i in text:
        print(i, end="")
        time.sleep(0.000)
    print()
    time.sleep(len(text) / 1000)


intro("Tervetuloa Lennä ja tiedä! -peliin, jossa opit lisää eri Euroopan maista!")
intro("Tässä pelissä saat tähtiä oikein vastatuista kysymyksistä eri maista, joihin olet lentämässä.")
intro("Sinun pitää vastata oikein vähintään yhteen kysymykseen maasta johon olet lentämässä, tai lentokone lentää takaisin maahan, josta lähdit. Tällöin voit yrittää uudelleen, tai valita toisen maan.")
intro("Sinun on kuitenkin palattava jossain vaiheessa takaisin maahan, jossa et vastannut yhteenkään kysymykseen oikein, jotta pääset pelin loppuun.")
intro("Pelin lopussa sinulle kerrotaan montako tähteä, eli pistettä, olet kerännyt. Maksimi pistemäärä on 30.")
intro("Oletko ymmärtänyt ohjeet? Paina enter aloittaaksesi!")
input("")
intro("Olet Helsinki-Vantaan lentokentällä. Olet saanut tarpeeksesi Suomen kylmyydestä ja haluat vaihtaa maisemaa.")


cursor = yhteys.cursor()

# Käytä parameterisoitua kyselyä
sql = "INSERT INTO player_state (nykyinen_maa, tähdet, vieraillut_maat) VALUES (%s, %s, %s)"
arvot = ("Suomi", 0, "")

# Suorita SQL-lause turvallisesti
cursor.execute(sql, arvot)

# Varmistetaan tietokantamuutokset
yhteys.commit()

# Suljetaan tietokantayhteys
cursor.close()
yhteys.close()
#cursor = yhteys.cursor()
#sql = 'INSERT INTO player_state (nykyinen_maa, tähdet, vieraillut_maat) VALUES ("Suomi", 0, "")';
#cursor.execute(sql)
#yhteys.commit()
#cursor.close()
#yhteys.close()



#cursor.execute("SELECT maa, kysymys, vaihtoehdot FROM questions WHERE maa = 'Ruotsi'")

#for (maa, kysymys, vaihtoehdot) in cursor.fetchmany(3):
    #print(kysymys, vaihtoehdot)
    #input('')



