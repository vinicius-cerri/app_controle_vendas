# Importar Biblioteca
import requests
from kivy.app import App

# Criar a Classe para usar o Google REST API
class MyFirebase():
    API_KEY = 'AIzaSyBrWeYrKbCDNNUVAFu2NHPcpxUxcTdZ4fE'

    # Função para Criar a Conta do Usuário
    def criar_conta(self, email, senha):
        link = f'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.API_KEY}'
        info = {"email": email, "password": senha, "returnSecureToken": True}
        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()

        # Verificar se a Requisição deu Certo
        if requisicao.ok:

            # Salvar as Informações da Requisição
            refresh_token = requisicao_dic['refreshToken']
            local_id = requisicao_dic['localId']
            id_token = requisicao_dic['idToken']
            meu_app = App.get_running_app()
            meu_app.local_id = local_id
            meu_app.id_token = id_token

            # Salvar o RefreshToken do Usuário em um Arquivo .txt
            with open('refreshtoken.txt', 'w') as arquivo:
                arquivo.write(refresh_token)

            # Descobrir o Próximo ID de Usuário
            link = f"https://aplicativovendashash-default-rtdb.firebaseio.com/proximo_id_vendedor.json?auth={id_token}"
            requisicao_id = requests.get(link)
            id_vendedor = requisicao_id.json()
            # id_vendedor = int(requisicao_id.json())

            # Criar Usuário no Banco de Dados
            link = f"https://aplicativovendashash-default-rtdb.firebaseio.com/{local_id}.json?auth={id_token}"
            info_usuario = f'{{"avatar": "foto1.png", "equipe": "", "total_vendas": "0", "vendas": "", "id_vendedor": "{id_vendedor}"}}'
            requests.patch(link, data=info_usuario)

            # Atualizar o Valor do Próximo ID de Usuário
            link = f"https://aplicativovendashash-default-rtdb.firebaseio.com/.json?auth={id_token}"
            proximo_id = int(id_vendedor) + 1
            info_id = f'{{"proximo_id_vendedor": "{proximo_id}"}}'
            requests.patch(link, data=info_id)


            # Carregar as Informações do Usuário para o App
            meu_app.carregar_infos_usuario()

            # Ir para a HomePage
            meu_app.mudar_tela('homepage')

        else:
            # Retornar a Mensagem de Erro
            mensagem_erro = requisicao_dic['error']['message']
            meu_app = App.get_running_app()
            pagina_login = meu_app.root.ids['loginpage']
            pagina_login.ids['mensagem_login'].text = mensagem_erro
            pagina_login.ids['mensagem_login'].color = (1, 0, 0, 1)


    # Função para Fazer Login
    def fazer_login(self, email, senha):
        link = f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.API_KEY}'
        info = {"email": email, "password": senha, "returnSecureToken": True}
        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()

        # Verificar se a Requisição deu Certo
        if requisicao.ok:

            # Salvar as Informações da Requisição
            refresh_token = requisicao_dic['refreshToken']
            local_id = requisicao_dic['localId']
            id_token = requisicao_dic['idToken']
            meu_app = App.get_running_app()
            meu_app.local_id = local_id
            meu_app.id_token = id_token

            # Salvar o RefreshToken do Usuário em um Arquivo .txt
            with open('refreshtoken.txt', 'w') as arquivo:
                arquivo.write(refresh_token)

            # Carregar as Informações do Usuário para o App
            meu_app.carregar_infos_usuario()

            # Ir para a HomePage
            meu_app.mudar_tela('homepage')

        else:
            # Retornar a Mensagem de Erro
            mensagem_erro = requisicao_dic['error']['message']
            meu_app = App.get_running_app()
            pagina_login = meu_app.root.ids['loginpage']
            pagina_login.ids['mensagem_login'].text = mensagem_erro
            pagina_login.ids['mensagem_login'].color = (1, 0, 0, 1)

    # Função para Fazer a Autenticação do Usuário
    def trocar_token(self, refresh_token):
        link = f'https://securetoken.googleapis.com/v1/token?key={self.API_KEY}'
        info = {"grant_type": "refresh_token", "refresh_token": refresh_token}
        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()
        local_id = requisicao_dic['user_id']
        id_token = requisicao_dic['id_token']
        return local_id, id_token