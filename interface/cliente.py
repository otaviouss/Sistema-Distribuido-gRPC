from __future__ import print_function

import logging

import grpc
import servidor_pb2 as s
import servidor_pb2_grpc as s_grpc

class Cliente():

    def __init__(self):
        pass

    def solicitarCriarUsuario(self, nome, email, senha):

        with grpc.insecure_channel('localhost:50051') as channel:
            stub = s_grpc.opcoesClienteStub(channel)
            response = stub.cadastrarCliente(s.Cliente(email=email, nome=nome, senha=str(senha)))

        if(response.message == 1):
            print("Sucesso!")
            self.realizarLogin(email, senha)
        else:
            print("Falha! Email já utilizado.")

    def realizarLogin(self, email, senha):

        with grpc.insecure_channel('localhost:50051') as channel:
            stub = s_grpc.opcoesClienteStub(channel)
            response = stub.checarCliente(s.Cliente(email=email, senha=str(senha)))

        if(response.message != 0):
            self.user_id = int(response.message)
            print("Logado com Sucesso!")
            return 1
        else:
            print("Falha ao Logar!")
            return 0
    
    def cadastrarVoucher(self, titulo, descricao, gato, local, lanche, duracao):

        with grpc.insecure_channel('localhost:50051') as channel:
            stub = s_grpc.opcoesVoucherStub(channel)
            response = stub.cadastrarVoucher(s.Voucher(titulo=titulo, descricao=descricao, gato=gato, local=local, lanche=lanche, duracao=duracao, titular_id=self.user_id))

        return response.message
    
    def apresentarVouchersUsuario(self):

        with grpc.insecure_channel('localhost:50051') as channel:
            stub = s_grpc.opcoesVoucherStub(channel)
            response = stub.apresentarVouchersUsuario(s.ID(id=self.user_id))

        print("Apresentando vouchers do usuário logado.")

        return response
    
    def apresentarVouchers(self):

        with grpc.insecure_channel('localhost:50051') as channel:
            stub = s_grpc.opcoesVoucherStub(channel)
            response = stub.apresentarVouchers(s.ID(id=self.user_id))

        print("Apresentando todos os vouchers.")

        return response

    def apresentarTrocas(self):

        with grpc.insecure_channel('localhost:50051') as channel:
            stub = s_grpc.opcoesTrocaStub(channel)
            response = stub.apresentarTrocas(s.ID(id=self.user_id))

        print(response)
        print("Apresentando todas as trocas pendentes.")

        return response

    def proporTroca(self, id_voucher1, id_voucher2):

        with grpc.insecure_channel('localhost:50051') as channel:
            stub = s_grpc.opcoesTrocaStub(channel)
            response = stub.apresentarTrocas(s.Troca(id1=id_voucher1, id2=id_voucher2))

        print("Propondo Troca")

        return response

    def realizarTroca(self, id_troca):

        with grpc.insecure_channel('localhost:50051') as channel:
            stub = s_grpc.opcoesTrocaStub(channel)
            response = stub.realizarTroca(s.Troca(id1=id_troca))

        print("Troca Aceita")

        return response

    def negarTroca(self, id_troca):

        with grpc.insecure_channel('localhost:50051') as channel:
            stub = s_grpc.opcoesTrocaStub(channel)
            response = stub.negarTroca(s.Troca(id1=id_troca))

        print("Troca Negada")

        return response
    
    def deslogar(self):
        self.user_id = -1
        return 1


def main():
    c = Cliente()
    c.solicitarCriarUsuario(email="teste", nome="AAA", senha="123")	
    c.realizarLogin("marta@gmail.com", "123")
    c.cadastrarVoucher(titulo="hahah", descricao="hehehe", gato="GT", local="LC", lanche="LA", duracao=10)
    c.proporTroca(id_voucher1=2, id_voucher2=4)
    c.realizarTroca(id_troca=1)
    c.negarTroca(id_troca=2)
    c.apresentarVouchers()
    c.apresentarTrocas()
    c.realizarLogin("lsls", "123")

if __name__ == '__main__':
    logging.basicConfig()
    main()
