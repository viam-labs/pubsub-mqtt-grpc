# mqtt-grpc modular service

This module implements the [viam-labs pubsub API](https://github.com/viam-labs/pubsub-api) in a viam-labs:service:mqtt-grpc model.
With this service, you can interact with [MQTT](https://mqtt.org/) brokers to publish and subscribe to topics in your Viam projects.

## Requirements

Typically, you would need to have an MQTT broker like [Mosquitto](https://www.mosquitto.org/) or [EMQ X](https://www.emqx.io/) running somewhere that is reachable by this module over the network.

In some use-cases, you might use this module for inter-process communication locally.
In those scenarios, you can set the [local_mosquitto](#attributes) attribute to true and the module will attempt to install mosquitto locally and interface with it.

## Build and Run

To use this module, follow these instructions to [add a module from the Viam Registry](https://docs.viam.com/registry/configure/#add-a-modular-resource-from-the-viam-registry) and select the `viam-labs:pubsub:viam-labs:service:mqtt-grpc` model from the [`viam-labs:service:mqtt-grpc` module](https://app.viam.com/module/viam-labs/viam-labs:service:mqtt-grpc).

## Configure

> [!NOTE]  
> Before configuring your mqtt-grpc service, you must [create a machine](https://docs.viam.com/manage/fleet/machines/#add-a-new-machine).

Navigate to the **Config** tab of your robot’s page in [the Viam app](https://app.viam.com/).
Click on the **Services** subtab and click **Create service**.
Select the `pubsub` type, then select the `viam-labs:service:mqtt-grpc` model.
Enter a name for your pubsub and click **Create**.

On the new component panel, copy and paste the following attribute template into your pubsub’s **Attributes** box:

```json
{
  "broker": "my.mqtt.broker",
  "port": 1883,
  "username": "username_if_required",
  "password": "password_if_required"
}
```

> [!NOTE]  
> For more information, see [Configure a Robot](https://docs.viam.com/manage/configuration/).

### Attributes

The following attributes are available for `viam-labs:pubsub:viam-labs:service:mqtt-grpc` pubsubs:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `broker` | string | **Required** |  Address of MQTT broker, required unless local_mosquitto is set to true |
| `port` | int | Optional |  MQTT broker port, defaults to 1883 |
| `username` | string | Optional |  URI to MQTT broker, required unless local_mosquitto is set to true |
| `password` | string | Optional |  URI to MQTT broker, required unless local_mosquitto is set to true |
| `local_mosquitto` | boolean | Optional | Defaults to false, if true will attempt to install and use a local mosquitto instance |

### Example Configurations

A typical configuration might look like:

```json
{
  "broker": "192.168.0.140",
  "port": 1883,
  "username": "mqttclient",
  "password": "mysupers3cur3Password!"
}
```

### Usage

To interact with the your configured service with Viam SDKs, see the [viam-labs pubsub API](https://github.com/viam-labs/pubsub-api) documentation.
