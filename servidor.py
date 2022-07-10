import json
import socket
import asyncio

from bd import banco
from _thread import *

class Servidor():

    def __init__(self):
        pass

    def cadastrarCliente(self, email, nome, senha, c):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(banco.inserir_usuario(email, nome, senha))
            loop.close()
            
            c.sendall("1".encode())
            c.close()
        except:
            c.sendall("0".encode())
            c.close()

    def checarCliente(self, email, senha, c):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            user = loop.run_until_complete(banco.ver_usuario(email, senha))
            loop.close()

            if user is None:
                c.sendall("0".encode())
                return 0

            c.sendall(str(user.id).encode())
            c.close()
        except:
            c.sendall("0".encode())
            c.close()

    def cadastrarVoucher(self, titulo, descricao, gato, local, lanche, duracao, titular_id, c):
        imagem = str(gato[0].lower()) + '.png'
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(banco.inserir_voucher(titulo, descricao, gato, local, lanche, int(duracao), imagem, int(titular_id)))
        loop.close()
        c.close()
    
    def apresentarTrocas(self, id_usuario, c):
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

        file = json.dumps(v)

        c.sendall(file.encode())

        c.close()

    def proporTroca(self, id_voucher1, id_voucher2, c):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(banco.nova_Troca(int(id_voucher1), int(id_voucher2)))
        loop.close()
        c.close()

    def realizarTroca(self, id_troca, c):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(banco.alterar_Status_Troca_Aceito(int(id_troca)))
            loop.close()
            
            c.sendall("1".encode())
            c.close()
        except:
            c.sendall("0".encode())
            c.close()

    def negarTroca(self, id_troca, c):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(banco.alterar_Status_Troca_Rejeitado(int(id_troca)))
            loop.close()

            c.sendall("1".encode())
            c.close()
        except:
            c.sendall("0".encode())
            c.close()
    
    def apresentarVouchersUsuario(self, id_usuario, c):
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

        file = json.dumps(v)

        c.sendall(file.encode())

        c.close()

    def apresentarVouchers(self, c):
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

        file = json.dumps(v)

        c.sendall(file.encode())

        c.close()


def main():
    soc = socket.socket()		
    print ("Socket successfully created")

    s = Servidor()

    # reserve a port on your computer
    port = 7777

    # Next bind to the port
    # we have not typed any ip in the ip field
    # instead we have inputted an empty string
    # this makes the server listen to requests
    # coming from other computers on the network
    soc.bind(('', port))		
    print ("socket binded to %s" %(port))

    # put the socket into listening mode
    soc.listen(5)	
    print ("socket is listening")		

    # a forever loop until we interrupt it or
    # an error occurs
    while True:

        # Establish connection with client.
        c, addr = soc.accept()	
        print ('Got connection from', addr )

        dados = c.recv(1024).decode()

        file = json.loads(dados)
        print(file)

        if(file["op"]=="CC"):
            start_new_thread(s.cadastrarCliente, (file["email"], file['nome'], file["senha"], c))
        elif(file["op"]=="FL"):
            start_new_thread(s.checarCliente, (file["email"], file["senha"], c))
        elif(file["op"]=="CV"):
            start_new_thread(s.cadastrarVoucher, (file["titulo"], file["descricao"], file["gato"], file["local"], file["lanche"], file["duracao"], file["titular_id"], c))
        elif(file["op"]=="AT"):
            start_new_thread(s.apresentarTrocas, (file["id_usuario"], c))
        elif(file["op"]=="PT"):
            start_new_thread(s.proporTroca, (file["id_voucher1"], file["id_voucher2"], c))
        elif(file["op"]=="RT"):
            start_new_thread(s.realizarTroca, (file["id_troca"], c))
        elif(file["op"]=="NT"):
            start_new_thread(s.negarTroca, (file["id_troca"], c))
        elif(file["op"]=="VU"):
            start_new_thread(s.apresentarVouchersUsuario, (file["id_usuario"], c))
        elif(file["op"]=="AV"):
            start_new_thread(s.apresentarVouchers, (c,))



if __name__ == '__main__':
    main()
