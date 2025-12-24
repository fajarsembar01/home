"""
Test Filter Feature - Simulate filter flow without Telegram
"""
import sys
from database import (
    init_db,
    get_or_create_user,
    create_property,
    get_unique_cities,
    get_unique_districts,
    get_properties_by_location
)

print("=" * 80)
print("TESTING FILTER FEATURE")
print("=" * 80)

# Initialize database
init_db()

# Create test user
print("\n1. Creating test user...")
user = get_or_create_user(
    telegram_id=999999,
    username="test_filter",
    first_name="Test",
    last_name="Filter"
)
print(f"✓ User created: ID={user.id}")

# Create some test properties
print("\n2. Creating test properties...")
test_properties = [
    {
        'property_type': 'rumah',
        'transaction_type': 'jual',
        'city': 'Jakarta',
        'district': 'Pondok Indah',
        'address': 'Jl. Metro Pondok Indah',
        'price': 5000000000,
        'land_area': 200,
        'building_area': 150,
        'bedrooms': 3,
        'bathrooms': 2
    },
    {
        'property_type': 'rumah',
        'transaction_type': 'sewa',
        'city': 'Jakarta',
        'district': 'Kebayoran Baru',
        'address': 'Jl. Radio Dalam',
        'price': 100000000,
        'land_area': 150,
        'building_area': 120,
        'bedrooms': 2,
        'bathrooms': 1
    },
    {
        'property_type': 'apartemen',
        'transaction_type': 'jual',
        'city': 'Tangerang',
        'district': 'BSD',
        'address': 'BSD City',
        'price': 800000000,
        'building_area': 50,
        'bedrooms': 2,
        'bathrooms': 1
    }
]

for idx, prop_data in enumerate(test_properties, 1):
    try:
        prop = create_property(user.id, prop_data)
        print(f"✓ Property {idx} created: {prop.property_type} in {prop.city}, {prop.district}")
    except Exception as e:
        print(f"✗ Error creating property {idx}: {e}")

# Test get_unique_cities
print("\n3. Testing get_unique_cities()...")
try:
    cities = get_unique_cities(user.id)
    print(f"✓ Found {len(cities)} unique cities: {cities}")
    if not cities:
        print("⚠ WARNING: No cities found!")
except Exception as e:
    print(f"✗ ERROR in get_unique_cities: {e}")
    import traceback
    traceback.print_exc()

# Test get_unique_districts
print("\n4. Testing get_unique_districts()...")
if cities:
    for city in cities:
        try:
            districts = get_unique_districts(user.id, city)
            print(f"✓ City '{city}' has {len(districts)} districts: {districts}")
        except Exception as e:
            print(f"✗ ERROR in get_unique_districts for {city}: {e}")
            import traceback
            traceback.print_exc()

# Test get_properties_by_location
print("\n5. Testing get_properties_by_location()...")
if cities:
    test_city = cities[0]
    try:
        result = get_properties_by_location(user.id, city=test_city, page=1, limit=5)
        print(f"✓ Filter by city '{test_city}':")
        print(f"  Total: {result['total_items']}, Pages: {result['total_pages']}")
        print(f"  Properties on page 1: {len(result['items'])}")
        
        for prop in result['items']:
            print(f"    - {prop.property_type} in {prop.district}")
    except Exception as e:
        print(f"✗ ERROR in get_properties_by_location: {e}")
        import traceback
        traceback.print_exc()

# Test with city + district
print("\n6. Testing filter with city + district...")
if cities:
    test_city = cities[0]
    try:
        districts = get_unique_districts(user.id, test_city)
        if districts:
            test_district = districts[0]
            result = get_properties_by_location(
                user.id, 
                city=test_city, 
                district=test_district, 
                page=1, 
                limit=5
            )
            print(f"✓ Filter by '{test_city}' + '{test_district}':")
            print(f"  Total: {result['total_items']}, Properties: {len(result['items'])}")
        else:
            print(f"  No districts in {test_city}")
    except Exception as e:
        print(f"✗ ERROR in city+district filter: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
