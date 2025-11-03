import paho.mqtt.client as mqtt
import time

#configurações do broker
broker = "a3e9fa62e93546109153117bf581ba7b.s1.eu.hivemq.cloud"
port = 8883
topic = "teste/mqtt"

#função para quando o cliente receber msg do broker 
def on_message(client, userdata, message):
    print(f"Mensagem recebida no tópico {message.topic}: {str(message.payload.decode('utf-8'))}")

#Criar cliente MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id="ClientePython")

#configurar callback
client.connect(broker, port)

#Assinatura de tópico
client.subscribe(topic)

#Publicar mensagens a cada 5 segundos
try:
    while True:
        msg = "Olá MQTT com Python"
        client.publish(topic, msg)
        print(f"Mensagem publicada: {msg}")
        time.sleep(5)
except KeyboardInterrupt:
    print("Saindo...")
finally:
    client.loop_stop()
    client.disconnect()


