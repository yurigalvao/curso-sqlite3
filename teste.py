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
    
def select_all():
    try:
        with sqlite3.connect(DB_FILE) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            sql_select = f"""SELECT * FROM {TABLE_NAME}"""
            cursor.execute(sql_select)
            result = cursor.fetchall()
        return result
    except sqlite3.Error as e:
        print(f'Erro ao selecionar dados da tabela: {e}')
        return []
    
if __name__ == '__main__':
    # --- PASSO 1: CRIAR A ESTRUTURA ---
    # Garante que a nossa tabela 'teste' exista antes de tentarmos usá-la.
    print("Iniciando o teste: Criando a tabela (se não existir)...")
    create()

    # --- PASSO 2: PREPARAR OS DADOS ---
    # Criamos nossa lista de dicionários. As chaves ('name', 'cpf') devem
    # corresponder exatamente aos placeholders (:name, :cpf) na sua função de inserção.
    print("\nPreparando os dados para inserção...")
    lista_de_pessoas = [
        {'name': 'Yuri Galvão', 'cpf': '11122233344'},
        {'name': 'Fulano de Tal', 'cpf': '55566677788'},
        {'name': 'Ciclana Souza', 'cpf': '99988877766'}
    ]

    # --- PASSO 3: EXECUTAR A INSERÇÃO EM MASSA ---
    # Chamamos a função que usa o executemany para inserir todos os dados de uma vez.
    print("Executando a inserção em massa...")
    sucesso_insert = insert_many(lista_de_pessoas)
    print(f"--> Inserção bem-sucedida? {sucesso_insert}")

    # --- PASSO 4: LER E VALIDAR OS DADOS ---
    # Agora, usamos nossa nova função select_all para buscar os dados de volta.
    print("\nBuscando os dados do banco para verificação...")
    dados_do_banco = select_all()

    # Verificamos se a função retornou uma lista (e não False ou uma lista vazia)
    if dados_do_banco:
        print("--> Sucesso! Dados encontrados:")
        # Fazemos um loop e imprimimos os dados acessando-os pelo NOME da coluna.
        # Esta é a prova de que o row_factory funcionou!
        for pessoa in dados_do_banco:
            print(f"  ID: {pessoa['id']}, Nome: {pessoa['name']}, CPF: {pessoa['cpf']}")
    else:
        print("--> Falha! Nenhum dado foi encontrado no banco.")