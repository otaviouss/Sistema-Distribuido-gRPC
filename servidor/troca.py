import asyncio
import servidor_pb2_grpc

from banco.bd import banco
from _thread import *

class Trocas(servidor_pb2_grpc.opcoesTrocaServicer):

    def __init__(self):
        pass

    def apresentarTrocas(self, id_usuario):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        trocas = loop.run_until_complete(banco.ver_Trocas())
        loop.close()

        v = {}
        pos = 0
        for i in range(len(trocas)):
            # Status == 0 significa apresentar apenas trocas pendentes
            if(trocas[i].v2.titular_id == int(id_usuario) and trocas[i].status == 0):
                v[pos] = {
                    "id_troca": i+1,
                    "id_v1":trocas[i].v1.id,
                    "titulo_v1":trocas[i].v1.titulo,
                    "descricao_v1":trocas[i].v1.descricao,
                    "gato_v1":trocas[i].v1.gato,
                    "local_v1":trocas[i].v1.local,
                    "lanche_v1":trocas[i].v1.lanche,
                    "duracao_v1":trocas[i].v1.duracao,
                    "imagem_v1":trocas[i].v1.imagem,
                    "titular_id_v1":trocas[i].v1.titular_id,
                    "id_v2":trocas[i].v2.id,
                    "titulo_v2":trocas[i].v2.titulo,
                    "descricao_v2":trocas[i].v2.descricao,
                    "gato_v2":trocas[i].v2.gato,
                    "local_v2":trocas[i].v2.local,
                    "lanche_v2":trocas[i].v2.lanche,
                    "duracao_v2":trocas[i].v2.duracao,
                    "imagem_v2":trocas[i].v2.imagem,
                    "titular_id_v2":trocas[i].v2.titular_id,
                }
                pos += 1

        return v

    def proporTroca(self, id_voucher1, id_voucher2):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(banco.nova_Troca(int(id_voucher1), int(id_voucher2)))
        loop.close()
        return 1

    def realizarTroca(self, id_troca):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(banco.alterar_Status_Troca_Aceito(int(id_troca)))
            loop.close()
            
            return 1
        except:
            return 0

    def negarTroca(self, id_troca):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(banco.alterar_Status_Troca_Rejeitado(int(id_troca)))
            loop.close()

            return 1
        except:
            return 0

def main():
    pass

if __name__ == '__main__':
    main()
