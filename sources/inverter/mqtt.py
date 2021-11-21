from paho.mqtt.client import Client
# from paho.mqtt import publish, subscribe, MQTTv5 
from inverter.core import Battery, AC, PV, Inverter, Device 


class MqttClient(Client):
    def __init__(self, host: str, port: int, username: str,
            password: str, client_id: str, userdata:str, 
            topic: str, protocol=5, clean_session: bool=False):
        super().__init__()
        self.host = host
        self.port = port
        self.auth = {'username': username, 'password': password}

        self.client_id = client_id
        self.clean_session = clean_session
        self.userdata = userdata
        self.topic = topic
        self.protocol = protocol
    
    def init_mqtt_topics(
            self, battery: Battery, 
            ac: AC, pv: PV, inverter: Inverter, 
            device: Device):
        topics = []

    
    def _generate_simple_publish(
            self, name, unit_of_measurement, icon, device: Device 
            ):
        topic = f'{self.topic}/sensor/{device.name}_{device.serial_number}/{name}/config'
        message = {
                'name': f'{name}_{device.name}',
                'uniq_id': f'{device.serial_number}_{name}',
                'device': {
                    'ids': device.serial_number,
                    'mf': device.manufacturer,
                    'mdl': device.model,
                    'name': device.name,
                    'sw': device.firmware_version
                    },
                'state_topic': f'{self.topic}/sensor/{device.name}_{device.serial_number}/{name}',
                'state_class': 'measurement',
                'unit_of_meas': unit_of_measurement,
                'icon': icon
                }

        return topic, message

    def _generate_energy_publish(
            self, name, unit_of_measurement, icon, device: Device, device_class
            ):
        topic_lr = f'{self.topic}/sensor/{device.name}_{device.serial_number}/{name}/LastReset'
        message_lr = '1970-01-01T00:00:00+00:00'

        topic = f'{self.topic}/sensor/{device.name}_{device.serial_number}/{name}/config'
        message = {
                'name': f'{name}_{device.name}',
                'uniq_id': f'{device.serial_number}_{name}',
                'device': {
                    'ids': device.serial_number,
                    'mf': device.manufacturer,
                    'mdl': device.model,
                    'name': device.name,
                    'sw': device.firmware_version
                    },
                'state_topic': f'{self.topic}/sensor/{device.name}_{device.serial_number}/{name}',
                'state_class': 'total_increasing',
                'device_class': device_class,
                'unit_of_meas': unit_of_measurement,
                'icon': icon
                }
        return (topic_lr, message_lr), (topic, message)

    def _generate_mode_publish(
            self, name, icon, device: Device
            ):
        topic = f'{self.topic}/sensor/{device.name}_{device.serial_number}/{name}/config'
        message = {
                'name': f'{name}_{device.name}',
                'uniq_id': f'{device.serial_number}_{name}',
                'device': {
                    'ids': device.serial_number,
                    'mf': device.manufacturer,
                    'mdl': device.model,
                    'name': device.name,
                    'sw': device.firmware_version
                    },
                'state_topic': f'{self.topic}/sensor/{device.name}_{device.serial_number}/{name}',
                'icon': icon
                }

        return topic, message

    def subscribe_to_homeassistant(self, device: Device):
    # Make QOS = 2. It allows us to deliver messages with guarantee.
    # By the way, QOS 2 is a very slow solution. It requires to publish 4
    # messages, but as a result we guarantee message delivery without 
    # duplicates
        topic = f'{self.topic}/sensors/{device.name}/'
        
        def on_message(client, userdata, message):
            print(message.topic, message.payload)
        
        def on_connect(client, userdata, flags, rc, properties=None):
            match rc:
                case 0:
                    print('Connection successfull!')
                case 1:
                    print('Wrong protocol...')
                    raise TypeError
                case 2:
                    print('Invalid client id')
                    raise AttributeError
                case 3:
                    print('Server is unreachable...')
                    # Reconnect function
                    raise ConnectionError
                case 4:
                    print('Invalid credentials')
                    raise AttributeError
                case 5:
                    print('Not authorised')
                    raise PermissionError

        def on_subscribe(client, userdata, flags, qos, properies=None):
            print(f'{client.client_id} subscribed. QoS: {qos}')

        self.on_connect = on_connect
        self.on_subscribe = on_subscribe
        self.on_message = on_message

        self.username_pw_set(**self.auth)
        self.connect(
                host=self.host,
                port=self.port,
                keepalive=30,
                bind_address=''
                )
        
        self.subscribe(
                topic=topic, 
                qos=2,
                options=None,
                properties=None)

        self.loop_forever()

    def publish_battery(self, battery: Battery, device: Device):
        message_topic = f'{self.topic}/sensor/{device.name}_{device.serial_number}/'
        messages = []
        
        for battery_attr

        pass

    def publish_ac(self, ac: AC):
        pass

    def publish_pv(self, pv: PV):
        pass
    
    def publish_inverter(self, inverter: Inverter):
        pass
