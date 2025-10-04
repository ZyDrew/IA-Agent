import os
from dotenv import load_dotenv # type: ignore
from google import genai
from google.genai import types
import sys
from prompts import SYSTEM_PROMPT
from call_function import available_functions, call_function

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

    res = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages, 
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=SYSTEM_PROMPT))
    
    if verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}\nResponse tokens: {res.usage_metadata.candidates_token_count}")

    if not res.function_calls:
        print(res.text)
        return
    
    for function_call_part in res.function_calls:
        call_result = call_function(function_call_part, verbose)
        if call_result.parts and call_result.parts[0].function_response:
            if verbose:
                print(f"-> {call_result.parts[0].function_response.response}")
        else:
            print("Error call_result empty")
            sys.exit(1)

if __name__ == "__main__":
    main()
