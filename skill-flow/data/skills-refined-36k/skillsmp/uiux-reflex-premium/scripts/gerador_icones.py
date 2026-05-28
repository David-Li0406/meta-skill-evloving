import os
import sys
import io
from PIL import Image, ImageDraw, ImageFont

# Garante que a saída use UTF-8 para evitar erros com emojis no Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def gerar_icones(source_image=None):
    """
    O Gerador de Ícones:
    Cria favicon e apple-touch-icon a partir de uma imagem base.
    Se nenhuma imagem for fornecida, cria um placeholder.
    """
    print("🎨 [UI PREMIUM] Gerando ícones do aplicativo...")
    
    output_dir = "assets"
    # Ajuste para garantir que salvamos no lugar certo
    target_dir = os.path.join(os.getcwd(), "biodiagnostico_app", "assets")
    if os.path.exists(target_dir):
        output_dir = target_dir
    elif not os.path.exists(output_dir):
        os.makedirs(output_dir)

    sizes = {
        "favicon.ico": [(32, 32)], # Multi-size ICO support require specialized lib usually, saving as 32x32 basic
        "favicon.png": (32, 32),
        "apple-touch-icon.png": (180, 180),
        "android-chrome-192x192.png": (192, 192),
        "android-chrome-512x512.png": (512, 512)
    }
    
    # Se não tem source, cria um B (Biodiagnostico) verde
    img = None
    if source_image and os.path.exists(source_image):
        print(f"📸 Usando imagem base: {source_image}")
        img = Image.open(source_image)
    else:
        print("🎨 Nenhuma imagem base fornecida. Criando ícone padrão (Placeholder)...")
        img = Image.new('RGB', (512, 512), color='#4CAF50') # Color.PRIMARY
        d = ImageDraw.Draw(img)
        # Tenta desenhar um "B" ou Círculo
        d.ellipse([50, 50, 462, 462], fill='#1B5E20') # Color.DEEP
        # Texto centralizado simplificado (simulando logo)
        d.rectangle([200, 150, 312, 362], fill='#FFFFFF')
    
    for name, size in sizes.items():
        try:
            out_path = os.path.join(output_dir, name)
            
            if name.endswith(".ico"):
                # ICO simples
                icon_img = img.resize(size[0], Image.Resampling.LANCZOS)
                icon_img.save(out_path, format="ICO")
            else:
                icon_img = img.resize(size, Image.Resampling.LANCZOS)
                icon_img.save(out_path)
            
            print(f"✅ Gerado: {name}")
            
        except Exception as e:
            print(f"❌ Erro ao gerar {name}: {e}")
            
    print(f"✨ Ícones salvos em: {output_dir}")

if __name__ == "__main__":
    # Tenta achar um logo.png se existir, senão usa padrão
    logo_path = "logo.png" 
    if os.path.exists(logo_path):
        gerar_icones(logo_path)
    else:
        gerar_icones()
