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

        # Dados do pentágono (vértices e cores)
        angle = np.linspace(0, 2*np.pi, 6)[:-1]  # Ângulos dos vértices do pentágono
        self.pentagonData = []
        for i in range(5):
            x, y = 0.3 * np.cos(angle[i]), 0.3 * np.sin(angle[i])
            color = [i/5, 1-i/5, (i/5)**2]  # Cores diferentes para interpolação
            self.pentagonData.extend([x, y, 0.0] + color)
        self.pentagonData = np.array(self.pentagonData, dtype='float32')

        # Configura o VAO para o pentágono
        self.vao_pentagon = self.setup_vao(self.pentagonData)

        # Uniform para controlar a posição
        self.translation = Uniform("vec3", [0.0, 0.6, 0.0])  # Posição inicial (acima)
        self.translation.locateVariable(self.programRef, "translation")

        # Velocidade e limites de movimento
        self.speed = 0.01
        self.bottom_limit = -1.0 - 0.3  # Ajuste para altura do pentágono
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

    def draw_pentagon(self):
        self.translation.uploadData()  # Atualiza a posição do pentágono
        glBindVertexArray(self.vao_pentagon)
        glDrawArrays(GL_TRIANGLE_FAN, 0, 5)

    def update(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(self.programRef)

        # Atualiza a posição vertical (descida contínua)
        self.translation.data[1] -= self.speed
        # Ajustar para que a parte inferior do pentágono tenha um limite inferior
        if self.translation.data[1] < self.bottom_limit:
            self.translation.data[1] = self.top_limit

        # Desenha o pentágono
        self.draw_pentagon()

        self.input.update()
        if self.input.quit:
            print("Fechando a aplicação...")
            self.running = False

    def init_pygame(self, width, height):
        import pygame
        pygame.init()
        pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
        pygame.display.set_caption("Teste OpenGL - Pentágono")

if __name__ == "__main__":
    try:
        Test().run()
    except KeyboardInterrupt:
        print("Execução interrompida.")
