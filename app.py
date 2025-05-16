from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)  # <-- ESTA LÍNEA ES CLAVE

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

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres un asistente virtual de Nissan que atiende clientes por WhatsApp. "
                        "Tu tarea es responder preguntas sobre autos nuevos, seminuevos, enganches, buró de crédito, "
                        "planes como SICREA, precios, requisitos y tiempos de entrega. "
                        "Sé claro, profesional, empático y busca resolver sus dudas o invitarlos a agendar cita."
                    )
                },
                {"role": "user", "content": incoming_msg}
            ]
        )
        respuesta = completion.choices[0].message["content"].strip()
    except Exception as e:
        print("❌ Error al generar respuesta:", e)
        respuesta = "Lo siento, tuvimos un problema técnico al procesar tu mensaje. Intenta nuevamente más tarde."

    msg.body(respuesta)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)