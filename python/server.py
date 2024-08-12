from concurrent import futures
import random
import time
import grpc # type: ignore
import simple_pb2
import simple_pb2_grpc
import os
import queue
import threading

class Channel:
    def __init__(self, name, type) -> None:
        self.name:str = name
        self.type:simple_pb2.ChannelType = type
        self.messages:list = []
        self.subscribed_clients:dict = {}
    def __repr__(self) -> str:
        return f"nome: {self.name} tipo: {self.type} mensagens pendentes: {len(self.messages)}"


class MessagerieManager(simple_pb2_grpc.MessageManagerServicer):
    def __init__(self) -> None:
        # organiza os requests numa queue para organizar concorrencia
        self.request_queue = queue.Queue()
        # organiza respostas em queue, para devolver cada resposta do rpc em ordem
        self.result_queue = queue.Queue()
        # variavel de condicao
        self.condition_var = threading.Condition()
        self.conta_threads = 0
        
        self.channels:list = []
        self.channels_names:list = []
        self.channels_path:str = "channels_list.txt"
        with open(self.channels_path, '+ab') as f:
            file_path = os.path.abspath(f.name)
            match os.path.getsize(self.channels_path):
                case 0: self.SaveChannelsOnFile(self.channels_path)
                case _: self.LoadChannelsOnFile(self.channels_path)
    
    '''
        gpt -> Thread que vai cuidar dos processos requisitados, processando-os
        respeitando uma ordem, que esta integrada da request queue

        consome a fila de requests, utilizando a variavel de condicao para lidar
        com o estado da solicitacao.
        
    ''' 
    def RequestProcessor(self):
        while True:
            with self.condition_var:
                while self.request_queue.empty():
                    self.condition_var.wait()
                function_solicitada, args, kwargs = self.request_queue.get()
            result_request = function_solicitada(*args, **kwargs)
            self.result_queue.put(result_request)
            nome_function = function_solicitada.__name__.replace("_Logic","")
            print(f" Processado request: '{nome_function}'")
            self.request_queue.task_done()
            #return result_request
    
    '''
        Enfileira os requests na fila
        retorna a cabeca da fila com o resultado do ultimo request processado
    '''
    def EnqueueRequest(self, function, *args, **kwargs):
        with self.condition_var:
            self.request_queue.put((function, args, kwargs))
            self.condition_var.notify()
        return self.result_queue.get()

    # salva os canais no arquivo channels_list.txt de forma serializada
    def SaveChannelsOnFile(self, file_path) -> None:
        channel_list:list = simple_pb2.ChannelsList()
        grpc_channels:list = [simple_pb2.Channel(name=channel.name, 
                                            type=channel.type, 
                                            messages=channel.messages) 
                                            for channel in self.channels]
        channel_list.channels.extend(grpc_channels)
        with open(file_path, 'wb') as file:
            file.write(channel_list.SerializeToString())

    # carrega os canais do arquivo channels_list.txt, remontando a lista de canais
    def LoadChannelsOnFile(self, file_path) -> None:
        grpc_channels_list:list = simple_pb2.ChannelsList()
        with open(file_path, 'rb') as file: 
            grpc_channels_list.ParseFromString(file.read())
        
        self.channels = [Channel(name=c.name, type=c.type) for c in grpc_channels_list.channels]
        for i, c in enumerate(grpc_channels_list.channels):
            self.channels[i].messages = list(c.messages)
            self.channels_names.append(c.name)
    
    def CreateChannel(self, request, context) -> simple_pb2.CreateChannelResponse:
        def CreateChannel_Logic():
            print(context.peer())
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
        
        return self.EnqueueRequest(CreateChannel_Logic)
    
    def RemoveChannel(self, request, context) -> simple_pb2.RemoveChannelResponse:
        def RemoveChannel_Logic():
            print(context.peer())
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
        return self.EnqueueRequest(RemoveChannel_Logic)
    
    def ListChannels(self, request, context):
        def ListChannels_Logic():
            print(context.peer())
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
        return self.EnqueueRequest(ListChannels_Logic)
        
        
    '''
        Inscreve o cliente no canal, a inscrição NAO PERSISTE caso o server desconecte, sendo necessario nova inscrição
    '''
    def SubscribeChannel(self, request, context):
        def SubscribeChannel_Logic():
            try:
                channel_selected:Channel = next(filter(lambda c: c.name == request.channel, self.channels), None)
                if channel_selected:
                    # mapeia clientes inscritos a um canal
                    channel_selected.subscribed_clients[request.client_id] = context
                    server_response = simple_pb2.SubscribeChannelResponse(
                        success=True,
                        operation_status_message= f"Cliente {context.peer()} com id {request.client_id} inscrito no canal {channel_selected.name}"
                    )
                    return server_response
            except(Exception) as e:
                server_response = simple_pb2.SubscribeChannelResponse(
                        success=False,
                        operation_status_message= f"Server respondeu com erro {e}"
                    )
                return server_response
                 
        return self.EnqueueRequest(SubscribeChannel_Logic)
    
       
    
    # retorna apenas a mensagem no topo do canal >>nao funciona corretamente o multiple
    def ReceiveMessageUnary(self, request, context):
        
        try:
            channel_selected:Channel = next(filter(lambda c: c.name == request.channel, self.channels), None)
            
            if channel_selected.type == simple_pb2.ChannelType.SIMPLE:
                rand_client_key = random.choice(list(channel_selected.subscribed_clients.keys()))
                if request.client_id == rand_client_key:
                    with self.condition_var:
                        while len(channel_selected.messages) == 0:
                            self.condition_var.wait()
                    mensagem = channel_selected.messages[0]
                    server_response = simple_pb2.Message(
                            content=f"{mensagem}"
                        )
                    self.SaveChannelsOnFile(self.channels_path)                                        
                    self.condition_var.notify()
                    return server_response
                else:
                    server_response = simple_pb2.Message(
                            content=f"no message for u"
                        )                                        
                    return server_response
            
            if channel_selected.type == simple_pb2.ChannelType.MULTIPLE:
                #cv = threading.Condition()
                with self.condition_var:
                    while len(channel_selected.messages) == 0:
                        self.condition_var.wait()
                    mensagem = channel_selected.messages[0]

                    clients_amount = len(list(channel_selected.subscribed_clients.keys()))
                    
                    while True:
                        server_response = simple_pb2.Message(
                                content=f"{mensagem}"
                            )
                        print(self.conta_threads, clients_amount)
                        if self.conta_threads  == clients_amount :
                            channel_selected.messages.pop(0)
                            print(channel_selected.messages)
                            self.SaveChannelsOnFile(self.channels_path)
                            self.conta_threads = 0
                            self.condition_var.notify_all()
                        else:
                            self.conta_threads += 1
                            print(self.conta_threads)
                            #self.condition_var.wait()                       
                    
                        return server_response

        except(Exception) as e:
            server_response = simple_pb2.Message(
                    content=f"Server respondeu com erro {str(e)}"
                )
            return server_response

    
                    
    def SendMessageToAllClients(self, messages:list, context):
        for message in messages:
            context.write(message)
            
    
    # retorna todas as mensagens do canal
    def ReceiveMessageStream(self, request, context):
        try:
            channel_selected:Channel = next(filter(lambda c: c.name == request.channel, self.channels), None)
            
            if channel_selected.type == simple_pb2.ChannelType.SIMPLE:
                rand_client_key = random.choice(list(channel_selected.subscribed_clients.keys()))
                with self.condition_var:
                    while len(channel_selected.messages) == 0:
                        self.condition_var.wait()

                if request.client_id == rand_client_key:
                    for message in channel_selected.messages:
                        yield simple_pb2.Message(content=f"{message}")
                        channel_selected.messages.pop(0)
                        self.SaveChannelsOnFile(self.channels_path)
            
            if channel_selected.type == simple_pb2.ChannelType.MULTIPLE:
                threads = []
                while len(channel_selected.messages) == 0:
                        self.condition_var.wait()
                
                for client_stub in channel_selected.subscribed_clients.values():
                    thread = threading.Thread(target=self.SendMessageToAllClients,args=(channel_selected.messages, client_stub),daemon=True)
                    thread.start()
                    threads.append(thread)
                
                for thread in threads:
                    thread.join()
                channel_selected.messages.clear()
                self.SaveChannelsOnFile(self.channels_path)

        
        except(Exception) as e:
            server_response = simple_pb2.Message(
                    content=f"Server respondeu com erro {str(e)}"
                )
            return server_response
    
    
    
    def PublishMessage(self, request, context):
        '''
            A publicacao de mensagens deve ser feita de forma unaria, mas deve permitir
            que o cliente publique uma unica mensagem ou uma lista de mensagens ao canal
        '''
        # Implementacao -> cliente manda uma lista de mensagens, contendo 1 ou n mensagens

        def PublishMessage_Logic():
            try:
                if request.channel not in self.channels_names:
                    return simple_pb2.PublishMessageResponse(
                        success=False,
                        operation_status_message=f"Canal '{request.channel}' não existe."
                    )
                
                if len(request.messageList) == 0:
                    return simple_pb2.PublishMessageResponse(
                            success=True,
                            operation_status_message=f"Foram publicadas 0 mensagens no canal '{request.channel}'."
                        ) 

                message_list:list = [m.content for m in request.messageList]
                channel_selected:Channel = next(filter(lambda c: c.name == request.channel, self.channels), None)

                # adiciona lista de mensagens ao canal
                if channel_selected:
                    channel_selected.messages.extend(message_list)
                    self.SaveChannelsOnFile(self.channels_path)
                    return simple_pb2.PublishMessageResponse(
                        success=True,
                        operation_status_message=f"Mensagens publicadas no canal '{request.channel}'."
                    )
            
            except (Exception) as e:
                return simple_pb2.PublishMessageResponse(
                    success=False,
                    operation_status_message=f"Falha ao publicar mensagens no canal '{request.channel}'. Canal nao encontrado."
                )               
                
        return self.EnqueueRequest(PublishMessage_Logic)
            


def main():
    port = "12345"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    manager = MessagerieManager()
    simple_pb2_grpc.add_MessageManagerServicer_to_server(manager, server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print(f"Server iniciado na porta: {port}")
    threading.Thread(target=manager.RequestProcessor, daemon=True).start()
    server.wait_for_termination()


if __name__ == "__main__":
    main()