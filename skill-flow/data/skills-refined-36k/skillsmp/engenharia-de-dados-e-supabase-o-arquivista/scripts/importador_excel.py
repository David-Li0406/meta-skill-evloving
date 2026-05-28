import os
import sys
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client, Client

# Carrega as chaves do cofre (.env)
load_dotenv()

URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not URL or not KEY:
    print("❌ Erro: Chaves do Supabase não encontradas no .env")
    sys.exit(1)

supabase: Client = create_client(URL, KEY)

def importar_dados(caminho_arquivo):
    """
    O Tradutor de Planilhas (Importador):
    Lê um arquivo Excel ou CSV e envia para o Supabase de forma organizada.
    """
    print(f"📖 Lendo o arquivo: {caminho_arquivo}...")
    
    try:
        # Detecta se é Excel ou CSV
        if caminho_arquivo.endswith('.csv'):
            df = pd.read_csv(caminho_arquivo)
        else:
            df = pd.read_excel(caminho_arquivo)
            
        print(f"✅ Arquivo carregado com {len(df)} linhas.")
        
        # Mapeamento de colunas (Exemplo: coluna da planilha -> coluna do banco)
        # Você pode ajustar isso conforme sua planilha real!
        print("🔗 Traduzindo colunas para a língua do banco de dados...")
        
        registros = []
        for index, row in df.iterrows():
            # Aqui criamos o "dicionário" que o Supabase entende
            try:
                item = {
                    "date": str(row.get("Data", row.get("date"))),
                    "exam_name": str(row.get("Exame", row.get("exam_name"))),
                    "level": str(row.get("Nível", row.get("level"))),
                    "value": float(row.get("Valor", row.get("value"))),
                    "target_value": float(row.get("Alvo", row.get("target_value", 0))),
                    # Adicione outros campos necessários aqui
                }
                registros.append(item)
            except Exception as e_row:
                print(f"⚠️  Pulando linha {index+1} por erro de conversão: {e_row}")

        if registros:
            print(f"🚀 Enviando {len(registros)} novos dados para o cofre...")
            response = supabase.table("qc_records").insert(registros).execute()
            print("✅ Importação concluída com sucesso!")
        else:
            print("🤷 Nenhum dado válido encontrado para importar.")

    except Exception as e:
        print(f"⚠️  O tradutor se confundiu (erro na importação): {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("💡 Uso: python importador_excel.py caminho/para/seu/arquivo.xlsx")
    else:
        importar_dados(sys.argv[1])
