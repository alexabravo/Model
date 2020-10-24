#Codigo visto en clase.

class Obj(object):
    def __init__(self,filename):
        with open(filename) as f:
            self.lines = f.read().splitlines()
        self.vertices = []
        self.faces = []
        self.read()
            
    def read(self):
        for line in self.lines:
            splitable = len(line.split(' ')) > 1
            if splitable:
                prefix, value = line.split(' ', 1)
                
            if prefix == 'v':
                temp_vertices = []
                for v in value.split(' '):
                    if v != '':
                        temp_vertices.append(float(v))
                self.vertices.append(temp_vertices)
             
            elif prefix == 'f':
                temp_face = []
                for face in value.split(' '):
                    f = face.split('/')
                    if f != '':
                        temp_face.append(f)
                self.faces.append(temp_face)                
                    

            
