import glfw
from OpenGL.GL import *

# Inicializar GLFW
if not glfw.init():
    raise Exception("GLFW não pôde ser inicializado")

# Criar uma janela com o contexto OpenGL
window = glfw.create_window(800, 600, "OpenGL Window", None, None)

# Verificar se a janela foi criada corretamente
if not window:
    glfw.terminate()
    raise Exception("Falha ao criar a janela GLFW")

# Tornar o contexto da janela atual
glfw.make_context_current(window)

# Agora podemos chamar funções OpenGL
print("Versão do OpenGL:", glGetString(GL_VERSION))

# Rodar o loop principal
while not glfw.window_should_close(window):
    glClear(GL_COLOR_BUFFER_BIT)

    # Atualizar a tela
    glfw.swap_buffers(window)

    # Verificar se há eventos
    glfw.poll_events()

# Finalizar o GLFW
glfw.terminate()
