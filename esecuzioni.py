import mysql.connector
from datetime import datetime

# Connessione al database MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="PasswordSql1999!",
    database="azienda_spedizioni"
)

cursor = db.cursor()

# Funzione per eseguire una query e stampare il risultato
def execute_query(query, data=None):
    try:
        if data:
            cursor.executemany(query, data)
        else:
            cursor.execute(query)
        db.commit()
        print("Query eseguita con successo")
    except mysql.connector.Error as err:
        print(f"Errore durante l'esecuzione della query: {err}")

# 1. Eliminazione delle tabelle (ordine per evitare conflitti)
print("Eliminazione delle tabelle in corso...")
tables = [
    "Feedback", "Tappa_Spedizione", "Spedizione", "Pagamento", "Corriere",
    "Destinazione", "Tipo_Destinazione", "Tipo_Pagamento", "Tariffa", "Stato", "Cliente"
]
for table in tables:
    execute_query(f"DROP TABLE IF EXISTS {table};")

# 2. Creazione delle tabelle
print("Creazione delle tabelle in corso...")
queries = [
    """CREATE TABLE IF NOT EXISTS Cliente (
        id_cliente INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(50),
        cognome VARCHAR(50),
        email VARCHAR(100),
        telefono VARCHAR(20)
    ) ENGINE=InnoDB;""",
    """CREATE TABLE IF NOT EXISTS Tariffa (
        id_tariffa INT AUTO_INCREMENT PRIMARY KEY,
        descrizione VARCHAR(100),
        peso_massimo DECIMAL(10,2),
        costo DECIMAL(10,2)
    ) ENGINE=InnoDB;""",
    """CREATE TABLE IF NOT EXISTS Tipo_Pagamento (
        id_tipo_pagamento INT AUTO_INCREMENT PRIMARY KEY,
        descrizione VARCHAR(50)
    ) ENGINE=InnoDB;""",
    """CREATE TABLE IF NOT EXISTS Pagamento (
        id_pagamento INT AUTO_INCREMENT PRIMARY KEY,
        data DATE,
        stato VARCHAR(50),
        pagato BOOLEAN,
        id_tipo_pagamento INT,
        id_tariffa INT,
        FOREIGN KEY (id_tipo_pagamento) REFERENCES Tipo_Pagamento(id_tipo_pagamento),
        FOREIGN KEY (id_tariffa) REFERENCES Tariffa(id_tariffa)
    ) ENGINE=InnoDB;""",
    """CREATE TABLE IF NOT EXISTS Stato (
        id_stato INT AUTO_INCREMENT PRIMARY KEY,
        descrizione VARCHAR(50)
    ) ENGINE=InnoDB;""",
    """CREATE TABLE IF NOT EXISTS Spedizione (
        id_spedizione BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        peso DECIMAL(10,2),
        id_cliente INT NOT NULL,
        id_tariffa INT NOT NULL,
        id_pagamento INT NOT NULL,
        id_stato INT NOT NULL,
        FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente),
        FOREIGN KEY (id_tariffa) REFERENCES Tariffa(id_tariffa),
        FOREIGN KEY (id_pagamento) REFERENCES Pagamento(id_pagamento),
        FOREIGN KEY (id_stato) REFERENCES Stato(id_stato)
    ) ENGINE=InnoDB;""",
    """CREATE TABLE IF NOT EXISTS Feedback (
        id_feedback INT AUTO_INCREMENT PRIMARY KEY,
        descrizione TEXT,
        valutazione INT,
        id_cliente INT,
        id_spedizione BIGINT UNSIGNED,
        FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente),
        FOREIGN KEY (id_spedizione) REFERENCES Spedizione(id_spedizione)
    ) ENGINE=InnoDB;""",
    """CREATE TABLE IF NOT EXISTS Corriere (
        id_corriere INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(50),
        cognome VARCHAR(50),
        email VARCHAR(100),
        telefono VARCHAR(20)
    ) ENGINE=InnoDB;""",
    """CREATE TABLE IF NOT EXISTS Tipo_Destinazione (
        id_tipo_destinazione INT AUTO_INCREMENT PRIMARY KEY,
        descrizione VARCHAR(50)
    ) ENGINE=InnoDB;""",
    """CREATE TABLE IF NOT EXISTS Destinazione (
        id_destinazione INT AUTO_INCREMENT PRIMARY KEY,
        cap VARCHAR(10),
        citta VARCHAR(50),
        indirizzo VARCHAR(100),
        id_cliente INT,
        id_tipo_destinazione INT,
        FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente),
        FOREIGN KEY (id_tipo_destinazione) REFERENCES Tipo_Destinazione(id_tipo_destinazione)
    ) ENGINE=InnoDB;""",
    """CREATE TABLE IF NOT EXISTS Tappa_Spedizione (
        id_tappa BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        conferma_consegna BOOLEAN,
        id_corriere INT,
        id_destinazione INT NOT NULL,
        id_stato INT NOT NULL,
        id_spedizione BIGINT UNSIGNED NOT NULL,
        data_ultima_modifica TIMESTAMP,
        FOREIGN KEY (id_corriere) REFERENCES Corriere(id_corriere),
        FOREIGN KEY (id_destinazione) REFERENCES Destinazione(id_destinazione),
        FOREIGN KEY (id_stato) REFERENCES Stato(id_stato),
        FOREIGN KEY (id_spedizione) REFERENCES Spedizione(id_spedizione)
    ) ENGINE=InnoDB;"""
]

for query in queries:
    execute_query(query)

# 3. Inserimento dei dati di prova
print("Inserimento dati di prova in corso...")

# Inserimento nella tabella Cliente
data_cliente = [
    ('Mario', 'Rossi', 'mario.rossi@example.com', '1234567890'),
    ('Luigi', 'Bianchi', 'luigi.bianchi@example.com', '0987654321')
]
execute_query("""INSERT INTO Cliente (nome, cognome, email, telefono) VALUES (%s, %s, %s, %s)""", data_cliente)

# Inserimento nella tabella Tariffa
data_tariffa = [
    ('Standard', 20.0, 10.0),
    ('Espressa', 5.0, 20.0)
]
execute_query("""INSERT INTO Tariffa (descrizione, peso_massimo, costo) VALUES (%s, %s, %s)""", data_tariffa)

# Inserimento nella tabella Tipo_Pagamento
data_tipo_pagamento = [
    ('Carta di credito',),
    ('PayPal',)
]
execute_query("""INSERT INTO Tipo_Pagamento (descrizione) VALUES (%s)""", data_tipo_pagamento)

# Inserimento nella tabella Stato
data_stato = [
    ('In corso',),
    ('Completato',)
]
execute_query("""INSERT INTO Stato (descrizione) VALUES (%s)""", data_stato)

# Inserimento nella tabella Pagamento
data_pagamento = [
    ('2024-12-01', 'Pagato', True, 1, 1),
    ('2024-12-02', 'In attesa', False, 2, 2)
]
execute_query("""INSERT INTO Pagamento (data, stato, pagato, id_tipo_pagamento, id_tariffa) VALUES (%s, %s, %s, %s, %s)""", data_pagamento)

# Inserimento nella tabella Spedizione
data_spedizione = [
    (10.0, 1, 1, 1, 1),
    (15.5, 2, 2, 2, 2)
]
execute_query("""INSERT INTO Spedizione (peso, id_cliente, id_tariffa, id_pagamento, id_stato) VALUES (%s, %s, %s, %s, %s)""", data_spedizione)

# Inserimento nella tabella Feedback
data_feedback = [
    ('Servizio eccellente', 5, 1, 1),
    ('Tempi di consegna migliorabili', 3, 2, 2)
]
execute_query("""INSERT INTO Feedback (descrizione, valutazione, id_cliente, id_spedizione) VALUES (%s, %s, %s, %s)""", data_feedback)

# Inserimento nella tabella Corriere
data_corriere = [
    ('Giovanni', 'Verdi', 'giovanni.verdi@example.com', '3339876543'),
    ('Alessandro', 'Blu', 'alessandro.blu@example.com', '3348765432')
]
execute_query("""INSERT INTO Corriere (nome, cognome, email, telefono) VALUES (%s, %s, %s, %s)""", data_corriere)

# Inserimento nella tabella Tipo_Destinazione
data_tipo_destinazione = [
    ('Casa',),
    ('Centro di ritiro',),
    ('Centro di smistamento',)
]
execute_query("""INSERT INTO Tipo_Destinazione (descrizione) VALUES (%s)""", data_tipo_destinazione)

# Inserimento nella tabella Destinazione
data_destinazione = [
    ('00100', 'Roma', 'Via Nazionale 10', 1, 1),
    ('20100', 'Milano', 'Corso Buenos Aires 15', 2, 2),
    ('00001', 'Roma', 'Via Smistamento 1', None, 3),
]
execute_query("""INSERT INTO Destinazione (cap, citta, indirizzo, id_cliente, id_tipo_destinazione) VALUES (%s, %s, %s, %s, %s)""", data_destinazione)

# Inserimento nella tabella Tappa_Spedizione
data_tappa_spedizione = [
    (True, 1, 1, 1, 1, datetime.now()), 
    (False, 2, 2, 2, 2, datetime.now()), 
    (True, 1, 3, 2, 1, datetime.now()),  
    (False, 2, 3, 2, 1, datetime.now()) 
]
execute_query("""INSERT INTO Tappa_Spedizione (conferma_consegna, id_corriere, id_destinazione, id_stato, id_spedizione, data_ultima_modifica) VALUES (%s, %s, %s, %s, %s, %s)""", data_tappa_spedizione)

print("Operazioni completate.")
