
class ShaderProgram:
    def __init__(self, ctx):
        self.ctx = ctx
        self.programs = {}
        self.programs['default'] = self.get_program('default')
        self.programs['2dsurf'] = self.get_program('2dsurf')
        
    def get_program(self, shader_name):
        with open(f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read() 

        with open(f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()
        
        prog = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return prog
    
    def destroy(self):
        [program.release() for program in self.programs.values()]