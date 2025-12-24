"""
AI Processor using Google Gemini for property data extraction
"""

import os
import logging
import json
from typing import Dict, Any, Optional
from google import genai
from google.genai.types import GenerateContentConfig
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'))
logger = logging.getLogger(__name__)

# Configure Gemini AI
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY not found in environment variables")
    raise ValueError("GEMINI_API_KEY is required")

# Initialize client with new package
client = genai.Client(api_key=GEMINI_API_KEY)


# Function declarations for Gemini function calling
property_extraction_function = {
    "name": "extract_property_data",
    "description": "Extract structured property information from user's natural language description",
    "parameters": {
        "type": "object",
        "properties": {
            "property_type": {
                "type": "string",
                "description": "Type of property",
                "enum": ["rumah", "apartemen", "tanah", "ruko", "villa", "kost", "gudang", "kantor", "lainnya"]
            },
            "transaction_type": {
                "type": "string",
                "description": "Sale or rent",
                "enum": ["jual", "sewa"]
            },
            "address": {
                "type": "string",
                "description": "Full address of the property"
            },
            "city": {
                "type": "string",
                "description": "City name"
            },
            "district": {
                "type": "string",
                "description": "District/Kecamatan name"
            },
            "province": {
                "type": "string",
                "description": "Province name"
            },
            "price": {
                "type": "integer",
                "description": "Price in Indonesian Rupiah"
            },
            "negotiable": {
                "type": "boolean",
                "description": "Whether price is negotiable"
            },
            "land_area": {
                "type": "integer",
                "description": "Land area in square meters"
            },
            "building_area": {
                "type": "integer",
                "description": "Building area in square meters"
            },
            "bedrooms": {
                "type": "integer",
                "description": "Number of bedrooms"
            },
            "bathrooms": {
                "type": "integer",
                "description": "Number of bathrooms"
            },
            "floors": {
                "type": "integer",
                "description": "Number of floors"
            },
            "carports": {
                "type": "integer",
                "description": "Number of carports"
            },
            "garages": {
                "type": "integer",
                "description": "Number of garages"
            },
            "year_built": {
                "type": "integer",
                "description": "Year the property was built"
            },
            "facilities": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of facilities/amenities"
            },
            "certificate_type": {
                "type": "string",
                "description": "Certificate type",
                "enum": ["SHM", "SHGB", "AJB", "Girik", "Lainnya"]
            },
            "description": {
                "type": "string",
                "description": "Additional description"
            },
            "contact_name": {
                "type": "string",
                "description": "Contact person name"
            },
            "contact_phone": {
                "type": "string",
                "description": "Contact phone number"
            },
            "contact_whatsapp": {
                "type": "string",
                "description": "WhatsApp number"
            }
        },
        "required": ["property_type", "transaction_type"]
    }
}


class QuotaExceededError(Exception):
    """Raised when Gemini API quota is exceeded"""
    pass

def extract_property_info(user_input: str, conversation_history: Optional[str] = None) -> Dict[str, Any]:
    """
    Extract property information from user's natural language input using Gemini AI
    
    Args:
        user_input: User's message describing the property
        conversation_history: Optional conversation context
        
    Returns:
        Dictionary with extracted property data
    """
    # Try Gemini AI first
    try:
        # Build prompt with context
        system_prompt = """Anda adalah asisten AI yang membantu mengekstrak informasi properti dari deskripsi pengguna.
Tugas Anda adalah mengidentifikasi dan mengekstrak data properti terstruktur dari percakapan natural.

PENTING: Keluarkan hasil HANYA dalam format JSON dengan key bahasa Inggris berikut:
{
    "property_type": "rumah/apartemen/tanah/ruko/villa/dll",
    "condition": "Baru/Bekas/Siap Huni/Butuh Renovasi",
    "transaction_type": "jual/sewa/jual sewa",
    "city": "nama kota",
    "district": "nama kecamatan",
    "address": "alamat lengkap",
    "price": 1000000000 (angka dalam rupiah, prioritas harga jual),
    "rent_price": 50000000 (angka dalam rupiah, jika ada harga sewa),
    "negotiable": true/false,
    "land_area": 100 (angka m2),
    "building_area": 100 (angka m2),
    "bedrooms": 3 (angka),
    "bathrooms": 2 (angka),
    "floors": 2 (angka),
    "garages": 1 (angka),
    "carports": 1 (angka),
    "year_built": 2020 (angka),
    "orientation": "Selatan/Utara/dll",
    "dimensions": "10 x 20",
    "row_road": "3 mobil/6 meter",
    "water_type": "PDAM/Sumur",
    "electricity": 2200 (angka watt),
    "phone_line_count": 1 (angka),
    "furnished": "Full/Semi/Kosongan",
    "kpr": true/false,
    "imb": true/false,
    "blueprint": true/false,
    "facilities": ["ac", "taman", "kolam renang"],
    "certificate_type": "SHM/SHGB/dll",
    "description": "deskripsi singkat",
    "contact_name": "nama kontak",
    "contact_phone": "nomor telepon",
    "property_url": "link properti",
    "agent_url": "link agen",
    "video_review_url": "link video review"
}

Peraturan:
1. "property_type" harus salah satu dari: rumah, apartemen, tanah, ruko, villa, gudang, kantor
2. "condition" ekstrak dari kata kunci: "Baru/New/Gress" -> "Baru", "Second/Lama" -> "Bekas", "Siap Huni" -> "Siap Huni", "Hitung Tanah" -> "Butuh Renovasi"
3. "transaction_type" harus: jual, sewa, atau "jual sewa" (jika kedua opsi tersedia)
4. Jika ada dua harga (jual & sewa), masukkan harga jual ke "price" dan harga sewa ke "rent_price".
5. Jika hanya satu harga, masukkan ke "price".
6. Harga harus angka murni tanpa titik/koma.
7. PERHATIAN KHUSUS HARGA vs UKURAN:
   - Angka dengan akhiran "M" bisa berarti Miliar atau Meter. LIHAT KONTEKSNYA!
   - Jika didahului "Rp", "Jual", "Harga" -> MILIAR (contoh: "Harga 1.300M" atau "1.3M" -> 1300000000)
   - Jika didahului "LT", "LB", "Luas", "Dimensi", "Panjang", "Lebar" -> METER (contoh: "LT 180" -> 180, BUKAN harga)
   - Format "12x15" atau "12 x 15" -> itu DIMENSI, masuk ke "dimensions"
8. PARSING KAMAR (KT/KM):
   - "KT 3+1" atau "3+1 KT" -> bedrooms: 3 (ambil angka PERTAMA saja, abaikan pembantu)
   - "KM 2+1" atau "2+1 KM" -> bathrooms: 2 (ambil angka PERTAMA saja)
   - Jika ada "KT PEMBANTU" atau "KM PEMBANTU", jangan hitung di angka utama
9. HARGA DENGAN POTONGAN:
   - Jika ada beberapa harga (misal "1.650M >> 1.350M >> 1.300M"), ambil yang TERAKHIR/PALING KECIL sebagai harga final
   - "NEGO" atau "NEGOTIABLE" -> negotiable: true
10. KONTAK:
   - Cari nama dan nomor telepon di seluruh teks
   - Format nomor: 08xxx, +62xxx, (0xx)xxx, dsb
   - Biasanya ada kata "Hubungi", "Kontak", "CP", atau nama di dekat nomor
11. LOKASI:
   - "district" untuk kecamatan (misal: "Rambutan", "Pondok Indah")
   - "city" untuk kota (misal: "Sidoarjo", "Jakarta Selatan")
   - Jika ada nama komplek/area, masukkan ke "address"
12. URLS:
   - Ekstrak semua link http/https ke field yang sesuai (property_url, agent_url)
13. Jika informasi tidak ada atau tidak jelas, isi dengan null (JANGAN isi sembarangan).
"""

        # Combine conversation history if available
        full_prompt = f"{system_prompt}\n\nInput pengguna: {user_input}"
        
        # Use gemini-flash-latest (stable, good balance of speed and quota)
        response = client.models.generate_content(
            model='gemini-flash-latest',
            contents=full_prompt,
            config=GenerateContentConfig(
                temperature=0.1,  # Low temperature for consistent extraction
            )
        )
        
        # Parse response
        extracted_data = {}
        
        if response.text:
            # Try to extract JSON from response
            try:
                # Look for JSON in the response
                text = response.text
                if '{' in text and '}' in text:
                    start = text.index('{')
                    end = text.rindex('}') + 1
                    json_str = text[start:end]
                    extracted_data = json.loads(json_str)
            except json.JSONDecodeError:
                logger.warning("Could not parse JSON from AI response, using text analysis")
                # Fallback: manual parsing
                extracted_data = _parse_text_response(user_input, response.text)
        
        # If AI returned some data, use it; otherwise fallback
        if extracted_data:
            logger.info(f"Extracted property data via AI: {extracted_data}")
            return extracted_data
        
    except Exception as e:
        error_msg = str(e)
        if '429' in error_msg or 'RESOURCE_EXHAUSTED' in error_msg:
            logger.warning(f"Gemini API quota exceeded: {error_msg}")
            raise QuotaExceededError("Gemini API quota exceeded")
        else:
            logger.error(f"Error extracting property info with Gemini: {e}")
    
    # Fallback to basic extraction
    logger.info("Using fallback text parser due to error")
    return _parse_text_response(user_input, "")


def parse_search_query(user_query: str) -> Dict[str, Any]:
    """
    Parse user's natural language search query into structured filters
    """
    try:
        system_prompt = """Anda adalah asisten pencarian properti. 
Tugas Anda: Terjemahkan keinginan user menjadi filter database SQL.

Input User: "Cari rumah di Jaksel minimal 3 kamar harga max 5M yang ada kolam renang"

Output JSON:
{
    "property_type": "rumah",
    "location_keyword": "Jakarta Selatan", 
    "min_price": null,
    "max_price": 5000000000,
    "min_bedrooms": 3,
    "min_land_area": null,
    "must_have_facilities": ["kolam renang"]
}

Peraturan:
1. Harga harus angka murni (5M -> 5000000000).
2. location_keyword bisa nama kota, kecamatan, atau area.
3. null jika tidak disebutkan.
4. "must_have_facilities" adalah list string.
"""
        
        full_prompt = f"{system_prompt}\n\nInput User: {user_query}"
        
        response = client.models.generate_content(
            model='gemini-flash-latest',
            contents=full_prompt,
            config=GenerateContentConfig(temperature=0.1)
        )
        
        filters = {}
        if response.text:
            try:
                text = response.text
                if '{' in text and '}' in text:
                    start = text.index('{')
                    end = text.rindex('}') + 1
                    json_str = text[start:end]
                    filters = json.loads(json_str)
            except json.JSONDecodeError:
                pass
                
        logger.info(f"Parsed search query: {filters}")
        return filters

    except Exception as e:
        error_msg = str(e)
        if '429' in error_msg or 'RESOURCE_EXHAUSTED' in error_msg:
            logger.warning(f"Gemini API quota exceeded for search")
            raise QuotaExceededError("Gemini API quota exceeded")
        logger.error(f"Error parsing search query: {e}")
        return {}  # Return empty dict on error (will fall back to basic text search)


def _parse_text_response(user_input: str, ai_response: str = "") -> Dict[str, Any]:
    """
    Fallback parser for extracting basic property info from text
    """
    data = {}
    text = (user_input + " " + ai_response).lower()
    
    # Property type detection
    if "rumah" in text:
        data['property_type'] = "rumah"
    elif "apartemen" in text or "apartment" in text:
        data['property_type'] = "apartemen"
    elif "tanah" in text or "kavling" in text:
        data['property_type'] = "tanah"
    elif "ruko" in text:
        data['property_type'] = "ruko"
    elif "villa" in text:
        data['property_type'] = "villa"
    
    # Transaction type
    if "sewa" in text or "rent" in text or "kontrak" in text:
        data['transaction_type'] = "sewa"
    elif "jual" in text or "dijual" in text or "beli" in text:
        data['transaction_type'] = "jual"
    
    # Price extraction (basic)
    import re
    
    # Look for price patterns like "2 miliar", "500 juta", "2M", "500jt"
    price_patterns = [
        r'(\d+[\.,]?\d*)\s*(?:miliar|milyar|m\b)',  # billions
        r'(\d+[\.,]?\d*)\s*(?:juta|jt)',  # millions
        r'rp\.?\s*(\d+[\.,]?\d*)',  # Rp notation
    ]
    
    for pattern in price_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            price_str = match.group(1).replace(',', '.')
            price_val = float(price_str)
            
            if 'miliar' in match.group(0).lower() or 'm' in match.group(0).lower():
                data['price'] = int(price_val * 1_000_000_000)
            elif 'juta' in match.group(0).lower() or 'jt' in match.group(0).lower():
                data['price'] = int(price_val * 1_000_000)
            else:
                data['price'] = int(price_val)
            break
    
    # Bedrooms
    bedroom_match = re.search(r'(\d+)\s*(?:kamar tidur|kt|bedroom|bed)', text, re.IGNORECASE)
    if bedroom_match:
        data['bedrooms'] = int(bedroom_match.group(1))
    
    # Bathrooms
    bathroom_match = re.search(r'(\d+)\s*(?:kamar mandi|km|bathroom|bath)', text, re.IGNORECASE)
    if bathroom_match:
        data['bathrooms'] = int(bathroom_match.group(1))
    
    # Land area
    land_match = re.search(r'(?:luas tanah|lt)\s*[:\-]?\s*(\d+)\s*(?:m2|m²|meter)', text, re.IGNORECASE)
    if land_match:
        data['land_area'] = int(land_match.group(1))
    
    # Building area
    building_match = re.search(r'(?:luas bangunan|lb)\s*[:\-]?\s*(\d+)\s*(?:m2|m²|meter)', text, re.IGNORECASE)
    if building_match:
        data['building_area'] = int(building_match.group(1))
    
    return data


def generate_property_summary(property_data: Dict[str, Any]) -> str:
    """
    Generate a human-readable summary of property data
    """
    data = property_data # Use a shorter alias for convenience
    
    # Start with title
    parts = ["✨ *Ringkasan Properti:*"]
    
    # 1. Type and Transaction
    prop_type = data.get('property_type', 'Properti').capitalize()
    trans_type = data.get('transaction_type', '').capitalize()
    condition = data.get('condition', '')
    
    type_str = f"🏠 *{prop_type}*"
    if condition:
        type_str += f" ({condition})"
    type_str += f" - {trans_type}"
    parts.append(type_str)
    
    # 2. Location
    location_parts = []
    if data.get('address'):
        location_parts.append(data['address'])
    if data.get('district'):
        location_parts.append(data['district'])
    if data.get('city'):
        location_parts.append(data['city'])
    
    if location_parts:
        parts.append(f"📍 {', '.join(location_parts)}")
    
    # 3. Price
    price_info = ""
    if data.get('price'):
        price = data['price']
        if price >= 1_000_000_000:
            price_str = f"Rp {price / 1_000_000_000:.1f} Miliar"
        elif price >= 1_000_000:
            price_str = f"Rp {price / 1_000_000:.0f} Juta"
        else:
            price_str = f"Rp {price:,}"
            
        price_info += f"💰 *Jual: {price_str}*"
        
    if data.get('rent_price'):
        r_price = data['rent_price']
        if r_price >= 1_000_000_000:
            r_price_str = f"Rp {r_price / 1_000_000_000:.1f} Miliar"
        elif r_price >= 1_000_000:
            r_price_str = f"Rp {r_price / 1_000_000:.0f} Juta"
        else:
            r_price_str = f"Rp {r_price:,}"
            
        if price_info: price_info += " | "
        price_info += f"🪙 *Sewa: {r_price_str}*"
        
    if data.get('negotiable'):
        price_info += " (Nego)"
        
    if price_info:
        parts.append(price_info)
    
    parts.append("") # Spacer
    
    # 4. Main Specs (Grid style)
    specs_list = []
    if data.get('land_area'): specs_list.append(f"📐 LT: {data['land_area']}m²")
    if data.get('building_area'): specs_list.append(f"🏗️ LB: {data['building_area']}m²")
    if data.get('bedrooms'): specs_list.append(f"🛏️ KT: {data['bedrooms']}")
    if data.get('bathrooms'): specs_list.append(f"🚿 KM: {data['bathrooms']}")
    if data.get('floors'): specs_list.append(f"🏢 Lantai: {data['floors']}")
    
    if specs_list:
        # Group into rows of 2-3
        parts.append(" | ".join(specs_list))
    
    # 5. Detailed Specs
    details = []
    if data.get('dimensions'): details.append(f"📏 Dimensi: {data['dimensions']}")
    if data.get('orientation'): details.append(f"🧭 Hadap: {data['orientation']}")
    if data.get('electricity'): details.append(f"⚡ Listrik: {data['electricity']} Watt")
    if data.get('water_type'): details.append(f"💧 Air: {data['water_type']}")
    if data.get('furnished'): details.append(f"🪑 Furnish: {data['furnished']}")
    if data.get('row_road'): details.append(f"🛣️ Jalan: {data['row_road']}")
    
    # Carport/Garage
    park = []
    if data.get('carports'): park.append(f"{data['carports']} Carport")
    if data.get('garages'): park.append(f"{data['garages']} Garasi")
    if park: details.append(f"🚗 {' + '.join(park)}")
    
    if details:
        parts.append("\n".join([f"• {d}" for d in details]))

    # 6. Legal & Facilities
    legal_parts = []
    if data.get('certificate_type'): legal_parts.append(data['certificate_type'])
    if data.get('imb'): legal_parts.append("IMB")
    if data.get('blueprint'): legal_parts.append("Blueprint")
    if data.get('kpr'): legal_parts.append("Bisa KPR")
    
    if legal_parts:
        parts.append(f"\n📜 *Legalitas:* {', '.join(legal_parts)}")
        
    if data.get('facilities'):
        facs = ', '.join(data['facilities'])
        parts.append(f"✨ *Fasilitas:* {facs}")
        
    # 7. Contact (if extracted)
    contact_parts = []
    if data.get('contact_name'): contact_parts.append(data['contact_name'])
    if data.get('contact_phone'): contact_parts.append(data['contact_phone'])
    
    if contact_parts:
        parts.append(f"\n📞 *Kontak:* {' - '.join(contact_parts)}")
    
    return "\n".join(parts)


def ask_gemini(question: str, context: str = "") -> str:
    """
    General purpose AI assistant for answering questions
    """
    try:
        prompt = f"{context}\n\nPertanyaan: {question}" if context else question
        response = client.models.generate_content(
            model='gemini-flash-latest',
            contents=prompt
        )
        return response.text
    except Exception as e:
        error_msg = str(e)
        if '429' in error_msg or 'RESOURCE_EXHAUSTED' in error_msg:
            return "Maaf, kuota AI sementara habis. Silakan coba lagi sebentar lagi atau hubungi admin."
        logger.error(f"Error asking Gemini: {e}")
        return "Maaf, saya mengalami kesulitan memproses pertanyaan Anda. Silakan coba lagi."
