from core.base import Base
from core.OpenGLUtils import OpenGLUtils
from core.Attribute import Attribute
from OpenGL.GL import *
import numpy as np  # Importar numpy para manipulação de arrays


class Test(Base):
    def initialize(self):
        print("Initializing program...")

        # Código do Vertex Shader
        vsCode = """
        in vec3 position;
        in vec3 vertexColor;
        out vec3 color;
        void main()
        {
            gl_Position = vec4(position.x, position.y, position.z, 1.0);
            color = vertexColor;
        }
        """

        # Código do Fragment Shader
        fsCode = """
        in vec3 color;
        out vec4 fragColor;
        void main()
        {
            fragColor = vec4(color.r, color.g, color.b, 1.0);
        }
        """

        # Inicializar o programa de shaders
        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)

        ### Configurações de renderização (opcional) ###
        glPointSize(10)
        glLineWidth(4)

        ### Configuração do Vertex Array Object (VAO) ###
        vaoRef = glGenVertexArrays(1)
        glBindVertexArray(vaoRef)

        ### Dados dos Vértices e Atributos ###
        positionData = np.array([
            [-0.5, 0.5, 0.0],  # Top-left vertex
            [0.5, 0.5, 0.0],   # Top-right vertex
            [-0.5, -0.5, 0.0], # Bottom-left vertex
            [0.5, -0.5, 0.0]   # Bottom-right vertex
        ], dtype=np.float32)

        colorData = np.array([
            [1.0, 0.0, 0.0],  # Red
            [0.0, 1.0, 0.0],  # Green
            [0.0, 0.0, 1.0],  # Blue
            [1.0, 1.0, 0.0]   # Yellow
        ], dtype=np.float32)

        # Atributo de posição
        positionAttribute = Attribute("vec3", positionData)
        positionAttribute.associateVariable(self.programRef, "position")

        # Atributo de cor
        colorAttribute = Attribute("vec3", colorData)
        colorAttribute.associateVariable(self.programRef, "vertexColor")

        # Gerar e associar o buffer de vértices (VBO)
        self.vertexCount = len(positionData)
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)

        # Concatenar os dados de posição e cor em um único array
        vertexData = np.hstack([positionData, colorData])  # Concatenando os arrays
        glBufferData(GL_ARRAY_BUFFER, vertexData.nbytes, vertexData, GL_STATIC_DRAW)

        # Configurar ponteiros de atributo
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * positionData.itemsize, None)
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * positionData.itemsize,
                              ctypes.c_void_p(3 * positionData.itemsize))
        glEnableVertexAttribArray(1)

        # Desvincular buffer e VAO
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def update(self):
        # Usar o programa de shaders
        glUseProgram(self.programRef)
        glBindVertexArray(1)  # Certifique-se de que o VAO correto está vinculado

        # Desenhar os vértices como dois triângulos que formam um quadrado
        glDrawArrays(GL_TRIANGLE_STRIP, 0, self.vertexCount)

        # Desvincular o VAO
        glBindVertexArray(0)

        # Atualizar o estado da entrada do usuário
        self.input.update()

        # Verifica se o usuário fechou a aplicação
        if self.input.quit:
            self.running = False


# Instanciando a classe e rodando o programa
Test().run()
