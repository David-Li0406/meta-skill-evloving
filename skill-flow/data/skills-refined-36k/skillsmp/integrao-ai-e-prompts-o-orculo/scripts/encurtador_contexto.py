import os
import sys
import io

# Garante que a saída use UTF-8 para evitar erros com emojis no Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def encurtar_texto(texto, limite=500):
    """
    O Encurtador de Contexto:
    Remove partes irrelevantes de textos longos para economizar tokens.
    """
    print(f"✂️  [ORÁCULO] Encurtando contexto (Limite: {limite} caracteres)...")
    
    # Lógica simples de limpeza: remove linhas vazias e espaços duplos
    linhas = [l.strip() for l in texto.split("\n") if l.strip()]
    texto_limpo = " ".join(linhas)
    
    original_size = len(texto)
    
    if len(texto_limpo) > limite:
        texto_final = texto_limpo[:limite] + "..."
    else:
        texto_final = texto_limpo
        
    reduction = (1 - (len(texto_final) / original_size)) * 100 if original_size > 0 else 0
    
    print(f"📉 Redução de tamanho: {reduction:.1f}%")
    print(f"📄 Resultado final ({len(texto_final)} caracteres):")
    print("-" * 20)
    print(texto_final)
    print("-" * 20)
    
    return texto_final

if __name__ == "__main__":
    texto_longo = """
    ESTE É UM RELATÓRIO MUITO LONGO QUE CONTÉM MUITAS INFORMAÇÕES REPETITIVAS.
    MUITAS LINHAS VAZIAS ABAIXO.
    
    
    OS RESULTADOS SÃO IMPORTANTES, MAS A PALHA NÃO.
    
    REPETINDO: ESTE É UM RELATÓRIO MUITO LONGO QUE CONTÉM MUITAS INFORMAÇÕES REPETITIVAS.
    REPETINDO: ESTE É UM RELATÓRIO MUITO LONGO QUE CONTÉM MUITAS INFORMAÇÕES REPETITIVAS.
    """
    encurtar_texto(texto_longo, 100)
