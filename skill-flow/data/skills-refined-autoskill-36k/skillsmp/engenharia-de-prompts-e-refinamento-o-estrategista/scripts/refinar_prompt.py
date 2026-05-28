import os
import sys
import io
import argparse
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

def refinar_prompt(input_text):
    """
    O Estrategista:
    Reescreve um prompt simples aplicando as melhores práticas de Engenharia de Prompt.
    """
    print("🧠 [ESTRATEGISTA] Analisando sua solicitação e desenhando a melhor estratégia...")
    
    meta_prompt = f"""
    Você é um Engenheiro de Prompts Sênior e Especialista em LLMs (Large Language Models).
    Sua missão é reescrever a solicitação do usuário abaixo para torná-la PERFEITA, seguindo as melhores práticas de 'Prompt Engineering'.
    
    A solicitação original do usuário é:
    "{input_text}"
    
    REGRAS PARA A REESCRITA (Use o framework CREFO):
    1. CONTEXTO/PERSONA: Defina quem a IA deve ser (ex: Senior Python Dev, Data Scientist, UX Designer).
    2. OBJETIVO CLARO: Defina a meta em uma frase direta.
    3. RESTRIÇÕES ESPECÍFICAS: Adicione regras de segurança, estilo de código, ou proibições (ex: "Não use bibliotecas obsoletas").
    4. PASSO A PASSO (Chain of Thought): Se a tarefa for complexa, peça para a IA pensar passo a passo.
    5. FORMATO DE SAÍDA: Especifique exatamente como quer a resposta (JSON, Markdown, Código comentado).
    
    SAÍDA ESPERADA:
    Retorne APENAS o prompt reescrito, pronto para ser copiado e colado. 
    Use formatação Markdown para deixar o prompt organizado (Bullets, Negrito).
    O tom deve ser profissional e técnico.
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=meta_prompt
        )
        
        print("\n✨ PROMPT REFINADO (Copie e use):")
        print("=" * 60)
        print(response.text)
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ O Estrategista falhou: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Refinador de Prompts com IA")
    parser.add_argument("prompt", nargs="*", help="O texto do prompt que você quer melhorar")
    args = parser.parse_args()
    
    # Se não passou argumento, tenta pegar input interativo ou uma string default
    user_input = " ".join(args.prompt) if args.prompt else ""
    
    if not user_input:
        print("📝 Digite o prompt que você quer melhorar (Pressione Enter para enviar):")
        user_input = input("> ")
    
    if user_input:
        refinar_prompt(user_input)
    else:
        print("⚠️ Nenhum prompt fornecido.")
