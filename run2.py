import pygame
import sys
from core.base import Base
from core.input import Input

class MyApplication(Base):
    def initialize(self):
        # Inicializa o processamento de entrada
       # self.input = Input()
        self.input.update()
        print("Janela fechada!")
        if self.input.quit:
            self.running = False

    def update(self):
        # Atualiza o estado dos inputs
        self.input.update()
        # Verifica se o usuário fechou a aplicação
        if self.input.quit:
            self.running = False

# Cria uma instância da aplicação e executa
if __name__ == "__main__":
    app = MyApplication()
    app.run()
