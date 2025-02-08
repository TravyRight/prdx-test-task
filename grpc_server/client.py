import asyncio

import grpc
from grpc_server import messages_pb2 as pb2
from grpc_server import messages_pb2_grpc as pb2_grpc


async def run(message: str, discord_channel_id: int):
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = pb2_grpc.SendMessageServiceStub(channel)
        request = pb2.SendMessageRequest(message=message, channel_id=discord_channel_id)
        response = await stub.SendMessage(request)

    print(response.result)


if __name__ == "__main__":
    asyncio.run(run("test1", 1337427406277054569))

"""
class Client(object):
    def __init__(self):
        self.host = "localhost"
        self.port = 50051

        self.channel = grpc.aio.insecure_channel(f"{self.host}:{self.port}")
        self.stub = pb2_grpc.SendMessageServiceStub(self.channel)

    async def send_message(self, message: str, discord_channel_id: int):
        request = pb2.SendMessageRequest(message=message, channel_id=discord_channel_id)
        response = await self.stub.SendMessage(request)
        return response


if __name__ == "__main__":
    client = Client()
    
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(client.send_message("test1", 1337427406277054569))
    
    print(result)
"""
