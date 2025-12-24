"""
Test script to verify database connection and basic functionality
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment():
    """Test if all required environment variables are set"""
    print("🔍 Testing Environment Variables...")
    
    required_vars = ['TELEGRAM_BOT_TOKEN', 'GEMINI_API_KEY', 'DATABASE_URL']
    missing = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value or 'your_' in value or '_here' in value:
            missing.append(var)
            print(f"   ❌ {var}: Not set or using default value")
        else:
            masked_value = value[:10] + '...' if len(value) > 10 else '***'
            print(f"   ✅ {var}: {masked_value}")
    
    if missing:
        print(f"\n⚠️  Missing or invalid variables: {', '.join(missing)}")
        print("   Please edit .env file with your actual credentials")
        return False
    
    print("✅ All environment variables are set!\n")
    return True


def test_database():
    """Test database connection"""
    print("🗄️  Testing Database Connection...")
    
    try:
        from database import init_db, get_db
        
        # Initialize database
        init_db()
        print("   ✅ Database tables created/verified")
        
        # Test connection
        db = get_db()
        db.close()
        print("   ✅ Database connection successful")
        
        return True
    except Exception as e:
        print(f"   ❌ Database error: {e}")
        return False


def test_gemini():
    """Test Gemini AI connection"""
    print("\n🤖 Testing Gemini AI Connection...")
    
    try:
        from ai_processor import extract_property_info
        
        # Test with simple input
        test_input = "Rumah 2 kamar tidur di Jakarta, harga 1 miliar"
        result = extract_property_info(test_input)
        
        if result:
            print(f"   ✅ Gemini AI responding")
            print(f"   📊 Extracted: {result}")
            return True
        else:
            print("   ⚠️  Gemini returned empty result")
            return False
            
    except Exception as e:
        print(f"   ❌ Gemini error: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 50)
    print("🏠 Property Collection Bot - System Test")
    print("=" * 50)
    print()
    
    tests = [
        ("Environment", test_environment),
        ("Database", test_database),
        ("Gemini AI", test_gemini),
    ]
    
    results = {}
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"❌ {name} test failed: {e}")
            results[name] = False
        print()
    
    # Summary
    print("=" * 50)
    print("📊 Test Summary")
    print("=" * 50)
    
    all_passed = True
    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 All tests passed! You're ready to run the bot.")
        print("   Run: python3 bot.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        print("   Check README.md for troubleshooting guide.")
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
