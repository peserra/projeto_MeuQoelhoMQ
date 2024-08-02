from concurrent import futures
import grpc
import simple_pb2
import simple_pb2_grpc

class Channel:
    def __init__(self, name, type) -> None:
        self.name = name
        self.type = type
        self.messages = []

    def __repr__(self) -> str:
        return f"Name: {self.name} \nType: {self.type} \nMessages: {len(self.messages)} "
        

class MessagerieManager(simple_pb2_grpc.MessageManagerServicer):
    def __init__(self) -> None:
        self.channels = []
    
    def CreateChannel(self, request, context):
        channel = Channel(name=request.name, type=request.type)
        self.channels.append(channel)
        f = open(f"{request.name}.txt")
        f.close()
        server_response = simple_pb2.CreateChannelResponse(
            success=True,
            operation_status_message= f"canal '{self.channels[0].name}' criado!"
        )
        return server_response
    
    def RemoveChannel(self, request, context):
        return super().RemoveChannel(request, context)
    
    def ListChannels(self, request, context):
        return super().ListChannels(request, context)
        
    def SubscribeChannel(self, request, context):
        return super().SubscribeChannel(request, context)
    
    def PublishMessage(self, request, context):
        return super().PublishMessage(request, context)
    
    def ReceiveMessage(self, request, context):
        return super().ReceiveMessage(request, context)
    



def main():
    port = "12345"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    simple_pb2_grpc.add_MessageManagerServicer_to_server(MessagerieManager(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print(f"Server iniciado na porta: {port}")
    server.wait_for_termination()


if __name__ == "__main__":
    main()