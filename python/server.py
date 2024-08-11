from concurrent import futures
import grpc
import simple_pb2
import simple_pb2_grpc
import os

class Channel:
    def __init__(self, name, type) -> None:
        self.name:str = name
        self.type:simple_pb2.ChannelType = type
        self.messages:list = []
    def __repr__(self) -> str:
        return f"nome: {self.name} tipo: {self.type} mensagens pendentes: {len(self.messages)}"


class MessagerieManager(simple_pb2_grpc.MessageManagerServicer):
    def __init__(self) -> None:
        self.channels:list = []
        self.channels_names:list = []
        self.channels_path:str = "channels_list.txt"
        with open(self.channels_path, '+ab') as f:
            file_path = os.path.abspath(f.name)
            match os.path.getsize(self.channels_path):
                case 0: self.SaveChannelsOnFile(self.channels_path)
                case _: self.LoadChannelsOnFile(self.channels_path)

    # salva os canais no arquivo channels_list.txt
    def SaveChannelsOnFile(self, file_path) -> None:
        channel_list:list = simple_pb2.ChannelsList()
        grpc_channels:list = [simple_pb2.Channel(name=channel.name, 
                                            type=channel.type, 
                                            messages=channel.messages) 
                                            for channel in self.channels]
        channel_list.channels.extend(grpc_channels)
        with open(file_path, 'wb') as file:
            file.write(channel_list.SerializeToString())

    # carrega os canais do arquivo channels_list.txt
    def LoadChannelsOnFile(self, file_path) -> None:
        grpc_channels_list:list = simple_pb2.ChannelsList()
        with open(file_path, 'rb') as file: 
            grpc_channels_list.ParseFromString(file.read())
        
        self.channels = [Channel(name=c.name, type=c.type) for c in grpc_channels_list.channels]
        for i, c in enumerate(grpc_channels_list.channels):
            self.channels[i].messages = list(c.messages)
            self.channels_names.append(c.name)
    
    def CreateChannel(self, request, context) -> simple_pb2.CreateChannelResponse:
        print (request.name, request.type)
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
    
    def RemoveChannel(self, request, context) -> simple_pb2.RemoveChannelResponse:
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
        #print(channel_response)
        server_response = simple_pb2.ListChannelsResponse(
          channels = channel_response 
        )
        return server_response
        
        
    '''
        Clientes devem poder escolher entre Stream (ficar esperando ate chamada acabar)
        ou unary, que faz uma chamada independente e retorna so uma mensagem

        caso nao tenha mensagem disponivel, server deve dar a opção de um timout
    '''
    # cliente fica conectado ao canal, ate que todas as mensagens acabem
    def SubscribeChannelStream(self, request, context):
        channel_name = request.channel
        '''
        busca a lista ou coleção de canais disponíveis na instância da classe e itera sobre cada canal
        disponível até encontrar um que corresponda ao nome do canal solicitado
        '''
        for channel in self.channels:
            if channel.name == channel_name:
                #iterar sobre as mensagens no canal
                for message in channel.messages:
                    '''
                    yield transforma a função em um gerador, permitindo que o método envie
                    uma série de respostas parciais ao invés de uma única resposta completa
                    por fim, cria uma mensagem onde o content é o conteúdo da mensagem a ser enviada
                    '''
                    yield simple_pb2.Message(content=message)
                return
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details('Canal não encontrado.')

    # retorna apenas a mensagem no topo do canal
    def SubscribeChannelUnary(self, request, context):
        channel_name = request.channel
        for channel in self.channels:
            if channel.name == channel_name:
                if channel.messages:
                    '''
                    Se encontrar o canal e tiver mensagens, retorna a primeira mensagem [0] do canal
                    Se encontrar o canal e não houver mensagens, retorna mensagem vazia
                    Se não encontrar o canal, define o status como NOT_FOUND e retorna mensagem vazia
                    '''
                    return simple_pb2.Message(content=channel.messages[0])
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Nenhuma mensagem disponível no canal.')
                return simple_pb2.Message()
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details('Canal não encontrado.')
        return simple_pb2.Message()
    
    # def PublishMessage(self, request, context):
    #     '''
    #         A publicacao de mensagens deve ser feita de forma unaria, mas deve permitir
    #         que o cliente publique uma unica mensagem ou uma lista de mensagens ao canal
    #     '''
    #     # Implementacao -> cliente manda uma lista de mensagens, contendo 1 ou n mensagens
    #     return super().PublishMessage(request, context)
    
    def PublishMessage(self, request, context):
        channel_name = request.channel
        '''
        Cria uma lista de conteúdos de mensagens extraídos de 'request.messageList onde
        cada item do request.messageList é um objeto de mensage
        '''
        messageList = [msg.content for msg in request.messageList]
        
        for channel in self.channels:
            if channel.name == channel_name:
                '''
                se encontrar o canal, adicionar as mensagens da lista de messages a lista de
                mensagens do canal channel.messages, usando o método extend que anexa todas as mensagens
                no final da lista
                '''
                channel.messages.extend(messageList)
                #Salva o estado atual dos canais, incluindo as mensagens recém publicadas
                self.SaveChannelsOnFile(self.channels_path)
                return simple_pb2.PublishMessageResponse(
                    success=True,
                    operation_status_message=f"Mensagens publicadas no canal '{channel_name}'."
                )
        '''
        Se nenhum canal encontrado, definir o código de status para NOT FOUND e fornecer resposta
        E retornar uma resposta PublishMessageResponse indicando que não houve publicação, pois
        o canal não foi encontrado
        '''
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details('Canal não encontrado.')
        return simple_pb2.PublishMessageResponse(
            success=False,
            operation_status_message=f"Falha ao publicar mensagens no canal '{channel_name}'."
        )
    
    def ReceiveMessage(self, request, context):
        return super().ReceiveMessage(request, context)
   
    # def ReceiveMessage(self, request, context):
    #     channel_name = request.channel
        
    #     for channel in self.channels:
    #         if channel.name == channel_name:
    #             if channel.messages:
    #                 message = channel.messages.pop(0)
    #                 self.SaveChannelsOnFile(self.channels_path)
    #                 return simple_pb2.Message(content=message)
    #             context.set_code(grpc.StatusCode.NOT_FOUND)
    #             context.set_details('Nenhuma mensagem disponível no canal.')
    #             return simple_pb2.Message()
        
    #     context.set_code(grpc.StatusCode.NOT_FOUND)
    #     context.set_details('Canal não encontrado.')
    #     return simple_pb2.Message()


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