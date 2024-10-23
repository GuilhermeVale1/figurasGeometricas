import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import numpy as np
import math

# Shader de vértice
vertex_shader = """
#version 330 core
layout(location = 0) in vec3 position;
void main()
{
    gl_Position = vec4(position.x, position.y, position.z, 1.0);
}
"""

# Shader de fragmento (cor verde por padrão)
fragment_shader_green = """
#version 330 core
out vec4 fragColor;
void main()
{
    fragColor = vec4(0.0, 0.5, 0.0, 1.0);  // Cor verde (RGB)
}
"""

# Shader de fragmento (cor amarela)
fragment_shader_yellow = """
#version 330 core
out vec4 fragColor;
void main()
{
    fragColor = vec4(1.0, 1.0, 0.0, 1.0);  // Cor amarela (RGB)
}
"""

# Shader de fragmento (cor azul)
fragment_shader_blue = """
#version 330 core
out vec4 fragColor;
void main()
{
    fragColor = vec4(0.0, 0.0, 1.0, 1.0);  // Cor azul (RGB)
}
"""

# Inicialização do contexto GLFW
if not glfw.init():
    raise Exception("GLFW não pôde ser inicializado!")

# Criar uma janela OpenGL
window = glfw.create_window(800, 600, "Bandeira do Brasil", None, None)
if not window:
    glfw.terminate()
    raise Exception("A janela GLFW não pôde ser criada!")

glfw.make_context_current(window)

# Função para criar shaders
def create_shader_program(vertex_shader, fragment_shader):
    vertex_shader_ref = compileShader(vertex_shader, GL_VERTEX_SHADER)
    fragment_shader_ref = compileShader(fragment_shader, GL_FRAGMENT_SHADER)
    program = compileProgram(vertex_shader_ref, fragment_shader_ref)
    return program

# Programas de shader para as diferentes cores
program_green = create_shader_program(vertex_shader, fragment_shader_green)
program_yellow = create_shader_program(vertex_shader, fragment_shader_yellow)
program_blue = create_shader_program(vertex_shader, fragment_shader_blue)

# Definindo os pontos para o retângulo verde (bandeira)
vertices_green = np.array([
    [-1.0,  0.6, 0.0],   # Superior esquerdo
    [-1.0, -0.6, 0.0],   # Inferior esquerdo
    [ 1.0, -0.6, 0.0],   # Inferior direito
    [ 1.0,  0.6, 0.0]    # Superior direito
], dtype=np.float32)

# Definindo os pontos para o losango amarelo
vertices_yellow = np.array([
    [ 0.0,  0.55, 0.0],  # Superior
    [-0.75,  0.0, 0.0],  # Esquerdo
    [ 0.0, -0.55, 0.0],  # Inferior
    [ 0.75,  0.0, 0.0]   # Direito
], dtype=np.float32)

# Definindo os pontos para o círculo azul
num_segments = 100
theta = np.linspace(0, 2 * np.pi, num_segments)
circle_vertices = np.array([[0.3 * math.cos(t), 0.3 * math.sin(t), 0.0] for t in theta], dtype=np.float32)

# Função para configurar buffers
def setup_buffer(vertices):
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    position_location = glGetAttribLocation(program_green, "position")
    glVertexAttribPointer(position_location, 3, GL_FLOAT, GL_FALSE, 3 * vertices.itemsize, None)
    glEnableVertexAttribArray(position_location)
    return vao

# Criar os buffers para os diferentes elementos
vao_green = setup_buffer(vertices_green)
vao_yellow = setup_buffer(vertices_yellow)
vao_blue = setup_buffer(circle_vertices)

# Loop de renderização
while not glfw.window_should_close(window):
    glClear(GL_COLOR_BUFFER_BIT)

    # Desenhar o retângulo verde
    glUseProgram(program_green)
    glBindVertexArray(vao_green)
    glDrawArrays(GL_QUADS, 0, len(vertices_green))

    # Desenhar o losango amarelo
    glUseProgram(program_yellow)
    glBindVertexArray(vao_yellow)
    glDrawArrays(GL_TRIANGLE_FAN, 0, len(vertices_yellow))

    # Desenhar o círculo azul
    glUseProgram(program_blue)
    glBindVertexArray(vao_blue)
    glDrawArrays(GL_TRIANGLE_FAN, 0, len(circle_vertices))

    # Trocar os buffers e verificar eventos
    glfw.swap_buffers(window)
    glfw.poll_events()

# Limpeza
glDeleteBuffers(1, [vao_green, vao_yellow, vao_blue])

# Encerrar GLFW
glfw.terminate()
