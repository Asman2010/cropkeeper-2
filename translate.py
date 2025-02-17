from typing import List
from deep_translator import GoogleTranslator
import sys

def translate_chunk(text: str, target_lang: str) -> str:
    try:
        translator = GoogleTranslator(source='auto', target=target_lang)
        return translator.translate(text)
    except Exception as e:
        return f"Translation error: {str(e)}"

def split_text(text: str, chunk_size: int = 500) -> List[str]:
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def translate_text(text: str, target_language: str) -> str:
    sys.stdout.reconfigure(encoding='utf-8')
    chunks = split_text(text)
    translated_chunks = []
    for chunk in chunks:
        translated_chunk = translate_chunk(chunk, target_language)
        translated_chunks.append(translated_chunk)
    return " ".join(translated_chunks)
