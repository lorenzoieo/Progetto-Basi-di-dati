import mysql.connector

# Connessione al database
def connessione_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="PasswordSql1999!",
        database="azienda_spedizioni"
    )
    return conn

# Funzione per visualizzare i dettagli della spedizione
def dettagli_spedizione():
    # Chiedi l'ID della spedizione
    id_spedizione = input("Inserisci l'ID della spedizione: ")

    # Connessione al database
    conn = connessione_db()
    cursor = conn.cursor()

    # Query per ottenere i dettagli della spedizione
    query = """
    SELECT s.id_spedizione, c.nome, c.cognome, c.email, t.descrizione AS tariffa_descrizione, d.indirizzo, td.descrizione AS tipo_destinazione
    FROM Spedizione s
    JOIN Cliente c ON s.id_cliente = c.id_cliente
    JOIN Tariffa t ON s.id_tariffa = t.id_tariffa
    JOIN Tappa_Spedizione ts ON s.id_spedizione = ts.id_spedizione
    JOIN Destinazione d ON ts.id_destinazione = d.id_destinazione
    JOIN Tipo_Destinazione td ON d.id_tipo_destinazione = td.id_tipo_destinazione
    WHERE s.id_spedizione = %s
    """
    
    try:
        cursor.execute(query, (id_spedizione,))
        result = cursor.fetchall()

        # Verifica se ci sono risultati
        if result:
            for row in result:
                print(f"ID Spedizione: {row[0]}")
                print(f"Cliente: {row[1]} {row[2]} ({row[3]})")
                print(f"Tariffa: {row[4]}")
                print(f"Indirizzo Destinazione: {row[5]}")
                print(f"Tipo Destinazione: {row[6]}")
        else:
            print("Nessuna spedizione trovata con questo ID.")
    
    except mysql.connector.Error as err:
        print(f"Errore durante l'esecuzione della query: {err}")
    
    finally:
        cursor.close()
        conn.close()

# Funzione per visualizzare tutte le tappe di una spedizione
def visualizza_tappe():
    # Chiedi l'ID della spedizione
    id_spedizione = input("Inserisci l'ID della spedizione per visualizzare le tappe: ")

    # Connessione al database
    conn = connessione_db()
    cursor = conn.cursor()

    # Query per ottenere tutte le tappe di una spedizione
    query = """
    SELECT ts.id_tappa, ts.data_ultima_modifica, s.descrizione AS stato_descrizione, c.nome AS corriere_nome, c.cognome AS corriere_cognome, td.descrizione AS tipo_tappa
    FROM Tappa_Spedizione ts
    JOIN Stato s ON ts.id_stato = s.id_stato
    LEFT JOIN Corriere c ON ts.id_corriere = c.id_corriere
    JOIN Destinazione d ON ts.id_destinazione = d.id_destinazione
    JOIN Tipo_Destinazione td ON d.id_tipo_destinazione = td.id_tipo_destinazione
    WHERE ts.id_spedizione = %s
    ORDER BY ts.id_tappa
    """

    try:
        cursor.execute(query, (id_spedizione,))
        result = cursor.fetchall()

        # Verifica se ci sono tappe per quella spedizione
        if result:
            print("\nTappe della spedizione:")
            for row in result:
                print(f"ID Tappa: {row[0]}")
                print(f"Data Ultima Modifica: {row[1]}")
                print(f"Stato: {row[2]}")
                print(f"Corriere: {row[3]} {row[4]}" if row[3] else "Corriere: Non assegnato")
                print(f"Tipo Tappa: {row[5]}")
                print("-" * 40)
        else:
            print("Nessuna tappa trovata per questa spedizione.")
    
    except mysql.connector.Error as err:
        print(f"Errore durante l'esecuzione della query: {err}")
    
    finally:
        cursor.close()
        conn.close()

# Funzione per il menu principale
def menu():
    while True:
        print("\nMenu:")
        print("1. Cerca nelle tabelle per ID")
        print("2. Dettagli della spedizione (Cliente, Tariffa, Destinazione)")
        print("3. Visualizza tutte le tappe di una spedizione")
        print("4. Uscire")
        
        scelta = input("Scegli un'opzione (1/2/3/4): ")

        if scelta == '1':
            cerca_per_id()
        elif scelta == '2':
            dettagli_spedizione()
        elif scelta == '3':
            visualizza_tappe()
        elif scelta == '4':
            print("Uscita dal programma.")
            break
        else:
            print("Scelta non valida, riprova.")

# Funzione per cercare nelle tabelle per ID
def cerca_per_id():
    print("Scegli la tabella in cui cercare:")
    tabelle = {
        "1": "Destinazione",
        "2": "Cliente",
        "3": "Spedizione",
        "4": "Tariffa",
        "5": "Feedback",
        "6": "Corriere",
        "7": "Tipo_Pagamento",
        "8": "Pagamento",
        "9": "Stato",
        "10": "Tappa_Spedizione",
        "11": "Tipo_Destinazione"
    }
    for key, value in tabelle.items():
        print(f"{key}. {value}")
    
    scelta_tabella = input("Scegli un numero per la tabella: ")

    if scelta_tabella in tabelle:
        id_ricerca = input(f"Inserisci l'ID per cercare in {tabelle[scelta_tabella]}: ")
        conn = connessione_db()
        cursor = conn.cursor()

        # Costruzione della query dinamica per la ricerca
        query = f"SELECT * FROM {tabelle[scelta_tabella]} WHERE id_{tabelle[scelta_tabella].lower()} = %s"
        
        try:
            cursor.execute(query, (id_ricerca,))
            result = cursor.fetchall()

            if result:
                for row in result:
                    print(row)
            else:
                print(f"Nessun risultato trovato per l'ID {id_ricerca} in {tabelle[scelta_tabella]}.")
        
        except mysql.connector.Error as err:
            print(f"Errore durante l'esecuzione della query: {err}")
        
        finally:
            cursor.close()
            conn.close()

# Avvio del programma
if __name__ == "__main__":
    menu()
