import pytest
from database.models import Ingredient, SafetyRating

def populate_db(db_session):
    ing1 = Ingredient(name="Water", safety_rating=SafetyRating.SAFE, description="Base", compatible_skin_types="All")
    ing2 = Ingredient(name="Fragrance", safety_rating=SafetyRating.IRRITANT, description="Scent", compatible_skin_types="None")
    db_session.add_all([ing1, ing2])
    db_session.commit()

def test_search_ingredients_empty(client):
    response = client.get("/api/ingredients/search")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert data["total"] == 0

def test_search_ingredients_with_query(client, db_session):
    populate_db(db_session)
    response = client.get("/api/ingredients/search?query=Fragrance")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["name"] == "Fragrance"

def test_analyze_label(client, db_session, monkeypatch):
    populate_db(db_session)
    
    # Mocking the OCR service extraction inside main.py to avoid calling actual pytesseract
    def mock_extract(*args):
        return ["Water", "Fragrance", "UnknownChemical"]
    
    import main
    monkeypatch.setattr(main, "extract_ingredients_from_image", mock_extract)
    
    # Provide a dummy file structure to UploadFile parameter via FastAPI test client
    files = {"file": ("test.jpg", b"fake_image", "image/jpeg")}
    response = client.post("/api/analyze/image", files=files)
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["extracted_raw_count"] == 3
    assert len(data["ingredients"]) == 3
    assert data["summary"]["safe"] == 1
    assert data["summary"]["irritant"] == 1
    assert data["summary"]["unknown"] == 1

def test_get_recommendations(client, db_session):
    populate_db(db_session)
    response = client.post(
        "/api/quiz/recommendations",
        data={"skin_type": "All", "sensitivities": "None"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["skin_type"] == "All"
    assert len(data["recommended_ingredients"]) == 1
    assert data["recommended_ingredients"][0]["name"] == "Water"
