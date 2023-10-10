import math
import sys
import pygame

pygame.init()

size = width, height = 300, 300
screen = pygame.display.set_mode(size)
white = (255, 255, 255)
black = (12, 12, 12)
screen.fill(white)
clock = pygame.time.Clock()
pygame.display.flip()


# Declaracion de clases
# Clase punto

class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return "{x}, {y}".format(x=self.x, y=self.y)


# Clase triangulo

class Triangulo:
    def __init__(self, _p1, p2, p3):
        self.puntos = set()
        self.puntos.add(_p1)
        self.puntos.add(p2)
        self.puntos.add(p3)

    def __str__(self):
        arPuntos = []
        for p in self.puntos:
            arPuntos.append(str(p))
        return str(arPuntos)


# Colores para los triangulos

colores = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (0, 255, 255),
    (255, 255, 0),
    (255, 0, 255),
    (153, 51, 255),
    (255, 102, 255)
]

while True:
    pygame.event.pump()

    # Crea y muestra la grilla

    w = int(input("width: "))
    h = int(input("height: "))
    grid = []
    dots_h = []
    dots = []
    setTriangulos = set()
    puntosAEvitar = set()


    def dibujar_grilla():
        for _w in range(w):
            for _h in range(h):
                pygame.draw.circle(screen, (0, 0, 0), (_w * (300 / w) + 10, _h * (300 / h) + 10), 2)

    def lineas_para_triangulo(_p1, _p2, c):
        while c > len(colores) - 1:
            c = c - len(colores) - 1
        pygame.draw.line(screen, colores[c], (_p1.x * (300 / w) + 10, (h - _p1.y - 1) * (300 / h) + 10),
                         (_p2.x * (300 / w) + 10, (h - _p2.y - 1) * (300 / h) + 10), 2)

    dibujar_grilla()
    pygame.display.update()

    # Calculos de pendiente y angulos

    def calcular_pendiente(_p1, _p2):
        if (_p2.x - _p1.x) == 0:
            return "Pendiente indefinida"
        return (_p2.y - _p1.y) / (_p2.x - _p1.x)

    def verificar_angulos(_listaAngulos):
        if _listaAngulos[0] == 0 and _listaAngulos[1] != 0 and _listaAngulos[2] != 0:
            _listaAngulos[0] = 180 - (_listaAngulos[1] + _listaAngulos[2])
        elif _listaAngulos[1] == 0 and _listaAngulos[0] != 0 and _listaAngulos[2] != 0:
            _listaAngulos[1] = 180 - (_listaAngulos[0] + _listaAngulos[2])
        elif _listaAngulos[2] == 0 and _listaAngulos[1] != 0 and _listaAngulos[0] != 0:
            _listaAngulos[2] = 180 - (_listaAngulos[0] + _listaAngulos[1])
        return _listaAngulos

    def calcular_angulos(m1, m2):
        if type(m1) == str and m2 == 0 or -0:
            return 90
        elif type(m2) == str and m1 == 0 or -0:
            return 90
        elif type(m1) == str or type(m2) == str:
            return 0
        elif (1 + m2 * m1) == 0:
            return 90
        else:
            ang = math.degrees(math.atan((m2 - m1) / (1 + m2 * m1)))
            if ang < 0:
                ang += 180
            return ang

    # Funcion principal

    def buscar_todos_los_triangulos(p1, _h, _w, _setTriangulos, listaPuntosEvitar):
        color = 0
        for y2 in range(_h):
            for x2 in range(_w):
                if Punto(x2, y2) in listaPuntosEvitar:
                    continue
                for y3 in range(_h):
                    for x3 in range(_w):
                        if Punto(x3, y3) in listaPuntosEvitar:
                            continue

                        p2 = Punto(x2, y2)
                        p3 = Punto(x3, y3)

                        mAB = calcular_pendiente(p1, p3)
                        mAC = calcular_pendiente(p1, p2)
                        mBC = calcular_pendiente(p2, p3)

                        aX = calcular_angulos(mAB, mAC)
                        aY = calcular_angulos(mBC, mAB)
                        aZ = calcular_angulos(mAC, mBC)

                        listaAngulos = [aX, aY, aZ]
                        listaAngulos = verificar_angulos(listaAngulos)

                        if listaAngulos.count(90) == 1 and listaAngulos.count(0) == 0:
                            __t = Triangulo(p1, p2, p3)
                            flag = triangulos_repetidos(_setTriangulos, __t)
                            if flag:
                                del __t
                            else:
                                color += 1
                                lineas_para_triangulo(p1, p2, color)
                                lineas_para_triangulo(p1, p3, color)
                                lineas_para_triangulo(p2, p3, color)
                                pygame.display.flip()

                                pygame.time.wait(1000)
                                screen.fill((255, 255, 255))

                                pygame.display.flip()
                                _setTriangulos.add(__t)

                        del p2
                        del p3

    # Evitar triangulos repetidos
    def triangulos_repetidos(_setTriangulos: set, ___t: Triangulo):
        for _t in _setTriangulos:
            if _t.puntos == ___t.puntos:
                return True
        return False

    # Evitar puntos en grilla

    res = input("Evitar puntos en la grilla? S/N: ")

    while res.capitalize() == "S":
        auxP = Punto(int(input("coordenada x del punto ")), int(input("coordenada y del punto ")))
        puntosAEvitar.add(auxP)
        pygame.display.flip()
        res = input("Continuar? S/N: ")

    # Buscar triangulos en toda la grilla

    for _y in range(h):
        for _x in range(w):
            _p = Punto(_x, _y)
            if _p in puntosAEvitar:
                del _p
                continue
            buscar_todos_los_triangulos(_p, h, w, setTriangulos, puntosAEvitar)
            del _p

    # Guardar triangulos en un documento de texto

    f = open("triangulos.txt", "w")
    for t in setTriangulos:
        f.write(str(t))
        f.write('\n')
    f.close()

    # Terminar programa

    _doesExec = input("Continuar? S/N: ")
    if _doesExec.capitalize() != "S":
        pygame.quit()
        sys.exit()
