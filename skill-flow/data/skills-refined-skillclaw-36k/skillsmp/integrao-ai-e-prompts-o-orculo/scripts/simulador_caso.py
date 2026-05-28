import os
import sys
import io
from google import genai
from dotenv import load_dotenv

# Garante que a saída use UTF-8 para evitar erros com emojis no Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

# Configuração da API
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("❌ Erro: GEMINI_API_KEY não encontrada no .env")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)

def simular_paciente():
    """
    O Simulador de Paciente:
    Gera um caso clínico fictício para testar a lógica do sistema.
    """
    print("🧪 [ORÁCULO] Gerando Caso de Teste...")
    
    try:
        prompt = """
        Gere um perfil de paciente fictício para teste de laboratório clínico.
        Inclua: Nome, Idade, Sexo, e uma lista de 3 resultados de exames alterados (ex: Glicose, Colesterol, Hemoglobina).
        O formato deve ser uma descrição simples para um relatório.
        """
        
        print("⏳ Simulando paciente via Gemini 2.5 Flash...")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        print("\n👤 Paciente Simulado:")
        print("-" * 30)
        print(response.text)
        print("-" * 30)
        print("\n✅ Caso gerado para uso em testes de QA.")
        
    except Exception as e:
        print(f"❌ Falha ao criar paciente virtual: {e}")

if __name__ == "__main__":
    simular_paciente()
