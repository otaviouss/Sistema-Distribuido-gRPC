import kivy

from cliente.cliente import Cliente

kivy.require('2.1.0')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import StringProperty, ListProperty
from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.popup import Popup

class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior, RecycleGridLayout):
    ''' Adds selection and focus behaviour to the view. '''

class Voucher(RecycleDataViewBehavior, BoxLayout):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    '''Atributos Voucher'''
    imagem = StringProperty()
    label_titulo = StringProperty()
    label_descricao = StringProperty()
    label_nome_gato = StringProperty()
    label_local = StringProperty()
    label_lanche = StringProperty()
    label_duracao = StringProperty()
    '''----------------------------'''

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(Voucher, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(Voucher, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    
    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        #print("__> ", self.selected)
        global selecionado
        selecionado = self.selected
        if is_selected:
            print("selection changed to {0}".format(index))
            pass
        else:
            print("selection removed for {0}".format(index))
            pass
    

class RV(RecycleView):
    rv_data_list = ListProperty()
    dupla_troca = []
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)

    # Carrega todos os Vouchers
    def LoadData(self):
        self.rv_data_list.clear()
        dados = c.apresentarVouchers()
        print(dados)
        self.rv_data_list.extend([{'imagem': 'figuras/' + dados[str(i)]["imagem"], 
                                   'label_titulo': dados[str(i)]["titulo"],
                                   'label_descricao': dados[str(i)]["descricao"],
                                   'label_nome_gato': dados[str(i)]["gato"],
                                   'label_local': dados[str(i)]["local"],
                                   'label_lanche': dados[str(i)]["lanche"],
                                   'label_duracao': str(dados[str(i)]["duracao"])} for i in range(len(dados))])
    
    
    # Carrega os Vouchers do Usuário Logado
    def LoadDataUser(self):
        self.rv_data_list.clear()
        dados = c.apresentarVouchersUsuario()
        self.meus_vouchers = dados
        self.id_troca = -1

        self.rv_data_list.extend([{'imagem': 'figuras/' + dados[str(i)]["imagem"],
                                   'label_titulo': dados[str(i)]["titulo"],
                                   'label_descricao': dados[str(i)]["descricao"],
                                   'label_nome_gato': dados[str(i)]["gato"],
                                   'label_local': dados[str(i)]["local"],
                                   'label_lanche': dados[str(i)]["lanche"],
                                   'label_duracao': str(dados[str(i)]["duracao"])} for i in range(len(dados))])
    
    def IsAnyVoucherSelected(self):
        if not self.layout_manager.selected_nodes:
            return False
        
        return True

    def AddVoucherSelected(self):
        print("Check : ", self.dupla_troca)
        self.dupla_troca.append(self.layout_manager.selected_nodes[0])
        self.layout_manager.selected_nodes = []

    # Propõe uma Troca
    def GetPropostaTroca(self):
        print("HELPS : ", self.dupla_troca)
        todos_vouchers = c.apresentarVouchers()
        c.proporTroca(self.meus_vouchers[str(self.dupla_troca[1])]["id"], todos_vouchers[str(self.dupla_troca[0])]["id"])
        self.dupla_troca.clear()


    def InicializarTrocas(self):
        trocas = c.apresentarTrocas()
        qtd_trocas = len(trocas)

        self.rv_data_list = []

        if(qtd_trocas==0): 
            self.rv_data_list = []
            return

        self.rv_data_list.extend([{'label_titulo': 'Troca ' + str(i),
                                    'label_trocaI_titulo': trocas[str(i)]['titulo_v1'],
                                    'label_trocaI_gato': trocas[str(i)]['gato_v1'],
                                    'label_trocaII_titulo': trocas[str(i)]['titulo_v2'],
                                    'label_trocaII_gato': trocas[str(i)]['gato_v2'],
                                    'id_troca': str(trocas[str(i)]['id_troca']),
                                    } for i in range(qtd_trocas)])

c = Cliente() # Variável "global" por falta de melhor forma