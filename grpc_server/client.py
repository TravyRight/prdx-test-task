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
    asyncio.run(run("gRPC server test", 1338165904630087873))
