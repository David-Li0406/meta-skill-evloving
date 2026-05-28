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

def treinar_prompt():
    """
    O Treinador de Prompts:
    Permite testar diferentes abordagens e ver como a IA se comporta.
    """
    print("🔮 [ORÁCULO] Iniciando Ensaio de IA...")
    
    # Exemplo de teste de prompt
    contexto = "Você é um assistente de laboratório de análises clínicas especializado em hematologia."
    pergunta = "Explique para um paciente de 70 anos o que significa um Hemoglobina de 10.5 g/dL de forma acolhedora."
    
    print(f"\n📝 Prompt de Teste:\n--- \n{pergunta}\n---")
    
    try:
        print("⏳ Consultando o Oráculo (Gemini 2.5 Flash)...")
        
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=f"Contexto: {contexto}\n\nPergunta: {pergunta}"
        )
        
        print("\n✨ Resposta do Oráculo:")
        print("--------------------------------------------------")
        print(response.text)
        print("--------------------------------------------------")
        
        print(f"\n💰 Tokens gastos (estimados): {len(response.text) // 4} tokens.")
        
    except Exception as e:
        print(f"❌ O Oráculo falhou na visão: {e}")

if __name__ == "__main__":
    treinar_prompt()
