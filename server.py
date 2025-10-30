from flask import Flask, request, jsonify, render_template
import paho.mqtt.client as mqtt
from threading import Lock
from paho.mqtt.client import Client, CallbackAPIVersion

app = Flask(__name__)

broker = "broker.hivemq.com" 
#broker: servidor que atua como intermediário
topico = "simulador/mqtt/mensagens" 
#tópico:Categoria para troca de mensagens
mensagens = []
lock = Lock() #objeto de sincronização


#configurar o cliente MQTT
cliente =  Client(client_id="", protocol=mqtt.MQTTv311, callback_api_version=CallbackAPIVersion.VERSION2)

def on_connect(cliente, userdata, flags, rc, properties=None):
    print(f"Conectado ao broker MQTT com código {rc}")
    cliente.subscribe(topico) #subscribe: assinatura

def on_message(client, userdata, msg):
    msg_text = msg.payload.decode()
    with lock:
        mensagens.append(msg_text)
        if len(mensagens) > 50: #limita o tamanho da lista para 50 msgs
            mensagens.pop(0)

cliente.on_connect = on_connect
cliente.on_message = on_message
cliente.connect(broker) #conecta ao broker MQTT
cliente.loop_start()

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/enviar',methods=['POST'])
def enviar():
    data = request.json
    msg = data.get('mensagem')
    if not msg:
        return "Mensagem vazia", 400
    cliente.publish(topico, msg)
    return '', 200

@app.route('/mensagens')
def get_mensagens():
    with lock:
        return jsonify(mensagens)
if __name__ == '__main__':
    app.run(debug=True)

    


