from concurrent import futures
import grpc
import simple_pb2
import simple_pb2_grpc
import os

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
        self.channels_path = "channels_list.txt"
        with open(self.channels_path, '+ab') as f:
            file_path = os.path.abspath(f.name)
            match os.path.getsize(self.channels_path):
                case 0: self.SaveChannelsOnFile(self.channels_path)
                case _: self.LoadChannelsOnFile(self.channels_path)

    # funcao com falhas -> mapear tipos Channel python para tipos proto
    def SaveChannelsOnFile(self, file_path):
        channel_list = simple_pb2.ChannelsList()
        channel_list.channels.extend(self.channels)
        with open(file_path, 'wb') as f:
            f.write(channel_list.SerializeToString())

    def LoadChannelsOnFile(self, file_path):
        channels_list = simple_pb2.ChannelsList()
        with open(file_path, 'rb') as f: 
            channels_list.ParseFromString(f.read())

        self.channels = channels_list.channels 
    
    def Ping(self, request, context):
        no_param = simple_pb2.noParam(conteudo = "bbbbbb", type=simple_pb2.SIMPLE)
        print(f"recebido {request.conteudo} e {request.type}")
        return no_param
    
    def CreateChannel(self, request, context):
        channel = Channel(name=request.conteudo, type=request.type)
        self.channels.append(channel)
        f = open(f"{request.conteudo}.txt", 'w')
        f.close()
        
        server_response = simple_pb2.CreateChannelResponse(
            success=True,
            operation_status_message= f"canal '{self.channels[0].name}' criado!"
        )
        #self.SaveChannelsOnFile(self.channels_path)
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