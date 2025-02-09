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
            channel = await bot.fetch_channel(int(request.channel_id))

            if channel is None:
                result = f"gRPC server error: bot can not get the channel by id: {request.channel_id}"
            elif len(request.message) == 0:
                result = "gRPC server error: The message can not be null"
            else:
                await channel.send(request.message)
                result = f"gRPC server: message was sent to the channel"

            return pb2.SendMessageResponse(result=result)

        except Exception as e:
            logging.error(f'gRPC server func "SendMessage" error: {e}')
            print(e)


async def serve():
    log_message = "gRPC server was started"
    logging.info(log_message)
    print(log_message)

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
    asyncio.run(serve())
