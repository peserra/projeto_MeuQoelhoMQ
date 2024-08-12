import grpc
import simple_pb2
import simple_pb2_grpc


def main():
    with grpc.insecure_channel("127.0.0.1:12345") as channel:
        client_stub = simple_pb2_grpc.MessageManagerStub(channel)
        
        resposta = client_stub.CreateChannel(simple_pb2.CreateChannelRequest(name ="canal3", type = simple_pb2.ChannelType.MULTIPLE))
        print(f"recebido do server: {resposta}")
    
    
    with grpc.insecure_channel("127.0.1.1:12345") as channel:
        client_stub = simple_pb2_grpc.MessageManagerStub(channel)
        
        resposta = client_stub.SubscribeChannel(simple_pb2.SubscribeChannelRequest(client_id='1',channel ="canal3"))
        print(f"recebido do server: {resposta}")
        resposta = client_stub.ReceiveMessageUnary(simple_pb2.ReceiveMessageRequest(client_id='2',channel ="canal3"))
        print(f"recebido do server client1 : {resposta}")
      

    with grpc.insecure_channel("127.0.2.1:12345") as channel:
        client_stub = simple_pb2_grpc.MessageManagerStub(channel)
        
        resposta = client_stub.SubscribeChannel(simple_pb2.SubscribeChannelRequest(client_id='2',channel ="canal3")) 
        print(f"recebido do server cliente 2: {resposta}")
        resposta = client_stub.ReceiveMessageUnary(simple_pb2.ReceiveMessageRequest(client_id='2',channel ="canal3"))
        print(f"recebido do server cliente 2: {resposta}")

    with grpc.insecure_channel("127.0.2.1:12345") as channel:
        client_stub = simple_pb2_grpc.MessageManagerStub(channel)

        resposta = client_stub.ListChannels(simple_pb2.ListChannelsRequest())
        print(f"recebido do server: {resposta}")
    

if __name__ == "__main__":
    main()