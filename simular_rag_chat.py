import openai
import os
from rag.buscador import recuperar_contexto

openai.api_key = os.getenv("OPENAI_API_KEY")

def simular_chat():
    while True:
        pregunta = input("\n🤖 Escribe una pregunta (o 'salir'): ")
        if pregunta.lower() in ["salir", "exit", "q"]:
            break

        contexto = recuperar_contexto(pregunta)
        messages = [
            {
                "role": "system",
                "content": (
                    "Eres un asesor experto de Nissan que ayuda a clientes interesados en comprar un auto con financiamiento. "
                    "Responde en un tono claro, amigable y profesional, usando la información proporcionada."
                )
            },
            {
                "role": "user",
                "content": f"Información útil:\n{contexto}\n\nPregunta:\n{pregunta}"
            }
        ]

        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )

        respuesta = response.choices[0].message.content.strip()
        print(f"\n💬 Respuesta del bot:\n{respuesta}")

if __name__ == "__main__":
    simular_chat()