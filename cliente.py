import json
import socket

class Cliente():

    def __init__(self):
        pass

    def conectar(self):
        s = socket.socket()
        # Define the port on which you want to connect
        port = 7777
        # connect to the server on local computer
        s.connect(('127.0.0.1', port))
        return s

    def solicitarCriarUsuario(self, email, nome, senha):
        self.s = self.conectar()

        file = json.dumps({"op": "CC", "email": email, "nome": nome, "senha": senha})

        self.s.sendall(file.encode())

        dados = self.s.recv(1024).decode()

        if(dados=="1"):
            print("Sucesso!")
        else:
            print("Falha! Email já utilizado.")
        
        self.desconectar()

    def realizarLogin(self, email, senha):
        self.s = self.conectar()

        file = json.dumps({"op": "FL", "email": email, "senha": senha})

        self.s.sendall(file.encode())

        dados = self.s.recv(1024).decode()

        if(dados!="0"):
            self.user_id = int(dados)
            print("Logado com Sucesso!")
            self.desconectar()
            return 1
        else:
            print("Falha ao Logar!")
            self.desconectar()
            return 0

    def cadastrarVoucher(self, titulo, descricao, gato, local, lanche, duracao):
        self.s = self.conectar()

        file = json.dumps({"op": "CV", "titulo": titulo, "descricao": descricao,
                            "gato": gato, "local": local, "lanche": lanche,
                            "duracao": duracao, "titular_id": self.user_id})

        self.s.sendall(file.encode())

        self.desconectar()
    
    def apresentarTrocas(self):
        self.s = self.conectar()
        
        file = json.dumps({"op": "AT", "id_usuario": self.user_id})

        self.s.sendall(file.encode())

        dados = self.s.recv(1048576).decode()

        print(dados)
        print("Apresentando todas as trocas pendentes.")

        self.desconectar()

        return json.loads(dados)

    def proporTroca(self, id_voucher1, id_voucher2):
        self.s = self.conectar()

        print("Propondo Troca")
        file = json.dumps({"op": "PT", "id_voucher1": id_voucher1, "id_voucher2": id_voucher2})
        
        self.s.sendall(file.encode())

        self.desconectar()

    def realizarTroca(self, id_troca):
        self.s = self.conectar()

        file = json.dumps({"op": "RT", "id_troca": id_troca})

        self.s.sendall(file.encode())

        print("Troca Aceita")

        self.desconectar()

    def negarTroca(self, id_troca):
        self.s = self.conectar()

        file = json.dumps({"op": "NT", "id_troca": id_troca})

        self.s.sendall(file.encode())

        print("Troca Negada")

        self.desconectar()

    def apresentarVouchersUsuario(self):
        self.s = self.conectar()
        
        file = json.dumps({"op": "VU", "id_usuario": self.user_id})

        self.s.sendall(file.encode())

        dados = self.s.recv(1048576).decode()

        print("Apresentando vouchers do usuário logado.")

        self.desconectar()

        return json.loads(dados)

    def apresentarVouchers(self):
        self.s = self.conectar()
        
        file = json.dumps({"op": "AV"})

        self.s.sendall(file.encode())

        dados = self.s.recv(1048576).decode()

        print("Apresentando todos os vouchers.")

        self.desconectar()

        return json.loads(dados)
    
    def desconectar(self):
        self.s.close()

def main():
    c = Cliente()
    #c.solicitarCriarUsuario(email="teste", nome="AAA", senha="123")	
    c.realizarLogin("marta@gmail.com", "123")
    #c.cadastrarVoucher(titulo="hahah", descricao="hehehe", gato="GT", local="LC", lanche="LA", duracao="DU", imagem="IM", titular_id="1")
    #c.proporTroca(id_voucher1="2", id_voucher2="4")
    #c.realizarTroca(id_troca="1")
    #c.negarTroca(id_troca="2")
    #c.apresentarVouchers()
    c.apresentarTrocas()
    #c.realizarLogin("lsls", "123")
    c.desconectar()

if __name__ == '__main__':
    main()