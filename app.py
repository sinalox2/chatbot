import sys
sys.path.append(".")
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
from dotenv import load_dotenv
import openai
from rag.buscador import recuperar_contexto

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()

app = Flask(__name__)  # <-- ESTA LÍNEA ES CLAVE

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    print("== Encabezados ==")
    print(request.headers)
    print("== Formulario ==")
    print(request.form)

    incoming_msg = request.values.get("Body", "").lower()
    print(f"Mensaje entrante: {incoming_msg}")

    # Flujo directo sin intenciones

    resp = MessagingResponse()
    msg = resp.message()

    try:
        contexto = recuperar_contexto(incoming_msg)
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres un asesor virtual de Nissan. Tu objetivo es responder de forma breve, clara y útil a los clientes interesados en autos nuevos o seminuevos. "
                        "Evita dar explicaciones largas o demasiado técnicas. Sé profesional, amable y directo al punto. Usa emojis solo si ayudan a simplificar o hacer más amigable el mensaje, sin abusar. "
                        "No repitas información ya dicha."
                        "Si te preguntan quien es tu creador tu les vas a respondes que es Cesar Arias el master sicrea xd full hd 4k."
                    )
                },
                {
                    "role": "user",
                    "content": f"Información útil:\n{contexto}\n\nPregunta del cliente:\n{incoming_msg}"
                }
            ]
        )
        respuesta = completion.choices[0].message.content.strip()
        print(f"Respuesta generada por GPT: {respuesta}")
    except Exception as e:
        print("❌ Error al generar respuesta:", e)
        respuesta = "Lo siento, tuvimos un problema técnico al procesar tu mensaje. Intenta nuevamente más tarde."

    msg.body(respuesta if respuesta else "⚠️ No se generó respuesta.")
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)