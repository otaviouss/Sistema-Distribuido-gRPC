from tokenize import String
from recycleView import *

    
class ComponenteTroca(BoxLayout):
    label_titulo = StringProperty()
    label_trocaI_titulo = StringProperty()
    label_trocaI_gato = StringProperty()
    label_trocaII_titulo = StringProperty()
    label_trocaII_gato = StringProperty()
    id_troca = StringProperty()

    def aceitarClick(self):
        c.realizarTroca(int(self.id_troca))

    def rejeitarClick(self):
        c.negarTroca(int(self.id_troca))

class PopupTroca(Popup):
    pass


class TelaInicial(Screen):
    def IrParaLogin(self):
        self.parent.current = 'login'

    def IrParaCadastroUsuario(self):
        self.parent.current = 'telacadastrousuario'

class TelaCadastroUsuario(Screen):
    def IrParaTelaInicial(self):
        self.parent.current = 'telainicial'

    def CadastrarUsuario(self):
        nome = self.ids.nome.text
        email = self.ids.email.text
        senha = self.ids.senha.text

        if (nome != '' and email != '' and senha != ''):
            c.solicitarCriarUsuario(nome, email, senha)
            self.parent.current = 'telamenu'

            self.ids.nome.text = ''
            self.ids.email.text = ''
            self.ids.senha.text = ''
        else:
            self.ids.cad.text = 'Preencha todos os campos!'

class Login(Screen):
    
    def Clicou(self):
        login = self.ids.OK.text
        senha = self.ids.not_OK.text

        if (login != '') and (senha != ''):
            r = c.realizarLogin(login, senha)
            self.VerificarLogin(r)
            self.ids.OK.text = ''
            self.ids.not_OK.text = ''
            return True
        else:
            #self.ids.Jovem.text = 'Preencha todos os campos!'
            popup = Popup(title='Warning', content=Label(text='Preencha todos os campos!'), size_hint=(None, None), size=(400, 400))
            popup.open()
            return False


    def VerificarLogin(self, validado):
        if validado:
            self.parent.current = 'telamenu'
        else:
            popup = Popup(title='Warning', content=Label(text='Credenciais Inválidas!'), size_hint=(None, None), size=(400, 400))
            popup.open()
            #self.ids.Jovem.text = 'Credenciais Inválidas.'

class TelaVouchers(Screen):
    def IrParaMenu(self):
        self.parent.current = 'telamenu'

class TelaMeusVouchers(Screen):
    def IrParaMenu(self):
        self.parent.current = 'telamenu'

class TelaTrocas(Screen):
    def IrParaMenu(self):
        self.parent.current = 'telamenu'

class TelaCadastro(Screen):

    def CadastrarVoucher(self):
        titulo = self.ids.titulo.text
        descricao = self.ids.descricao.text
        gato = self.ids.gato.text
        local = self.ids.local.text
        lanche = self.ids.lanche.text
        duracao = self.ids.duracao.text

        if (titulo != '' and descricao != '' and gato != '' and local != '' and lanche != '' and duracao != ''):
            c.cadastrarVoucher(titulo, descricao, gato, local, lanche, int(duracao))
            self.parent.current = 'telamenu'

            self.ids.titulo.text = ''
            self.ids.descricao.text = ''
            self.ids.gato.text = ''
            self.ids.local.text = ''
            self.ids.lanche.text = ''
            self.ids.duracao.text = ''
        else:
            popup = Popup(title='Warning', content=Label(text='Preencha todos os campos!'), size_hint=(None, None), size=(400, 100))
            popup.open()
            #self.ids.cad.text = 'Preencha todos os campos!'
    
    def IrParaMenu(self):
        self.ids.cad.text = 'Cadastrar Voucher'
        self.parent.current = 'telamenu'

class TelaMenu(Screen):

    def IrParaCadastro(self):
        self.parent.current = 'telacadastro'

    def IrParaMeusVouchers(self):
        self.parent.current = 'telameusvouchers'

    def IrParaVouchers(self):
        self.parent.current = 'telavouchers'

    def IrParaTrocas(self):
        self.parent.current = 'telatrocas'
    
    def Deslogar(self):
        c.deslogar()
        self.parent.current = 'telainicial'

class TrocatApp(App):

    def build(self):
        Window.clearcolor = ( 218/255, 195/255, 232/255, 1)
        manager = ScreenManager()

        manager.add_widget(TelaInicial(name='telainicial'))
        manager.add_widget(Login(name='login'))
        manager.add_widget(TelaCadastroUsuario(name='telacadastrousuario'))
        manager.add_widget(TelaMenu(name='telamenu'))
        manager.add_widget(TelaCadastro(name='telacadastro'))
        manager.add_widget(TelaMeusVouchers(name='telameusvouchers'))
        manager.add_widget(TelaVouchers(name='telavouchers'))
        manager.add_widget(TelaTrocas(name='telatrocas'))

        return manager

if __name__ == '__main__':
    #c = Cliente() # Variável "global" por falta de melhor forma
    principal = TrocatApp()
    principal.run()


'''
https://stackoverflow.com/questions/40470992/too-many-indentation-levels-in-on-press-button
https://stackoverflow.com/questions/56226448/how-to-get-the-instance-from-a-recycleview-with-viewclass-as-button
'''


'''
Ajustes a serem feitos:
 - Alterar a cor do botão quando selecionado na tela de trocas

Problem: 
    Tá permitindo trocas entre vouchers próprios

'''