import os
import sys
import io

# Garante que a saída use UTF-8 para evitar erros com emojis no Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def luminance(rgb):
    # Fórmula WCAG para luminância relativa
    a = [v / 255.0 for v in rgb]
    a = [((v + 0.055) / 1.055) ** 2.4 if v > 0.03928 else v / 12.92 for v in a]
    return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722

def contrast_ratio(l1, l2):
    newer = max(l1, l2)
    older = min(l1, l2)
    return (newer + 0.05) / (older + 0.05)

def verificar_contraste():
    """
    O Verificador de Contraste:
    Calcula se as cores primárias do sistema têm contraste suficiente com fundo branco/escuro.
    """
    print("👁️  [UI PREMIUM] Verificando acessibilidade (Contraste)...")
    
    # Definição manual das cores principais (idealmente leria de styles.py)
    # Baseado na descrição da Skill: PRIMARY #4CAF50, DEEP #1B5E20, BACKGROUND #F8F9FA
    
    palette = {
        "PRIMARY": "#4CAF50", # Verde
        "DEEP": "#1B5E20",    # Verde Escuro
        "BACKGROUND": "#F8F9FA", # Fundo Claro
        "TEXT_PRIMARY": "#1B5E20", # Assumindo igual ao DEEP para texto
        "PURE_WHITE": "#FFFFFF"
    }
    
    pairs_to_test = [
        ("PRIMARY", "PURE_WHITE", "Botão Primário (Texto Branco)"),
        ("DEEP", "BACKGROUND", "Título no Fundo"),
        ("PRIMARY", "BACKGROUND", "Texto Primário no Fundo"),
        ("DEEP", "PURE_WHITE", "Botão Escuro (Texto Branco)")
    ]
    
    print(f"🎨 Paleta Identificada: {palette}")
    print("-" * 40)
    
    for fg_name, bg_name, context in pairs_to_test:
        fg_hex = palette[fg_name]
        bg_hex = palette[bg_name]
        
        lum_fg = luminance(hex_to_rgb(fg_hex))
        lum_bg = luminance(hex_to_rgb(bg_hex))
        
        ratio = contrast_ratio(lum_fg, lum_bg)
        
        status = "✅ PASSOU" if ratio >= 4.5 else "⚠️  FALHOU (AA)"
        if ratio < 3.0:
            status = "❌ CRÍTICO"
            
        print(f"Contexto: {context}")
        print(f"   Cores: {fg_name} ({fg_hex}) vs {bg_name} ({bg_hex})")
        print(f"   Ratio: {ratio:.2f}:1 -> {status}")
        print("")
        
    print("ℹ️  Nota: O padrão WCAG AA exige razão mínima de 4.5:1 para texto normal e 3:1 para texto grande/interface.")

if __name__ == "__main__":
    verificar_contraste()
