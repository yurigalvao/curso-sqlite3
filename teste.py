import sqlite3

DB_FILE = 'exercicio.db'

TABLE_NAME = 'teste'

def create():
    try:
        with sqlite3.connect(DB_FILE) as connection:
            cursor = connection.cursor()
            sql_create = f"""
                CREATE TABLE IF NOT EXISTS {TABLE_NAME}
                (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(30) NOT NULL,
                cpf VARCHAR(11) 
                );
            """
            cursor.execute(sql_create)
            connection.commit()
        return True
    except sqlite3.Error as e:
        print(f'Erro ao criar tabela: {e}')
        return False
    
def insert_many(dados_para_inserir):
    try:
        with sqlite3.connect(DB_FILE) as connection:
            cursor = connection.cursor()
            sql_insert = f"""INSERT INTO {TABLE_NAME} (name, cpf) VALUES (:name, :cpf)"""
            cursor.executemany(sql_insert, dados_para_inserir)
            connection.commit()
        return True
    except sqlite3.Error as e:
        print(f'Erro ao inserir dados: {e}')
        return False
    
if __name__ == '__main__':
    # 1. Garante que a tabela exista
    print("Criando tabela...")
    create()

    # 2. Prepara a lista de dicionários para inserir
    # As chaves 'name' e 'cpf' devem bater com os placeholders do SQL
    lista_de_pessoas = [
        {'name': 'Yuri Galvão', 'cpf': '11122233344'},
        {'name': 'Fulano de Tal', 'cpf': '55566677788'},
        {'name': 'Ciclana Souza', 'cpf': '99988877766'}
    ]
    print("Inserindo múltiplos dados...")
    # 3. Chama a função de inserção, passando a lista de dados
    sucesso = insert_many(lista_de_pessoas)
    
    print(f"A inserção em massa foi um sucesso? {sucesso}")

    # 4. Opcional: Verifica se os dados estão no banco
    if sucesso:
        print("\nVerificando dados na tabela...")
        with sqlite3.connect(DB_FILE) as conn:
            # Para ler como dicionário, configuramos o row_factory
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {TABLE_NAME}")
            for linha in cursor.fetchall():
                # Agora podemos acessar por nome da coluna!
                print(dict(linha))