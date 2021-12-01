from paho.mqtt.client import Client
from inverter.core import Battery, AC, PV, Inverter, Device 


class MqttClient(Client):
    def __init__(self, host: str, port: int, username: str,
            password: str, client_id: str, userdata:str, 
            topic: str, protocol=5, clean_session: bool=False):
        super().__init__()
        self.host = host
        self.port = port
        self.__auth = {'username': username, 'password': password}

        self.client_id = client_id
        self.clean_session = clean_session
        self.userdata = userdata
        self.topic = topic
        self.protocol = protocol
    
    def init_mqtt_topics(
            self,  
            device: Device,
            *components: Inverter|Battery|AC|PV):
        init_data = []

        for component in components:
            init_data += self._init_object(device, component)

        self.push_multiple_mqtt_data(msgs=init_data)

    def _init_object(self, device: Device, related_object: Battery|Inverter|PV|AC) -> list[tuple[str, dict]]:
        object_messages = []
        # iterate by params of object to get publish messages
        for b_key in related_object.__dict__:
            match len(related_object.__dict__[b_key]):
                case 2:
                    _, icon = related_object.__dict__[b_key]
                    object_msg = self._generate_mode_publish(
                        device=device,
                        name=b_key,
                        icon=icon
                    )
                case 3:
                    _, unit_of_meas, icon = related_object.__dict__[b_key]
                    object_msg = self._generate_simple_publish(
                        device=device,
                        name=b_key, 
                        unit_of_measurement=unit_of_meas,
                        icon=icon)
                case 4:
                    _, unit_of_meas, icon, device_class = related_object.__dict__[b_key]
                    object_msg_last_reset, object_msg = self._generate_energy_publish(
                        device=device,
                        name=b_key,
                        unit_of_measurement=unit_of_meas,
                        icon=icon,
                        device_class=device_class)
                    object_messages.append(object_msg_last_reset)
                case _:
                    raise AttributeError
            object_messages.append(object_msg)
        
        return object_messages

    def _generate_simple_publish(
            self, device: Device, name, unit_of_measurement, icon, qos=0, retain=False
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

        return {'topic': topic, 'message': str(message), 'qos': qos, 'retain':retain}

    def _generate_energy_publish(
            self, device: Device, name, unit_of_measurement, icon, device_class, qos=0, retain=False 
            ):
        topic_last_reset = f'{self.topic}/sensor/{device.name}_{device.sw}/{name}/LastReset'
        message_last_reset = '1970-01-01T00:00:00+00:00'

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
        return {'topic': topic_last_reset, 'message': message_last_reset, 'qos': qos, 'retain':retain}, \
               {'topic': topic, 'message': str(message), 'qos': qos, 'retain':retain}

    def _generate_mode_publish(
            self, device: Device, name, icon, qos=0, retain=False
            ):
        topic = f'{self.topic}/sensor/{device.name}_{device.sw}/{name}/config'
        message = {
                'name': f'{name}_{device.name}',
                'uniq_id': f'{device.sw}_{name}',
                'device': device.__dict__,
                'state_topic': f'{self.topic}/sensor/{device.name}_{device.sw}/{name}',
                'icon': icon
                }

        return {'topic': topic, 'message': str(message), 'qos': qos, 'retain':retain}

    def generate_message(self, device: Device, sensor_name, sensor_value, qos=0, retain=False):
        topic = f'{self.topic}/sensor/{device.name}_{device.sw}/{sensor_name}/'
        return {'topic': topic, 'payload': str(sensor_value), 'qos': qos, 'retain': retain}

    def push_multiple_mqtt_data(self, msgs):
        ''' msgs: [{"topic": "<topic>", "payload":"<payload>", "qos":"<qos>", "retain":"<retain>"}, ...] '''
        
        result = self.publish.multiple(
                msgs, 
                hostname=self.host,
                port=self.port,
                client_id=self.client_id,
                keepalive=30,
                protocol=self.protocol,
                auth=self.__auth) 

        if result != 0:
            raise Exception # TODO create new exception

        return result

    def push_single_mqtt_data(self, topic, payload, qos=0, retain=False):
        result = self.publish.single(
                topic,
                payload,
                qos=qos,
                retain=retain
                )
        return result

    def subscribe_to_homeassistant(self, device: Device):
    # Make QOS = 2. It allows us to deliver messages with guarantee.
    # By the way, QOS 2 is a very slow solution. It requires to publish 4
    # messages, but as a result we guarantee message delivery without 
    # duplicates
        topic = f'{self.topic}/sensor/{device.name}/'
        
        def on_message(client, userdata, message):
            print(message.topic, message.payload)
        
        def on_connect(client, userdata, flags, rc, properties=None):
            match rc:
                case 0:
                    print('Connection successfull!')
                    return client, userdata, flags, rc
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

        self.username_pw_set(**self.__auth)
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
