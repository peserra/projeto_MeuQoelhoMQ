import grpc
import simple_pb2
import simple_pb2_grpc


def main():
    print("Tentando abrir um canal")

    with grpc.insecure_channel("localhost:12345") as channel:
        client_stub = simple_pb2_grpc.MQ_stuffStub(channel)
        resposta = client_stub.CriaCanal(simple_pb2.RequestOpening(client_id=1, client_name="joao"))
        print(f"recebido do server: {resposta}")



if __name__ == "__main__":
    main()