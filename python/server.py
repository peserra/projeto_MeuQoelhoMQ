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
        return f"nome: {self.name} tipo: {self.type} mensagens pendentes: {len(self.messages)}"


class MessagerieManager(simple_pb2_grpc.MessageManagerServicer):
    def __init__(self) -> None:
        self.channels = []
        self.channels_names = []
        self.channels_path = "channels_list.txt"
        with open(self.channels_path, '+ab') as f:
            file_path = os.path.abspath(f.name)
            match os.path.getsize(self.channels_path):
                case 0: self.SaveChannelsOnFile(self.channels_path)
                case _: self.LoadChannelsOnFile(self.channels_path)

    # salva os canais no arquivo channels_list.txt
    def SaveChannelsOnFile(self, file_path):
        channel_list = simple_pb2.ChannelsList()
        grpc_channels = [simple_pb2.Channel(name=channel.name, 
                                            type=channel.type, 
                                            messages=channel.messages) 
                                            for channel in self.channels]
        channel_list.channels.extend(grpc_channels)
        with open(file_path, 'wb') as f:
            f.write(channel_list.SerializeToString())

    # carrega os canais do arquivo channels_list.txt
    def LoadChannelsOnFile(self, file_path):
        grpc_channels_list = simple_pb2.ChannelsList()
        with open(file_path, 'rb') as f: 
            grpc_channels_list.ParseFromString(f.read())
        
        self.channels = [Channel(name=c.name, type=c.type) for c in grpc_channels_list.channels]
        for i, c in enumerate(grpc_channels_list.channels):
            self.channels[i].messages = list(c.messages)
            self.channels_names.append(c.name)
    
    def CreateChannel(self, request, context):
        if request.name in self.channels_names:
            server_response = simple_pb2.CreateChannelResponse(
            success = False,
            operation_status_message = f"canal com nome '{request.name}' já existe."
            )
            return server_response

        channel = Channel(name=request.name, type=request.type)
        self.channels.append(channel)
        # lookup table para os nomes dos canais
        self.channels_names.append(channel.name)
        
        self.SaveChannelsOnFile(self.channels_path)
        server_response = simple_pb2.CreateChannelResponse(
            success = True,
            operation_status_message = f"canal '{request.name}' criado!"
        )
        return server_response
    
    def RemoveChannel(self, request, context):
        try: 
            self.channels.pop(self.channels_names.index(request.name))
            self.channels_names.remove(request.name)
            self.SaveChannelsOnFile(self.channels_path)
            
            server_response = simple_pb2.RemoveChannelResponse(
                success=True,
                operation_status_message= f"canal '{request.name}' removido!"
            )
        except(ValueError) as e:
            server_response = simple_pb2.RemoveChannelResponse(
                success=False,
                operation_status_message= f"canal '{request.name}' não encontrado."
            )
             
        return server_response
    
    # por algum motivo, o tipo do canal nao eh mandado
    def ListChannels(self, request, context):
        channel_response = [simple_pb2.ChannelInfo(
                            name=channel.name,
                            type=channel.type,
                            pendingMessages=len(channel.messages))
                            for channel in self.channels]
        print(channel_response[0].type)
        server_response = simple_pb2.ListChannelsResponse(
          channels = channel_response 
        )
        return server_response
        
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