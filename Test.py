import mysql.connector

# Yhdista tietokantaan
try:
    yhteys = mysql.connector.connect(
        host='localhost',
        database='lentopeli',
        user='username',
        password='password',
        autocommit=True,
        collation = 'utf8mb4_unicode_ci'
    )

    cursor = yhteys.cursor()

    # Haetaan kysymykset
    cursor.execute("SELECT id, maa, kysymys FROM questions;")

    # Tulostetaan tiedot
    for (id, maa, kysymys) in cursor.fetchall():
        print(f'ID: {id}, Maa: {maa}, Kysymys: {kysymys}')

except mysql.connector.Error as e:
    print(f'Virhe tietokantayhteydessä: {e}')

finally:
    if 'yhteys' in locals() and yhteys:
        cursor.close()
        yhteys.close()