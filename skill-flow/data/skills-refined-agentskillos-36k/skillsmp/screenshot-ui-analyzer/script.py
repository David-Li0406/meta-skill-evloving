#!/usr/bin/env python3
"""
Screenshot UI Analyzer Script
Takes a screenshot, detects UI elements using AI (Gemini Vision), saves data to JSON and annotated image.
"""

import argparse
import json
import os
import sys
from datetime import datetime

try:
    import cv2
    import numpy as np
    import pyautogui
    import google.generativeai as genai
    from PIL import Image
except ImportError as e:
    print(f"Missing dependency: {e}. Please install required packages: pip install opencv-python pyautogui google-generativeai pillow")
    sys.exit(1)

def take_screenshot():
    """Take a screenshot of the entire screen."""
    screenshot = pyautogui.screenshot()
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

def detect_elements_gemini(img_path):
    """Detect UI elements using Gemini Vision."""
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable not set.")
        sys.exit(1)
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    image = Image.open(img_path)
    
    prompt = """
Analyze this screenshot and identify all visible UI elements such as buttons, text fields, icons, menus, etc.
For each element, provide:
- name: A short descriptive name
- description: A brief description of the element
- bbox: Bounding box as [x, y, width, height] where x,y are top-left coordinates
- center: Center coordinates as [x, y]

Return the result as a valid JSON object with a key "elements" containing a list of element objects.
Only include elements that are clearly identifiable.
"""
    
    response = model.generate_content([prompt, image])
    text = response.text.strip()
    
    # Extract JSON from response
    try:
        # Assume the response is JSON
        data = json.loads(text)
        return data.get('elements', [])
    except json.JSONDecodeError:
        print("Error parsing Gemini response as JSON. Response:", text)
        return []

def detect_elements(img, model='gemini'):
    """Detect UI elements in the image."""
    if model == 'gemini':
        # Save temp image for Gemini
        temp_path = f"temp_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        cv2.imwrite(temp_path, img)
        try:
            elements = detect_elements_gemini(temp_path)
        finally:
            os.remove(temp_path)
        return elements
    elif model == 'text':
        # Fallback to OCR
        try:
            import pytesseract
            data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
            elements = []
            n_boxes = len(data['text'])
            for i in range(n_boxes):
                if int(data['conf'][i]) > 0:
                    text = data['text'][i].strip()
                    if text:
                        x = data['left'][i]
                        y = data['top'][i]
                        w = data['width'][i]
                        h = data['height'][i]
                        center_x = x + w // 2
                        center_y = y + h // 2
                        elements.append({
                            'name': text,
                            'description': 'Text element',
                            'bbox': [x, y, w, h],
                            'center': [center_x, center_y]
                        })
            return elements
        except ImportError:
            print("pytesseract not installed, cannot use 'text' model.")
            return []
    elif model == 'hybrid':
        # Hybrid: Tesseract for bbox, LightOn for text refinement
        try:
            import pytesseract
            from transformers import pipeline
            import torch
            from PIL import Image
            device = 0 if torch.cuda.is_available() else -1
            lighton_pipe = pipeline("image-text-to-text", model="lightonai/LightOnOCR-2-1B", device=device)
            
            data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
            elements = []
            n_boxes = len(data['text'])
            for i in range(n_boxes):
                conf = int(data['conf'][i])
                if conf > 0:
                    text_tess = data['text'][i].strip()
                    if text_tess:
                        x = data['left'][i]
                        y = data['top'][i]
                        w = data['width'][i]
                        h = data['height'][i]
                        center_x = x + w // 2
                        center_y = y + h // 2
                        
                        final_text = text_tess
                        if conf < 80:  # Low confidence, refine with LightOn
                            try:
                                # Crop region
                                x_int, y_int, w_int, h_int = int(x), int(y), int(w), int(h)
                                cropped = img[y_int:y_int+h_int, x_int:x_int+w_int]
                                if cropped.size > 0:
                                    pil_cropped = Image.fromarray(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))
                                    result = lighton_pipe(pil_cropped)
                                    refined_text = result[0]['generated_text'].strip()
                                    if refined_text:
                                        final_text = refined_text
                            except Exception as e:
                                print(f"Error refining text: {e}")
                        
                        elements.append({
                            'name': final_text,
                            'description': 'Text element',
                            'bbox': [x, y, w, h],
                            'center': [center_x, center_y]
                        })
            
            # Detect images with LightOn-bbox
            try:
                import re
                from transformers import LightOnOcrProcessor, LightOnOcrForConditionalGeneration
                processor_bbox = LightOnOcrProcessor.from_pretrained("lightonai/LightOnOCR-2-1B-bbox")
                model_bbox = LightOnOcrForConditionalGeneration.from_pretrained("lightonai/LightOnOCR-2-1B-bbox", torch_dtype=torch.bfloat16).to(device)
                
                pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                conversation = [{"role": "user", "content": [{"type": "image"}]}]
                inputs = processor_bbox.apply_chat_template(conversation, add_generation_prompt=True, tokenize=True, return_dict=True, return_tensors="pt")
                # Add image - assuming processor handles it
                inputs = {k: v.to(device=device) for k, v in inputs.items()}
                output_ids = model_bbox.generate(**inputs, max_new_tokens=1024)
                generated_ids = output_ids[0, inputs["input_ids"].shape[1]:]
                bbox_text = processor_bbox.decode(generated_ids, skip_special_tokens=True)
                
                # Parse for ![image](...) x1,y1,x2,y2
                image_matches = re.findall(r'!\[image\]\([^)]+\)\s+(\d+),(\d+),(\d+),(\d+)', bbox_text)
                for match in image_matches:
                    x1, y1, x2, y2 = map(int, match)
                    w = x2 - x1
                    h = y2 - y1
                    center_x = x1 + w // 2
                    center_y = y1 + h // 2
                    elements.append({
                        'name': 'Icon/Image',
                        'description': 'Detected image or icon',
                        'bbox': [x1, y1, w, h],
                        'center': [center_x, center_y]
                    })
            except Exception as e:
                print(f"Error detecting images: {e}")
            
            return elements
        except ImportError as e:
            print(f"Missing dependency for hybrid: {e}")
            return []
    else:
        print(f"Model '{model}' not supported.")
        return []

def save_json(elements, output_dir):
    """Save elements to JSON file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = os.path.join(output_dir, f"screenshot_elements_{timestamp}.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({'elements': elements}, f, indent=2, ensure_ascii=False)
    return json_path

def save_annotated_image(img, elements, output_dir):
    """Save annotated image with bounding boxes and names."""
    annotated = img.copy()
    for elem in elements:
        try:
            bbox = elem.get('bbox', [])
            if len(bbox) == 4:
                x, y, w, h = map(int, bbox)
                cv2.rectangle(annotated, (x, y), (x + w, y + h), (0, 255, 0), 2)
                name = elem.get('name', 'Unknown')[:20]  # Limit name length
                cv2.putText(annotated, name, (x, max(y - 10, 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        except Exception as e:
            print(f"Error drawing element {elem.get('name', 'Unknown')}: {e}")
            continue
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    img_path = os.path.join(output_dir, f"screenshot_annotated_{timestamp}.png")
    success = cv2.imwrite(img_path, annotated)
    if not success:
        print(f"Failed to save image to {img_path}")
        return None
    return img_path

def main():
    parser = argparse.ArgumentParser(description="Analyze screenshot for UI elements.")
    parser.add_argument('--output-dir', default='.', help='Output directory for files')
    parser.add_argument('--model', default='gemini', choices=['gemini', 'text', 'hybrid'], help='Detection model')
    args = parser.parse_args()

    output_dir = os.path.abspath(args.output_dir)
    os.makedirs(output_dir, exist_ok=True)

    print("Taking screenshot...")
    img = take_screenshot()

    print("Detecting elements...")
    elements = detect_elements(img, args.model)

    print(f"Detected {len(elements)} elements.")

    json_path = save_json(elements, output_dir)
    img_path = save_annotated_image(img, elements, output_dir)

    print(f"Results saved to: {json_path} and {img_path}")

if __name__ == "__main__":
    main()