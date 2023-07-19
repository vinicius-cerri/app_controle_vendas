# Importar Bibliotecas
from botoes import ImageButton, LabelButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
import requests
from kivy.app import App
from functools import partial

# Classe que Cria o Banner com os Vendedores da Equipe
class BannerVendedor(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__()

        # Formatar o Plano de Fundo
        with self.canvas:
            Color(rgb=(0, 0, 0, 1))
            self.rec = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.atualizar_rec, size=self.atualizar_rec)

        # Pegar o ID do Vendedor
        id_vendedor = kwargs["id_vendedor"]

        # Fazer uma Requisição para Pegar as Informações da Equipe
        link = f'https://aplicativovendashashtag-b0ed3-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"&equalTo="{id_vendedor}"'
        requisicao = requests.get(link)
        requisicao_dic = requisicao.json()
        valor = list(requisicao_dic.values())[0]
        avatar = valor["avatar"]
        total_vendas = valor["total_vendas"]

        meu_app = App.get_running_app()

        # Separar o Banner em 3 Partes
        imagem = ImageButton(source=f"icones/fotos_perfil/{avatar}",
                             pos_hint={"right":0.4, "top": 0.9}, size_hint=(0.3, 0.8),
                             on_release=partial(meu_app.carregar_vendas_vendedor, valor))
        label_id = LabelButton(text=f"ID Vendedor: {id_vendedor}",
                               pos_hint={"right":0.9, "top": 0.9}, size_hint=(0.5, 0.5),
                               on_release=partial(meu_app.carregar_vendas_vendedor, valor))
        label_total = LabelButton(text=f"Total de Vendas: R${total_vendas}",
                                  pos_hint={"right":0.9, "top": 0.6}, size_hint=(0.5, 0.5),
                                  on_release=partial(meu_app.carregar_vendas_vendedor, valor))

        # Adicionar as 3 Partes do Banner
        self.add_widget(imagem)
        self.add_widget(label_id)
        self.add_widget(label_total)

    # Função para Atualizar o Tamanho do Retângulo de acordo com o Tamanho do Banner
    def atualizar_rec(self, *args):
        self.rec.pos = self.pos
        self.rec.size = self.size