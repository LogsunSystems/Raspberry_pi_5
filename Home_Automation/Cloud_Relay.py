import paho.mqtt.client as mqtt
import gpiod as GPIO
import json

THINGSBOARD_HOST = 'demo.thingsboard.io'
ACCESS_TOKEN = 'ahDTJJKgSCnsqPuUnelS'

Relay_1_Pin = 7
Relay_2_pin = 5

chip = GPIO.Chip('gpiochip4')

Relay1 = chip.get_line(Relay_1_Pin)
Relay2 = chip.get_line(Relay_2_pin)

Relay1.request(consumer = "Relay-1", type = GPIO.LINE_REQ_DIR_OUT)
Relay2.request(consumer = "Relay-2", type = GPIO.LINE_REQ_DIR_OUT)

# We assume that all GPIOs are LOW
gpio_state = {7: False, 11: False, 12: False, 13: False, 15: False, 16: False, 18: False, 22: False, 29: False,
              31: False, 32: False, 33: False, 35: False, 36: False, 37: False, 38: False, 40: False}


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc, *extra_params):
    print('Connected with result code ' + str(rc))
    # Subscribing to receive RPC requests
    client.subscribe('v1/devices/me/rpc/request/+')
    # Sending current GPIO status
    client.publish('v1/devices/me/attributes', get_gpio_status(), 1)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print ('Topic: ' + msg.topic + '\nMessage: ' + str(msg.payload))
    # Decode JSON request
    data = json.loads(msg.payload)
    # Check request method
    if data['method'] == 'getGpioStatus':
        # Reply with GPIO status
        client.publish(msg.topic.replace('request', 'response'), get_gpio_status(), 1)
    elif data['method'] == 'setGpioStatus':
        # Update GPIO status and reply
        set_gpio_status(data['params']['pin'], data['params']['enabled'])
        client.publish(msg.topic.replace('request', 'response'), get_gpio_status(), 1)
        client.publish('v1/devices/me/attributes', get_gpio_status(), 1)


def get_gpio_status():
    # Encode GPIOs state to json
    return json.dumps(gpio_state)


def set_gpio_status(pin, status):
    if (pin == 26):
        Relay1.set_value(status)
    
    if	(pin == 29):
        Relay2.set_value(status)
    
    # Update GPIOs state
    gpio_state[pin] = status



client = mqtt.Client()
# Register connect callback
client.on_connect = on_connect
# Registed publish message callback
client.on_message = on_message
# Set access token
client.username_pw_set(ACCESS_TOKEN)
# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)

try:
    client.loop_forever()
except KeyboardInterrupt:
    GPIO.cleanup()