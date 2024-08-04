import grpc
import simple_pb2
import simple_pb2_grpc


def main():
    print("Tentando abrir um canal")

    with grpc.insecure_channel("localhost:12345") as channel:
        client_stub = simple_pb2_grpc.MessageManagerStub(channel)
        #chama_ping = client_stub.Ping(simple_pb2.noParam(conteudo = "aaaaa", type = simple_pb2.MULTIPLE))
        resposta = client_stub.ListChannels(simple_pb2.ListChannelsRequest())
        print(f"recebido do server: {resposta}")



if __name__ == "__main__":
    main()