import grpc
import simple_pb2
import simple_pb2_grpc


def main():
    with grpc.insecure_channel("localhost:12345") as channel:
        client_stub = simple_pb2_grpc.MessageManagerStub(channel)
        #chama_ping = client_stub.Ping(simple_pb2.noParam(conteudo = "aaaaa", type = simple_pb2.MULTIPLE))
        resposta = client_stub.CreateChannel(simple_pb2.CreateChannelRequest(name ="canal3", type = simple_pb2.ChannelType.SIMPLE))
        resposta = client_stub.ListChannels(simple_pb2.ListChannelsRequest())
        print(f"recebido do server: {resposta}")

        publish_response = client_stub.PublishMessage(
            simple_pb2.PublishMessageRequest(
                channel='canal3',
                messageList=[simple_pb2.Message(content="Primeira mensagem"), simple_pb2.Message(content="Segunda mensagem")]
            ))
        print(f"PublishMessage Response: {publish_response}")

        # Chamada para SubscribeChannelUnary
        subscribe_unary_response = client_stub.SubscribeChannelUnary(
            simple_pb2.SubscribeChannelRequest(channel="canal3", timeout=10))
        print(f"SubscribeChannelUnary Response: {subscribe_unary_response.content}")

        # Chamada para SubscribeChannelStream
        print("SubscribeChannelStream Responses:")
        for message in client_stub.SubscribeChannelStream(
            simple_pb2.SubscribeChannelRequest(channel="canal3", timeout=10)
        ):
            print(f"Message received: {message.content}")       

        # Chamada para ReceiveMessage
        receive_message_response = client_stub.ReceiveMessage(
            simple_pb2.ReceiveMessageRequest(channel="canal3", timeout=10)
        )
        print(f"ReceiveMessage Response: {receive_message_response.content}")         

if __name__ == "__main__":
    main()