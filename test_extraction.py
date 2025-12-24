"""
Test AI Extraction with real property data
"""
import json
from ai_processor import extract_property_info

# Test data from user
test_input = """DEKAT SEKOLAH TK SD PETRA, RAMBUTAN PONDOK TJANDRA
Jual Rumah
PONDOK CANDRA RAMBUTAN - Sidoarjo
LT 180 LB 200
KT 3+1 KM 2+1
Dimensi 12 x 15
Listrik 2200
Rp 1.300.000.000 
SHM
Hadap Utara

JUAL CEPAT TURUN HARGA  RAMBUTAN  PONDOK TJANDRA 

LUAS 12X15M = 180M2
SHM , HADAP UTARA
KT 3 + 1 KT PEMBANTU 
KM DLM BATHTUB 1 + KM LUAR 1 + KM PEMBANTU 1 
ATAS ADA 1 RUANGAN LOSS 
ADA RUANGAN U/ GUDANG 
DAPUR 
GALVALUM 
SIAP HUNI 

 LOKASI SUPER STRATEGIS DISAMPING MERR DAN TOL JUANDA
•  10 MENIT KE BANDARA JUANDA
•  DEKAT CLUBHOUSE
•  DEKAT SUPERMARKET 
•  DEKAT SEKOLAH SD PETRA & SMP SMA ACITYA
•  LINGKUNGAN ELIT DAN NYAMAN
•  1 GATE SYSTEM AMAN
•  JARINGAN TELKOM
•  PLN (2200 WATT)
•  PDAM
•  JALAN FULL PAVING
•  BEBAS BANJIR 

HARGA 1.650M 》1.350M 》1.300 NEGO

https://www.brighton.co.id/cari-properti/view/pondok-candra-rambutan-9?related=24525

Untuk foto dan keterangan properti bisa klik link yang ada di bawahnya.

Hubungi: 
ELISABETH YULIANA (FACP) - 08123267388
Brighton Eagle
Rungkut - Surabaya
https://www.brighton.co.id/yuliana123456
"""

print("=" * 80)
print("TESTING AI EXTRACTION")
print("=" * 80)
print("\nProcessing property description...\n")

try:
    result = extract_property_info(test_input)
    
    print("✅ EXTRACTION SUCCESSFUL!\n")
    print("=" * 80)
    print("EXTRACTED DATA:")
    print("=" * 80)
    
    # Pretty print critical fields
    print(f"\n🏠 PROPERTY TYPE: {result.get('property_type', 'NOT FOUND')}")
    print(f"💼 TRANSACTION: {result.get('transaction_type', 'NOT FOUND')}")
    print(f"🏷️  CONDITION: {result.get('condition', 'NOT FOUND')}")
    
    print(f"\n💰 PRICING:")
    price = result.get('price')
    if price:
        print(f"  • Harga Jual: Rp {price:,}")
    else:
        print(f"  • Harga Jual: NOT FOUND ❌")
    print(f"  • Negotiable: {result.get('negotiable', 'NOT FOUND')}")
    
    print(f"\n📐 SPECIFICATIONS:")
    print(f"  • Land Area (LT): {result.get('land_area', 'NOT FOUND')} m²")
    print(f"  • Building Area (LB): {result.get('building_area', 'NOT FOUND')} m²")
    print(f"  • Bedrooms (KT): {result.get('bedrooms', 'NOT FOUND')}")
    print(f"  • Bathrooms (KM): {result.get('bathrooms', 'NOT FOUND')}")
    print(f"  • Dimensions: {result.get('dimensions', 'NOT FOUND')}")
    print(f"  • Electricity: {result.get('electricity', 'NOT FOUND')} Watt")
    print(f"  • Orientation: {result.get('orientation', 'NOT FOUND')}")
    
    print(f"\n📍 LOCATION:")
    print(f"  • Address: {result.get('address', 'NOT FOUND')}")
    print(f"  • District: {result.get('district', 'NOT FOUND')}")
    print(f"  • City: {result.get('city', 'NOT FOUND')}")
    
    print(f"\n📜 LEGAL:")
    print(f"  • Certificate: {result.get('certificate_type', 'NOT FOUND')}")
    print(f"  • IMB: {result.get('imb', 'NOT FOUND')}")
    
    print(f"\n📞 CONTACT:")
    print(f"  • Name: {result.get('contact_name', 'NOT FOUND')}")
    print(f"  • Phone: {result.get('contact_phone', 'NOT FOUND')}")
    
    print(f"\n🔗 LINKS:")
    print(f"  • Property URL: {result.get('property_url', 'NOT FOUND')}")
    print(f"  • Agent URL: {result.get('agent_url', 'NOT FOUND')}")
    
    print(f"\n✨ FACILITIES:")
    facilities = result.get('facilities', [])
    if facilities:
        print(f"  {', '.join(facilities)}")
    else:
        print(f"  NOT FOUND")
    
    print("\n" + "=" * 80)
    print("FULL JSON OUTPUT:")
    print("=" * 80)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
