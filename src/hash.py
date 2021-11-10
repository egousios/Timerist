

def hash_char_for_astrix(character_sequence: str) -> str:
    """Replaces every character in a sequence of characters with an astrix."""
    return ", ".join(["*" for c in character_sequence]).replace(", ", "")