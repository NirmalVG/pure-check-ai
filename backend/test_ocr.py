import urllib.request
from ocr_service import extract_ingredients_from_image

url = "https://images.squarespace-cdn.com/content/v1/5c4883155b409b6992d9f8c6/1614051034446-A1XQZ3SDBJ5TQHY7VQ0R/skincare-label-ingredients.jpg"
print(f"Downloading from {url}...")
urllib.request.urlretrieve(url, "label_test.jpg")
print("Downloaded. Running OCR...")

with open("label_test.jpg", "rb") as f:
    data = f.read()

ingredients = extract_ingredients_from_image(data)
print("EXTRACTED INGREDIENTS:")
for i in ingredients:
    print(f"- {i}")
