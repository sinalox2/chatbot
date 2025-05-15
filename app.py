from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    print("== Encabezados ==")
    print(request.headers)
    print("== Formulario ==")
    print(request.form)

    incoming_msg = request.values.get("Body", "").lower()
    print(f"Mensaje entrante: {incoming_msg}")

    resp = MessagingResponse()
    msg = resp.message()

    # Enviar mensaje a GPT-4o
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Eres un asesor virtual de Nissan que contesta dudas sobre autos nuevos, seminuevos y planes de financiamiento como SICREA. Sé claro, amable y directo."},
                {"role": "user", "content": incoming_msg}
            ]
        )
        respuesta = completion.choices[0].message["content"].strip()
        print("Respuesta de GPT:", respuesta)
    except Exception as e:
        print("❌ Error al llamar a OpenAI:", e)
        respuesta = "Lo siento, tuve un problema técnico al procesar tu mensaje. Intenta más tarde."

    msg.body(respuesta)

    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)