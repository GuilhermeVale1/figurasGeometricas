from OpenGL.GL import *
class OpenGLUtils:
    @staticmethod
    def initializeShader(shaderCode, shaderType):
        # compila o código do shader e retorna a referência
        shaderRef = glCreateShader(shaderType)
        glShaderSource(shaderRef, shaderCode)
        glCompileShader(shaderRef)
        compileSuccess = glGetShaderiv(shaderRef, GL_COMPILE_STATUS)

        if not compileSuccess:
            errorMessage = glGetShaderInfoLog(shaderRef)
            glDeleteShader(shaderRef)
            errorMessage = '\n' + errorMessage.decode('utf-8')
            raise Exception(errorMessage)
        return shaderRef

    @staticmethod
    def initializeProgram(vertexShaderCode, fragmentShaderCode):
        # compila e liga os shaders
        vertexShaderRef = OpenGLUtils.initializeShader(vertexShaderCode, GL_VERTEX_SHADER)
        fragmentShaderRef = OpenGLUtils.initializeShader(fragmentShaderCode, GL_FRAGMENT_SHADER)

        # cria o programa e anexa os shaders
        programRef = glCreateProgram()
        glAttachShader(programRef, vertexShaderRef)
        glAttachShader(programRef, fragmentShaderRef)
        glLinkProgram(programRef)

        # verifica se o link foi bem-sucedido
        linkSuccess = glGetProgramiv(programRef, GL_LINK_STATUS)
        if not linkSuccess:
            errorMessage = glGetProgramInfoLog(programRef)
            glDeleteProgram(programRef)
            errorMessage = '\n' + errorMessage.decode('utf-8')
            raise Exception(errorMessage)

        # retorno do programa após sucesso
        return programRef
