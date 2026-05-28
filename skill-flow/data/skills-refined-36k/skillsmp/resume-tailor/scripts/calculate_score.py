import sys
import json
import math

def cosine_similarity(vec_a, vec_b):
    """
    Computes the cosine similarity between two vectors.
    Returns a score between -1.0 and 1.0 (1.0 is identical).
    """
    if len(vec_a) != len(vec_b):
        raise ValueError(f"Vector dimensions do not match: {len(vec_a)} vs {len(vec_b)}")

    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = math.sqrt(sum(a * a for a in vec_a))
    magnitude_b = math.sqrt(sum(b * b for b in vec_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python calculate_score.py <vector_a_json> <vector_b_json>")
        sys.exit(1)

    try:
        # Load vectors from JSON strings or files
        # (Assuming the agent passes them as JSON strings for simplicity here)
        vec_a = json.loads(sys.argv[1])
        vec_b = json.loads(sys.argv[2])
        
        score = cosine_similarity(vec_a, vec_b)
        
        # Output: Normalized percentage score (0-100)
        # Cosine similarity is usually -1 to 1. For text embeddings, it's typically 0 to 1.
        normalized_score = max(0, score) * 100
        
        result = {
            "cosine_similarity": score,
            "match_score": round(normalized_score, 2)
        }
        
        print(json.dumps(result))

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON input: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
