from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client with the API key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def translate_text(text, languages):
    """
    Translate text into multiple languages using OpenAI
    """
    # Construct the prompt
    prompt = f"phrase: {text}\nlanguages: {', '.join(languages)}"
    
    try:
        # Get completion from OpenAI
        response = client.chat.completions.create(
            model="gpt-4",  # or "gpt-3.5-turbo" for a faster, cheaper option
            messages=[
                {
                    "role": "system",
                    "content": open("system_prompts/translate.txt", "r").read()
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        # Return the translation response
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error during translation: {e}")
        return f"Translation error: {str(e)}" 