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
        user='riikka',
        password='koodar1',
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
    arvot = ("Suomi", 0, "[]")

    cursor.execute(sql, arvot)
    yhteys.commit()

    while True:
        cursor.execute("SELECT * FROM airports")
        tulos = cursor.fetchall()

        print('\nValitse tästä listasta kohde, johon haluat lentää. Tee valinta antamalla kohdemaata vastaava numero.')
        for x in tulos:
            print(x)

        maa_id = int(input('\nAnna kohdemaata vastaava numero: '))
        kohdemaa_query = "SELECT maa FROM airports WHERE id = %s"
        cursor.execute(kohdemaa_query, (maa_id,))
        rivit = cursor.fetchall()

        if rivit:
            kohdemaa = rivit[0][0]
            print(f'Olet matkalla maahan {kohdemaa}')

            kysymykset_query = "SELECT kysymys, vaihtoehdot, oikea_vastaus FROM questions WHERE maa = %s"
            cursor.execute(kysymykset_query, (kohdemaa,))
            questions = cursor.fetchall()
            random.shuffle(questions)

            oikeat_vastaukset = 0
            kysymys_lista = []

            for kysymys, vaihtoehdot, oikea_vastaus in questions[:3]:
                print(f"\n{kysymys}")
                vaihtoehdot = json.loads(vaihtoehdot)
                for key, value in vaihtoehdot.items():
                    print(f"{key}. {value}")

                vastaus = input("Valitse oikea vaihtoehto (A/B/C): ").strip().upper()

                # Tarkistetaan, onko syöte kelvollinen
                if vastaus not in vaihtoehdot:
                    print("Virheellinen syöte, yritä uudelleen.")
                    continue  # Jos syöte ei ole kelvollinen, palaa kysymykseen

                valittu_vastaus = vaihtoehdot[vastaus]  # Haetaan valittu vastaus sanakirjasta

                if valittu_vastaus == oikea_vastaus:
                    print(f"Vastaus oikein: {valittu_vastaus} == {oikea_vastaus}")  # Debugging
                    oikeat_vastaukset += 1
                    kysymys_lista.append(f"Oikein: {kysymys}")
                else:
                    print(f"Vastaus väärin: {valittu_vastaus} != {oikea_vastaus}")  # Debugging
                    kysymys_lista.append(f"Väärin: {kysymys}")

            print(f"Oikeat vastaukset: {oikeat_vastaukset}")  # Debugging
            if oikeat_vastaukset > 0:
                print("\nOnneksi olkoon! Vastasit oikein seuraaviin kysymyksiin:")
                for kysymys in kysymys_lista:
                    print(kysymys)
                break
            else:
                print("\nEt vastannut yhteenkään kysymykseen oikein. Kone palaa lähtömaahan.")

    # Jatketaan tähän kohtaan

except mysql.connector.Error as err:
    # Tietokantaoperaatioissa tapahtuneet virheet
    print(f"Virhe tietokantaoperaatiossa: {err}")

except Exception as e:
    # Muut virheet, kuten pelin logiikassa
    print(f'Virhe pelin aikana: {e}')

finally:

    # Suljetaan kursori ja yhteys
    if cursor:
        cursor.close()
    if yhteys:
        yhteys.close()
