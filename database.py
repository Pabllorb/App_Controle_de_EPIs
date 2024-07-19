import sqlite3
from sqlite3 import connect


def create_tables():
    conn = sqlite3.connect('epi_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS epi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            descricao TEXT,
            marca TEXT,
            ca INTEGER,
            validade TEXT,
            unidade INTEGER,
            image_path TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entrega (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            epi_id INTEGER,
            data_entrega TEXT,
            setor TEXT,
            quantidade INTEGER,
            FOREIGN KEY(epi_id) REFERENCES epi(id)
        )
    ''')

    conn.commit()
    conn.close()

def add_epi(nome, descricao, marca, ca, validade, quantidade_a_cadastrar, image_path):
    conn = sqlite3.connect('epi_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT unidade FROM epi WHERE nome = ? AND descricao = ? AND marca = ? AND ca = ?', (nome, descricao, marca, ca))

    result = cursor.fetchone()

    if result:
        # Atualiza o estoque se o EPI já existe
        cursor.execute('''
            UPDATE epi
            SET unidade = unidade + ?, validade = ?, image_path = ?
            WHERE nome = ? AND descricao = ? AND marca = ? AND ca = ?
        ''', (quantidade_a_cadastrar, validade, image_path, nome, descricao, marca, ca))
    else:
        # Insere um novo EPI se não existe
        cursor.execute('''
            INSERT INTO epi (nome, descricao, marca, ca, validade, unidade, image_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nome, descricao, marca, ca, validade, quantidade_a_cadastrar, image_path))

    conn.commit()
    conn.close()

def remove_epi(epi_id):
    conn = sqlite3.connect('epi_database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM epi WHERE id = ?', (epi_id,))

    conn.commit()
    conn.close()

def get_epis():
    conn = sqlite3.connect('epi_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM epi')
    epis = cursor.fetchall()
    conn.close()
    return epis

def add_entrega(epi_id, data_entrega, setor, quantidade):
    conn = sqlite3.connect('epi_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO entrega (epi_id, data_entrega, setor, quantidade)
        VALUES (?, ?, ?, ?)
    ''', (epi_id, data_entrega, setor, quantidade))

    cursor.execute('''
        UPDATE epi
        SET unidade = unidade - ?
        WHERE id = ?
    ''', (quantidade, epi_id))

    conn.commit()
    conn.close()

def get_entregas():
    conn = sqlite3.connect('epi_database.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT entrega.id, entrega.epi_id, epi.nome, epi.descricao, entrega.data_entrega, entrega.setor, entrega.quantidade
                   FROM entrega
                   JOIN epi on entrega.epi_id = epi.id""")
    entregas = cursor.fetchall()
    conn.close()
    return entregas

create_tables()
