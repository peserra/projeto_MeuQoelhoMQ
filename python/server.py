from concurrent import futures
import grpc
import simple_pb2
import simple_pb2_grpc

class MqStuff(simple_pb2_grpc.MQ_stuffServicer):
    def CriaCanal(self, request, context):
        with open("./canal1.txt", 'a+') as f:
            f.write("Abrindo canal 1")
        return simple_pb2.StatusOpening(f"Consegui abrir canal 1 recebendo {request.client_id} e {request.client_name}")
    


def main():
    port = "12345"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    simple_pb2_grpc.add_MQ_stuffServicer_to_server(MqStuff(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print(f"Server iniciado na porta: {port}")
    server.wait_for_termination()


if __name__ == "__main__":
    main()