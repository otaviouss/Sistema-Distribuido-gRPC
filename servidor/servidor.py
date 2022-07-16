
import grpc
import servidor_pb2_grpc

from concurrent import futures
from cliente import Clientes
from voucher import Vouchers
from troca import Trocas

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servidor_pb2_grpc.add_opcoesClienteServicer_to_server(Clientes(), server)
    servidor_pb2_grpc.add_opcoesVoucherServicer_to_server(Vouchers(), server)
    servidor_pb2_grpc.add_opcoesTrocaServicer_to_server(Trocas(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()