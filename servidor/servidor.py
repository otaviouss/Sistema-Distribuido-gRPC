import grpc
import servidor_pb2_grpc

from servidor_pb2_grpc import opcoesClienteServicer

def serve():
    server = grpc.server(grpc.Future.ThreadPoolExecutor(max_workers=10))
    servidor_pb2_grpc.add_RouteGuideServicer_to_server(
        opcoesClienteServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()