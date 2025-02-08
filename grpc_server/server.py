import asyncio
import logging

import grpc
from concurrent import futures

from grpc_server import messages_pb2 as pb2
from grpc_server import messages_pb2_grpc as pb2_grpc
from config import bot


class Messages(pb2_grpc.SendMessageServiceServicer):
    def __init__(self, *args, **kwargs):
        pass

    async def SendMessage(self, request, context):
        try:
            channel = bot.get_channel(int(request.channel_id))

            if channel is None:
                return pb2.SendMessageResponse(result=f"bot can not get the channel by id: {request.channel_id}")

            if len(request.message) == 0:
                return pb2.SendMessageResponse(result="The message can not be null")

            await channel.send(request.message)
            # asyncio.run(channel.send(request.message))
            return pb2.SendMessageResponse(result=f"message was sent to the channel")

        except Exception as e:
            print(e)
            logging.error(f'gRPC server func "SendMessage" error: {e}')


async def serve():
    try:
        server = grpc.aio.server()  # args:  futures.ThreadPoolExecutor(max_workers=10)
        pb2_grpc.add_SendMessageServiceServicer_to_server(Messages(), server)
        server.add_insecure_port("[::]:50051")
        await server.start()
        await server.wait_for_termination()

    except Exception as e:
        print(e)
        logging.error(f"gRPC server error: {e}")


if __name__ == "__main__":
    logging.info(f"gRPC server was started")
    print("gRPC server start")
    asyncio.run(serve())
