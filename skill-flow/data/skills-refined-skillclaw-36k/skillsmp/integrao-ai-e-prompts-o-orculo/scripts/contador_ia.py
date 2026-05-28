import os
import sys
import io
from dotenv import load_dotenv

# Garante que a saída use UTF-8 para evitar erros com emojis no Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

def contar_moedas():
    """
    O Contador de Moedas:
    Monitora estimativas de custo baseado no volume de dados processados.
    """
    print("💰 [ORÁCULO] Relatório de Consumo (Estimado)")
    print("-" * 40)
    
    # Preços aproximados Gemini 1.5 Flash (Jan 2026)
    # Entrada: $0.075 / 1M tokens
    # Saída: $0.30 / 1M tokens (estimativa para exemplificar)
    
    # Simulação de dados de uso (em um caso real, leríamos de um log ou DB)
    uso_simulado = [
        {"data": "2026-01-21", "tokens_in": 15000, "tokens_out": 5000},
        {"data": "2026-01-22", "tokens_in": 3500, "tokens_out": 1200},
    ]
    
    total_custo = 0
    total_tokens = 0
    
    for dia in uso_simulado:
        custo_dia = (dia["tokens_in"] * 0.000000075) + (dia["tokens_out"] * 0.0000003)
        total_custo += custo_dia
        total_tokens += (dia["tokens_in"] + dia["tokens_out"])
        print(f"📅 {dia['data']}: {dia['tokens_in'] + dia['tokens_out']} tokens | Est. Custo: ${custo_dia:.5f}")

    print("-" * 40)
    print(f"📊 TOTAL ACUMULADO: ${total_custo:.5f}")
    print(f"🎫 TOTAL DE TOKENS: {total_tokens}")
    
    if total_custo > 0.50:
        print("⚠️ ALERTA: Consumo acima do esperado para o período de teste!")
    else:
        print("✅ Consumo dentro do orçamento operacional.")

if __name__ == "__main__":
    contar_moedas()
