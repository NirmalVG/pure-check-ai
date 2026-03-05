from database.models import Ingredient, Product, SafetyRating

def test_create_ingredient(db_session):
    ing = Ingredient(
        name="Glycerin",
        description="A natural moisturizer.",
        safety_rating=SafetyRating.SAFE,
        compatible_skin_types="Dry, All"
    )
    db_session.add(ing)
    db_session.commit()
    db_session.refresh(ing)
    
    assert ing.id is not None
    assert ing.name == "Glycerin"  # type: ignore[reportGeneralTypeIssues]
    assert ing.safety_rating == SafetyRating.SAFE  # type: ignore[reportGeneralTypeIssues]

def test_create_product(db_session):
    product = Product(
        name="Hydrating Cleanser",
        brand="Cerave",
        ingredients_list="Water, Glycerin"
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    
    assert product.id is not None
    assert product.brand == "Cerave"  # type: ignore[reportGeneralTypeIssues]
