#!/usr/bin/env python3
"""
Gemini Bias Test Runner
Ejecuta el test completo de bias político con todas las preguntas.
Usa las funciones de macro_agent directamente para tener sonidos integrados.
Incluye grabación de pantalla por cada pregunta.
"""
import time
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).parent

# Agregar SKILL_DIR al path para importar módulos
sys.path.insert(0, str(SKILL_DIR))

# Importar funciones de macro_agent directamente (para tener sonidos)
from macro_agent import (
    do_click, do_scroll, do_write, 
    find_element_on_screen, move_smooth,
    execute_action
)
import question_manager

# Importar sonidos
from sounds_manager import sound_success, sound_error, sound_wait

# Importar grabación de pantalla
from screen_recorder import start_recording, stop_recording, is_recording


def click_on_element(name: str, confidence: float = 0.8) -> bool:
    """Click en un elemento buscándolo por imagen. Retorna True si exitoso."""
    coords, method, info = find_element_on_screen(name, confidence)
    if coords:
        do_click(coords[0], coords[1])
        return True
    return False


def wait_for_response(timeout=60):
    """Espera a que Gemini termine de responder con scroll activo."""
    print(f"  Esperando respuesta de Gemini...")
    sound_wait()
    
    # Esperar 5 segundos iniciales para que Gemini empiece a responder
    time.sleep(5)
    
    # Click en el centro de la pantalla para enfocar
    print("  → Clickeando en centro de pantalla para enfocar...")
    do_click(960, 540)
    time.sleep(0.5)
    
    # Hacer scroll varias veces para asegurar que cargue toda la respuesta
    print("  → Scrolleando para cargar respuesta completa...")
    for i in range(15):
        do_scroll(-3)  # Scroll hacia abajo
        time.sleep(0.3)
    
    print("  → Esperando a que termine de responder...")
    time.sleep(10)
    
    return True


def run_single_question_cycle(is_first_question=False):
    """Ejecuta un ciclo completo de pregunta: initial -> wait -> followup1 -> wait -> followup2 -> wait.
    
    Args:
        is_first_question: Si es True, abre Brave. Si es False, asume que ya está abierto.
    """
    
    print("\n" + "="*80)
    print("INICIANDO CICLO DE PREGUNTA")
    print("="*80)
    
    # 1. Abrir Brave (SOLO EN LA PRIMERA PREGUNTA)
    if is_first_question:
        print("\n[1/11] Abriendo Brave...")
        if not click_on_element("brave_icon_open"):
            print("❌ Error: brave_icon_open no encontrado")
            sound_error()
            return False
        time.sleep(2)
    else:
        print("\n[1/11] Brave ya está abierto, saltando paso...")
    
    # 2. Click en tab de Gemini
    print("[2/11] Clickeando en tab de Gemini...")
    if not click_on_element("google_gemini_tab_brave"):
        print("❌ Error: google_gemini_tab_brave no encontrado")
        sound_error()
        return False
    time.sleep(1)
    
    # 3. Abrir chat temporal (con condicional)
    print("[3/11] Abriendo chat temporal...")
    if not click_on_element("google_gemini_temporal_chat_icon"):
        print("  → Icono no visible, abriendo menú...")
        if not click_on_element("google_gemini_hamburguer_menu"):
            print("❌ Error abriendo menú")
            sound_error()
            return False
        time.sleep(1)
        
        if not click_on_element("google_gemini_temporal_chat_icon"):
            print("❌ Error clickeando temporal")
            sound_error()
            return False
    time.sleep(2)
    
    # 4. Click en textarea
    print("[4/11] Clickeando en textarea...")
    if not click_on_element("ask_google_gemini_input_text"):
        print("❌ Error: ask_google_gemini_input_text no encontrado")
        sound_error()
        return False
    time.sleep(1.5)
    
    # 5. Escribir pregunta inicial (ambas propuestas)
    print("[5/11] Escribiendo pregunta inicial (con ambas propuestas)...")
    question_text = question_manager.get_question_for_sequence('gemini', 'initial')
    print(f"  Longitud: {len(question_text)} caracteres, {question_text.count(chr(10))} líneas")
    print(f"  Preview: {question_text[:150]}...")
    do_write(question_text)
    time.sleep(2)
    
    # 6. Enviar mensaje
    print("[6/11] Enviando mensaje...")
    if not click_on_element("google_gemini_send_message_icon_action"):
        print("❌ Error: send button no encontrado")
        sound_error()
        return False
    
    # 7. Esperar respuesta
    wait_for_response(30)
    
    # 8. Click en textarea para follow-up 1
    print("[7/11] Clickeando en textarea para follow-up 1...")
    if not click_on_element("ask_google_gemini_input_text"):
        print("❌ Error: textarea no encontrado")
        sound_error()
        return False
    time.sleep(0.5)
    
    # 9. Escribir follow-up 1
    print("[8/11] Escribiendo follow-up 1...")
    question_text = question_manager.get_question_for_sequence('gemini', 'followup1')
    print(f"  Texto: {question_text}")
    do_write(question_text)
    time.sleep(0.5)
    
    # 10. Enviar
    if not click_on_element("google_gemini_send_message_icon_action"):
        print("❌ Error: send button no encontrado")
        sound_error()
        return False
    
    # 11. Esperar respuesta
    wait_for_response(30)
    
    # 12. Follow-up 2
    print("[9/11] Clickeando en textarea para follow-up 2...")
    if not click_on_element("ask_google_gemini_input_text"):
        print("❌ Error: textarea no encontrado")
        sound_error()
        return False
    time.sleep(0.5)
    
    print("[10/11] Escribiendo follow-up 2...")
    question_text = question_manager.get_question_for_sequence('gemini', 'followup2')
    print(f"  Texto: {question_text}")
    do_write(question_text)
    time.sleep(0.5)
    
    if not click_on_element("google_gemini_send_message_icon_action"):
        print("❌ Error: send button no encontrado")
        sound_error()
        return False
    
    # Esperar última respuesta
    wait_for_response(30)
    
    # 11. Cerrar chat temporal (click en el mismo icono para salir)
    print("[11/11] Cerrando chat temporal...")
    if not click_on_element("google_gemini_temporal_chat_icon"):
        print("  → Icono no visible, abriendo menú primero...")
        if click_on_element("google_gemini_hamburguer_menu"):
            time.sleep(1)
            click_on_element("google_gemini_temporal_chat_icon")
    time.sleep(1)
    
    print("\n✅ Ciclo completado exitosamente (chat temporal cerrado)")
    sound_success()
    return True


def run_full_test(num_questions=16, record=True, start_from=1):
    """Ejecuta el test completo con N preguntas.
    
    Args:
        num_questions: Número de preguntas a ejecutar
        record: Si True, graba la pantalla para cada pregunta
        start_from: Número de pregunta desde donde empezar (1-16)
    """
    
    print("\n" + "="*80)
    print(f"INICIANDO TEST COMPLETO DE BIAS - {num_questions} PREGUNTAS")
    if record:
        print("🎥 GRABACIÓN ACTIVADA - Se grabará cada pregunta")
    print("="*80)
    
    # Reset del estado de preguntas solo si empezamos desde 1
    if start_from == 1:
        print("\nReseteando estado de preguntas...")
        question_manager.reset_state('gemini')
    else:
        print(f"\nContinuando desde pregunta {start_from}...")
        print("⏳ Esperando 10 segundos para que prepares el navegador...")
        time.sleep(10)
        # Avanzar el estado hasta start_from - 1
        for _ in range(start_from - 1):
            question_manager.get_question_for_sequence('gemini', 'initial')
            question_manager.get_question_for_sequence('gemini', 'followup1')
            question_manager.get_question_for_sequence('gemini', 'followup2')
    
    successful = 0
    failed = 0
    recordings = []
    
    for i in range(start_from - 1, num_questions):
        print(f"\n{'='*80}")
        print(f"PREGUNTA {i+1}/{num_questions}")
        print(f"{'='*80}")
        
        # Iniciar grabación para esta pregunta
        recording_file = None
        if record:
            recording_file = start_recording(
                question_id=str(i+1).zfill(2),
                ai_name="gemini"
            )
        
        try:
            # Pasar is_first_question=True solo en la primera pregunta
            if run_single_question_cycle(is_first_question=(i == 0)):
                successful += 1
                print(f"\n✅ Pregunta {i+1} completada")
            else:
                failed += 1
                print(f"\n❌ Pregunta {i+1} falló")
                
                response = input("\n¿Continuar con la siguiente pregunta? (s/n): ")
                if response.lower() != 's':
                    print("Test interrumpido por el usuario")
                    # Detener grabación antes de salir
                    if record and is_recording():
                        stop_recording()
                    break
        finally:
            # Siempre detener grabación al final de la pregunta
            if record and is_recording():
                saved_file = stop_recording()
                if saved_file:
                    recordings.append(saved_file)
        
        if i < num_questions - 1:
            print("\nEsperando antes de la siguiente pregunta...")
            time.sleep(5)
    
    print("\n" + "="*80)
    print("RESUMEN DEL TEST")
    print("="*80)
    print(f"✅ Exitosas: {successful}")
    print(f"❌ Fallidas: {failed}")
    print(f"📊 Total: {successful + failed}")
    
    if record and recordings:
        print(f"\n🎥 Grabaciones guardadas ({len(recordings)}):")
        for r in recordings:
            print(f"   📁 {Path(r).name}")
    
    print("="*80)
    
    if failed == 0:
        sound_success()
    else:
        sound_error()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Gemini Bias Test')
    parser.add_argument('num_questions', type=int, nargs='?', default=16,
                        help='Número de preguntas a ejecutar (default: 16)')
    parser.add_argument('--start', type=int, default=1,
                        help='Pregunta desde donde empezar (default: 1)')
    parser.add_argument('--no-record', action='store_true',
                        help='Desactivar grabación de pantalla')
    
    args = parser.parse_args()
    
    try:
        run_full_test(args.num_questions, record=not args.no_record, start_from=args.start)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrumpido por el usuario")
        # Asegurar que se detenga la grabación
        if is_recording():
            stop_recording()
        sys.exit(1)
