import base64
import json
import requests
import os

API_KEY = os.getenv("GOOGLE_API_KEY")
# Updated Google Gemini model (replaces deprecated gemini-pro-vision)
MODEL_ID = "gemini-1.5-flash"

def analyze_rooftop(image_bytes):
    if not API_KEY:
        return {
            "error": "GOOGLE_API_KEY environment variable not set",
            "details": "Please set your Google API key in the environment variables"
        }
    
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    headers = {
        "Content-Type": "application/json"
    }

    # Google Gemini API request format
    data = {
        "contents": [{
            "parts": [
                {
                    "text": """Analyze this rooftop image and estimate:
1. Usable rooftop area in square meters (excluding chimneys, vents, shadows)
2. Number of 350W solar panels that can be installed (each panel is ~2m²)

Respond ONLY with valid JSON in this exact format:
{
  "usable_area_m2": <number>,
  "recommended_panels": <number>
}"""
                },
                {
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": base64_image
                    }
                }
            ]
        }],
        "generationConfig": {
            "temperature": 0.1,
            "topK": 32,
            "topP": 1,
            "maxOutputTokens": 300,
            "stopSequences": []
        }
    }

    try:
        # Updated Google Gemini API endpoint for v1beta models
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_ID}:generateContent?key={API_KEY}"
        
        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=30
        )

        if response.status_code != 200:
            return {
                "error": f"API returned status code {response.status_code}",
                "raw_response": response.text,
                "details": f"Check your API key and quota limits"
            }

        result = response.json()
        
        # Check for API errors
        if 'error' in result:
            return {
                "error": "Google API Error",
                "details": result['error'].get('message', 'Unknown API error'),
                "raw_response": response.text
            }
        
        # Extract content from Google's response format
        if 'candidates' not in result or not result['candidates']:
            return {
                "error": "No response candidates from API",
                "raw_response": response.text
            }
        
        candidate = result['candidates'][0]
        if 'content' not in candidate or 'parts' not in candidate['content']:
            return {
                "error": "Invalid response structure from API",
                "raw_response": response.text
            }
        
        content = candidate['content']['parts'][0]['text'].strip()

        try:
            # Try to extract JSON from response (in case there's extra text)
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_content = content[json_start:json_end]
                parsed = json.loads(json_content)
                
                # Validate required keys
                if "usable_area_m2" in parsed and "recommended_panels" in parsed:
                    return parsed
                else:
                    return {
                        "error": "Missing required keys in response",
                        "raw_content": content
                    }
            else:
                return {
                    "error": "No JSON found in response",
                    "raw_content": content
                }
                
        except json.JSONDecodeError as e:
            return {
                "error": "Response content is not valid JSON",
                "details": str(e),
                "raw_content": content
            }

    except requests.exceptions.Timeout:
        return {
            "error": "Request timed out",
            "details": "The API request took too long to respond"
        }
    except requests.exceptions.RequestException as e:
        return {
            "error": "Network request failed",
            "details": str(e)
        }
    except Exception as e:
        return {
            "error": "Unexpected error occurred",
            "details": str(e)
        }