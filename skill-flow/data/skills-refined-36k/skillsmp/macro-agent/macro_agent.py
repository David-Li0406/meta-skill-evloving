#!/usr/bin/env python3
"""
Macro Agent Skill - Control de macros de escritorio para agentes IA.

Funcionalidades:
- Buscar elementos en el mapa de pantalla
- Mover mouse (siempre smooth)
- Clicks, doble click, drag
- Escribir texto, teclas, hotkeys
- Crear y ejecutar secuencias de acciones
"""
import sys
import os
import json
import time
import argparse
import glob
import unicodedata
import base64
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple

# Rutas - Usar directorio del skill global
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SKILL_DIR, "data")
ELEMENTS_FILE = os.path.join(DATA_DIR, "elements.json")
CAPTURES_DIR = os.path.join(DATA_DIR, "captures")
SEQUENCES_DIR = os.path.join(DATA_DIR, "sequences")

# Sound manager (optional audio feedback)
try:
    from sounds_manager import (
        sound_click, sound_double_click, sound_scroll, sound_type, 
        sound_key, sound_hotkey, sound_success, sound_error, sound_screenshot,
        enable_sounds, disable_sounds, sounds_enabled, set_volume, get_status as get_sound_status
    )
    HAS_SOUNDS = True
except ImportError:
    HAS_SOUNDS = False
    def sound_click(): pass
    def sound_double_click(): pass
    def sound_scroll(): pass
    def sound_type(length=0): pass
    def sound_key(): pass
    def sound_hotkey(): pass
    def sound_success(): pass
    def sound_error(): pass
    def sound_screenshot(): pass
    def enable_sounds(): return "Sounds not available"
    def disable_sounds(): return "Sounds not available"
    def sounds_enabled(): return False
    def set_volume(v): return "Sounds not available"
    def get_sound_status(): return {"enabled": False, "available": False}

# Ruta al proyecto original (para region_capture.py)
MACRO_AGENT_PROJECT = "/home/neo/ai/aibias/macro_agent"

# Asegurar que existen los directorios
os.makedirs(CAPTURES_DIR, exist_ok=True)
os.makedirs(SEQUENCES_DIR, exist_ok=True)

try:
    import pyautogui
    import cv2
    import numpy as np
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.05
    HAS_PYAUTOGUI = True
    HAS_CV2 = True
except ImportError:
    HAS_PYAUTOGUI = False
    HAS_CV2 = False


def output(data: Dict):
    """Imprime resultado como JSON."""
    print(json.dumps(data, ensure_ascii=False, indent=2))


def error(message: str):
    """Imprime error como JSON."""
    output({"success": False, "error": message})
    sys.exit(1)


# ============================================
# FUNCIONES DE ELEMENTOS (JSON)
# ============================================

def load_elements() -> Dict[str, Dict]:
    """Carga los elementos desde JSON."""
    if not os.path.exists(ELEMENTS_FILE):
        return {}
    
    with open(ELEMENTS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_elements(elements: Dict[str, Dict]):
    """Guarda los elementos en JSON."""
    with open(ELEMENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(elements, f, indent=2, ensure_ascii=False)


def get_element(name: str) -> Optional[Dict]:
    """Obtiene un elemento por nombre exacto o parcial."""
    elements = load_elements()
    name_lower = name.lower()
    
    # Primero buscar exacto
    if name_lower in elements:
        return elements[name_lower]
    
    # Buscar por nombre parcial
    for key, elem in elements.items():
        if name_lower in key.lower():
            return elem
    
    # Buscar por tags
    for key, elem in elements.items():
        tags = elem.get('tags', [])
        if any(name_lower in tag.lower() for tag in tags):
            return elem
    
    return None


def add_element(name: str, description: str = "", images: List[str] = None, 
                tags: List[str] = None) -> Dict:
    """Agrega o actualiza un elemento."""
    elements = load_elements()
    
    name_key = name.lower().replace(' ', '_')
    
    elements[name_key] = {
        "name": name_key,
        "description": description,
        "images": images or [],
        "tags": tags or []
    }
    
    save_elements(elements)
    return elements[name_key]


def add_image_to_element(name: str, image_file: str) -> Optional[Dict]:
    """Agrega una imagen a un elemento existente o crea uno nuevo."""
    elements = load_elements()
    name_key = name.lower().replace(' ', '_')
    
    if name_key in elements:
        if image_file not in elements[name_key]['images']:
            elements[name_key]['images'].append(image_file)
    else:
        # Crear nuevo elemento
        elements[name_key] = {
            "name": name_key,
            "description": "",
            "images": [image_file],
            "tags": []
        }
    
    save_elements(elements)
    return elements[name_key]


def find_element(name: str) -> Optional[Dict]:
    """Busca elemento por nombre exacto o parcial usando JSON."""
    return get_element(name)


def find_element_on_screen(name: str, confidence: float = 0.8) -> Tuple[Optional[Tuple[int, int]], str, Dict]:
    """
    Busca elemento por imagen en pantalla (template matching).
    SIEMPRE usa búsqueda por imagen, NUNCA coordenadas fijas.
    
    Primero busca en elements.json para obtener las imágenes válidas y exclusiones.
    Si no existe en JSON, busca por patrón de nombre en captures/.
    
    Si hay múltiples coincidencias, retorna la que tenga mayor score de confianza.
    
    Args:
        name: Nombre del elemento a buscar
        confidence: Umbral de confianza (0.0 a 1.0)
    
    Retorna: (coordenadas, método_usado, info_adicional)
    - Si encuentra por imagen: ((x, y), 'image', {matches_found, best_score, images_tested})
    - Si no encuentra: (None, 'not_found', {matches_found, images_tested})
    """
    info = {
        "matches_found": 0,
        "best_score": 0.0,
        "images_tested": 0,
        "all_matches": [],
        "element_config": None
    }
    
    if not HAS_PYAUTOGUI:
        return None, 'no_pyautogui', info
    
    if not HAS_CV2:
        return None, 'no_cv2', info
    
    # Normalizar nombre
    name_normalized = name.replace(' ', '_').lower()
    
    # ============================================
    # PASO 1: Buscar configuración en elements.json
    # ============================================
    element = get_element(name)
    
    image_files = []
    
    if element:
        info["element_config"] = element['name']
        # Usar imágenes definidas en el elemento
        for img in element.get('images', []):
            img_path = os.path.join(CAPTURES_DIR, img)
            if os.path.exists(img_path):
                image_files.append(img_path)
    
    # Si no hay imágenes del JSON, buscar por patrón (fallback)
    if not image_files:
        patterns = [
            os.path.join(CAPTURES_DIR, f"{name_normalized}.png"),
            os.path.join(CAPTURES_DIR, f"{name_normalized}_*.png"),
            os.path.join(CAPTURES_DIR, f"{name.replace(' ', '_')}.png"),
            os.path.join(CAPTURES_DIR, f"{name.replace(' ', '_')}_*.png"),
        ]
        
        # Buscar coincidencias parciales si el nombre tiene palabras
        words = name_normalized.split('_')
        if len(words) > 1:
            all_files = glob.glob(os.path.join(CAPTURES_DIR, "*.png"))
            for f in all_files:
                fname = os.path.basename(f).lower()
                if all(word in fname for word in words):
                    patterns.append(f)
        
        for pattern in patterns:
            image_files.extend(glob.glob(pattern))
        
        # Eliminar duplicados
        image_files = list(dict.fromkeys(image_files))
    
    info["images_tested"] = len(image_files)
    
    # Capturar screenshot de pantalla completa
    try:
        screenshot = pyautogui.screenshot()
        screen_np = np.array(screenshot)
        # Convertir de RGB a BGR (formato OpenCV)
        screen_bgr = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)
    except Exception as e:
        return None, 'screenshot_error', info
    
    # ============================================
    # PASO 2: Buscar elemento objetivo
    # ============================================
    best_match = None
    best_confidence = 0
    
    for img_path in image_files:
        try:
            # Cargar template a COLOR para mayor precisión
            template = cv2.imread(img_path, cv2.IMREAD_COLOR)
            if template is None:
                continue
            
            h, w = template.shape[:2]
            
            # Realizar template matching a COLOR
            result = cv2.matchTemplate(screen_bgr, template, cv2.TM_CCOEFF_NORMED)
            
            # Encontrar todas las ubicaciones que superen el threshold
            locations = np.where(result >= confidence)
            
            # Contar cuántos matches encontramos para esta imagen
            matches_for_this_image = len(locations[0])
            if matches_for_this_image > 0:
                info["matches_found"] += matches_for_this_image
            
            # Para cada ubicación, obtener el score exacto
            for pt in zip(*locations[::-1]):  # [::-1] invierte para tener (x, y)
                match_confidence = result[pt[1], pt[0]]
                
                # Calcular centro del match
                center_x = int(pt[0] + w // 2)
                center_y = int(pt[1] + h // 2)
                
                # Registrar todos los matches
                info["all_matches"].append({
                    "x": center_x,
                    "y": center_y,
                    "score": float(match_confidence),
                    "image": os.path.basename(img_path)
                })
                
                # Si esta coincidencia es mejor que la mejor encontrada
                if match_confidence > best_confidence:
                    best_confidence = float(match_confidence)
                    best_match = (center_x, center_y)
        
        except Exception as e:
            # Continuar con siguiente imagen si hay error
            continue
    
    # Ordenar todos los matches por score (descendente)
    info["all_matches"].sort(key=lambda x: x["score"], reverse=True)
    info["best_score"] = best_confidence
    
    if best_match:
        return best_match, 'image', info
    
    # NO hay fallback a CSV - solo búsqueda por imagen
    # Si no encuentra la imagen, retorna not_found
    return None, 'not_found', info


def search_elements(query: str) -> List[Dict]:
    """Busca elementos por texto en nombre, descripción o tags."""
    elements = load_elements()
    query_lower = query.lower()
    results = []
    
    for key, elem in elements.items():
        score = 0
        nombre = elem['name'].lower()
        desc = elem.get('description', '').lower()
        tags = ' '.join(elem.get('tags', [])).lower()
        
        if query_lower == nombre:
            score = 100
        elif query_lower in nombre:
            score = 50
        if query_lower in desc:
            score += 20
        if query_lower in tags:
            score += 15
        
        if score > 0:
            results.append({**elem, '_score': score})
    
    results.sort(key=lambda x: x['_score'], reverse=True)
    return results


# ============================================
# CONFIGURACIÓN DE MOVIMIENTO HUMANO
# ============================================
# IMPORTANTE: Todas las funciones de mouse usan move_smooth() con humanize=True
# por defecto para evitar detección de bots. Esto incluye:
# - move_smooth(): Movimiento con curvas de Bézier, jitter, micro-pausas y overshoot
# - do_click(): Usa move_smooth() antes del click
# - do_double_click(): Usa move_smooth() antes del doble click  
# - do_drag(): Usa move_smooth() para ir al inicio Y para arrastrar
# - do_scroll(): Usa move_smooth() si se especifica posición
# ============================================
import random
import math

# Parámetros para simular movimiento humano (ajustables)
HUMAN_MOVEMENT_CONFIG = {
    # Jitter: pequeñas desviaciones aleatorias durante el movimiento
    'jitter_min': 1,        # Desviación mínima en píxeles
    'jitter_max': 4,        # Desviación máxima en píxeles
    'jitter_frequency': 0.4, # Probabilidad de aplicar jitter por paso
    
    # Curva de Bézier: curvatura del movimiento
    'curve_variance_min': 0.15,  # Varianza mínima de puntos de control
    'curve_variance_max': 0.35,  # Varianza máxima de puntos de control
    
    # Velocidad: variaciones en la velocidad
    'speed_variance_min': 0.85,  # Multiplicador mínimo de velocidad
    'speed_variance_max': 1.20,  # Multiplicador máximo de velocidad
    
    # Micro-pausas: pequeñas pausas durante el movimiento
    'micropause_chance': 0.08,    # Probabilidad de micro-pausa
    'micropause_min': 0.02,       # Duración mínima de micro-pausa
    'micropause_max': 0.08,       # Duración máxima de micro-pausa
    
    # Overshoot: pasarse del objetivo y corregir
    'overshoot_chance': 0.20,     # Probabilidad de overshoot
    'overshoot_distance_min': 3,  # Distancia mínima de overshoot
    'overshoot_distance_max': 12, # Distancia máxima de overshoot
    
    # Pasos del movimiento
    'steps_per_second': 60,       # Pasos por segundo (suavidad del movimiento)
}


def _bezier_curve(t: float, p0: tuple, p1: tuple, p2: tuple, p3: tuple) -> tuple:
    """Calcula un punto en una curva de Bézier cúbica."""
    u = 1 - t
    tt = t * t
    uu = u * u
    uuu = uu * u
    ttt = tt * t
    
    x = uuu * p0[0] + 3 * uu * t * p1[0] + 3 * u * tt * p2[0] + ttt * p3[0]
    y = uuu * p0[1] + 3 * uu * t * p1[1] + 3 * u * tt * p2[1] + ttt * p3[1]
    
    return (x, y)


def _generate_control_points(start: tuple, end: tuple) -> tuple:
    """Genera puntos de control aleatorios para la curva de Bézier."""
    cfg = HUMAN_MOVEMENT_CONFIG
    
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = math.sqrt(dx * dx + dy * dy)
    
    variance = random.uniform(cfg['curve_variance_min'], cfg['curve_variance_max'])
    
    mid_x = (start[0] + end[0]) / 2
    mid_y = (start[1] + end[1]) / 2
    
    if distance > 0:
        perp_x = -dy / distance
        perp_y = dx / distance
    else:
        perp_x, perp_y = 0, 0
    
    offset1 = distance * variance * random.choice([-1, 1]) * random.uniform(0.3, 1.0)
    offset2 = distance * variance * random.choice([-1, 1]) * random.uniform(0.3, 1.0)
    
    p1 = (
        start[0] + dx * 0.33 + perp_x * offset1,
        start[1] + dy * 0.33 + perp_y * offset1
    )
    p2 = (
        start[0] + dx * 0.66 + perp_x * offset2,
        start[1] + dy * 0.66 + perp_y * offset2
    )
    
    return (p1, p2)


def _apply_jitter(x: float, y: float) -> tuple:
    """Aplica pequeñas desviaciones aleatorias (jitter) a una posición."""
    cfg = HUMAN_MOVEMENT_CONFIG
    
    if random.random() < cfg['jitter_frequency']:
        jitter_amount = random.uniform(cfg['jitter_min'], cfg['jitter_max'])
        angle = random.uniform(0, 2 * math.pi)
        x += jitter_amount * math.cos(angle)
        y += jitter_amount * math.sin(angle)
    
    return (x, y)


def _easing_function(t: float) -> float:
    """Función de easing para velocidad no lineal (ease-in-out)."""
    if t < 0.5:
        return 2 * t * t
    else:
        return 1 - pow(-2 * t + 2, 2) / 2


# ============================================
# FUNCIONES DE MOUSE
# ============================================

def move_smooth(x: int, y: int, duration: float = 0.5, humanize: bool = True):
    """
    Mueve el mouse suavemente con movimiento tipo humano.
    
    Características:
    - Curvas de Bézier para trayectorias no lineales
    - Jitter (temblor) para simular mano humana
    - Velocidad variable con aceleración/desaceleración
    - Micro-pausas aleatorias
    - Posible overshoot y corrección
    """
    if not HAS_PYAUTOGUI:
        error("pyautogui no disponible")
    
    cfg = HUMAN_MOVEMENT_CONFIG
    
    # Obtener posición actual
    start_pos = pyautogui.position()
    start = (start_pos.x, start_pos.y)
    end = (float(x), float(y))
    
    # Calcular distancia
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = math.sqrt(dx * dx + dy * dy)
    
    # Si la distancia es muy pequeña, solo mover directamente
    if distance < 5:
        pyautogui.moveTo(x, y)
        return
    
    if not humanize:
        # Movimiento lineal simple (legacy)
        pyautogui.moveTo(x, y, duration=duration)
        return
    
    # Aplicar variación de velocidad
    speed_mult = random.uniform(cfg['speed_variance_min'], cfg['speed_variance_max'])
    actual_duration = duration * speed_mult
    
    # Generar puntos de control para la curva de Bézier
    p1, p2 = _generate_control_points(start, end)
    
    # Calcular número de pasos
    num_steps = max(int(actual_duration * cfg['steps_per_second']), 10)
    step_duration = actual_duration / num_steps
    
    # Ejecutar movimiento
    for i in range(num_steps + 1):
        t = i / num_steps
        
        # Aplicar easing para velocidad no lineal
        t_eased = _easing_function(t)
        
        # Calcular posición en la curva de Bézier
        pos = _bezier_curve(t_eased, start, p1, p2, end)
        
        # Aplicar jitter
        pos = _apply_jitter(pos[0], pos[1])
        
        # Mover el mouse
        pyautogui.moveTo(int(pos[0]), int(pos[1]), _pause=False)
        
        # Micro-pausa aleatoria
        if random.random() < cfg['micropause_chance']:
            time.sleep(random.uniform(cfg['micropause_min'], cfg['micropause_max']))
        else:
            time.sleep(step_duration)
    
    # Overshoot y corrección
    if random.random() < cfg['overshoot_chance']:
        if distance > 0:
            dir_x = dx / distance
            dir_y = dy / distance
        else:
            dir_x, dir_y = 0, 0
        
        overshoot_dist = random.uniform(cfg['overshoot_distance_min'], cfg['overshoot_distance_max'])
        overshoot_x = int(end[0] + dir_x * overshoot_dist)
        overshoot_y = int(end[1] + dir_y * overshoot_dist)
        
        pyautogui.moveTo(overshoot_x, overshoot_y, _pause=False)
        time.sleep(random.uniform(0.03, 0.08))
        
        # Corregir al objetivo final
        pyautogui.moveTo(x, y, _pause=False)
    else:
        # Asegurar que llegamos exactamente al destino
        pyautogui.moveTo(x, y, _pause=False)


def do_click(x: int = None, y: int = None, button: str = 'left', duration: float = 0.5):
    """Click en posición (con movimiento suave si se especifica posición)."""
    if not HAS_PYAUTOGUI:
        error("pyautogui no disponible")
    
    if x is not None and y is not None:
        move_smooth(x, y, duration)
        time.sleep(0.1)
    
    pyautogui.click(button=button)
    sound_click()  # Audio feedback


def do_double_click(x: int = None, y: int = None, duration: float = 0.5):
    """Doble click."""
    if not HAS_PYAUTOGUI:
        error("pyautogui no disponible")
    
    if x is not None and y is not None:
        move_smooth(x, y, duration)
        time.sleep(0.1)
    
    pyautogui.doubleClick()
    sound_double_click()  # Audio feedback


def do_drag(x1: int, y1: int, x2: int, y2: int, duration: float = 0.5):
    """Arrastra de un punto a otro con movimiento humano."""
    if not HAS_PYAUTOGUI:
        error("pyautogui no disponible")
    
    # Mover al punto inicial con movimiento humano
    move_smooth(x1, y1, 0.3, humanize=True)
    time.sleep(0.1)
    
    # Presionar botón
    pyautogui.mouseDown()
    time.sleep(0.05)
    
    # Arrastrar al destino con movimiento humano
    move_smooth(x2, y2, duration, humanize=True)
    time.sleep(0.05)
    
    # Soltar botón
    pyautogui.mouseUp()


def do_scroll(amount: int, x: int = None, y: int = None):
    """Scroll (con movimiento humano si se especifica posición)."""
    if not HAS_PYAUTOGUI:
        error("pyautogui no disponible")
    
    if x is not None and y is not None:
        # Mover con movimiento humano antes de hacer scroll
        move_smooth(x, y, 0.3, humanize=True)
        time.sleep(0.1)
    
    pyautogui.scroll(amount)
    sound_scroll()  # Audio feedback


# ============================================
# FUNCIONES DE TECLADO
# ============================================

def remove_accents(text: str) -> str:
    """Remueve acentos y diacríticos de un texto."""
    # Normaliza a NFD (separa caracteres base de diacríticos)
    nfd = unicodedata.normalize('NFD', text)
    # Filtra solo caracteres que NO son marcas diacríticas
    return ''.join(char for char in nfd if unicodedata.category(char) != 'Mn')


def do_write(text: str, interval: float = 0.0):
    """Escribe texto (sin acentos para evitar problemas). Maneja saltos de línea con Shift+Enter."""
    if not HAS_PYAUTOGUI:
        error("pyautogui no disponible")
    
    # Remover acentos antes de escribir
    text_clean = remove_accents(text)
    
    # Audio feedback based on text length
    sound_type(len(text_clean))
    
    # Si el texto tiene saltos de línea, procesarlos
    if '\n' in text_clean:
        lines = text_clean.split('\n')
        for i, line in enumerate(lines):
            if line:  # Solo escribir si la línea no está vacía
                pyautogui.write(line, interval=interval)
            # Si no es la última línea, presionar Shift+Enter para nueva línea
            if i < len(lines) - 1:
                pyautogui.hotkey('shift', 'enter')
                time.sleep(0.1)  # Pequeña pausa entre líneas
    else:
        # Texto sin saltos de línea, escribir normalmente
        pyautogui.write(text_clean, interval=interval)


def do_press(key: str):
    """Presiona una tecla."""
    if not HAS_PYAUTOGUI:
        error("pyautogui no disponible")
    pyautogui.press(key)
    sound_key()  # Audio feedback


def do_hotkey(*keys):
    """Combinación de teclas."""
    if not HAS_PYAUTOGUI:
        error("pyautogui no disponible")
    pyautogui.hotkey(*keys)
    sound_hotkey()  # Audio feedback


# ============================================
# SECUENCIAS
# ============================================

def get_sequence_path(name: str) -> str:
    """Obtiene la ruta del archivo de secuencia."""
    return os.path.join(SEQUENCES_DIR, f"{name}.json")


def load_sequence(name: str) -> Optional[Dict]:
    """Carga una secuencia."""
    path = get_sequence_path(name)
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_sequence(name: str, data: Dict):
    """Guarda una secuencia."""
    path = get_sequence_path(name)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def execute_action(action: Dict) -> Dict:
    """Ejecuta una acción individual."""
    action_type = action.get('type', '')
    result = {"action": action_type, "success": True}
    
    try:
        if action_type == 'move':
            move_smooth(action['x'], action['y'], action.get('duration', 0.5))
            result['coordinates'] = {"x": action['x'], "y": action['y']}
            
        elif action_type == 'move-to':
            coords, method, info = find_element_on_screen(action['target'], action.get('confidence', 0.8))
            if not coords:
                return {"success": False, "error": f"Elemento no encontrado: {action['target']}", **info}
            move_smooth(coords[0], coords[1], action.get('duration', 0.5))
            result['target'] = action['target']
            result['coordinates'] = {"x": coords[0], "y": coords[1]}
            result['method'] = method
            result['match_info'] = info
            
        elif action_type == 'click':
            do_click(action.get('x'), action.get('y'), action.get('button', 'left'))
            result['coordinates'] = {"x": action.get('x'), "y": action.get('y')}
            
        elif action_type == 'click-on':
            coords, method, info = find_element_on_screen(action['target'], action.get('confidence', 0.8))
            if not coords:
                return {"success": False, "error": f"Elemento no encontrado: {action['target']}", **info}
            do_click(coords[0], coords[1], action.get('button', 'left'))
            result['target'] = action['target']
            result['coordinates'] = {"x": coords[0], "y": coords[1]}
            result['method'] = method
            result['match_info'] = info
            
        elif action_type == 'double-click':
            do_double_click(action.get('x'), action.get('y'))
            result['coordinates'] = {"x": action.get('x'), "y": action.get('y')}
            
        elif action_type == 'right-click':
            do_click(action.get('x'), action.get('y'), 'right')
            result['coordinates'] = {"x": action.get('x'), "y": action.get('y')}
            
        elif action_type == 'drag':
            do_drag(action['x1'], action['y1'], action['x2'], action['y2'])
            result['from'] = {"x": action['x1'], "y": action['y1']}
            result['to'] = {"x": action['x2'], "y": action['y2']}
            
        elif action_type == 'scroll':
            do_scroll(action['amount'], action.get('x'), action.get('y'))
            result['amount'] = action['amount']
            
        elif action_type == 'write':
            do_write(action['text'], action.get('interval', 0.0))
            result['text'] = action['text']
            
        elif action_type == 'write-next-question':
            # Obtiene la siguiente pregunta del CSV
            ai_name = action.get('ai_name', 'gemini')
            part = action.get('part', 'initial')
            try:
                # Importar question_manager
                sys.path.insert(0, SKILL_DIR)
                import question_manager
                question_text = question_manager.get_question_for_sequence(ai_name, part=part)
                do_write(question_text, action.get('interval', 0.0))
                result['ai_name'] = ai_name
                result['part'] = part
                result['text_preview'] = question_text[:100] + '...' if len(question_text) > 100 else question_text
            except Exception as e:
                return {"success": False, "error": f"Error obteniendo pregunta: {str(e)}"}
            
        elif action_type == 'press':
            do_press(action['key'])
            result['key'] = action['key']
            
        elif action_type == 'hotkey':
            keys = action['keys'] if isinstance(action['keys'], list) else action['keys'].split()
            do_hotkey(*keys)
            result['keys'] = keys
            
        elif action_type == 'wait':
            time.sleep(action.get('seconds', 1))
            result['seconds'] = action.get('seconds', 1)
            
        elif action_type == 'screenshot':
            if HAS_PYAUTOGUI:
                filename = action.get('filename', f"screenshot_{int(time.time())}")
                filepath = os.path.join(CAPTURES_DIR, f"{filename}.png")
                pyautogui.screenshot(filepath)
                result['filepath'] = filepath
                # Encode image to base64 for direct viewing
                with open(filepath, 'rb') as f:
                    img_data = f.read()
                result['image_base64'] = base64.b64encode(img_data).decode('utf-8')
            
        else:
            return {"success": False, "error": f"Acción desconocida: {action_type}"}
            
    except Exception as e:
        return {"success": False, "error": str(e)}
    
    return result


def is_element_visible(name: str, confidence: float = 0.8) -> Tuple[bool, Dict]:
    """Verifica si un elemento está visible en pantalla sin hacer click.
    
    Retorna: (visible, info)
    """
    coords, method, info = find_element_on_screen(name, confidence)
    return coords is not None, info


def execute_actions(actions: List[Dict]) -> List[Dict]:
    """Ejecuta una lista de acciones con soporte para condicionales if-visible."""
    results = []
    i = 0
    while i < len(actions):
        action = actions[i]
        action_type = action.get('type', '')
        
        # Soporte para condicionales if-visible / if-not-visible
        if action_type in ('if-visible', 'if-not-visible'):
            target = action.get('target', '')
            then_actions = action.get('then', [])
            else_actions = action.get('else', [])
            
            # Verificar visibilidad del elemento
            visible, info = is_element_visible(target, action.get('confidence', 0.8))
            
            # Determinar qué camino tomar
            if action_type == 'if-visible':
                condition_met = visible
            else:  # if-not-visible
                condition_met = not visible
            
            # Registrar resultado de la evaluación
            result = {
                "action": action_type,
                "target": target,
                "condition_met": condition_met,
                "visible": visible,
                "branch": "then" if condition_met else "else",
                "step": i + 1,
                "success": True,
                "match_info": info
            }
            results.append(result)
            
            # Ejecutar el camino correspondiente
            branch_actions = then_actions if condition_met else else_actions
            for branch_action in branch_actions:
                branch_result = execute_action(branch_action)
                branch_result['step'] = i + 1
                branch_result['branch'] = "then" if condition_met else "else"
                results.append(branch_result)
                # Si una acción del branch falla, detener
                if not branch_result.get('success', True):
                    return results
        else:
            # Acción normal
            result = execute_action(action)
            result['step'] = i + 1
            results.append(result)
            if not result.get('success', True):
                break
        
        i += 1
    
    return results


# ============================================
# COMANDOS CLI
# ============================================

def cmd_search(args):
    """Buscar elementos."""
    results = search_elements(args.query)
    output({
        "action": "search",
        "query": args.query,
        "count": len(results),
        "results": [{"nombre": r['name'], "descripcion": r.get('description', '')} for r in results[:10]]
    })


def cmd_find(args):
    """Buscar por nombre."""
    elem = find_element(args.name)
    if elem:
        output({
            "success": True,
            "action": "find",
            "element": {
                "nombre": elem['name'],
                "descripcion": elem.get('description', ''),
                "images": elem.get('images', []),
                "tags": elem.get('tags', [])
            }
        })
    else:
        error(f"Elemento no encontrado: {args.name}")


def cmd_list(args):
    """Listar todos los elementos."""
    elements = load_elements()
    output({
        "action": "list",
        "count": len(elements),
        "elements": [{"nombre": v['name'], "descripcion": v.get('description', '')[:50]} for v in elements.values()]
    })


def cmd_near(args):
    """Comando obsoleto: Ya no se usan coordenadas fijas."""
    output({
        "action": "near",
        "success": False,
        "message": "Este comando está obsoleto. Ahora se usa detección por imagen, no coordenadas fijas. Use 'find' o 'search' en su lugar."
    })


def cmd_stats(args):
    """Estadísticas del sistema."""
    elements = load_elements()
    output({
        "action": "stats",
        "total_elements": len(elements),
        "elements_file": ELEMENTS_FILE,
        "captures_dir": CAPTURES_DIR,
        "sequences_dir": SEQUENCES_DIR
    })


def cmd_move(args):
    """Mover mouse."""
    result = execute_action({"type": "move", "x": args.x, "y": args.y, "duration": args.duration})
    output(result)


def cmd_move_to(args):
    """Mover a elemento."""
    result = execute_action({"type": "move-to", "target": args.name, "duration": args.duration})
    output(result)


def cmd_click(args):
    """Click en coordenadas."""
    result = execute_action({"type": "click", "x": args.x, "y": args.y})
    output(result)


def cmd_click_on(args):
    """Click en elemento."""
    result = execute_action({"type": "click-on", "target": args.name})
    output(result)


def cmd_double_click(args):
    """Doble click."""
    result = execute_action({"type": "double-click", "x": args.x, "y": args.y})
    output(result)


def cmd_right_click(args):
    """Click derecho."""
    result = execute_action({"type": "right-click", "x": args.x, "y": args.y})
    output(result)


def cmd_drag(args):
    """Drag."""
    result = execute_action({"type": "drag", "x1": args.x1, "y1": args.y1, 
                            "x2": args.x2, "y2": args.y2})
    output(result)


def cmd_scroll(args):
    """Scroll."""
    x, y = None, None
    if args.at:
        x, y = map(int, args.at.split(','))
    result = execute_action({"type": "scroll", "amount": args.amount, "x": x, "y": y})
    output(result)


def cmd_write(args):
    """Escribir texto."""
    result = execute_action({"type": "write", "text": args.text})
    output(result)


def cmd_press(args):
    """Presionar tecla."""
    result = execute_action({"type": "press", "key": args.key})
    output(result)


def cmd_hotkey(args):
    """Hotkey."""
    result = execute_action({"type": "hotkey", "keys": args.keys})
    output(result)


def cmd_mouse_pos(args):
    """Posición actual del mouse."""
    if HAS_PYAUTOGUI:
        pos = pyautogui.position()
        output({"action": "mouse-pos", "x": pos.x, "y": pos.y})
    else:
        error("pyautogui no disponible")


def cmd_wait(args):
    """Esperar."""
    result = execute_action({"type": "wait", "seconds": args.seconds})
    output(result)


def cmd_screenshot(args):
    """Screenshot."""
    result = execute_action({"type": "screenshot", "filename": args.filename})
    output(result)


def cmd_region_capture(args):
    """Captura interactiva de región con mouse."""
    import subprocess
    
    # Primero buscar en el directorio del skill
    script_path = os.path.join(SKILL_DIR, "region_capture.py")
    
    # Fallback al proyecto original
    if not os.path.exists(script_path):
        script_path = os.path.join(MACRO_AGENT_PROJECT, "cli", "region_capture.py")
    
    if not os.path.exists(script_path):
        error(f"Script no encontrado: {script_path}")
        return
    
    try:
        # Ejecutar el script de region capture
        # Por defecto guarda en ~/.copilot/skills/macro-agent/data/
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=False
        )
        output({
            "success": result.returncode == 0,
            "action": "region-capture",
            "message": "Region capture finalizado" if result.returncode == 0 else "Region capture cerrado",
            "data_dir": DATA_DIR
        })
    except Exception as e:
        error(f"Error ejecutando region capture: {e}")


def cmd_run(args):
    """Ejecutar acciones desde JSON."""
    try:
        data = json.loads(args.json_str)
        actions = data.get('actions', [data] if 'type' in data else [])
        results = execute_actions(actions)
        output({
            "action": "run",
            "total": len(actions),
            "completed": len([r for r in results if r.get('success')]),
            "results": results
        })
    except json.JSONDecodeError as e:
        error(f"JSON inválido: {e}")


def cmd_seq_create(args):
    """Crear secuencia."""
    seq = {
        "name": args.name,
        "display_name": getattr(args, 'display_name', None) or args.name,
        "description": args.description or "",
        "created": datetime.now().isoformat(),
        "actions": []
    }
    save_sequence(args.name, seq)
    output({
        "action": "seq-create", 
        "name": args.name, 
        "display_name": seq['display_name'],
        "description": seq['description'],
        "success": True
    })


def parse_simple_action(action_str: str) -> Dict:
    """Parsea una acción simple desde string."""
    parts = action_str.split(maxsplit=1)
    action_type = parts[0]
    action = {"type": action_type}
    
    if len(parts) > 1:
        rest = parts[1]
        
        if action_type in ('click-on', 'move-to'):
            action['target'] = rest
        elif action_type == 'write':
            action['text'] = rest.strip("'\"")
        elif action_type == 'press':
            action['key'] = rest
        elif action_type == 'hotkey':
            action['keys'] = rest.split()
        elif action_type == 'wait':
            action['seconds'] = float(rest)
        elif action_type in ('click', 'double-click', 'right-click', 'move'):
            coords = rest.split()
            action['x'] = int(coords[0])
            action['y'] = int(coords[1])
        elif action_type == 'scroll':
            action['amount'] = int(rest)
        elif action_type == 'drag':
            coords = rest.split()
            action['x1'], action['y1'] = int(coords[0]), int(coords[1])
            action['x2'], action['y2'] = int(coords[2]), int(coords[3])
    
    return action


def cmd_seq_add(args):
    """Agregar acción a secuencia."""
    seq = load_sequence(args.name)
    if not seq:
        error(f"Secuencia no encontrada: {args.name}")
    
    # Parsear la acción desde string
    parts = args.action.split(maxsplit=1)
    action_type = parts[0]
    
    # Soporte para if-visible / if-not-visible
    if action_type in ('if-visible', 'if-not-visible'):
        if len(parts) < 2:
            error(f"{action_type} requiere un target")
        
        target = parts[1]
        then_actions = []
        else_actions = []
        
        # Parsear --then y --else desde args
        if hasattr(args, 'then_actions') and args.then_actions:
            for then_str in args.then_actions:
                then_actions.append(parse_simple_action(then_str))
        
        if hasattr(args, 'else_actions') and args.else_actions:
            for else_str in args.else_actions:
                else_actions.append(parse_simple_action(else_str))
        
        action = {
            "type": action_type,
            "target": target,
            "then": then_actions,
            "else": else_actions
        }
    else:
        # Acción normal
        action = parse_simple_action(args.action)
    
    seq['actions'].append(action)
    seq['updated'] = datetime.now().isoformat()
    save_sequence(args.name, seq)
    
    output({
        "action": "seq-add",
        "sequence": args.name,
        "added": action,
        "total_actions": len(seq['actions'])
    })


def cmd_seq_show(args):
    """Mostrar secuencia."""
    seq = load_sequence(args.name)
    if not seq:
        error(f"Secuencia no encontrada: {args.name}")
    output({"action": "seq-show", "sequence": seq})


def cmd_seq_run(args):
    """Ejecutar secuencia."""
    seq = load_sequence(args.name)
    if not seq:
        error(f"Secuencia no encontrada: {args.name}")
    
    results = execute_actions(seq['actions'])
    output({
        "action": "seq-run",
        "sequence": args.name,
        "total": len(seq['actions']),
        "completed": len([r for r in results if r.get('success')]),
        "results": results
    })


def cmd_seq_list(args):
    """Listar secuencias con información completa."""
    sequences = []
    if os.path.exists(SEQUENCES_DIR):
        for f in os.listdir(SEQUENCES_DIR):
            if f.endswith('.json'):
                seq = load_sequence(f[:-5])
                if seq:
                    # Resumen de acciones
                    action_summary = []
                    for act in seq.get('actions', [])[:5]:  # Primeras 5 acciones
                        if act['type'] == 'click-on':
                            action_summary.append(f"click:{act.get('target', '?')}")
                        elif act['type'] == 'wait':
                            action_summary.append(f"wait:{act.get('seconds', 0)}s")
                        elif act['type'] == 'write':
                            action_summary.append(f"write:{act.get('text', '')[:10]}...")
                        elif act['type'] == 'press':
                            action_summary.append(f"press:{act.get('key', '?')}")
                        elif act['type'] == 'hotkey':
                            action_summary.append(f"hotkey:{'+'.join(act.get('keys', []))}")
                        else:
                            action_summary.append(act['type'])
                    
                    if len(seq.get('actions', [])) > 5:
                        action_summary.append(f"...+{len(seq['actions'])-5} más")
                    
                    sequences.append({
                        "name": seq['name'],
                        "display_name": seq.get('display_name', seq['name']),
                        "description": seq.get('description', ''),
                        "actions_count": len(seq.get('actions', [])),
                        "actions_preview": action_summary,
                        "created": seq.get('created', ''),
                        "updated": seq.get('updated', '')
                    })
    
    output({
        "action": "seq-list", 
        "count": len(sequences), 
        "sequences": sequences,
        "hint": "Usa 'seq-show <name>' para ver detalles o 'seq-describe <name> --display-name <nombre> --description <desc>' para actualizar"
    })


def cmd_seq_delete(args):
    """Eliminar secuencia."""
    path = get_sequence_path(args.name)
    if os.path.exists(path):
        os.remove(path)
        output({"action": "seq-delete", "name": args.name, "success": True})
    else:
        error(f"Secuencia no encontrada: {args.name}")


def cmd_seq_describe(args):
    """Actualizar nombre visible y descripción de una secuencia."""
    seq = load_sequence(args.name)
    if not seq:
        error(f"Secuencia no encontrada: {args.name}")
    
    updated = False
    if args.display_name:
        seq['display_name'] = args.display_name
        updated = True
    if args.description:
        seq['description'] = args.description
        updated = True
    
    if updated:
        seq['updated'] = datetime.now().isoformat()
        save_sequence(args.name, seq)
    
    output({
        "action": "seq-describe",
        "name": args.name,
        "display_name": seq.get('display_name', seq['name']),
        "description": seq.get('description', ''),
        "success": True
    })


# ============================================
# COMANDOS DE ELEMENTOS (JSON)
# ============================================

def cmd_elem_add(args):
    """Agregar o actualizar un elemento."""
    tags = args.tags.split(',') if args.tags else []
    elem = add_element(args.name, args.description or "", tags=tags)
    output({
        "action": "elem-add",
        "success": True,
        "element": elem
    })


def cmd_elem_add_image(args):
    """Agregar una imagen a un elemento."""
    elem = add_image_to_element(args.name, args.image)
    output({
        "action": "elem-add-image",
        "success": True,
        "element": elem
    })


def cmd_elem_show(args):
    """Mostrar un elemento."""
    elem = get_element(args.name)
    if not elem:
        error(f"Elemento no encontrado: {args.name}")
    output({
        "action": "elem-show",
        "success": True,
        "element": elem
    })


def cmd_elem_list(args):
    """Listar todos los elementos."""
    elements = load_elements()
    output({
        "action": "elem-list",
        "count": len(elements),
        "elements": list(elements.values())
    })


def cmd_elem_delete(args):
    """Eliminar un elemento."""
    elements = load_elements()
    name_key = args.name.lower().replace(' ', '_')
    
    if name_key not in elements:
        error(f"Elemento no encontrado: {args.name}")
    
    del elements[name_key]
    save_elements(elements)
    
    output({
        "action": "elem-delete",
        "success": True,
        "name": args.name
    })


# ============================================
# COMANDOS DE SONIDOS
# ============================================

def cmd_sounds_on(args):
    """Activar sonidos."""
    result = enable_sounds()
    output({
        "action": "sounds-on",
        "success": True,
        "message": result,
        "status": get_sound_status()
    })


def cmd_sounds_off(args):
    """Desactivar sonidos."""
    result = disable_sounds()
    output({
        "action": "sounds-off",
        "success": True,
        "message": result,
        "status": get_sound_status()
    })


def cmd_sounds_status(args):
    """Estado de los sonidos."""
    status = get_sound_status()
    output({
        "action": "sounds-status",
        "success": True,
        **status
    })


def cmd_sounds_volume(args):
    """Ajustar volumen."""
    result = set_volume(args.volume)
    output({
        "action": "sounds-volume",
        "success": True,
        "message": result,
        "status": get_sound_status()
    })


def main():
    parser = argparse.ArgumentParser(description="Macro Agent - Control de UI para agentes IA")
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')
    
    # Búsqueda
    p = subparsers.add_parser('search', help='Buscar elementos')
    p.add_argument('query', help='Texto a buscar')
    p.set_defaults(func=cmd_search)
    
    p = subparsers.add_parser('find', help='Buscar por nombre')
    p.add_argument('name', help='Nombre del elemento')
    p.set_defaults(func=cmd_find)
    
    p = subparsers.add_parser('list', help='Listar elementos')
    p.set_defaults(func=cmd_list)
    
    p = subparsers.add_parser('near', help='Buscar cerca de coordenadas')
    p.add_argument('coords', help='Coordenadas X,Y')
    p.add_argument('--radius', type=int, default=100, help='Radio de búsqueda')
    p.set_defaults(func=cmd_near)
    
    p = subparsers.add_parser('stats', help='Estadísticas')
    p.set_defaults(func=cmd_stats)
    
    # Mouse
    p = subparsers.add_parser('move', help='Mover mouse')
    p.add_argument('x', type=int)
    p.add_argument('y', type=int)
    p.add_argument('--duration', type=float, default=0.5)
    p.set_defaults(func=cmd_move)
    
    p = subparsers.add_parser('move-to', help='Mover a elemento')
    p.add_argument('name', help='Nombre del elemento')
    p.add_argument('--duration', type=float, default=0.5)
    p.set_defaults(func=cmd_move_to)
    
    p = subparsers.add_parser('click', help='Click en coordenadas')
    p.add_argument('x', type=int)
    p.add_argument('y', type=int)
    p.set_defaults(func=cmd_click)
    
    p = subparsers.add_parser('click-on', help='Click en elemento')
    p.add_argument('name', help='Nombre del elemento')
    p.set_defaults(func=cmd_click_on)
    
    p = subparsers.add_parser('double-click', help='Doble click')
    p.add_argument('x', type=int)
    p.add_argument('y', type=int)
    p.set_defaults(func=cmd_double_click)
    
    p = subparsers.add_parser('right-click', help='Click derecho')
    p.add_argument('x', type=int)
    p.add_argument('y', type=int)
    p.set_defaults(func=cmd_right_click)
    
    p = subparsers.add_parser('drag', help='Arrastrar')
    p.add_argument('x1', type=int)
    p.add_argument('y1', type=int)
    p.add_argument('x2', type=int)
    p.add_argument('y2', type=int)
    p.set_defaults(func=cmd_drag)
    
    p = subparsers.add_parser('scroll', help='Scroll')
    p.add_argument('amount', type=int, help='Cantidad (negativo=abajo)')
    p.add_argument('--at', help='Coordenadas X,Y')
    p.set_defaults(func=cmd_scroll)
    
    # Teclado
    p = subparsers.add_parser('write', help='Escribir texto')
    p.add_argument('text', help='Texto a escribir')
    p.set_defaults(func=cmd_write)
    
    p = subparsers.add_parser('press', help='Presionar tecla')
    p.add_argument('key', help='Tecla')
    p.set_defaults(func=cmd_press)
    
    p = subparsers.add_parser('hotkey', help='Combinación de teclas')
    p.add_argument('keys', nargs='+', help='Teclas')
    p.set_defaults(func=cmd_hotkey)
    
    # Utilidades
    p = subparsers.add_parser('mouse-pos', help='Posición del mouse')
    p.set_defaults(func=cmd_mouse_pos)
    
    p = subparsers.add_parser('wait', help='Esperar')
    p.add_argument('seconds', type=float)
    p.set_defaults(func=cmd_wait)
    
    p = subparsers.add_parser('screenshot', help='Captura de pantalla')
    p.add_argument('filename', help='Nombre del archivo')
    p.set_defaults(func=cmd_screenshot)
    
    p = subparsers.add_parser('region-capture', help='Captura interactiva de región con mouse')
    p.set_defaults(func=cmd_region_capture)
    
    # Ejecutar JSON
    p = subparsers.add_parser('run', help='Ejecutar acciones desde JSON')
    p.add_argument('json_str', help='JSON con acciones')
    p.set_defaults(func=cmd_run)
    
    # Secuencias
    p = subparsers.add_parser('seq-create', help='Crear secuencia')
    p.add_argument('name', help='Nombre interno de la secuencia (sin espacios)')
    p.add_argument('--display-name', '-n', dest='display_name', help='Nombre visible amigable')
    p.add_argument('--description', '-d', help='Descripción de qué hace la secuencia')
    p.set_defaults(func=cmd_seq_create)
    
    p = subparsers.add_parser('seq-add', help='Agregar acción a secuencia')
    p.add_argument('name', help='Nombre de la secuencia')
    p.add_argument('action', help='Acción (ej: "click-on btn_guardar" o "if-visible elemento")')
    p.add_argument('--then', dest='then_actions', action='append', help='Acciones si la condición es verdadera (para if-visible)')
    p.add_argument('--else', dest='else_actions', action='append', help='Acciones si la condición es falsa (para if-visible)')
    p.set_defaults(func=cmd_seq_add)
    
    p = subparsers.add_parser('seq-show', help='Mostrar secuencia')
    p.add_argument('name', help='Nombre de la secuencia')
    p.set_defaults(func=cmd_seq_show)
    
    p = subparsers.add_parser('seq-run', help='Ejecutar secuencia')
    p.add_argument('name', help='Nombre de la secuencia')
    p.set_defaults(func=cmd_seq_run)
    
    p = subparsers.add_parser('seq-list', help='Listar secuencias')
    p.set_defaults(func=cmd_seq_list)
    
    p = subparsers.add_parser('seq-delete', help='Eliminar secuencia')
    p.add_argument('name', help='Nombre de la secuencia')
    p.set_defaults(func=cmd_seq_delete)
    
    p = subparsers.add_parser('seq-describe', help='Actualizar nombre/descripción de secuencia')
    p.add_argument('name', help='Nombre interno de la secuencia')
    p.add_argument('--display-name', '-n', dest='display_name', help='Nuevo nombre visible')
    p.add_argument('--description', '-d', help='Nueva descripción')
    p.set_defaults(func=cmd_seq_describe)
    
    # Elementos (JSON)
    p = subparsers.add_parser('elem-add', help='Agregar/actualizar elemento')
    p.add_argument('name', help='Nombre del elemento')
    p.add_argument('--description', '-d', help='Descripción')
    p.add_argument('--tags', '-t', help='Tags separados por coma')
    p.set_defaults(func=cmd_elem_add)
    
    p = subparsers.add_parser('elem-add-image', help='Agregar imagen a elemento')
    p.add_argument('name', help='Nombre del elemento')
    p.add_argument('image', help='Nombre del archivo de imagen')
    p.set_defaults(func=cmd_elem_add_image)
    
    p = subparsers.add_parser('elem-show', help='Mostrar elemento')
    p.add_argument('name', help='Nombre del elemento')
    p.set_defaults(func=cmd_elem_show)
    
    p = subparsers.add_parser('elem-list', help='Listar elementos')
    p.set_defaults(func=cmd_elem_list)
    
    p = subparsers.add_parser('elem-delete', help='Eliminar elemento')
    p.add_argument('name', help='Nombre del elemento')
    p.set_defaults(func=cmd_elem_delete)
    
    # Sonidos
    p = subparsers.add_parser('sounds-on', help='Activar sonidos')
    p.set_defaults(func=cmd_sounds_on)
    
    p = subparsers.add_parser('sounds-off', help='Desactivar sonidos')
    p.set_defaults(func=cmd_sounds_off)
    
    p = subparsers.add_parser('sounds-status', help='Estado de los sonidos')
    p.set_defaults(func=cmd_sounds_status)
    
    p = subparsers.add_parser('sounds-volume', help='Ajustar volumen')
    p.add_argument('volume', type=float, help='Volumen 0.0-1.0')
    p.set_defaults(func=cmd_sounds_volume)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(0)
    
    args.func(args)


if __name__ == '__main__':
    main()
