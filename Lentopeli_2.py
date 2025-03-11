#importit
import mysql.connector
import time
import json
import random

try:

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
    # Poistetaan vanhat pelit ennen uuden aloittamista
    cursor.execute("Delete FROM player_state")

    # SQL-komento uuden rivin lisäämiseksi
    sql = "INSERT INTO player_state (nykyinen_maa, tähdet, vieraillut_maat) VALUES (%s, %s, %s)"
    arvot = ("Suomi", 0, "[]")  # Huom! Suomi on oletusalkumaatila, vieraillut_maat jätetään tyhjäksi.

    cursor.execute(sql, arvot)
    yhteys.commit()

    cursor.execute("SELECT * FROM airports")
    tulos = cursor.fetchall()

    print('\nValitse tästä listasta kohde, johon ensimmäisenä haluat lentää. Tee valinta antamalla kohdemaata vastaava numero.')
    for x in tulos:
        print(x)

    float(input('\nAnna kohdemaata vastaava numero: '))


# Jatketaan tähän kohtaan

except mysql.connector.Error as err:
    # Tietokantaoperaatioissa tapahtuneet virheet
    print(f"Tapahtui virhe: {err}")

except Exception as e:
    # Muut virheet, kuten pelin logiikassa
    print(f'Virhe pelin aikana: {e}')

finally:

    # Suljetaan kursori ja yhteys
    if cursor:
        cursor.close()
    if yhteys:
        yhteys.close()
