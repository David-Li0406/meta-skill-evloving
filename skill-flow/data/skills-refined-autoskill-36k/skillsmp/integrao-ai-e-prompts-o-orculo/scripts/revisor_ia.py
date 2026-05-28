import os
import sys
import io
import re

# Garante que a saída use UTF-8 para evitar erros com emojis no Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def revisar_resposta(texto):
    """
    O Revisor de Respostas:
    Verifica se a resposta da IA atende critérios de qualidade e simplicidade.
    """
    print("🧐 [ORÁCULO] Revisando Resposta da IA...")
    
    erros = []
    
    # 1. Verifica tecnicismos exagerados (exemplo simples)
    termos_complexos = ["estratificação", "idiopático", "fisiopatologia", "morfologia celular"]
    encontrados = [t for t in termos_complexos if t.lower() in texto.lower()]
    
    if encontrados:
        erros.append(f"Uso de termos técnicos que podem confundir o paciente: {', '.join(encontrados)}")
    
    # 2. Verifica se a resposta é muito curta
    if len(texto) < 50:
        erros.append("A resposta parece curta demais para ser acolhedora.")
    
    # 3. Verifica alucinação de formato (ex: se deveria ser JSON mas veio texto)
    if texto.strip().startswith("{") and not texto.strip().endswith("}"):
        erros.append("Possível erro de formatação JSON (alucinação de estrutura).")

    if not erros:
        print("✅ Resposta aprovada! Linguagem clara e formato correto.")
    else:
        print("⚠️  Recomendação de Ajuste:")
        for erro in erros:
            print(f"  - {erro}")

if __name__ == "__main__":
    # Exemplo de texto para revisar
    exemplo = "O seu exame indica uma morfologia celular estável, porém com estratificação de risco idiopática."
    revisar_resposta(exemplo)
