import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random

# We must import from models and database relative to the current working directory or absolute
# Let's just put it in a script that imports from database and models
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import Base, SQLALCHEMY_DATABASE_URL
from database.models import Ingredient, Product, SafetyRating

def create_db():
    pass

def seed_data():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Clear existing data if necessary (optional)
    session.query(Ingredient).delete()
    session.query(Product).delete()
    session.commit()

    # 1. Add required canonical ingredients from UI designs
    real_ingredients = [
        ("Methylparaben", SafetyRating.AVOID, "Known endocrine disruptor. May interfere with hormone function.", "All"),
        ("Fragrance (Parfum)", SafetyRating.IRRITANT, "Complex mixture of chemicals. High potential for allergic reactions.", "Not suitable for sensitive skin"),
        ("Sodium Hyaluronate", SafetyRating.SAFE, "Premium humectant that draws moisture into the skin.", "Dry, All"),
        ("Niacinamide", SafetyRating.SAFE, "Vitamin B3. Highly effective skin-restoring ingredient.", "Oily, Aging, All"),
        ("Hyaluronic Acid", SafetyRating.SAFE, "A naturally occurring glycosaminoglycan found throughout the body.", "Dry, All"),
        ("Oxybenzone", SafetyRating.AVOID, "Chemical sunscreen filter linked to endocrine disruption and coral reef damage.", "All"),
        ("Retinyl Palmitate", SafetyRating.MODERATE, "A combination of retinol and palmitic acid. Effective for anti-aging but may cause skin sensitivity.", "Aging"),
        ("Phenoxyethanol", SafetyRating.MODERATE, "A common preservative used to prevent bacteria growth. Generally safe at 1% or less.", "All"),
        ("Formaldehyde", SafetyRating.AVOID, "A known human carcinogen often released by certain preservatives.", "All"),
        ("Titanium Dioxide", SafetyRating.SAFE, "Mineral sunscreen filter. Safe and effective.", "Sensitive, All"),
        ("Zinc Oxide", SafetyRating.SAFE, "Mineral sunscreen filter. Reef safe.", "Sensitive, All"),
        ("Avobenzone", SafetyRating.MODERATE, "Chemical UVA filter. Can degrade in sunlight.", "All"),
    ]

    for name, rating, desc, skin in real_ingredients:
        session.add(Ingredient(name=name, safety_rating=rating, description=desc, compatible_skin_types=skin))

    session.commit()

    # 2. Generate remaining ingredients to hit the 300 requirement
    prefixes = ["Sodium", "Potassium", "Calcium", "Magnesium", "Methyl", "Ethyl", "Propyl", "Butyl", "Isobutyl", "Tert-butyl",
                "PEG-", "PPG-", "Alpha-", "Beta-", "Gamma-", "Iso", "Cyclo", "Di", "Tri", "Poly", "Acryl", "Benzyl", "Cetyl",
                "Decyl", "Lauryl", "Myristyl", "Palmitoyl", "Stearyl", "Behenyl", "Oleyl", "Linoleyl", "Coco-", "Capryl",
                "Glyceryl", "Sorbitan", "Polysorbate", "Dimethicone", "Silicone", "Fluor", "Chloro", "Bromo", "Iodo",
                "Amino", "Hydroxy", "Methoxy", "Ethoxy", "Propoxy", "Butoxy", "Phenoxy", "Nitro", "Cyan", "Sulf", "Phospho"]
    
    suffixes = ["paraben", "sulfate", "chloride", "bromide", "acetate", "propionate", "butyrate", "benzoate", "salicylate",
                "sorbate", "phosphate", "nitrate", "carbonate", "oxide", "peroxide", "hydroxide", "glycol", "glycerin",
                "alcohol", "phenol", "ether", "acid", "peptide", "ceramide", "extract", "oil", "wax", "butter"]

    existing_names = {i[0] for i in real_ingredients}
    generated_count = 0
    target_total = 350
    
    ratings_pool = list(SafetyRating)

    all_combos = [(p, s) for p in prefixes for s in suffixes]
    random.shuffle(all_combos)

    for p, s in all_combos:
        if len(existing_names) >= target_total:
            break
        
        # Format the name
        name = f"{p} {s}" if not p.endswith("-") else f"{p}{s}"
        name = name.title() if not name.isupper() else name

        if name not in existing_names:
            rating = random.choice(ratings_pool)
            
            # Artificial descriptions
            if rating == SafetyRating.SAFE:
                desc = f"A commonly used {s.lower()} derivative acting as a conditioning agent and emulsifier."
            elif rating == SafetyRating.MODERATE:
                desc = f"A standard {s.lower()} compound. Can occasionally cause mild sensitivity in broken skin."
            elif rating == SafetyRating.IRRITANT:
                desc = f"A strong {s.lower()} derivative known to cause contact dermatitis."
            else:
                desc = f"A harsh {s.lower()} chemical linked to toxicity concerns in high concentrations."

            session.add(Ingredient(
                name=name,
                safety_rating=rating,
                description=desc,
                compatible_skin_types="All" if rating == SafetyRating.SAFE else "None"
            ))
            existing_names.add(name)
    
    session.commit()
    print(f"Successfully seeded {len(existing_names)} ingredients.")
    session.close()

if __name__ == "__main__":
    print("Creating DB...")
    create_db()
    print("Seeding data...")
    seed_data()
    print("Done!")
