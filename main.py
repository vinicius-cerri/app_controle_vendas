# Importar Bibliotecas
from kivy.app import App
from kivy.lang import Builder # Vai Conectar o main.kv com main.py
from telas import *
from botoes import *
import requests
from banner_venda import BannerVenda
from banner_vendedor import BannerVendedor
import os
from functools import partial # Passar uma Informação para uma Função que está sendo usada com Parâmetro
from myfirebase import MyFirebase
from datetime import date

# Interface Gráfica
GUI = Builder.load_file('main.kv')

# Criar a Classe Principal
class MainApp(App):
    cliente = None
    produto = None
    unidade = None

    # Função para Criar o App
    def build(self):
        self.firebase = MyFirebase()
        return GUI
    
    # Função que será Executada ao Iniciar o Aplicativo
    def on_start(self):
        # Carregar as Fotos de Perfil
        arquivos = os.listdir('icones/fotos_perfil')
        pagina_foto_perfil = self.root.ids['foto_perfilpage'] # self.root: Faz referência ao Arquivo main.kv
        lista_fotos = pagina_foto_perfil.ids['lista_fotos_perfil']
        for foto in arquivos:
            imagem = ImageButton(source=f'icones/fotos_perfil/{foto}', on_release=partial(self.mudar_foto_perfil, foto))
            lista_fotos.add_widget(imagem)

        # Carregar Fotos dos Clientes
        arquivos = os.listdir("icones/fotos_clientes")
        pagina_adicionar_vendas = self.root.ids["adicionar_vendaspage"]
        lista_clientes = pagina_adicionar_vendas.ids["lista_clientes"]
        for foto_cliente in arquivos:
            imagem = ImageButton(source=f"icones/fotos_clientes/{foto_cliente}",
                                 on_release=partial(self.selecionar_cliente, foto_cliente))
            label = LabelButton(text=foto_cliente.replace(".png", "").capitalize(),
                                on_release=partial(self.selecionar_cliente, foto_cliente))
            lista_clientes.add_widget(imagem)
            lista_clientes.add_widget(label)

        # Carregar Fotos dos Produtos
        arquivos = os.listdir("icones/fotos_produtos")
        pagina_adicionar_vendas = self.root.ids["adicionar_vendaspage"]
        lista_produtos = pagina_adicionar_vendas.ids["lista_produtos"]
        for foto_produto in arquivos:
            imagem = ImageButton(source=f"icones/fotos_produtos/{foto_produto}",
                                 on_release=partial(self.selecionar_produto, foto_produto))
            label = LabelButton(text=foto_produto.replace(".png", "").capitalize(),
                                on_release=partial(self.selecionar_produto, foto_produto))
            lista_produtos.add_widget(imagem)
            lista_produtos.add_widget(label)

        # Carregar a Data
        pagina_adicionar_vendas = self.root.ids["adicionar_vendaspage"]
        label_data = pagina_adicionar_vendas.ids["label_data"]
        label_data.text = f"Data: {date.today().strftime('%d/%m/%Y')}"

        # Rodar a Função para Carregar as Informações do Usuário
        self.carregar_infos_usuario()
        
    # Função para Carregar as Informações do Usuário
    def carregar_infos_usuario(self):
        try:
            # Ler as Informações do Arquivo refreshtoken.txt
            with open('refreshtoken.txt', 'r') as arquivo:
                refresh_token = arquivo.read()

            # Fazer a Autenticação do Usuário
            local_id, id_token = self.firebase.trocar_token(refresh_token)
            self.local_id = local_id
            self.id_token = id_token

            # Puxar as Informações do Usuário que está Logado
            link = f"https://aplicativovendashashtag-b0ed3-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}"
            requisicao = requests.get(link)
            requisicao_dic = requisicao.json()

            # Exibir a Foto de Perfil do Usuário que está Logado
            avatar = requisicao_dic['avatar']
            self.avatar = avatar
            foto_perfil = self.root.ids['foto_perfil']
            foto_perfil.source = f'icones/fotos_perfil/{avatar}'

            # Preencher o ID do Vendedor
            id_vendedor = requisicao_dic['id_vendedor']
            self.id_vendedor = id_vendedor
            pagina_ajustes = self.root.ids['ajustespage']
            pagina_ajustes.ids['id_vendedor'].text = f'Seu ID Único: {id_vendedor}'

            # Preencher o Total de Vendas
            total_vendas = requisicao_dic['total_vendas']
            self.total_vendas = total_vendas
            homepage = self.root.ids['homepage']
            homepage.ids['label_total_vendas'].text = f'[color=#000000]Total de Vendas:[/color] [b]R${total_vendas}[/b]'

           # Preencher Equipe
            self.equipe = requisicao_dic["equipe"]

            # Preencher a Lista de Vendas do Usuário
            try:
                vendas = requisicao_dic['vendas']
                self.vendas = vendas
                pagina_homepage = self.root.ids['homepage']
                lista_vendas = pagina_homepage.ids['lista_vendas']
                for id_venda in vendas:
                    venda = vendas[id_venda]
                    banner = BannerVenda(cliente=venda['cliente'], foto_cliente=venda['foto_cliente'],
                                        produto=venda['produto'], foto_produto=venda['foto_produto'], 
                                        data=venda['data'], preco=venda['preco'],
                                        unidade=venda['unidade'], quantidade=venda['quantidade'])
                    lista_vendas.add_widget(banner)
            except Exception as excecao:
                print(excecao)

            # Preencher a Equipe de Vendedores
            equipe = requisicao_dic["equipe"]
            lista_equipe = equipe.split(",")
            pagina_lista_vendedores = self.root.ids["listar_vendedorespage"]
            lista_vendedores = pagina_lista_vendedores.ids["lista_vendedores"]

            for id_vendedor_equipe in lista_equipe:
                if id_vendedor_equipe != "":
                    banner_vendedor = BannerVendedor(id_vendedor=id_vendedor_equipe)
                    lista_vendedores.add_widget(banner_vendedor)

            # Levar o Usuário para a HomePage
            self.mudar_tela('homepage')
        except:
            pass
        
    # Função para Mudar de Tela
    def mudar_tela(self, id_tela):
        gerenciador_telas = self.root.ids['screen_manager']
        gerenciador_telas.current = id_tela

    # Função para Mudar a Foto de Perfil
    def mudar_foto_perfil(self, foto, *args):
        # Alterar Foto de Perfil no App
        foto_perfil = self.root.ids['foto_perfil']
        foto_perfil.source = rf'icones/fotos_perfil/{foto}'

        # Alterar Foto de Perfil no Banco de Dados
        link = f"https://aplicativovendashashtag-b0ed3-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}"
        info = f'{{"avatar": "{foto}"}}'
        requests.patch(link, data=info)
        # Levar o Usuário para a AjustesPage
        self.mudar_tela('ajustespage')
    
    # Função para Adicionar Vendedor
    def adicionar_vendedor(self, id_vendedor_adicionado):
        # Puxar as Informações do Vendedor a ser Adicionado
        link = f'https://aplicativovendashashtag-b0ed3-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"&equalTo="{id_vendedor_adicionado}"'
        requisicao = requests.get(link)
        requisicao_dic = requisicao.json()

        pagina_adicionar_vendedor = self.root.ids["adicionar_vendedorpage"]
        mensagem_texto = pagina_adicionar_vendedor.ids["mensagem_outro_vendedor"]

        # Verificar se o Vendedor foi Encontrado
        if requisicao_dic == {}:
            mensagem_texto.text = "Usuário Não Encontrado"
        else:
            equipe = self.equipe.split(",")

            # Verificar se o Vendedor já faz parte da Equipe
            if id_vendedor_adicionado in equipe:
                mensagem_texto.text = "Vendedor já faz parte da Equipe"

            else:
                # Adicionar o Vendedor na Equipe
                self.equipe = self.equipe + f",{id_vendedor_adicionado}"
                link = f"https://aplicativovendashashtag-b0ed3-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}"
                info = f'{{"equipe": "{self.equipe}"}}'
                requests.patch(link, data=info)
                mensagem_texto.text = "Vendedor Adicionado com Sucesso"

                # Adicionar um Novo Banner na Lista de Vendedores
                pagina_lista_vendedores = self.root.ids["listar_vendedorespage"]
                lista_vendedores = pagina_lista_vendedores.ids["lista_vendedores"]
                banner_vendedor = BannerVendedor(id_vendedor=id_vendedor_adicionado)
                lista_vendedores.add_widget(banner_vendedor)

    # Função para Marcar o Cliente Selecionado
    def selecionar_cliente(self, foto, *args):
        self.cliente = foto.replace(".png", "")

        # Pintar de Branco Todos os Clientes
        pagina_adicionar_vendas = self.root.ids["adicionar_vendaspage"]
        lista_clientes = pagina_adicionar_vendas.ids["lista_clientes"]

        # Percorrer Todos os Clientes do GridLayout
        for item in list(lista_clientes.children):
            item.color = (1, 1, 1, 1)
            # Pintar de Azul o Cliente Selecionado
            try:
                texto = item.text
                texto = texto.lower() + ".png"
                if foto == texto:
                    item.color = (0, 207/255, 219/255, 1)
            except:
                pass
    
    # Função para Marcar o Produto Selecionado
    def selecionar_produto(self, foto, *args):
        self.produto = foto.replace(".png", "")
        
        # Pintar de Branco Todos os Produtos
        pagina_adicionar_vendas = self.root.ids["adicionar_vendaspage"]
        lista_produtos = pagina_adicionar_vendas.ids["lista_produtos"]

        # Percorrer Todos os Produtos do GridLayout
        for item in list(lista_produtos.children):
            item.color = (1, 1, 1, 1)
            # Pintar de Azul o Produto Selecionado
            try:
                texto = item.text
                texto = texto.lower() + ".png"
                if foto == texto:
                    item.color = (0, 207/255, 219/255, 1)
            except:
                pass

    # Função para Marcar a Unidade Selecionada
    def selecionar_unidade(self, id_label, *args):
        pagina_adicionar_vendas = self.root.ids["adicionar_vendaspage"]
        self.unidade = id_label.replace("unidades_", "")

        # Pintar de Branco Todos as Unidades
        pagina_adicionar_vendas.ids["unidades_kg"].color = (1, 1, 1, 1)
        pagina_adicionar_vendas.ids["unidades_unidades"].color = (1, 1, 1, 1)
        pagina_adicionar_vendas.ids["unidades_litros"].color = (1, 1, 1, 1)

        # Pintar de Azul a Unidade Selecionada
        pagina_adicionar_vendas.ids[id_label].color = (0, 207/255, 219/255, 1)

    # Função para Adicionar a Venda com as Informações Fornecidas pelo Usuário
    def adicionar_venda(self):
        # Extrair as Informações da Venda
        cliente = self.cliente
        produto = self.produto
        unidade = self.unidade

        pagina_adicionar_vendas = self.root.ids["adicionar_vendaspage"]
        data = pagina_adicionar_vendas.ids["label_data"].text.replace("Data: ", "")
        preco = pagina_adicionar_vendas.ids["preco_total"].text
        quantidade = pagina_adicionar_vendas.ids["quantidade"].text

        # Pintar de Vermelho os Campos Não Selecionados
        if not cliente:
            pagina_adicionar_vendas.ids["label_selecione_cliente"].color = (1, 0, 0, 1)

        if not produto:
            pagina_adicionar_vendas.ids["label_selecione_produto"].color = (1, 0, 0, 1)

        if not unidade:
            pagina_adicionar_vendas.ids["unidades_kg"].color = (1, 0, 0, 1)
            pagina_adicionar_vendas.ids["unidades_unidades"].color = (1, 0, 0, 1)
            pagina_adicionar_vendas.ids["unidades_litros"].color = (1, 0, 0, 1)

        if not preco:
            pagina_adicionar_vendas.ids["label_preco"].color = (1, 0, 0, 1)
        else:
            try:
                preco = float(preco)
            except:
                pagina_adicionar_vendas.ids["label_preco"].color = (1, 0, 0, 1)

        if not quantidade:
            pagina_adicionar_vendas.ids["label_quantidade"].color = (1, 0, 0, 1)
        else:
            try:
                quantidade = float(quantidade)
            except:
                pagina_adicionar_vendas.ids["label_quantidade"].color = (1, 0, 0, 1)

        # Verificar se o Usuário Forneceu Todas as Informações da Venda
        if cliente and produto and unidade and preco and quantidade and (type(preco) == float) and (type(quantidade)==float):
            # Pegar as Fotos
            foto_produto = produto + ".png"
            foto_cliente = cliente + ".png"

            # Requisição para Adicionar as Informações da Venda
            link = f"https://aplicativovendashashtag-b0ed3-default-rtdb.firebaseio.com/{self.local_id}/vendas.json?auth={self.id_token}"
            info = f'{{"cliente": "{cliente}", "produto": "{produto}", "foto_cliente": "{foto_cliente}", ' \
                   f'"foto_produto": "{foto_produto}", "data": "{data}", "unidade": "{unidade}", ' \
                   f'"preco": "{preco}", "quantidade": "{quantidade}"}}'
            requests.post(link, data=info)

            # Adicionar um Novo Banner na Lista de Vendas
            banner = BannerVenda(cliente=cliente, produto=produto, foto_cliente=foto_cliente, foto_produto=foto_produto,
                                 data=data, preco=preco, quantidade=quantidade, unidade=unidade)
            pagina_homepage = self.root.ids["homepage"]
            lista_vendas = pagina_homepage.ids["lista_vendas"]
            lista_vendas.add_widget(banner)

            # Requisição para Extrair o Preço da Venda
            link = f"https://aplicativovendashashtag-b0ed3-default-rtdb.firebaseio.com/{self.local_id}/total_vendas.json?auth={self.id_token}"
            requisicao = requests.get(link)
            total_vendas = float(requisicao.json())
            total_vendas += preco
            
            # Requisição para Atualizar o Total Vendas
            link = f"https://aplicativovendashashtag-b0ed3-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}"
            info = f'{{"total_vendas": "{total_vendas}"}}'
            requests.patch(link, data=info)
            homepage = self.root.ids["homepage"]
            homepage.ids["label_total_vendas"].text = f"[color=#000000]Total de Vendas:[/color] [b]R${total_vendas}[/b]"
            
            # Levar o Usuário para a HomePage
            self.mudar_tela("homepage")

        # Resetar as Variáveis
        self.cliente = None
        self.produto = None
        self.unidade = None

    # Função para Carregar as Informações de Todas as Vendas
    def carregar_todas_vendas(self):
        pagina_todas_vendas = self.root.ids["todas_vendaspage"]
        lista_vendas = pagina_todas_vendas.ids["lista_vendas"]

        # Limpar a Lista de Vendas (Para Não Ficar com Vendas Repetidas)
        for item in list(lista_vendas.children):
            lista_vendas.remove_widget(item)

        # Pegar Informações da Empresa
        link = f'https://aplicativovendashashtag-b0ed3-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"'
        requisicao = requests.get(link)
        requisicao_dic = requisicao.json()

        # Preencher Foto da Empresa
        foto_perfil = self.root.ids["foto_perfil"]
        foto_perfil.source = f"icones/fotos_perfil/hash.png"

        # Adicionar um Novo Banner na Lista Todas as Vendas
        total_vendas = 0
        for local_id_usuario in requisicao_dic:
            try:
                vendas = requisicao_dic[local_id_usuario]["vendas"]
                for id_venda in vendas:
                    venda = vendas[id_venda]
                    total_vendas += float(venda["preco"])
                    banner = BannerVenda(cliente=venda["cliente"], produto=venda["produto"], foto_cliente=venda["foto_cliente"],
                                         foto_produto=venda["foto_produto"], data=venda["data"],
                                         preco=venda["preco"], quantidade=venda["quantidade"], unidade=venda["unidade"])
                    lista_vendas.add_widget(banner)
            except:
                pass

        # Preencher o Total de Vendas
        pagina_todas_vendas.ids["label_total_vendas"].text = f"[color=#000000]Total de Vendas:[/color] [b]R${total_vendas}[/b]"

        # Levar o Usuário para a TodasVendasPage
        self.mudar_tela("todas_vendaspage")

    # Função para Sair da Tela de Vendas sem Modificar a Foto de Perfil
    def sair_todas_vendas(self, id_tela):
        # Voltar com Foto de Perfil do Usuário
        foto_perfil = self.root.ids["foto_perfil"]
        foto_perfil.source = f"icones/fotos_perfil/{self.avatar}"

        # Levar o Usuário para a Tela Passada como Parâmetro
        self.mudar_tela(id_tela)

    # Função para Carregar a Vendas do Vendedor Selecionado
    def carregar_vendas_vendedor(self, dic_info_vendedor, *args):
        try:
            vendas = dic_info_vendedor["vendas"]
            pagina_vendas_outro_vendedor = self.root.ids["vendas_outro_vendedorpage"]
            lista_vendas = pagina_vendas_outro_vendedor.ids["lista_vendas"]
            
            # Limpar a Lista de Vendas
            for item in list(lista_vendas.children):
                lista_vendas.remove_widget(item)

            for id_venda in vendas:
                venda = vendas[id_venda]
                banner = BannerVenda(cliente=venda["cliente"], produto=venda["produto"], foto_cliente=venda["foto_cliente"],
                                     foto_produto=venda["foto_produto"], data=venda["data"],
                                     preco=venda["preco"], quantidade=venda["quantidade"], unidade=venda["unidade"])
                lista_vendas.add_widget(banner)
        except:
            pass

        # Preencher o Total de Vendas
        total_vendas = dic_info_vendedor["total_vendas"]
        pagina_vendas_outro_vendedor.ids["label_total_vendas"].text = f"[color=#000000]Total de Vendas:[/color] [b]R${total_vendas}[/b]"

        # Preencher Foto de Perfil com o Vendedor Selecionado
        foto_perfil = self.root.ids["foto_perfil"]
        avatar = dic_info_vendedor["avatar"]
        foto_perfil.source = f"icones/fotos_perfil/{avatar}"

        # Levar o Usuário para a VendasOutroVendedorPage
        self.mudar_tela("vendas_outro_vendedorpage")


# Rodar o App
if __name__ == '__main__':
    MainApp().run()