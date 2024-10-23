from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.Uniform import Uniform
from OpenGL.GL import *
import numpy as np

class Test(Base):
    def initialize(self):
        print("Inicializando o programa...")

        # Tamanho da janela
        width, height = 600, 400
        self.init_pygame(width, height)

        glClearColor(0.1, 0.1, 0.1, 1.0)  # Cor de fundo: cinza escuro

        # Shaders com interpolação de cor
        vsCode = """
        #version 330 core
        in vec3 position;
        in vec3 vertexColor;
        out vec3 color;
        uniform vec3 translation;
        void main()
        {
            vec3 pos = position + translation;
            gl_Position = vec4(pos, 1.0);
            color = vertexColor;
        }
        """
        fsCode = """
        #version 330 core
        in vec3 color;
        out vec4 fragColor;
        void main()
        {
            fragColor = vec4(color, 1.0);
        }
        """

        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)
        if self.programRef is None:
            print("Falha na inicialização do programa!")
            return

        print("Programa inicializado com sucesso.")

        # Dados do quadrado
        self.squareData = np.array([
            [-0.2, 0.2, 0.0], [1.0, 0.0, 0.0],  # Vértice 1, vermelho
            [0.2, 0.2, 0.0], [0.0, 1.0, 0.0],   # Vértice 2, verde
            [-0.2, -0.2, 0.0], [0.0, 0.0, 1.0], # Vértice 3, azul
            [0.2, -0.2, 0.0], [1.0, 1.0, 0.0],  # Vértice 4, amarelo
        ], dtype='float32')

        # Configura o VAO para o quadrado
        self.vao_square = self.setup_vao(self.squareData)

        # Uniform para controlar a posição
        self.translation = Uniform("vec3", [0.0, 0.6, 0.0])  # Posição inicial (acima)
        self.translation.locateVariable(self.programRef, "translation")

        # Velocidade e limites de movimento
        self.speed = 0.01
        self.bottom_limit = -1.0 - 0.2  # Ajustar para altura do quadrado
        self.top_limit = 1.0

    def setup_vao(self, data):
        vaoRef = glGenVertexArrays(1)
        glBindVertexArray(vaoRef)

        vboRef = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vboRef)
        glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)

        positionAttribLocation = glGetAttribLocation(self.programRef, "position")
        glVertexAttribPointer(positionAttribLocation, 3, GL_FLOAT, GL_FALSE, 6 * data.itemsize, None)
        glEnableVertexAttribArray(positionAttribLocation)

        colorAttribLocation = glGetAttribLocation(self.programRef, "vertexColor")
        glVertexAttribPointer(colorAttribLocation, 3, GL_FLOAT, GL_FALSE, 6 * data.itemsize, ctypes.c_void_p(3 * data.itemsize))
        glEnableVertexAttribArray(colorAttribLocation)

        return vaoRef

    def draw_square(self):
        self.translation.uploadData()  # Atualiza a posição do quadrado
        glBindVertexArray(self.vao_square)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

    def update(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(self.programRef)

        # Atualiza a posição vertical (descida contínua)
        self.translation.data[1] -= self.speed
        # Ajustar para que a parte inferior do quadrado tenha um limite inferior
        if self.translation.data[1] < self.bottom_limit:
            self.translation.data[1] = self.top_limit

        # Desenha o quadrado
        self.draw_square()

        self.input.update()
        if self.input.quit:
            print("Fechando a aplicação...")
            self.running = False

    def init_pygame(self, width, height):
        import pygame
        pygame.init()
        pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
        pygame.display.set_caption("Teste OpenGL - Quadrado")

if __name__ == "__main__":
    try:
        Test().run()
    except KeyboardInterrupt:
        print("Execução interrompida.")