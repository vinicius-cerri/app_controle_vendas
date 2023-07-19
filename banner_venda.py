# Importar Bibliotecas
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle

# Classe que Cria o Banner com as Vendas
class BannerVenda(GridLayout):
    
    def __init__(self, **kwargs):
        self.rows = 1
        super().__init__()

        # Formatar o Plano de Fundo
        with self.canvas:
            Color(rgb=(0, 0, 0, 1))
            self.rec = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.atualizar_rec, size=self.atualizar_rec)

        # Pegar as Informações da Venda
        cliente = kwargs['cliente']
        foto_cliente = kwargs['foto_cliente']
        produto = kwargs['produto']
        foto_produto = kwargs['foto_produto']
        data = kwargs['data']
        preco = float(kwargs['preco'])
        unidade = kwargs['unidade']
        quantidade = float(kwargs['quantidade'])

        # Separar o Banner em 3 Partes
        esquerda = FloatLayout()
        esquerda_imagem = Image(pos_hint={'right': 1, 'top': 0.95}, size_hint=(1, 0.75), source=f'icones/fotos_clientes/{foto_cliente}')
        esquerda_label = Label(pos_hint={'right': 1, 'top': 0.2}, size_hint=(1, 0.2), text=cliente)
        esquerda.add_widget(esquerda_imagem)
        esquerda.add_widget(esquerda_label)

        meio = FloatLayout()
        meio_imagem = Image(pos_hint={'right': 1, 'top': 0.95}, size_hint=(1, 0.75), source=f'icones/fotos_produtos/{foto_produto}')
        meio_label = Label(pos_hint={'right': 1, 'top': 0.2}, size_hint=(1, 0.2), text=produto)
        meio.add_widget(meio_imagem)
        meio.add_widget(meio_label)

        direita = FloatLayout()
        direita_label_data = Label(pos_hint={'right': 1, 'top': 0.9}, size_hint=(1, 0.33), text=f'Data: {data}')
        direita_label_preco = Label(pos_hint={'right': 1, 'top': 0.65}, size_hint=(1, 0.33), text=f'Preço: R${preco:,.2f}')
        direita_label_unidade = Label(pos_hint={'right': 1, 'top': 0.4}, size_hint=(1, 0.33), text=f'{quantidade} {unidade}')
        
        direita.add_widget(direita_label_data)
        direita.add_widget(direita_label_preco)
        direita.add_widget(direita_label_unidade)

        # Adicionar as 3 Partes do Banner
        self.add_widget(esquerda)
        self.add_widget(meio)
        self.add_widget(direita)
        
    # Função para Atualizar o Tamanho do Retângulo de acordo com o Tamanho do Banner
    def atualizar_rec(self, *args):
        self.rec.pos = self.pos
        self.rec.size = self.size