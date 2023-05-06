import os
import openai
import requests
import json

# Recuperar la clave de la API de OpenAI desde localhost:9000
url = "http://localhost:9000/get_open_ai_key"
response = requests.get(url)
response_json = response.json()

if 'message' in response_json:
    api_key = response_json['message'].split(': ')[1]
    openai.api_key = api_key
else:
    print("Error: No se pudo obtener la clave de la API de OpenAI.")
    exit()

# Crear la carpeta Prompt si no existe
if not os.path.exists("Prompt"):
    os.makedirs("Prompt")

while True:
    # Paso 1
    prompt_a_procesar = input("Ingrese el texto a procesar o escriba 'exit()' para salir: ")

    if prompt_a_procesar.lower() == "exit()":
        break

    # Paso 2
    texto = f"""Dado este ejemplo dónde de esta función: 
    Generame 10 ideas combinando {{mundo 1}}  y  {{mundo 2}} .
    Generamos este contendio para archivo json: {{
        "Título": [
          "Ideas entre dos mundos"
        ],
        "Descripción": [
          "El objetivo de esta función es el de generar 10 ideas mezclando 2 mundos o cosas "
        ],
        "Inputs": [
          "mundo 1", "mundo 2"
        ],
        "Prompt": [
          "Generame 10 ideas combinando +input_1+  y  +input_2+ . "
        ],
        "Actúa como": [
          "Actúa como un recursos creativo."
        ]
    }} ----> Genera el contenido de json para esta función, teniendo en cuenta que los inputs en el prompt tienen este formato +input_1+, +input_2+, etc..: 
    {prompt_a_procesar}."""

    # Paso 3
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=texto,
        temperature=0.7,
        max_tokens=1557,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Paso 4
    respuesta = response.choices[0].text.strip()
    json_respuesta = json.loads(respuesta)

    # Paso 5
    nombre_archivo = json_respuesta['Título'][0] + '.json'
    with open(os.path.join("Prompt", nombre_archivo), 'w', encoding='utf-8') as outfile:
        json.dump(json_respuesta, outfile, ensure_ascii=False, indent=4)

    print(f"Archivo {nombre_archivo} creado.")