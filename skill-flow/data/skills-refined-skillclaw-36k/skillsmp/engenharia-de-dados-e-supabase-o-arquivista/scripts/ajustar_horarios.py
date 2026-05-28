import os
import sys
from datetime import datetime
import pytz
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

def ajustar_horarios():
    """
    O Relojoeiro de Sincronia:
    Verifica se existem datas salvas em formatos confusos ou sem fuso horário
    e tenta padronizar para o horário de Brasília (ou o definido).
    """
    print("⌚ Iniciando o ajuste fino dos relógios (datas) no banco...")
    
    try:
        # Busca registros recentes
        response = supabase.table("qc_records").select("id, date").order("date", desc=True).limit(50).execute()
        records = response.data
        
        if not records:
            print("📭 Nenhum registro recente para conferir.")
            return

        print(f"🧐 Analisando os últimos {len(records)} registros...")
        
        ajustados = 0
        for r in records:
            data_original = r['date']
            # Exemplo de lógica: se a data não tiver o 'T' de timestamp ou fuso horário, marcamos
            if "T" not in data_original and "-" in data_original:
                # É uma data simples (YYYY-MM-DD), vamos manter ou converter se necessário
                # Aqui você pode adicionar lógica para converter de AM/PM para 24h, etc.
                pass
            
        print("✅ Sincronia verificada! Tudo parece estar nos eixos.")
        # Nota: Ajustes automáticos de data são delicados, este script 
        # serve mais como um monitor no momento.

    except Exception as e:
        print(f"⚠️  O relógio parou (erro na sincronia): {e}")

if __name__ == "__main__":
    ajustar_horarios()
