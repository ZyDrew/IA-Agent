import os
from dotenv import load_dotenv # type: ignore
from google import genai
from google.genai import types
import sys
from prompts import SYSTEM_PROMPT
from call_function import available_functions, call_function

def main():
    print("Hello from littleboy! Your dedicated AI Agent")

    #Mise en place des données nécessaires au fonctionnement de l'API
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    #Bool verbose int + verification que la ligne de commande contient bien un prompt
    verbose = "--verbose" in sys.argv
    if len(sys.argv) < 2:
        print("Error, no prompt detected as param for the script")
        sys.exit(1)
    else:
        prompt = sys.argv[1]

    #Creation de la liste des messages (la conversation avec l'agent IA)    
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    #Boucle complète pour créer une conversation avec l'agent
    for i in range(0, 20):

        try:
            #Appel au model IA pour générer une réponse sur base du prompt 
            #system_instruction permet de donner au système un prompt de base qui lui indique comment il peut travailler
            #tools est une liste de toutes les méthodes que l'agent peut utiliser - déclarer dans call_function.py
            res = client.models.generate_content(
                model="gemini-2.0-flash-001", 
                contents=messages, 
                config=types.GenerateContentConfig(tools=[available_functions], system_instruction=SYSTEM_PROMPT))
            
            if verbose:
                    print(f"User prompt: {prompt}")
                    print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}\nResponse tokens: {res.usage_metadata.candidates_token_count}")
            
            #Candidates contient le raisonnement du modèle , exemple : Model: "I want to call run_python_file..."
            if res.candidates:
                for candidate in res.candidates:
                    messages.append(candidate.content)

            #Si le résultat du prompt n'a nécéssité aucun appel à une fonction, on retourne la réponse finale du modèle
            if not res.function_calls:
                print(res.text)
                return
            
            """Si le résultat du prompt a effectué des appels à une ou plusieurs fonctions.
            Pour chaque fonction, on effectue son appel avec les paramètres -- function_call_part contient un name (le nom de la fct) et un args , chaque param de la fct
            Dans chaque fichier .py qui déclare la fonction, on a mis en place un schéma de déclaration qui définit ce qu'elle fait, et ses paramètres
            C'est l'agent qui fait la correspondance entre le prompt et les args par lui-même
            Ci-dessous, on vérifie que l'appel a bien retourné une réponse, puis on la retourne au User
            """
            call_function_res = []
            for function_call_part in res.function_calls:
                call_result = call_function(function_call_part, verbose)
                if call_result.parts and call_result.parts[0].function_response:
                    call_result_response = call_result.parts[0].function_response.response
                    if verbose:
                        print(f"-> {call_result_response}")
                    call_function_res.append(call_result.parts[0])
                else:
                    print("Error call_result empty")
                    sys.exit(1)
            
            if not call_function_res:
                raise Exception("no function responses generated, exiting.")
            
            messages.append(types.Content(role="user", parts=call_function_res))
        
        except Exception as e:
            print(f"Error in main loop : {e}")
        

if __name__ == "__main__":
    main()
