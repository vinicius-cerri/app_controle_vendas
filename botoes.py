# Importar Bibliotecas
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import ButtonBehavior

# Criar a Classe para a Imagem do Botão
class ImageButton(ButtonBehavior, Image): # ButtonBehavior tem que vir na frente
    pass

# Criar a Classe para o Texto do Botão
class LabelButton(ButtonBehavior, Label):
    pass