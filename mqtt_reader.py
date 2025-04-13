import paho.mqtt.client as mqtt
import pandas as pd
import json

# Lista donde guardaremos los resultados
resultados = []

def on_message(client, userdata, msg):
    try:
        # Convertir el mensaje a JSON
        payload = json.loads(msg.payload.decode())

        # Extraer el campo 'time' dentro de 'MODEM'
        time_value = payload["MODEM"]["time"]

        # Extraer el IMEI desde el tópico
        imei = msg.topic.split("/")[1]

        print(f"📡 IMEI: {imei} → Time: {time_value}")  # Verificar datos en consola
        
        # Guardar en la lista
        resultados.append({"IMEI": imei, "Time": time_value})

    except Exception as e:
        print(f"⚠️ Error procesando mensaje: {e}")

# Configuración del cliente MQTT
broker = "3.129.163.139"  # Dirección del broker
port = 1883  # Puerto MQTT

client = mqtt.Client()
client.on_message = on_message
client.connect(broker, port, 60)

# Suscribirnos a TODOS los IMEIs en NEVERAS/{IMEI}/DATA
topic_base = "NEVERAS/+"
client.subscribe(f"{topic_base}/DATA")

print(f"✅ Suscrito a: {topic_base}/DATA")
client.loop_start()

# Esperar 30 segundos para recibir mensajes
import time
time.sleep(30)

# Detener el loop y cerrar la conexión
client.loop_stop()
client.disconnect()

# Guardar los resultados en un archivo Excel
if resultados:
    df_resultados = pd.DataFrame(resultados)
    df_resultados.to_excel("imeis_con_time.xlsx", index=False)
    print("✅ Archivo 'imeis_con_time.xlsx' generado con éxito.")
else:
    print("⚠️ No se recibieron datos.")
