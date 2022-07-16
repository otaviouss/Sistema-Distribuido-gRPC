import asyncio
import servidor_pb2_grpc
import servidor_pb2

from bd import banco

class Clientes(servidor_pb2_grpc.opcoesClienteServicer):

    def __init__(self):
        pass

    def cadastrarCliente(self, cliente, obj):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(banco.inserir_usuario(cliente.email, cliente.nome, cliente.senha))
            loop.close()

            return servidor_pb2.Resposta(message = 1)
        except:
            return servidor_pb2.Resposta(message = 0)

    def checarCliente(self, cliente, obj):

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            user = loop.run_until_complete(banco.ver_usuario(cliente.email, cliente.senha))
            loop.close()

            if user is None: return servidor_pb2.Resposta(message=0)

            return servidor_pb2.Resposta(message = user.id)
        except:
            return servidor_pb2.Resposta(message = 0)

if __name__ == '__main__':
    pass
