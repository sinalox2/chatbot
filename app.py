import sys
import json
sys.path.append(".")
from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import openai
from rag.buscador import recuperar_contexto
import csv
from datetime import datetime

load_dotenv()
client_mongo = MongoClient(os.getenv("MONGODB_URI"))
db = client_mongo["chatbot_nissan"]
coleccion_leads = db["leads"]
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai

app = Flask(__name__)  # <-- ESTA LÍNEA ES CLAVE

conversaciones = {}

with open("prompt_sistema_nissan.txt", "r", encoding="utf-8") as f:
    prompt_sistema = f.read()

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    print("== Encabezados ==")
    print(request.headers)
    print("== Formulario ==")
    print(request.form)

    incoming_msg = request.values.get("Body", "").lower()
    wa_id = request.values.get("WaId", "")
    if wa_id not in conversaciones:
        conversaciones[wa_id] = []

    conversaciones[wa_id].append({"role": "user", "content": incoming_msg})

    print(f"Mensaje entrante: {incoming_msg}")

    # Flujo directo sin intenciones

    resp = MessagingResponse()

    try:
        mensajes = [
            {
                "role": "system",
                "content": prompt_sistema
            },
            {
                "role": "user",
                "content": f"Información útil:\n{recuperar_contexto(incoming_msg)}"
            }
        ] + conversaciones[wa_id][-6:]  # últimos turnos

        completion = client.ChatCompletion.create(
            model="gpt-4o",
            messages=mensajes
        )
        respuesta = completion.choices[0].message.content.strip()
        conversaciones[wa_id].append({"role": "assistant", "content": respuesta})
        print(f"Respuesta generada por GPT: {respuesta}")
    except Exception as e:
        print("❌ Error al generar respuesta:", e)
        respuesta = "Lo siento, tuvimos un problema técnico al procesar tu mensaje. Intenta nuevamente más tarde."
    # Extraer datos del mensaje usando GPT
    try:
        extraccion = client.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Extrae del siguiente mensaje los siguientes datos si están presentes: modelo, enganche, buro y ingresos. Devuelve un JSON con las claves: modelo, enganche, buro, ingresos. Si no hay datos, usa null."},
                {"role": "user", "content": incoming_msg}
            ]
        )
        datos_extraidos = json.loads(extraccion.choices[0].message.content.strip())
    except Exception as e:
        print("⚠️ No se pudieron extraer datos del lead:", e)
        datos_extraidos = {"modelo": None, "enganche": None, "buro": None, "ingresos": None}

    lead = {
        "fecha": datetime.now().isoformat(),
        "wa_id": wa_id,
        "nombre": request.values.get("ProfileName", ""),
        "mensaje": incoming_msg,
        "respuesta": respuesta,
        "modelo": datos_extraidos.get("modelo"),
        "enganche": datos_extraidos.get("enganche"),
        "buro": datos_extraidos.get("buro"),
        "ingresos": datos_extraidos.get("ingresos")
    }
    guardar_lead_en_csv(lead)
    try:
        coleccion_leads.insert_one(lead)
        print("✅ Lead guardado en MongoDB Atlas.")
    except Exception as err:
        print("❌ Error al guardar en MongoDB:", err)

    respuesta = respuesta.strip() if respuesta else "Disculpa, hubo un error al generar respuesta."
    resp.message(respuesta)
    print("🧾 XML a enviar:", str(resp))
    return Response(str(resp), mimetype="application/xml")

def guardar_lead_en_csv(lead_data):
    archivo = "leads.csv"
    campos = ["fecha", "wa_id", "nombre", "mensaje", "respuesta", "modelo", "enganche", "buro", "ingresos"]
    existe = os.path.isfile(archivo)

    with open(archivo, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        if not existe:
            writer.writeheader()
        writer.writerow(lead_data)


# Endpoint de prueba para respuesta XML
@app.route("/test", methods=["POST"])
def test():
    resp = MessagingResponse()
    resp.message("Prueba exitosa de respuesta XML 🚀")
    print("🧾 XML de prueba:", str(resp))
    return Response(str(resp), mimetype="application/xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)