import struct
from Obj import Obj

def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(c):
    return struct.pack('=h', c)

def dword(c):
    return struct.pack('=l', c)

def color(red, green, blue):
    return bytes([round(blue * 255), round(green * 255), round(red * 255)])

class Render(object):

    def __init__(self):
        self.width = 0
        self.height = 0
        self.hVP = 0
        self.wVP = 0
        self.xVP = 0
        self.yVP = 0
        self.clear_color = color(1,1,1)
        self.framebuffer = []
        self.glClear()

    def glClear(self):
        self.framebuffer = [
            [self.clear_color for x in range(self.width)]
            for y in range(self.height)
        ]

    def glClearColor(self, red,blue,green):
        self.clear_color = color(red,blue,green)
    
    def glColor(self, red, green, blue):
        self.clear_color = color(red, green, blue)

    def glpoint(self, x, y):
        self.framebuffer[y][x] = self.clear_color

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height

    def glViewPort(self, xVP, yVP,  wVP, hVP):
        self.xVP = xVP
        self.yVP = yVP
        self.hVP = hVP
        self.wVP = wVP

    def glVertex(self, x, y):
        xVer = round((x + 1) * (self.wVP/ 2) + self.xVP)
        yVer = round((y + 1) * (self.hVP/2) + self.yVP)
        self.glpoint(round(xVer), round(yVer))

    def glLine(self, x1, y1, x2, y2):    
        dy = abs(y2 - y1)
        dx = abs(x2 - x1)
        steep = dy > dx
        
        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
            dy = abs(y2 - y1)
            dx = abs(x2 - x1)
        
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            
        offset = 0
        threshold = 1
        y = y1
        for x in range(x1, x2):
            if steep:
                self.glpoint(y, x)
            else:
                self.glpoint(x, y)
                
            offset += dy * 2
            
            if offset >= threshold:
                y += 1 if y1 < y2 else -1
                threshold += 2 * dx
                
    def glFinish(self, filename):
        f = open(filename, 'bw')

        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        for x in range(self.height):
          for y in range(self.width):
            f.write(self.framebuffer[x][y])

        f.close()
        
    def load_model(self, filename, scale, translate):
        model = Obj(filename)
        
        for face in model.faces:
            vcount = len(face)
            for position in range(vcount):
                vi_1 = int(face[position][0]) - 1
                vi_2 = int(face[(position + 1) % vcount][0]) - 1
                
                v1 = model.vertices[vi_1] 
                v2 = model.vertices[vi_2]
                
                x1 = round(v1[0] * scale[0] + translate[0])
                y1 = round(v1[1] * scale[1] + translate[1])
                x2 = round(v2[0] * scale[0] + translate[0])
                y2 = round(v2[1] * scale[1] + translate[1])
                
                self.glLine(x1, y1, x2, y2)

bitmap = Render()
bitmap.glCreateWindow(1920, 1080)
bitmap.glClearColor(0.09, 0.09, 0.43)
bitmap.glClear()
bitmap.glColor(0.48, 0.99, 0.00)
bitmap.load_model('./dino.obj', scale=[500, 500], translate=[960, 100 ])
bitmap.glFinish('Dinosauriooo.bmp')
    
