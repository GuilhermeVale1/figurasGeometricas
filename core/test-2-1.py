from core.base import Base

class Test(Base):
    def initialize(self):
        print("Inicializando programa...")

    def update(self):
        self.input.update()
        # Verifica se o usuário fechou a aplicação
        if self.input.quit:
            self.running = False

# Inicia e executa o programa
Test().run()