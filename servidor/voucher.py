import asyncio
import servidor_pb2_grpc

from banco.bd import banco
from _thread import *

class Vouchers(servidor_pb2_grpc.opcoesVoucherServicer):
    
    def __init__(self):
        pass

    def cadastrarVoucher(self, titulo, descricao, gato, local, lanche, duracao, titular_id):
        imagem = str(gato[0].lower()) + '.png'
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(banco.inserir_voucher(titulo, descricao, gato, local, lanche, int(duracao), imagem, int(titular_id)))
        loop.close()

        return 1

    def apresentarVouchersUsuario(self, id_usuario):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        vouchers = loop.run_until_complete(banco.ver_vouchers_usuario(id_usuario))
        loop.close()

        v = {}
        for i in range(len(vouchers)):
            v[i] = {
                "id":vouchers[i].id,
                "titulo":vouchers[i].titulo,
                "descricao":vouchers[i].descricao,
                "gato":vouchers[i].gato,
                "local":vouchers[i].local,
                "lanche":vouchers[i].lanche,
                "duracao":vouchers[i].duracao,
                "imagem":vouchers[i].imagem,
                "titular_id":vouchers[i].titular_id,
            }

        return v

    def apresentarVouchers(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        vouchers = loop.run_until_complete(banco.ver_vouchers())
        loop.close()

        v = {}
        for i in range(len(vouchers)):
            v[i] = {
                "id":vouchers[i].id,
                "titulo":vouchers[i].titulo,
                "descricao":vouchers[i].descricao,
                "gato":vouchers[i].gato,
                "local":vouchers[i].local,
                "lanche":vouchers[i].lanche,
                "duracao":vouchers[i].duracao,
                "imagem":vouchers[i].imagem,
                "titular_id":vouchers[i].titular_id,
            }

        return v

def main():
    pass

if __name__ == '__main__':
    main()
