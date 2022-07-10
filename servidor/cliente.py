import asyncio
import servidor_pb2_grpc

from banco.bd import banco
from _thread import *

class Clientes(servidor_pb2_grpc.opcoesClienteServicer):

    def __init__(self):
        pass

    def cadastrarCliente(self, email, nome, senha):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(banco.inserir_usuario(email, nome, senha))
            loop.close()
            return 1
        except:
            return 0

    def checarCliente(self, email, senha):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            user = loop.run_until_complete(banco.ver_usuario(email, senha))
            loop.close()

            if user is None: return 0

            return user.id
        except:
            return 0

def main():
    pass

if __name__ == '__main__':
    main()
