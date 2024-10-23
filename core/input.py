import pygame


class Input(object):
    def __init__(self):
        # Indica se o usuário encerrou a aplicação
        self.quit = False

    def update(self):
        # Itera sobre todos os eventos de entrada do usuário (como teclado ou mouse)
        for event in pygame.event.get():
            # Evento de saída ocorre ao clicar no botão para fechar a janela
            if event.type == pygame.QUIT:
                self.quit = True
