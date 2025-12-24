"""
Script to migrate database schema
Adds new columns to properties table
"""

import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)

def migrate():
    print("🔄 Migrating database...")
    
    with engine.connect() as conn:
        # List of new columns to add
        columns = [
            ("electricity", "INTEGER"),
            ("orientation", "VARCHAR(50)"),
            ("dimensions", "VARCHAR(50)"),
            ("row_road", "VARCHAR(100)"),
            ("property_url", "TEXT"),
            ("agent_url", "TEXT"),
            ("rent_price", "BIGINT"),
            ("condition", "VARCHAR(50)"),
            ("water_type", "VARCHAR(50)"),
            ("furnished", "VARCHAR(50)"),
            ("phone_line_count", "INTEGER"),
            ("kpr", "BOOLEAN"),
            ("imb", "BOOLEAN"),
            ("blueprint", "BOOLEAN"),
            ("video_review_url", "TEXT")
        ]
        
        for col_name, col_type in columns:
            try:
                # Changes floors to DECIMAL first if needed (manual step usually, but let's just add new cols)
                # Note: floors change from integer to decimal might need explicit ALTER COLUMN
                
                query = text(f"ALTER TABLE properties ADD COLUMN IF NOT EXISTS {col_name} {col_type};")
                conn.execute(query)
                print(f"   ✅ Added column: {col_name}")
            except Exception as e:
                print(f"   ⚠️  Error adding {col_name}: {e}")
        
        # Modify floors column type
        try:
            conn.execute(text("ALTER TABLE properties ALTER COLUMN floors TYPE DECIMAL(3,1);"))
            print("   ✅ Modified column: floors (to DECIMAL)")
        except Exception as e:
            print(f"   ⚠️  Error modifying floors: {e}")
            
        conn.commit()
    
    print("✨ Migration complete!")

if __name__ == "__main__":
    migrate()
