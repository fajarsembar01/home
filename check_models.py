from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

print("Listing available Gemini models:")
print("=" * 80)

try:
    models_response = client.models.list()
    count = 0
    for model in models_response:
        print(f"✓ {model.name}")
        count += 1
        if count > 20:  # Limit output
            print("... (showing first 20)")
            break
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
