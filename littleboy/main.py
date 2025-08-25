import os
from dotenv import load_dotenv # type: ignore
from google import genai
from google.genai import types
import sys

def main():
    print("Hello from littleboy! Your dedicated AI Agent")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    verbose = "--verbose" in sys.argv
    if len(sys.argv) < 2:
        print("Error, no prompt detected as param for the script")
        sys.exit(1)
    else:
        prompt = sys.argv[1]
        
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    res = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)
    print(res.text)
    
    if verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}\nResponse tokens: {res.usage_metadata.candidates_token_count}")

    

if __name__ == "__main__":
    main()
