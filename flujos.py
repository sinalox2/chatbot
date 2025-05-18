


def detectar_intencion(mensaje: str) -> str:
    mensaje = mensaje.lower()
    if any(p in mensaje for p in ["requisito", "documento", "necesito", "necesita"]):
        return "requisitos"
    elif any(p in mensaje for p in ["cotizar", "precio", "cuánto cuesta", "cuanto cuesta"]):
        return "cotizacion"
    elif any(p in mensaje for p in ["promoción", "promo", "descuento", "oferta"]):
        return "promocion"
    elif any(p in mensaje for p in ["buró", "buro", "mal historial"]):
        return "buro"
    elif any(p in mensaje for p in ["cita", "llamada", "quiero hablar", "contacto"]):
        return "agendar"
    return None

def respuesta_por_intencion(intencion: str) -> str:
    respuestas = {
        "requisitos": (
            "📑 Para solicitar un crédito SICREA necesitas:\n"
            "- INE vigente\n"
            "- Comprobante de domicilio\n"
            "- Comprobante de ingresos\n"
            "- RFC y CURP\n"
            "¿Te gustaría que te ayude a iniciar tu trámite? 😊"
        ),
        "cotizacion": (
            "💰 ¡Con gusto te ayudo a cotizar! Por favor dime:\n"
            "- ¿Qué modelo te interesa?\n"
            "- ¿Nuevo o seminuevo?\n"
            "- ¿Vas a dar enganche o buscas sin enganche?"
        ),
        "promocion": (
            "🎉 Este mes tenemos promociones especiales en Nissan con planes SICREA:\n"
            "- Enganche desde $5,000\n"
            "- Tasa fija\n"
            "- Plazos flexibles\n"
            "¿Te interesa algún modelo en especial?"
        ),
        "buro": (
            "🧾 ¡No te preocupes! Con SICREA podemos apoyarte incluso si estás en buró.\n"
            "Solo necesitamos comprobar ingresos y un buen comportamiento actual.\n"
            "¿Te gustaría saber qué modelos aplican?"
        ),
        "agendar": (
            "📅 Con gusto te agendo una cita con un asesor Nissan.\n"
            "¿Qué día y hora te acomoda?\n"
            "Estamos disponibles de lunes a viernes, 9am a 6pm."
        )
    }
    return respuestas.get(intencion, None)