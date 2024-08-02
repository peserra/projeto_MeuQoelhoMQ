import grpc
import simple_pb2
import simple_pb2_grpc


def main():
    print("Tentando abrir um canal")

    with grpc.insecure_channel("localhost:12345") as channel:
        client_stub = simple_pb2_grpc.MessageManagerStub(channel)
        resposta = client_stub.CreateChannel(simple_pb2.CreateChannelRequest(name="canal_bacana", type=simple_pb2.ChannelType.SIMPLE))
        print(f"recebido do server: {resposta}")



if __name__ == "__main__":
    main()