import pyodbc # type: ignore
import pandas as pd # type: ignore
from datetime import datetime, timedelta
from sqlalchemy import create_engine # type: ignore

# 📌 Definir as datas do mês passado
hoje = datetime.today()
primeiro_dia_mes_passado = hoje.replace(day=1) - timedelta(days=1)
primeiro_dia_mes_passado = primeiro_dia_mes_passado.replace(day=1)
primeiro_dia_atual = hoje.replace(day=1)

data_inicio = primeiro_dia_mes_passado.strftime("%Y-%m-%d 00:00:00")
data_fim = primeiro_dia_atual.strftime("%Y-%m-%d 00:00:00")

# 📌 Gerar o nome do arquivo no formato "MM-YYYY.txt"
nome_arquivo = primeiro_dia_mes_passado.strftime("%m-%Y") + ".txt"

# 📌 Configurar conexão com SQL Server via SQLAlchemy
server = 'pld-bacen.database.windows.net'
database = 'pld-bacen'
username = 'greenpass'
password = 'r9b2OCFg5VZB1P2zyJi6rVV8PiRy1f'
conn_str = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=SQL+Server"

# 📌 Criar o engine SQLAlchemy
engine = create_engine(conn_str)

# 📌 Definir a query SQL
query = f"""
SELECT * FROM Fattransaction_V2 
WHERE transactionDate BETWEEN '{data_inicio}' AND '{data_fim}'
"""

# 📌 Executar a query e armazenar os dados no DataFrame
df = pd.read_sql(query, engine)

# 📌 Caminho do arquivo no OneDrive (ajuste conforme seu usuário)
caminho_arquivo = fr'C:\Users\gsilva4\OneDrive - EDENRED\Bureau\Planilhas bacen\Transaction\{nome_arquivo}'

# 📌 Salvar em um arquivo TXT separado por ponto e vírgula
df.to_csv(caminho_arquivo, sep=';', index=False, encoding='utf-8')

# 📌 Fechar a conexão (não é mais necessário com SQLAlchemy)
print(f"✅ Arquivo salvo com sucesso: {caminho_arquivo}")
