#!/usr/bin/env python3
"""
Herramienta para capturar regiones alrededor del mouse con mapa para IA.

Controles:
  + / =     : Aumentar tamaño general (+1px)
  -         : Reducir tamaño general (-1px)
  x / X     : Aumentar/Reducir ancho (+/-1px)
  y / Y     : Aumentar/Reducir alto (+/-1px)
  f         : Modo FREEZE - congela pantalla, mueve el borde, click captura
  c / Space : Captura directa (sin freeze)
  r         : Resetear tamaño (200x200)
  q / ESC   : Salir

Formato archivo: {nombre}_{x}_{y}.png
Elementos: elements.json (formato JSON para agentes IA)
"""
import sys
import os
from datetime import datetime
import threading
import time
import signal
import csv
import re
import json

try:
    from pynput import keyboard
except ImportError:
    print("ERROR: pip install pynput")
    sys.exit(1)

try:
    from PIL import Image, ImageDraw, ImageTk, ImageGrab
    import tkinter as tk
except ImportError:
    print("ERROR: pip install Pillow")
    sys.exit(1)

try:
    import pyautogui
except ImportError:
    print("ERROR: pip install pyautogui")
    sys.exit(1)

# Config
DEFAULT_WIDTH = 200
DEFAULT_HEIGHT = 200
MIN_SIZE = 10
MAX_SIZE = 1000
SIZE_STEP = 1

# Parsear argumentos antes de definir rutas
import argparse
parser = argparse.ArgumentParser(description='Captura regiones de pantalla')
parser.add_argument('--data-dir', help='Directorio para guardar capturas y mapa')
_args, _ = parser.parse_known_args()

# Por defecto usar el skill global, si se especifica --data-dir usar esa ruta
if _args.data_dir:
    DATA_DIR = _args.data_dir
else:
    DATA_DIR = os.path.expanduser('~/.copilot/skills/macro-agent/data')

CAPTURES_DIR = os.path.join(DATA_DIR, 'captures')
ELEMENTS_FILE = os.path.join(DATA_DIR, 'elements.json')

def sanitize_filename(name):
    """Convierte un nombre a formato válido para archivo."""
    # Reemplazar espacios con guiones bajos
    name = name.strip().replace(' ', '_')
    # Remover caracteres especiales
    name = re.sub(r'[^\w\-]', '', name)
    # Limitar longitud
    return name[:50] if name else 'captura'


# ============================================
# FUNCIONES PARA ELEMENTS.JSON
# ============================================

def load_elements() -> dict:
    """Carga elementos desde JSON."""
    if not os.path.exists(ELEMENTS_FILE):
        return {}
    with open(ELEMENTS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_elements(elements: dict):
    """Guarda elementos en JSON."""
    with open(ELEMENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(elements, f, indent=2, ensure_ascii=False)


def get_element_names() -> list:
    """Retorna lista de nombres de elementos existentes."""
    elements = load_elements()
    return list(elements.keys())


def add_image_to_element(element_name: str, image_file: str, description: str = "", tags: list = None):
    """Agrega una imagen a un elemento existente o crea uno nuevo."""
    elements = load_elements()
    name_key = element_name.lower().replace(' ', '_')
    
    if name_key in elements:
        # Agregar imagen a elemento existente
        if image_file not in elements[name_key]['images']:
            elements[name_key]['images'].append(image_file)
    else:
        # Crear nuevo elemento
        elements[name_key] = {
            "name": name_key,
            "description": description,
            "images": [image_file],
            "tags": tags or []
        }
    
    save_elements(elements)
    return elements[name_key]


def count_elements() -> int:
    """Cuenta elementos en JSON."""
    return len(load_elements())


def ask_capture_info():
    """Pide nombre y descripción al usuario. Permite agregar a elemento existente."""
    result = {'name': None, 'description': None, 'tags': None, 'is_new': True}
    
    root = tk.Tk()
    root.title("Información de la captura")
    root.attributes('-topmost', True)
    root.geometry("550x400")
    root.configure(bg='#2d2d2d')
    
    # Centrar ventana
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - 275
    y = (root.winfo_screenheight() // 2) - 200
    root.geometry(f"+{x}+{y}")
    
    # Obtener elementos existentes
    existing_elements = get_element_names()
    
    # === Selector: Nuevo o Existente ===
    mode_var = tk.StringVar(value="new")
    
    mode_frame = tk.Frame(root, bg='#2d2d2d')
    mode_frame.pack(pady=(15, 5))
    
    rb_new = tk.Radiobutton(
        mode_frame, text="Crear nuevo elemento", variable=mode_var, value="new",
        bg='#2d2d2d', fg='white', selectcolor='#444444', font=('Sans', 10),
        activebackground='#2d2d2d', activeforeground='white'
    )
    rb_new.pack(side=tk.LEFT, padx=10)
    
    rb_existing = tk.Radiobutton(
        mode_frame, text="Agregar a existente", variable=mode_var, value="existing",
        bg='#2d2d2d', fg='white', selectcolor='#444444', font=('Sans', 10),
        activebackground='#2d2d2d', activeforeground='white'
    )
    rb_existing.pack(side=tk.LEFT, padx=10)
    
    # === Frame para elemento existente ===
    existing_frame = tk.Frame(root, bg='#2d2d2d')
    
    lbl_existing = tk.Label(
        existing_frame, text="Seleccionar elemento:",
        bg='#2d2d2d', fg='white', font=('Sans', 11)
    )
    lbl_existing.pack(pady=(5, 5))
    
    # Listbox con elementos
    listbox_frame = tk.Frame(existing_frame, bg='#2d2d2d')
    listbox_frame.pack(pady=5)
    
    scrollbar = tk.Scrollbar(listbox_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    listbox = tk.Listbox(
        listbox_frame, font=('Sans', 10), width=45, height=6,
        yscrollcommand=scrollbar.set
    )
    listbox.pack(side=tk.LEFT)
    scrollbar.config(command=listbox.yview)
    
    for elem in existing_elements:
        listbox.insert(tk.END, elem)
    
    # === Frame para nuevo elemento ===
    new_frame = tk.Frame(root, bg='#2d2d2d')
    
    # Nombre
    lbl_name = tk.Label(
        new_frame, text="Nombre (será el nombre del archivo):",
        bg='#2d2d2d', fg='white', font=('Sans', 11)
    )
    lbl_name.pack(pady=(5, 5))
    
    hint_name = tk.Label(
        new_frame, text="(ej: btn_guardar, icono_chrome, campo_busqueda)",
        bg='#2d2d2d', fg='#888888', font=('Sans', 9)
    )
    hint_name.pack()
    
    entry_name = tk.Entry(new_frame, font=('Sans', 12), width=45)
    entry_name.pack(pady=5)
    
    # Descripción
    lbl_desc = tk.Label(
        new_frame, text="Descripción (para que la IA entienda qué es):",
        bg='#2d2d2d', fg='white', font=('Sans', 11)
    )
    lbl_desc.pack(pady=(10, 5))
    
    entry_desc = tk.Entry(new_frame, font=('Sans', 12), width=45)
    entry_desc.pack(pady=5)
    
    # Tags
    lbl_tags = tk.Label(
        new_frame, text="Tags (separados por coma, para búsqueda):",
        bg='#2d2d2d', fg='white', font=('Sans', 11)
    )
    lbl_tags.pack(pady=(10, 5))
    
    hint_tags = tk.Label(
        new_frame, text="(ej: browser, button, whatsapp)",
        bg='#2d2d2d', fg='#888888', font=('Sans', 9)
    )
    hint_tags.pack()
    
    entry_tags = tk.Entry(new_frame, font=('Sans', 12), width=45)
    entry_tags.pack(pady=5)
    
    def update_mode(*args):
        """Muestra/oculta frames según modo seleccionado."""
        if mode_var.get() == "new":
            existing_frame.pack_forget()
            new_frame.pack(pady=10)
            entry_name.focus_set()
        else:
            new_frame.pack_forget()
            existing_frame.pack(pady=10)
            listbox.focus_set()
    
    mode_var.trace('w', update_mode)
    new_frame.pack(pady=10)  # Mostrar nuevo por defecto
    entry_name.focus_set()
    
    def on_submit(event=None):
        if mode_var.get() == "new":
            result['name'] = entry_name.get().strip()
            result['description'] = entry_desc.get().strip()
            tags_str = entry_tags.get().strip()
            result['tags'] = [t.strip() for t in tags_str.split(',') if t.strip()] if tags_str else []
            result['is_new'] = True
        else:
            selection = listbox.curselection()
            if selection:
                result['name'] = listbox.get(selection[0])
                result['is_new'] = False
            else:
                return  # No hay selección
        root.destroy()
        
    def on_cancel(event=None):
        root.destroy()
    
    # Botones
    btn_frame = tk.Frame(root, bg='#2d2d2d')
    btn_frame.pack(pady=15, side=tk.BOTTOM)
    
    btn_ok = tk.Button(btn_frame, text="Guardar", command=on_submit, width=12)
    btn_ok.pack(side=tk.LEFT, padx=5)
    
    btn_cancel = tk.Button(btn_frame, text="Cancelar", command=on_cancel, width=12)
    btn_cancel.pack(side=tk.LEFT, padx=5)
    
    # Bindings
    entry_name.bind('<Return>', lambda e: entry_desc.focus_set())
    entry_desc.bind('<Return>', lambda e: entry_tags.focus_set())
    entry_tags.bind('<Return>', on_submit)
    listbox.bind('<Double-1>', on_submit)
    root.bind('<Escape>', on_cancel)
    
    root.mainloop()
    
    return result['name'], result['description'], result['tags'], result['is_new']


class FreezeCapture:
    """Congela la pantalla y permite seleccionar región con borde visual."""
    
    def __init__(self, width, height, on_done):
        self.width = width
        self.height = height
        self.on_done = on_done
        self.result = None
        self.last_x = 0
        self.last_y = 0
        
    def run(self):
        """Ejecuta el modo freeze."""
        # Tomar screenshot
        screenshot = ImageGrab.grab()
        
        # Crear ventana
        root = tk.Tk()
        root.attributes('-fullscreen', True)
        root.attributes('-topmost', True)
        root.config(cursor="crosshair")
        
        # Canvas con el screenshot
        photo = ImageTk.PhotoImage(screenshot)
        canvas = tk.Canvas(root, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        
        # Elementos del borde
        rect_id = [None]
        cross_h = [None]
        cross_v = [None]
        
        # Info bar - ahora movible
        info_x = [10]
        info_y = [10]
        dragging_info = [False]
        drag_offset = [0, 0]
        
        info = tk.Label(
            root, 
            text=f"Región: {self.width}x{self.height} | +/-=Tamaño | x/X y/Y=Ejes | Click=Capturar | ESC=Cancelar",
            bg='#333333', fg='white', font=('Mono', 11), padx=10, pady=5,
            cursor="fleur"  # Cursor de mover
        )
        info.place(x=info_x[0], y=info_y[0])
        
        # Funciones para mover la barra de info
        def info_start_drag(event):
            dragging_info[0] = True
            drag_offset[0] = event.x
            drag_offset[1] = event.y
        
        def info_drag(event):
            if dragging_info[0]:
                new_x = info.winfo_x() + event.x - drag_offset[0]
                new_y = info.winfo_y() + event.y - drag_offset[1]
                info.place(x=new_x, y=new_y)
                info_x[0] = new_x
                info_y[0] = new_y
        
        def info_stop_drag(event):
            dragging_info[0] = False
        
        # Bindings para mover la barra
        info.bind('<Button-1>', info_start_drag)
        info.bind('<B1-Motion>', info_drag)
        info.bind('<ButtonRelease-1>', info_stop_drag)
        
        # Estado
        captured = [False]
        capture_data = [None, None, None]  # image, x, y
        
        def draw_border(x, y):
            """Dibuja el borde en la posición dada."""
            self.last_x = x
            self.last_y = y
            
            half_w = self.width // 2
            half_h = self.height // 2
            
            # Borrar anterior
            if rect_id[0]: canvas.delete(rect_id[0])
            if cross_h[0]: canvas.delete(cross_h[0])
            if cross_v[0]: canvas.delete(cross_v[0])
            
            # Dibujar borde
            rect_id[0] = canvas.create_rectangle(
                x - half_w, y - half_h, 
                x + half_w, y + half_h,
                outline='#FF0000', width=2
            )
            
            # Cruz central
            cross_h[0] = canvas.create_line(x-12, y, x+12, y, fill='#FF0000', width=1)
            cross_v[0] = canvas.create_line(x, y-12, x, y+12, fill='#FF0000', width=1)
            
            info.config(text=f"({x}, {y}) | Región: {self.width}x{self.height} | +/-=Tamaño | x/X y/Y=Ejes | Click=Capturar")
        
        def on_motion(event):
            draw_border(event.x, event.y)
            
        def on_key(event):
            """Maneja teclas en modo freeze."""
            key = event.char
            keysym = event.keysym
            
            if key in ('+', '='):
                self.width = min(self.width + SIZE_STEP, MAX_SIZE)
                self.height = min(self.height + SIZE_STEP, MAX_SIZE)
                draw_border(self.last_x, self.last_y)
            elif key == '-':
                self.width = max(self.width - SIZE_STEP, MIN_SIZE)
                self.height = max(self.height - SIZE_STEP, MIN_SIZE)
                draw_border(self.last_x, self.last_y)
            elif key == 'x':
                self.width = min(self.width + SIZE_STEP, MAX_SIZE)
                draw_border(self.last_x, self.last_y)
            elif key == 'X':
                self.width = max(self.width - SIZE_STEP, MIN_SIZE)
                draw_border(self.last_x, self.last_y)
            elif key == 'y':
                self.height = min(self.height + SIZE_STEP, MAX_SIZE)
                draw_border(self.last_x, self.last_y)
            elif key == 'Y':
                self.height = max(self.height - SIZE_STEP, MIN_SIZE)
                draw_border(self.last_x, self.last_y)
            
        def on_click(event):
            x, y = event.x, event.y
            half_w = self.width // 2
            half_h = self.height // 2
            
            # Recortar región del screenshot
            region = screenshot.crop((x - half_w, y - half_h, x + half_w, y + half_h))
            capture_data[0] = region
            capture_data[1] = x
            capture_data[2] = y
            captured[0] = True
            root.destroy()
            
        def on_cancel(event=None):
            root.destroy()
            
        canvas.bind('<Motion>', on_motion)
        canvas.bind('<Button-1>', on_click)
        root.bind('<Escape>', on_cancel)
        root.bind('<q>', on_cancel)
        root.bind('<Key>', on_key)  # Captura todas las teclas
        
        root.mainloop()
        
        # Callback con resultado (incluye nuevo tamaño)
        if captured[0] and self.on_done:
            self.on_done(capture_data[0], capture_data[1], capture_data[2], self.width, self.height)
        elif self.on_done:
            # Aunque no capture, devuelve el nuevo tamaño
            self.on_done(None, 0, 0, self.width, self.height)


class RegionCapture:
    """Capturador de regiones."""
    
    def __init__(self):
        self.width = DEFAULT_WIDTH
        self.height = DEFAULT_HEIGHT
        self.running = True
        self.capture_count = 0
        self.freeze_active = False
        
        os.makedirs(CAPTURES_DIR, exist_ok=True)
        
        # Keyboard listener
        self.kb_listener = keyboard.Listener(on_press=self.on_key)
        self.kb_listener.start()
        
        # Update thread
        self.update_thread = threading.Thread(target=self.update_loop, daemon=True)
        self.update_thread.start()
        
    def update_loop(self):
        """Muestra info en terminal."""
        while self.running:
            if not self.freeze_active:
                x, y = pyautogui.position()
                print(
                    f"\r  Mouse: ({x:4d}, {y:4d}) | "
                    f"Región: {self.width}x{self.height} | "
                    f"Capturas: {self.capture_count}    ",
                    end='', flush=True
                )
            time.sleep(0.1)
            
    def on_key(self, key):
        """Maneja teclas."""
        if self.freeze_active:
            return
            
        try:
            if hasattr(key, 'char') and key.char:
                c = key.char
                
                if c in ('+', '='):
                    self.width = min(self.width + SIZE_STEP, MAX_SIZE)
                    self.height = min(self.height + SIZE_STEP, MAX_SIZE)
                    
                elif c == '-':
                    self.width = max(self.width - SIZE_STEP, MIN_SIZE)
                    self.height = max(self.height - SIZE_STEP, MIN_SIZE)
                    
                elif c == 'x':
                    self.width = min(self.width + SIZE_STEP, MAX_SIZE)
                elif c == 'X':
                    self.width = max(self.width - SIZE_STEP, MIN_SIZE)
                    
                elif c == 'y':
                    self.height = min(self.height + SIZE_STEP, MAX_SIZE)
                elif c == 'Y':
                    self.height = max(self.height - SIZE_STEP, MIN_SIZE)
                    
                elif c == 'f':
                    self.start_freeze()
                    
                elif c in ('c', 'C'):
                    self.capture_direct()
                    
                elif c in ('r', 'R'):
                    self.width = DEFAULT_WIDTH
                    self.height = DEFAULT_HEIGHT
                    print(f"\n✓ Reset: {DEFAULT_WIDTH}x{DEFAULT_HEIGHT}")
                    
                elif c in ('q', 'Q'):
                    self.quit()
                    return False
                    
            elif key == keyboard.Key.space:
                self.capture_direct()
            elif key == keyboard.Key.esc:
                self.quit()
                return False
                
        except Exception as e:
            pass
            
    def start_freeze(self):
        """Inicia modo freeze en thread separado."""
        print("\n🔒 FREEZE - +/-=Tamaño | x/X=Ancho | y/Y=Alto | Click=Capturar | ESC=Cancelar")
        self.freeze_active = True
        
        def run_freeze():
            freeze = FreezeCapture(self.width, self.height, self.on_freeze_done)
            freeze.run()
            self.freeze_active = False
            
        # Ejecutar en thread del main (tkinter lo necesita)
        threading.Thread(target=run_freeze).start()
        
    def on_freeze_done(self, image, x, y, new_width, new_height):
        """Callback cuando freeze termina - actualiza tamaño y guarda si hay imagen."""
        # Actualizar tamaño (por si cambió en freeze)
        self.width = new_width
        self.height = new_height
        
        # Guardar si hay captura
        if image is not None:
            self.save_capture(image, x, y)
        
    def capture_direct(self):
        """Captura directa sin freeze."""
        x, y = pyautogui.position()
        half_w = self.width // 2
        half_h = self.height // 2
        
        try:
            img = ImageGrab.grab(bbox=(x-half_w, y-half_h, x+half_w, y+half_h))
            self.save_capture(img, x, y)
        except Exception as e:
            print(f"\n✗ Error: {e}")
            
    def save_capture(self, image, x, y):
        """Guarda la captura y agrega al JSON de elementos."""
        if image is None:
            return
        
        # Guardar imagen temporalmente
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        temp_filename = f"temp_{timestamp}.png"
        temp_filepath = os.path.join(CAPTURES_DIR, temp_filename)
        image.save(temp_filepath)
        
        print(f"\n📷 Captura tomada en ({x}, {y})")
        print("📝 Selecciona elemento o crea uno nuevo...")
        
        # Pedir nombre y descripción
        name, description, tags, is_new = ask_capture_info()
        
        # Si canceló, eliminar imagen temporal
        if not name:
            os.remove(temp_filepath)
            print("✗ Captura cancelada\n")
            return
        
        # Renombrar archivo con el nombre dado
        safe_name = sanitize_filename(name)
        final_filename = f"{safe_name}_{timestamp}.png"
        final_filepath = os.path.join(CAPTURES_DIR, final_filename)
        
        os.rename(temp_filepath, final_filepath)
        
        self.capture_count += 1
        
        # Agregar al JSON
        if is_new:
            # Crear nuevo elemento
            add_image_to_element(name, final_filename, description, tags)
            print(f"✓ #{self.capture_count}: Nuevo elemento '{name}' creado")
        else:
            # Agregar imagen a elemento existente
            add_image_to_element(name, final_filename)
            print(f"✓ #{self.capture_count}: Imagen agregada a '{name}'")
        
        total_elements = count_elements()
        print(f"✓ Guardado: {final_filename}")
        print(f"✓ elements.json actualizado ({total_elements} elementos)\n")
        
    def quit(self):
        """Sale."""
        self.running = False
        total_elements = count_elements()
        print(f"\n\n✓ {self.capture_count} capturas en esta sesión")
        print(f"  Carpeta: {CAPTURES_DIR}")
        print(f"✓ elements.json ({total_elements} elementos)")
        print(f"  {ELEMENTS_FILE}\n")
        self.kb_listener.stop()
        os._exit(0)
        
    def run(self):
        """Ejecuta."""
        try:
            self.kb_listener.join()
        except:
            self.quit()


def main():
    print("=" * 60)
    print("  REGION CAPTURE + MAPA IA (JSON)")
    print("=" * 60)
    print("\n  + / -     Tamaño (±1px)")
    print("  x / X     Ancho (±1px)")
    print("  y / Y     Alto (±1px)")
    print("  f         FREEZE (congela pantalla + borde visual)")
    print("  c/Space   Captura directa")
    print("  r         Reset (200x200)")
    print("  q/ESC     Salir")
    print(f"\n  Carpeta: {CAPTURES_DIR}")
    print(f"  Elementos: {ELEMENTS_FILE}")
    
    # Mostrar elementos existentes
    total = count_elements()
    if total > 0:
        print(f"\n  📍 Elementos registrados: {total}")
    
    print("-" * 60 + "\n")
    
    signal.signal(signal.SIGINT, lambda s,f: os._exit(0))
    
    app = RegionCapture()
    app.run()


if __name__ == '__main__':
    main()
