import asyncio
import servidor_pb2
import servidor_pb2_grpc

from bd import banco

class Vouchers(servidor_pb2_grpc.opcoesVoucherServicer):
    
    def __init__(self):
        pass

    def cadastrarVoucher(self, voucher, obj):
        imagem = str(voucher.gato[0].lower()) + '.png'
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(banco.inserir_voucher(voucher.titulo, voucher.descricao, voucher.gato, voucher.local, voucher.lanche, int(voucher.duracao), imagem, int(voucher.titular_id)))
        loop.close()

        return servidor_pb2.Resposta(message=1)

    def apresentarVouchersUsuario(self, ID, obj):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        vouchers = loop.run_until_complete(banco.ver_vouchers_usuario(ID.id))
        loop.close()

        v = []
        for i in range(len(vouchers)):
            s = servidor_pb2.Voucher(
                id = vouchers[i].id,
                titulo = vouchers[i].titulo,
                descricao = vouchers[i].descricao,
                gato = vouchers[i].gato,
                local = vouchers[i].local,
                lanche = vouchers[i].lanche,
                duracao = vouchers[i].duracao,
                imagem = vouchers[i].imagem,
                titular_id = vouchers[i].titular_id
            )
            v.append(s)

        return servidor_pb2.Vouchers(v)

    def apresentarVouchers(self, ID, obj):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        vouchers = loop.run_until_complete(banco.ver_vouchers())
        loop.close()

        v = []
        for i in range(len(vouchers)):
            s = servidor_pb2.Voucher(
                id = vouchers[i].id,
                titulo = vouchers[i].titulo,
                descricao = vouchers[i].descricao,
                gato = vouchers[i].gato,
                local = vouchers[i].local,
                lanche = vouchers[i].lanche,
                duracao = vouchers[i].duracao,
                imagem = vouchers[i].imagem,
                titular_id = vouchers[i].titular_id
            )
            v.append(s)

        return servidor_pb2.Vouchers(v)

if __name__ == '__main__':
    pass
