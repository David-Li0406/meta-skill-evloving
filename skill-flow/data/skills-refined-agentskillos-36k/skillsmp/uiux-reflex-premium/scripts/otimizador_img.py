import os
import sys
import io
from PIL import Image

# Garante que a saída use UTF-8 para evitar erros com emojis no Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def otimizar_imagens(target_dir="assets"):
    """
    O Otimizador de Imagens:
    Reduz o tamanho de arquivos PNG/JPG para web.
    """
    print("🖼️  [UI PREMIUM] Otimizando assets visuais...")
    
    start_dir = os.path.join(os.getcwd(), target_dir)
    if not os.path.exists(start_dir):
        # Tenta achar a pasta assets na raiz ou dentro do app
        alternatives = [
            os.path.join(os.getcwd(), "assets"),
            os.path.join(os.getcwd(), "biodiagnostico_app", "assets")
        ]
        found = False
        for alt in alternatives:
            if os.path.exists(alt):
                start_dir = alt
                found = True
                break
        
        if not found:
            print(f"⚠️ Pasta '{target_dir}' não encontrada. Nada para otimizar.")
            return

    count = 0
    saved_space = 0
    
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                filepath = os.path.join(root, file)
                
                try:
                    original_size = os.path.getsize(filepath)
                    
                    # Abre e otimiza
                    with Image.open(filepath) as img:
                        # Se for muito grande, redimensiona (opcional, aqui focado em compressão)
                        max_width = 1920
                        if img.width > max_width:
                            ratio = max_width / img.width
                            new_height = int(img.height * ratio)
                            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                        
                        # Salva otimizado em buffer para comparar
                        buffer = io.BytesIO()
                        fmt = "PNG" if file.lower().endswith(".png") else "JPEG"
                        
                        # Parametros de otimização
                        if fmt == "JPEG":
                            img.save(buffer, format=fmt, quality=85, optimize=True)
                        else:
                            img.save(buffer, format=fmt, optimize=True, compress_level=9)
                            
                        new_size = buffer.tell()
                        
                        if new_size < original_size:
                            # Sobrescreve apenas se houve ganho
                            with open(filepath, "wb") as f:
                                f.write(buffer.getvalue())
                            
                            diff = original_size - new_size
                            saved_space += diff
                            count += 1
                            print(f"✅ Otimizado: {file} (-{diff/1024:.1f} KB)")
                        else:
                            print(f"⏭️  Ignorado: {file} (já está otimizado)")
                            
                except Exception as e:
                    print(f"❌ Falha ao processar {file}: {e}")

    if count > 0:
        print(f"✨ Concluído! {count} imagens otimizadas.")
        print(f"📉 Espaço total economizado: {saved_space/1024:.2f} KB")
    else:
        print("🤷 Nenhuma imagem precisou de otimização.")

if __name__ == "__main__":
    otimizar_imagens()
