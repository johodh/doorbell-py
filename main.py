import paho.mqtt.client as mqtt
import time
import logging
import doorbell
import ts
from datetime import datetime

# Set ip address of MQTT broker
mqtt_ip=""
mqtt_user=""
mqtt_password=""

logname="/home/pi/debug.log"
chime=doorbell.Chime()
chime.set(True)
justrang=False 
tcount=0

logging.basicConfig(filename=logname,
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            level=logging.DEBUG)

logging.info("STARTUP")

# Topics
connected_topic="/$CONNECTED/doorbell"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    logging.debug("Connected flags"+str(flags)+"result code "+str(rc)+"client1_id")
    client.subscribe("/doorbell/chime")
    client.subscribe("/doorbell/testchime")

    if rc==0:
        client.connected_flag=True
        print('onconnect clientconnectedflag: ' + str(client.connected_flag))
        client.publish(connected_topic,1,retain=True)
    else:
        client.bad_connection_flag=True

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    payload=str(msg.payload.decode())
    print(msg.topic + " " + payload)

    # Chime control
    if msg.topic == "/doorbell/chime": 
        if payload == "off":
            logging.info("Chime turned off")
            chime.set(False)
            logging.info('chime: ' + str(chime.get()))
        elif payload == "on":
            logging.info ("Chime turned on")
            chime.set(True)
            logging.info('chime: ' + str(chime.get()))
        elif payload == "status":
            logging.info ("Chime status called")
            client.publish("/doorbell/chime", chime.get(), 1)
            logging.info('chime: ' + str(chime.get()))

    elif msg.topic == "/doorbell/testchime":
            doorbell.test()
            logging.info ("Chime was tested")

# Client setup
client = mqtt.Client()
client.connected_flag=False
client.username_pw_set(mqtt_user,mqtt_password)
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = print("signal published.. \n")
client.will_set(connected_topic,0, qos=0, retain=True)

try: 
    client.connect(mqtt_ip, 1883, 60)
    print('clientconnectedflag: ' +str(client.connected_flag))
    logging.info('Trying to connect')
    time.sleep(20)
    client.publish("/doorbell/signal", "waiting", 1)
    client.publish("/doorell/chime", "off", 1)

except ConnectionRefusedError:
    print('clientconnectedflag: ' +str(client.connected_flag))
    logging.info('Connection refused')
    time.sleep(20)

client.loop_start()

while True:
    if doorbell.sensor(chime.get()):
        if justrang == False:
            ts.toTelegram()
            tcount=50
        timestamp=datetime.now().strftime('%Y-%m-%d, %H:%M')
        client.publish("/doorbell/sensor", timestamp, 1)
        logging.info("Doorbell button pushed")
        logging.info('chime: ' + str(chime))
        justrang=True
 
    if justrang:
        tcount-=1

    if tcount == 0:
        justrang=False
        tcount=50

    time.sleep(0.1)

client.loop_stop()
