import asyncio

from viam.module.module import Module
from pubsub_python import Pubsub
from pubsub import mqttGrpc


async def main():
    """This function creates and starts a new module, after adding all desired resources.
    Resources must be pre-registered. For an example, see the `__init__.py` file.
    """
    module = Module.from_args()
    module.add_model_from_registry(Pubsub.SUBTYPE, mqttGrpc.MODEL)
    await module.start()


if __name__ == "__main__":
    asyncio.run(main())
