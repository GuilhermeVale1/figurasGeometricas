import OpenGL.GL as gl
import OpenGL.GL.shaders
import pygame
import numpy as np

# Initialize Pygame and OpenGL
pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)

# Vertex Shader code
vertex_shader_code = """
#version 330
void main() {
    gl_Position = vec4(0.0, 0.0, 0.0, 1.0);
}
"""

# Fragment Shader code
fragment_shader_code = """
#version 330
out vec4 color;
void main() {
    color = vec4(1.0, 1.0, 0.0, 1.0);
}
"""

# Compile shaders
shader_program = gl.glCreateProgram()
vertex_shader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
gl.glShaderSource(vertex_shader, vertex_shader_code)
gl.glCompileShader(vertex_shader)
gl.glAttachShader(shader_program, vertex_shader)

fragment_shader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
gl.glShaderSource(fragment_shader, fragment_shader_code)
gl.glCompileShader(fragment_shader)
gl.glAttachShader(shader_program, fragment_shader)

gl.glLinkProgram(shader_program)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glUseProgram(shader_program)
    gl.glDrawArrays(gl.GL_POINTS, 0, 1)
    pygame.display.flip()

pygame.quit()
