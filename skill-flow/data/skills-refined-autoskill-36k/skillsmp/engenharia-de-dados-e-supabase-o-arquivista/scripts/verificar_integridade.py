import os
import sys
import io

# Garante que a sada use UTF-8 para evitar erros com emojis no Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

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

def verificar_integridade():
    """
    O Alerta de Estoque (Integridade):
    Verifica se existem registros com informações vitais faltando.
    """
    print("🔍 Iniciando inspeção de integridade nos registros...")
    
    try:
        # Procuramos por registros onde colunas importantes estão vazias
        # Ex: exam_name, value, ou date
        
        campos_vitais = ["exam_name", "value", "date"]
        problemas_encontrados = 0
        
        for campo in campos_vitais:
            response = supabase.table("qc_records").select("id").is_(campo, "null").execute()
            if response.data:
                print(f"🚨 Alerta: Encontrados {len(response.data)} registros com o campo '{campo}' vazio!")
                problemas_encontrados += len(response.data)
        
        if problemas_encontrados == 0:
            print("✅ Inspeção completa. Todos os registros estão com as informações essenciais em dia!")
        else:
            print(f"⚠️  Atenção: Total de {problemas_encontrados} falhas de integridade detectadas.")
            print("💡 Sugestão: Use o sistema de edição para completar esses dados.")

    except Exception as e:
        print(f"⚠️  O inspetor tropeçou (erro na verificação): {e}")

if __name__ == "__main__":
    verificar_integridade()
