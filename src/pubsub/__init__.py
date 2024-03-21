"""
This file registers the model with the Python SDK.
"""

from viam.resource.registry import Registry, ResourceCreatorRegistration

from pubsub_python import Pubsub
from .mqttGrpc import mqttGrpc

Registry.register_resource_creator(Pubsub.SUBTYPE, mqttGrpc.MODEL, ResourceCreatorRegistration(mqttGrpc.new))
