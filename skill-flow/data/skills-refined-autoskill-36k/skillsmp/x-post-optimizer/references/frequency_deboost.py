# Technical Logic: Frequency Penalty Implementation
# Source: candidate-pipeline/src/filter/author_diversity.rs (Refactored logic)

def calculate_author_density_penalty(time_since_last_post_sec: int) -> float:
    """
    Simulates the deboost applied to multiple posts from the same author.
    Threshold: 3600 seconds (1 hour).
    """
    if time_since_last_post_sec < 3600:
        return 0.5  # 50% score reduction
    
    # Gradual recovery after 1 hour
    return 1.0

def get_optimized_score(base_score: float, seconds_since_last: int, has_link: bool) -> float:
    score = base_score
    
    # Apply Frequency Deboost
    score *= calculate_author_density_penalty(seconds_since_last)
    
    # Apply Link Penalty (Simulated de-amplification)
    if has_link:
        score *= 0.2  # 80% reduction for external URLs
        
    return score
