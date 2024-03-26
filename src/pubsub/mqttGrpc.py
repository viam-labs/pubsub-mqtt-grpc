from typing import ClassVar, Mapping, Sequence, Any, Dict, Optional, Tuple, Final, List, cast
from typing_extensions import Self

from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName, Vector3
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily

from pubsub_python import Pubsub
from viam.logging import getLogger

from paho.mqtt import client as mqtt_client

import os
import asyncio
import subprocess
import psutil
from sys import platform

LOGGER = getLogger(__name__)

class mqttGrpc(Pubsub, Reconfigurable):
    
    MODEL: ClassVar[Model] = Model(ModelFamily("viam-labs", "service"), "mqtt-grpc")
    client= None
    client_id: str

    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        my_class = cls(config.name)
        my_class.reconfigure(config, dependencies)
        return my_class

    @classmethod
    def validate(cls, config: ComponentConfig):
        broker = config.attributes.fields["broker"].string_value
        local_mosquitto = config.attributes.fields["local_mosquitto"].bool_value
        if broker == "" and local_mosquitto == False:
            raise Exception("Either broker must be defined or local_mosquitto set to true")
        return

    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        broker = config.attributes.fields["broker"].string_value
        port = int(config.attributes.fields["port"].number_value) or 1883
        mqtt_version = int(config.attributes.fields["mqtt_version"].number_value) or 3
        mqtt_transport = config.attributes.fields["mqtt_transport"].string_value or 'tcp'
        username = config.attributes.fields["username"].string_value
        password = config.attributes.fields["password"].string_value
        local_mosquitto = config.attributes.fields["local_mosquitto"].bool_value

        if local_mosquitto == True:
            broker = 'localhost'
            mosquitto_running = False
            for process in psutil.process_iter(['name']):
                if process.info['name'] == 'mosquitto':
                    mosquitto_running = True

            if not mosquitto_running:
                if platform == "linux" or platform == "linux2":
                    LOGGER.info("Will attempt to install mosquitto with apt")
                    result = subprocess.run(["apt", "install", "mosquitto"], capture_output=True, text=True)
                    LOGGER.info(result.stdout)
                elif platform == "darwin":
                    LOGGER.info("Will attempt to install mosquitto with brew")
                    result = subprocess.run(["brew", "install", "mosquitto"], capture_output=True, text=True)
                    LOGGER.info(result)
                    result = subprocess.run(["brew", "services", "start", "mosquitto"], capture_output=True, text=True)
                    LOGGER.info(result.stdout)
        
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                LOGGER.info("Connected to MQTT Broker!")
            else:
                LOGGER.error("Failed to connect, return code %d\n", rc)

        if self.client is not None and self.client.is_connected() == True:
            self.client.loop_stop()
            self.client.disconnect()

        self.client_id = f'viam{os.getpid()}'
        self.client = mqtt_client.Client(client_id=self.client_id, protocol=mqtt_version, transport=mqtt_transport)
        LOGGER.info("mqtt client instantiated, will connect to mqtt broker " + broker)
        if username != "":
            self.client.username_pw_set(username, password)
        self.client.on_connect = on_connect
        self.client.connect(broker, port)
        LOGGER.info("mqtt connect complete")
        self.client.loop_start()
        return

    async def publish(self, topic: str, message: str, qos: int=0) -> str:
        LOGGER.info("will publish to topic " + topic)
        self.client.publish(topic, payload=message, qos=qos)
        return "OK"

    async def unsubscribe(self, topic: str) -> str:
        LOGGER.info("will unsubscribe from topic " + topic)
        self.client.unsubscribe(topic)
        return "OK"
    
    async def subscribe(self, topic: str) -> str:
        LOGGER.info("will subscribe to topic " + topic)
        def on_message(client, userdata, msg):
            yield msg

        self.client.subscribe(topic)
        self.client.message_callback_add(topic, on_message)
        return "OK"