from paho.mqtt.client import Client
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
        init_data = []

        init_data.append(self._init_object(device=device, related_object=battery))
        init_data.append(self._init_object(device=device, related_object=inverter))
        init_data.append(self._init_object(device=device, related_object=pv))
        init_data.append(self._init_object(device=device, related_object=ac))
        # push data
        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(init_data)

    def _init_object(self, device: Device, related_object: Battery|Inverter|PV|AC) -> list[tuple[str, dict]]:
        object_data = []
        # iterate by params of object to initialize topics
        for b_key in related_object.__dict__:
            match len(related_object.__dict__[b_key]):
                case 2:
                    _, icon = related_object.__dict__[b_key]
                    topic, message = self._generate_mode_publish(
                        device=device,
                        name=b_key,
                        icon=icon
                    )
                case 3:
                    _, unit_of_meas, icon = related_object.__dict__[b_key]
                    topic, message = self._generate_simple_publish(
                        device=device,
                        name=b_key, 
                        unit_of_measurement=unit_of_meas,
                        icon=icon)
                case 4:
                    _, unit_of_meas, icon, device_class = related_object.__dict__[b_key]
                    topic, message = self._generate_energy_publish(
                        device=device,
                        name=b_key,
                        unit_of_measurement=unit_of_meas,
                        icon=icon,
                        device_class=device_class)
                case _:
                    raise AttributeError
            object_data.append((topic, message))
        
        return object_data

    def push_mqtt_data(self, device: Device, topic: str, value: dict):
        pass

    def _generate_simple_publish(
            self, device: Device, name, unit_of_measurement, icon
            ):
        topic = f'{self.topic}/sensor/{device.name}_{device.sw}/{name}/config'
        message = {
                'name': f'{name}_{device.name}',
                'uniq_id': f'{device.sw}_{name}',
                'device': device.__dict__,
                'state_topic': f'{self.topic}/sensor/{device.name}_{device.sw}/{name}',
                'state_class': 'measurement',
                'unit_of_meas': unit_of_measurement,
                'icon': icon
                }

        return topic, message

    def _generate_energy_publish(
            self, device: Device, name, unit_of_measurement, icon, device_class 
            ):
        topic_lr = f'{self.topic}/sensor/{device.name}_{device.sw}/{name}/LastReset'
        message_lr = '1970-01-01T00:00:00+00:00'

        topic = f'{self.topic}/sensor/{device.name}_{device.sw}/{name}/config'
        message = {
                'name': f'{name}_{device.name}',
                'uniq_id': f'{device.sw}_{name}',
                'device': device.__dict__,
                'state_topic': f'{self.topic}/sensor/{device.name}_{device.sw}/{name}',
                'state_class': 'total_increasing',
                'device_class': device_class,
                'unit_of_meas': unit_of_measurement,
                'icon': icon
                }
        return (topic_lr, message_lr), (topic, message)

    def _generate_mode_publish(
            self, device: Device, name, icon):
        topic = f'{self.topic}/sensor/{device.name}_{device.sw}/{name}/config'
        message = {
                'name': f'{name}_{device.name}',
                'uniq_id': f'{device.sw}_{name}',
                'device': device.__dict__,
                'state_topic': f'{self.topic}/sensor/{device.name}_{device.sw}/{name}',
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

    def publish_battery(self, battery: Battery, device: Device, register=False):
        message_topic = f'{self.topic}/sensor/{device.name}_{device.sw}/'
        messages = []
        pass

    def publish_ac(self, ac: AC, register=False):
        pass

    def publish_pv(self, pv: PV, register=False):
        pass
    
    def publish_inverter(self, inverter: Inverter, register=False):
        pass
