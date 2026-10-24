"""
This file registers the model with the Python SDK.
"""

from pubsub_python import Pubsub
from viam.resource.registry import Registry, ResourceCreatorRegistration

from .mqttGrpc import mqttGrpc

Registry.register_resource_creator(
    Pubsub.SUBTYPE, mqttGrpc.MODEL, ResourceCreatorRegistration(mqttGrpc.new)
)
