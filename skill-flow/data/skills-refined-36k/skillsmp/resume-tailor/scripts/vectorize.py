import sys
import json
import requests

# Configuration
OLLAMA_URL = "http://localhost:11434/api/embeddings"
MODEL_NAME = "llama3.2"  # Ensure this model is pulled in Ollama

def get_embedding(text):
    """
    Generates a vector embedding for the given text using local Ollama.
    """
    payload = {
        "model": MODEL_NAME,
        "prompt": text
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["embedding"]
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Ollama: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    # Input: JSON string with "text" field, or raw text file path
    if len(sys.argv) < 2:
        print("Usage: python vectorize.py <text_string_or_file>")
        sys.exit(1)

    input_arg = sys.argv[1]
    
    # Determine if input is a file path or raw string
    target_text = input_arg
    try:
        with open(input_arg, 'r') as f:
            target_text = f.read()
    except (FileNotFoundError, OSError):
        # Treat as raw string
        pass

    vector = get_embedding(target_text)
    
    # Output: JSON list of floats (the vector)
    print(json.dumps(vector))
