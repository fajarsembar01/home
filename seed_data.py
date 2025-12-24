"""
Script to seed database with sample property data
Uses AI processor to extract data from raw text first
"""

import asyncio
import logging
from database import init_db, get_or_create_user, create_property
from ai_processor import extract_property_info

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sample data from user (Batch 2)
SAMPLES = [
    """
    RUMAH SIAP HUNI PONDOK CANDRA
    JualSewa Rumah
    PONDOK CANDRA RAMBUTAN - Sidoarjo
    LT 180 LB 120
    KT 3+1 KM 1+1
    Dimensi 12 x 15
    Listrik 2200
    Rp 1.400.000.000 
    Rp 28.000.000 
    SHM
    Hadap Utara

    SIAP HUNI 

    LOKASI SUPER STRATEGIS DISAMPING MERR DAN TOL JUANDA

    •⁠  ⁠10 MENIT KE BANDARA JUANDA

    •⁠  ⁠DEKAT CLUBHOUSE

    •⁠  ⁠DEKAT SUPERMARKET 

    •⁠  ⁠DEKAT SEKOLAH TK SD PETRA

    •⁠  ⁠LINGKUNGAN ELIT DAN NYAMAN

    •⁠  ⁠1 GATE SYSTEM AMAN

    •⁠  ⁠JARINGAN TELKOM

    •⁠  ⁠PLN (2200 WATT)

    •⁠  ⁠PDAM

    •⁠  ⁠JALAN FULL PAVING

    •⁠  ⁠BEBAS BANJIR

    https://www.brighton.co.id/cari-properti/view/jalan-rambutan-jeoa?related=24525

    Untuk foto dan keterangan properti bisa klik link yang ada di bawahnya.

    Hubungi: 
    ELISABETH YULIANA (FACP) - 08123267388
    Brighton Eagle
    Rungkut - Surabaya
    https://www.brighton.co.id/yuliana123456
    """,
    
    """
    PONDOK CANDRA INDAH DEKAT MERR RUNGKUT CLUSTER DEPAN RS MITRA KELUARGA INDOMARET  BANYAK KULINER DISEKITARNYA TOLL JUANDA & TAMBAK SUMUR 
    Jual Rumah
    PONDOK CANDRA INDAH RAMBUTAN TENGAH - Sidoarjo
    LT 200 LB 160
    KT 3 KM 2
    Dimensi 10 x 20
    Listrik 2200
    Rp 2.100.000.000 
    SHM
    Hadap Barat

    LUAS 10X20 = 200M
    LUAS BANGUNAN 160M
    KT 3 KM 2 
    HADAP BARAT 
    PDAM  
    PLN 2200V
    CARPORT 2 MOBIL
    ROW JALAN 3MOBIL (8-9M)

    DEKAT SEKOLAH PETRA 
    CLUSTER DEPAN 
    DEKAT RS MITRA KELUARGA 
    DEKAT INDOMARET 
    BANYAK KULINER DISEKITARNYA 
    DEKAT TOLL JUANDA & TAMBAK SUMUR 

    HARGA 2,1 M


    https://www.brighton.co.id/cari-properti/view/pondok-candra-indah-rambutan-tengah-1?related=24525

    Untuk foto dan keterangan properti bisa klik link yang ada di bawahnya.

    Hubungi: 
    ELISABETH YULIANA (FACP) - 08123267388
    Brighton Eagle
    Rungkut - Surabaya
    https://www.brighton.co.id/yuliana123456
    """,
    
    """
    RUMAH SEMI 2 LANTAI DI KOMPLEK RAMBUTAN PONDOK TJANDRA INDAH
    Jual Rumah
    RAMBUTAN PONDOK TJANDRA INDAH - Sidoarjo
    LT 180 LB 120
    KT 6 KM 2
    Dimensi 12 x 15
    Listrik 2200
    Rp 1.2M
    SHM
    Hadap Utara

    DIJUAL CEPAT RUMAH SEMI 2 LANTAI, RAMBUTAN PONDOK TJANDRA INDA

    SELANGKAH KE GEREJA
    SELANGKAH KE SEKOLAH SD PETRA 13
    SELANGKAH KE MASJID

    KAMAR TIDUR 6
    KAMAR MANDI 2
    KAWASAN AMAN
    """
]

def seed_data():
    print("🌱 Starting data seeding...")
    
    # Init DB
    init_db()
    
    # Create a dummy admin user if not exists
    admin_user = get_or_create_user(
        telegram_id=999999999,
        username="admin_seeder",
        first_name="Admin",
        last_name="Seeder"
    )
    print(f"👤 Using admin user ID: {admin_user.id}")
    
    for i, raw_text in enumerate(SAMPLES, 1):
        print(f"\nProcessing Sample #{i}...")
        
        # 1. Extract data using AI
        print("   🤖 Extracting data with AI...")
        extracted_data = extract_property_info(raw_text)
        
        if not extracted_data:
            print("   ❌ Failed to extract data")
            continue
            
        print(f"   ✅ Extracted: {extracted_data.get('property_type')} in {extracted_data.get('city')}")
        
        # 2. Save to DB
        try:
            prop = create_property(admin_user.id, extracted_data)
            print(f"   💾 Saved to DB with ID: {prop.id}")
        except Exception as e:
            print(f"   ❌ Error saving: {e}")
            
    print("\n✨ Seeding complete!")

if __name__ == "__main__":
    seed_data()
