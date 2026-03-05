import easyocr
import re

# Initialize once at module level (downloads model on first run)
reader = easyocr.Reader(['en'], gpu=False)

def extract_ingredients_from_image(image_bytes: bytes) -> list[str]:
    try:
        results = reader.readtext(image_bytes, detail=0, paragraph=True)
        print(f"[DEBUG] EasyOCR raw results: {results}")

        # Join all detected text blocks
        full_text = ' '.join(results)
        print(f"[DEBUG] Full text: {full_text}")

        # Find ingredients section
        lower_text = full_text.lower()
        if 'ingredient' in lower_text:
            idx = lower_text.find('ingredient')
            full_text = full_text[idx:]
            colon_idx = full_text.find(':')
            if colon_idx != -1:
                full_text = full_text[colon_idx + 1:]

        # Normalize separators — newlines and semicolons become commas
        full_text = full_text.replace('\n', ',').replace('\r', ',').replace(';', ',')

        # Split by comma
        raw_ingredients = full_text.split(',')

        parsed = []
        for ing in raw_ingredients:
            cleaned = re.sub(r'[^a-zA-Z0-9\-\s\(\)]', '', ing).strip().title()
            if len(cleaned) > 2:
                parsed.append(cleaned)

        # Remove duplicates while preserving order
        seen = set()
        unique_parsed = []
        for i in parsed:
            if i.lower() not in seen:
                seen.add(i.lower())
                unique_parsed.append(i)

        print(f"[DEBUG] Parsed ingredients: {unique_parsed}")
        return unique_parsed

    except Exception as e:
        print(f"EasyOCR Error: {e}")
        return []