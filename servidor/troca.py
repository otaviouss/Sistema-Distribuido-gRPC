import asyncio
import servidor_pb2
import servidor_pb2_grpc

from bd import banco

class Trocas(servidor_pb2_grpc.opcoesTrocaServicer):

    def __init__(self):
        pass

    def apresentarTrocas(self, troca, obj):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        trocas = loop.run_until_complete(banco.ver_Trocas())
        loop.close()

        v = []
        for i in range(len(trocas)):
            # Status == 0 significa apresentar apenas trocas pendentes
            if(trocas[i].v2.titular_id == int(troca.id1) and trocas[i].status == 0):
                v1 = servidor_pb2.Voucher(
                    id = trocas[i].v1.id,
                    titulo = trocas[i].v1.titulo,
                    descricao = trocas[i].v1.descricao,
                    gato = trocas[i].v1.gato,
                    local = trocas[i].v1.local,
                    lanche = trocas[i].v1.lanche,
                    duracao = trocas[i].v1.duracao,
                    imagem = trocas[i].v1.imagem,
                    titular_id = trocas[i].v1.titular_id
                )
                v2 = servidor_pb2.Voucher(
                    id = trocas[i].v2.id,
                    titulo = trocas[i].v2.titulo,
                    descricao = trocas[i].v2.descricao,
                    gato = trocas[i].v2.gato,
                    local = trocas[i].v2.local,
                    lanche = trocas[i].v2.lanche,
                    duracao = trocas[i].v2.duracao,
                    imagem = trocas[i].v2.imagem,
                    titular_id = trocas[i].v2.titular_id
                )
                t = servidor_pb2.Comp_Troca(i+1, v1, v2)
                v.append(t)

        return v

    def proporTroca(self, troca, obj):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(banco.nova_Troca(int(troca.id1), int(troca.id2)))
        loop.close()
        return servidor_pb2.Resposta(message=1)

    def realizarTroca(self, troca, obj):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(banco.alterar_Status_Troca_Aceito(int(troca.id1)))
            loop.close()
            
            return servidor_pb2.Resposta(message=1)
        except:
            return servidor_pb2.Resposta(message=0)

    def negarTroca(self, troca, obj):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(banco.alterar_Status_Troca_Rejeitado(int(troca.id1)))
            loop.close()

            return servidor_pb2.Resposta(message=1)
        except:
            return servidor_pb2.Resposta(message=0)

if __name__ == '__main__':
    pass
