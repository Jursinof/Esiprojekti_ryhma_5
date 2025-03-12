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
        # Haetaan vieraillut maat tietokannasta
        cursor.execute("SELECT vieraillut_maat FROM player_state")
        result = cursor.fetchone()

        if result:
            vieraillut_maat = json.loads(result[0])  # Muunnetaan JSON-listaksi
        else:
            vieraillut_maat = []  # Jos sarake on tyhjä, aloitetaan tyhjällä listalla

        # Haetaan kaikki maat airports-taulusta
        cursor.execute("SELECT id, maa FROM airports")
        tulos = cursor.fetchall()

        # Suodatetaan pois maat, joissa on jo käyty
        saatavilla_olevat_maat = sorted([x for x in tulos if x[1] not in vieraillut_maat], key=lambda x: x[0])

        # Jos kaikki maat on käyty, peli päättyy
        if not saatavilla_olevat_maat:
            print("\nOnneksi olkoon! Olet vieraillut kaikissa maissa ja suorittanut pelin loppuun!")

            # Haetaan lopullinen tähtien määrä tietokannasta
            cursor.execute("SELECT tähdet FROM player_state")
            tulos = cursor.fetchone()
            kokonaistähdet = tulos[0] if tulos else 0

            print(f'Kokonaispistemääräsi: {kokonaistähdet} tähteä!')
            break  # Lopetetaan peli

        print('\nValitse seuraava kohdemaa. Tee valinta antamalla kohdemaata vastaava numero.')
        for x in saatavilla_olevat_maat:
            print(x)

        maa_id = int(input('\nAnna kohdemaata vastaava numero: '))
        kohdemaa_query = "SELECT maa, nimi FROM airports WHERE id = %s"
        cursor.execute(kohdemaa_query, (maa_id,))
        rivit = cursor.fetchall()

        if rivit:
            kohdemaa, nimi = rivit[0]
            print(f'Olet matkalla maahan {kohdemaa}, kentälle {nimi}.')

            oikeat_vastaukset = 0
            kysymys_lista = []

            kysymykset_query = "SELECT kysymys, vaihtoehdot, oikea_vastaus FROM questions WHERE maa = %s"
            cursor.execute(kysymykset_query, (kohdemaa,))
            questions = cursor.fetchall()

            random.shuffle(questions)
            questions = questions[:3]

            for kysymys, vaihtoehdot, oikea_vastaus in questions[:3]:
                print(f"\n{kysymys}")
                vaihtoehdot = json.loads(vaihtoehdot)

                for key, value in vaihtoehdot.items():
                    print(f"{key}. {value}")

                while True:  # Jatketaan kysymistä, kunnes käyttäjä antaa oikean syötteen
                    vastaus = input("Valitse oikea vaihtoehto (A/B/C): ").strip().upper()

                    if vastaus in vaihtoehdot:
                        break  # Käyttäjä antoi kelvollisen vastauksen, poistutaan loopista
                    else:
                        print("Virheellinen syöte, yritä uudelleen.")

                # Tässä verrataan suoraan käyttäjän syötettä tietokannassa olevaan oikeaan vastaukseen
                if vastaus == oikea_vastaus:
                    print(f"Vastaus oikein!")  # Debugging
                    oikeat_vastaukset += 1
                    kysymys_lista.append(f"Oikein: {kysymys}")
                else:
                    print(f"Vastaus väärin.")  # Debugging
                    kysymys_lista.append(f"Väärin: {kysymys}")

            if oikeat_vastaukset > 0:
                print(f"\nOnneksi olkoon! Sait yhteensä: {oikeat_vastaukset} tähteä! Saavuit kohteeseen.")
                print("Valitse alla olevasta listasta seuraava maa johon haluat matkustaa.")

                # Lisätään player_state tauluun saadut tähdet sekä vieraillut maat
                update_query = "UPDATE player_state SET tähdet = tähdet + %s"
                cursor.execute(update_query, (oikeat_vastaukset,))
                yhteys.commit()  # Tallennetaan muutos tietokantaan

                # Päivitetään nykyinen_maa tietokantaan
                update_query = "UPDATE player_state SET nykyinen_maa = %s"
                cursor.execute(update_query, (kohdemaa,))
                yhteys.commit()

                # Haetaan nykyinen vieraillut_maat -lista
                cursor.execute("SELECT vieraillut_maat FROM player_state")
                result = cursor.fetchone()

                if result:
                    vieraillut_maat = json.loads(result[0]) # Muunnetaan JSON-listaksi
                else:
                    vieraillut_maat = [] # Jos sarake on tyhjä, aloitetaan tyhjällä listalla

                # Lisätään uusi kohdemaa listaan, jos sitä ei ole vielä siellä
                if kohdemaa not in vieraillut_maat:
                    vieraillut_maat.append(kohdemaa)

                    # Päivitetään tietokantaan uusi lista JSON-muodossa
                    update_query = "UPDATE player_state SET vieraillut_maat = %s"
                    cursor.execute(update_query, (json.dumps(vieraillut_maat),))
                    yhteys.commit()


            else:
                print("\nEt vastannut yhteenkään kysymykseen oikein. Kone palaa lähtömaahan.")

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
