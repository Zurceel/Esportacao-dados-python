import pyodbc # type: ignore
import pandas as pd # type: ignore
import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine # type: ignore

# 📌 Definir as datas
hoje = datetime.today()
ontem = hoje - timedelta(days=1)
data_fim = hoje.strftime("%Y-%m-%d 00:00:00")  # Hoje às 00:00:00

data_inicio = ontem.strftime("%Y-%m-%d 00:00:00")

# 📌 Gerar o nome do arquivo no formato "DD-MM-YYYY.txt"
nome_arquivo = f"{ontem.strftime('%d-%m-%Y')}.txt"

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
SELECT * FROM Fattransaction_V2 with(nolock)
WHERE transactionDate BETWEEN '{data_inicio}' AND '{data_fim}'
"""

# 📌 Executar a query e armazenar os dados no DataFrame
df = pd.read_sql(query, engine)

# 📌 Caminho do arquivo no OneDrive
caminho_pasta = r'C:\Users\gsilva4\Downloads\DadosTesteTransaction'
caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)

# 📌 Salvar em um arquivo TXT separado por ponto e vírgula
df.to_csv(caminho_arquivo, sep=';', index=False, encoding='utf-8')
print(f"✅ Arquivo salvo com sucesso: {caminho_arquivo}")

# 📌 Se for dia 05, unir os arquivos
if hoje.day == 1:
    print("📌 Hoje é dia 01, iniciando a consolidação de arquivos...")
    
    arquivos = [os.path.join(caminho_pasta, f) for f in os.listdir(caminho_pasta) if f.endswith(".txt")]
    
    if arquivos:
        # 📌 Criar DataFrame consolidado
        df_consolidado = pd.concat([pd.read_csv(f, sep=';', encoding='utf-8') for f in arquivos], ignore_index=True)
        
        # 📌 Nome do arquivo final
        mes_passado = hoje.replace(day=1) - timedelta(days=1)  # Último dia do mês passado
        nome_final = f"{mes_passado.strftime('%m-%Y')}.txt"
        caminho_pasta_Final = r'C:\Users\gsilva4\OneDrive - EDENRED\Bureau\Planilhas bacen\Transaction'
        caminho_final = os.path.join(caminho_pasta_Final, nome_final)
        
        # 📌 Salvar arquivo consolidado
        df_consolidado.to_csv(caminho_final, sep=';', index=False, encoding='utf-8')
        print(f"✅ Arquivo consolidado salvo com sucesso: {caminho_final}")
        
        # 📌 Remover arquivos originais
        for f in arquivos:
            os.remove(f)
        print("🗑️ Arquivos originais removidos.")
    else:
        print("⚠️ Nenhum arquivo encontrado para consolidar.")
else:
    print("📌 Hoje não é dia 01. Apenas salvando os dados de D-1 normalmente.")
