import base64
import json
import requests
import os

API_KEY = os.getenv("OPENROUTER_API_KEY")
# Updated to use a working OpenRouter model for vision tasks
MODEL_ID = "openai/gpt-4o-mini"

def analyze_rooftop(image_bytes):
    if not API_KEY:
        return {
            "error": "OPENROUTER_API_KEY environment variable not set",
            "details": "Please set your OpenRouter API key in the environment variables"
        }
    
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://huggingface.co/spaces",  # Required for some OpenRouter models
        "X-Title": "Solar AI Assistant"  # Optional but recommended
    }

    data = {
        "model": MODEL_ID,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
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
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300,
        "temperature": 0.1
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )

        if response.status_code != 200:
            return {
                "error": f"API returned status code {response.status_code}",
                "raw_response": response.text,
                "details": f"Check your API key and model availability"
            }

        result = response.json()
        
        if 'error' in result:
            return {
                "error": "API Error",
                "details": result['error'].get('message', 'Unknown API error'),
                "raw_response": response.text
            }
        
        content = result['choices'][0]['message']['content'].strip()

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