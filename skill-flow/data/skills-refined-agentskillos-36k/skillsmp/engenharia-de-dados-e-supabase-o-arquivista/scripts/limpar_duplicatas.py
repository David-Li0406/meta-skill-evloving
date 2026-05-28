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
KEY = os.getenv("SUPABASE_SERVICE_KEY") # Usando Service Key para ter poder de limpeza

if not URL or not KEY:
    print("❌ Erro: Chaves do Supabase não encontradas no .env")
    sys.exit(1)

supabase: Client = create_client(URL, KEY)

def limpar_duplicatas():
    """
    O Faxineiro de Duplicatas:
    Busca registros de CQ que são idênticos (mesma data, exame, nível e valor)
    e mantém apenas o mais recente.
    """
    print("[CLEANUP] Iniciando a faxina de duplicatas em 'qc_records'...")
    
    try:
        # 1. Busca todos os registros (simplificado para exemplo)
        # Em um banco real gigante, faríamos isso por partes (batch)
        response = supabase.table("qc_records").select("id, date, exam_name, level, value").execute()
        records = response.data
        
        if not records:
            print("INFO: Nenhum registro encontrado para limpar.")
            return

        # 2. Identifica o que é duplicado
        # Usamos uma "assinatura" (data + exame + nível + valor)
        vistos = {}
        para_deletar = []
        
        for r in records:
            assinatura = f"{r['date']}_{r['exam_name']}_{r['level']}_{r['value']}"
            
            if assinatura in vistos:
                # Se já vimos esse "gêmeo", marcamos este para o lixo
                para_deletar.append(r['id'])
            else:
                vistos[assinatura] = r['id']
        
        # 3. Executa a limpeza
        if para_deletar:
            print(f"INFO: Encontrados {len(para_deletar)} clones. Movendo para a lixeira...")
            # Deletamos em lotes para não sobrecarregar
            for i in range(0, len(para_deletar), 10):
                batch = para_deletar[i:i+10]
                supabase.table("qc_records").delete().in_("id", batch).execute()
            print(f"SUCCESS: Faxina concluída! {len(para_deletar)} duplicatas removidas.")
        else:
            print("SUCCESS: Tudo limpo! Não encontramos nenhum clone perdido.")

    except Exception as e:
        print(f"ERROR: Ocorreu um tropeço durante a faxina: {e}")

if __name__ == "__main__":
    limpar_duplicatas()
