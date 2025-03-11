#importit
import mysql.connector
import time
import json
import random

#muodostetaan yhteys
yhteys = mysql.connector.connect(
    host='localhost',
    database='lentopeli',
    user='user',
    password='password',
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

# SQL-komento uuden rivin lisäämiseksi
sql = "INSERT INTO player_state (nykyinen_maa, tähdet, vieraillut_maat) VALUES (%s, %s, %s)"
arvot = ("Suomi", 0, "[]")  # Huom! Suomi on oletusalkumaatila, vieraillut_maat jätetään tyhjäksi.

try:
    # Suorita komento ja varmista tietokantamuutokset
    cursor.execute(sql, arvot)
    yhteys.commit()
    print("Uusi rivi lisättiin onnistuneesti tauluun player_state.")
except mysql.connector.Error as err:
    print(f"Tapahtui virhe: {err}")

# Suljetaan kursori ja yhteys
cursor.close()
yhteys.close()




