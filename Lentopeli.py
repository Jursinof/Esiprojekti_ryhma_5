import mysql.connector
import time

yhteys = mysql.connector.connect(
    host='localhost',
    database='flight_game',
    user='username',
    password='salasana',
    autocommit=True,
    collation = 'utf8mb4_unicode_ci'
)

def dialogue(text):
    for i in text:
        print(i, end="")
        time.sleep(0.035)
    print()
    time.sleep(len(text) / 1000)


dialogue("Tervetuloa Lennä ja tiedä! -peliin, jossa opit lisää eri Euroopan maista!")
dialogue("Tässä pelissä saat tähtiä oikein vastatuista kysymyksistä eri maista, joihin olet lentämässä.")
dialogue("Sinun pitää vastata vähintään oikein yhteen kysymykseen maasta johon olet lentämässä, tai lentokone lentää takaisin maahan mistä lähdit ja voit yrittää joko uudelleen tai valita toisen maan.")
dialogue("Sinun on kuitenkin palattava jossain vaiheessa takaisin maahan missä et vastannut yhteenkään oikeaan kysymykseen, jotta pääset pelin loppuun.")
dialogue("Pelin lopussa sinulle kerrotaan montako tähteä, eli pistettä,olet kerännyt. Maksimi pistemäärä on 30.")
dialogue("Oletko ymmärtänyt ohjeet? Paina enter aloittaaksesi!")
dialogue("")
dialogue("Olet Helsinki-Vantaan lentokentällä. Olet saanut tarpeeksesi Suomen kylmyydestä ja haluat vaihtaa maisemaa.")

# Lista maista
countries = [
    "Ruotsi", "Saksa", "Ranska", "Italia",
    "Espanja", "Englanti", "Tanska","Kreikka","Saksa", "Hollanti"]

print("\nValitse maa, johon haluat lentää (1-10):")
print("1. Ruotsi")
print("2. Saksa")
print("3. Ranska")
print("4. Italia")
print("5. Espanja")
print("6. Englanti")
print("7. Tanska")
print("8. Kreikka")
print("9. Saksa")
print("10. Hollanti")

while True:
    country = input("\nAnna numerosi valitsemastasi maasta: ")

    if country in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
        break
    else:
        print("\nValintasi on virheellinen. Valitse luku 1 ja 10 välillä.")


if country =="1":
    print("Olet valinnut Ruotsin! Lentokoneesi suuntaa sinne.")
elif country =="2":
    print("Olet valinnut Saksan! Lentokoneesi suuntaa sinne.")
elif country == "3":
    print("Olet valinnut Ranskan! Lentokoneesi suuntaa sinne.")
elif country == "4":
    print("Olet valinnut Italian! Lentokoneesi suuntaa sinne.")
elif country == "5":
    print("Olet valinnut Espanjan! Lentokoneesi suuntaa sinne.")
elif country == "6":
    print("Olet valinnut Englannin! Lentokoneesi suuntaa sinne.")
elif country == "7":
    print("Olet valinnut Tanskan! Lentokoneesi suuntaa sinne.")
elif country == "8":
    print("Olet valinnut Kreikan! Lentokoneesi suuntaa sinne.")
elif country == "9":
    print("Olet valinnut Saksan! Lentokoneesi suuntaa sinne.")
elif country == "10":
    print("Olet valinnut Hollannin! Lentokoneesi suuntaa sinne.")

#Toinen vaihtoehto
print('Valitse maa, johon haluat lentää.')
countries = ['\nRanska', '\nEspanja', '\nYhdistynyt Kuningaskunta', '\nHollanti',
             '\nSaksa', '\nItalia', '\nIrlanti', '\nKreikka', '\nTanska', '\nRuotsi']
print(*countries)
where_to = input('\nSyötä haluamasi maan nimi: ')

if where_to not in countries:
    print('Virhellinen maan nimi.')