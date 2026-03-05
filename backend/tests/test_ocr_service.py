import pytest
from unittest.mock import patch
from ocr_service import extract_ingredients_from_image

@patch('ocr_service.pytesseract.image_to_string')
@patch('ocr_service.Image.open')
def test_extract_ingredients_from_image(mock_image_open, mock_image_to_string):
    # Setup mock returns
    mock_image_to_string.return_value = "Water, Glycerin, Niacinamide\nDimethicone"
    
    # Call function
    res = extract_ingredients_from_image(b"fake_image_data")
    
    # Verify mock interactions
    mock_image_open.assert_called_once()
    mock_image_to_string.assert_called_once()
    
    # Verify OCR service cleaning logic
    assert "Water" in res
    assert "Glycerin" in res
    assert "Niacinamide Dimethicone" in res
    assert len(res) == 3

def test_extract_ingredients_returns_empty_on_error():
    # Provide an empty invalid byte array to force image open exception
    res = extract_ingredients_from_image(b"")
    assert res == []
