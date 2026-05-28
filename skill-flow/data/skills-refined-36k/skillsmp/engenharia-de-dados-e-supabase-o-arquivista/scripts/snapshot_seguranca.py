import os
import sys
import io
import json

# Garante que a saída use UTF-8 para evitar erros com emojis no Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from datetime import datetime
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

def criar_snapshot():
    """
    O Backup de Emergência (Snapshot):
    Tira uma foto atual dos dados de CQ e salva em um arquivo JSON.
    """
    agora = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"backup_qc_{agora}.json"
    caminho_pasta = os.path.join(os.getcwd(), "backups")
    
    # Cria a pasta de backups se não existir
    if not os.path.exists(caminho_pasta):
        os.makedirs(caminho_pasta)
    
    print(f"[SNAPSHOT] Tirando uma foto dos dados para o arquivo {nome_arquivo}...")
    
    try:
        # Busca todos os dados da tabela
        response = supabase.table("qc_records").select("*").execute()
        
        if response.data:
            caminho_completo = os.path.join(caminho_pasta, nome_arquivo)
            with open(caminho_completo, "w", encoding="utf-8") as f:
                json.dump(response.data, f, indent=4, ensure_ascii=False)
            
            print(f"SUCCESS: Foto salva com sucesso em: {caminho_completo}")
            print(f"INFO: Total de registros protegidos: {len(response.data)}")
        else:
            print("INFO: O cofre está vazio. Nada para fotografar.")

    except Exception as e:
        print(f"ERROR: A câmera falhou ao tirar a foto (erro no backup): {e}")

if __name__ == "__main__":
    criar_snapshot()
