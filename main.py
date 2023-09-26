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

# Crea la planilla sobre la que se buscaran los triangulos

_exec = True

while _exec:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    w = int(input("width: "))
    h = int(input("height: "))
    grid = []
    dots_h = []
    dots = []

    for _w in range(w):
        for _h in range(h):
            _dot = pygame.draw.circle(screen, (0, 0, 0), (_w * (300 / w) + 10, _h * (300 / h) + 10), 2)
            dots_h.append(_dot)
        dots.append(dots_h)

    pygame.display.update()

    for i in range(h):
        grid.append([])

    for i in range(w):
        for j in range(h):
            grid[j].append(".")

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


    # Muestra la planilla

    for i in range(h):
        print("{}  {}".format(h - i - 1, grid[i]))


    def puntos_similares(_p1: Punto, _p2: Punto):
        if _p1.x == _p2.x:
            if _p1.y == _p2.y:
                return True
            else:
                return False
        else:
            return False


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


    def mostrar_triangulos(_p1, _p2, _p3):
        print("Triangulo", _p1.x, _p1.y, _p2.x, _p2.y, _p3.x, _p3.y)
        grid[h - _p3.y - 1][_p3.x] = "X"
        grid[h - _p2.y - 1][_p2.x] = "X"
        for u in range(h):
            print(grid[u])
        grid[h - _p3.y - 1][_p3.x] = "."
        grid[h - _p2.y - 1][_p2.x] = "."

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

    def lineas_para_triangulo(_p1, _p2, c):
        while c > len(colores)-1:
            c = c - len(colores)-1
        pygame.draw.line(screen, colores[c], (_p1.x * (300 / w) + 10, (h - _p1.y - 1) * (300 / h) + 10),
                         (_p2.x * (300 / w) + 10, (h - _p2.y - 1) * (300 / h) + 10))


    def buscar_todos_los_triangulos(_p1, _h, _w, _setTriangulos, listaPuntosEvitar):
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

                        mAB = calcular_pendiente(_p1, p3)
                        mAC = calcular_pendiente(_p1, p2)
                        mBC = calcular_pendiente(p2, p3)

                        aX = calcular_angulos(mAB, mAC)
                        aY = calcular_angulos(mBC, mAB)
                        aZ = calcular_angulos(mAC, mBC)

                        listaAngulos = [aX, aY, aZ]
                        listaAngulos = verificar_angulos(listaAngulos)

                        if listaAngulos.count(90) == 1 and listaAngulos.count(0) == 0:
                            __t = Triangulo(_p1, p2, p3)
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
                                mostrar_triangulos(_p1, p2, p3)
                                _setTriangulos.add(__t)

                        del p2
                        del p3


    p7 = Punto(0, 5)
    p8 = Punto(0, 5)

    print(puntos_similares(p7, p8))

    setTriangulos = set()


    def triangulos_repetidos(_setTriangulos: set, ___t: Triangulo):
        for _t in _setTriangulos:
            if _t.puntos == ___t.puntos:
                return True
        return False


    p1 = Punto(int(input("coordenada x del punto ")), int(input("coordenada y del punto ")))

    grid[h - p1.y - 1][p1.x] = "X"
    pygame.draw.circle(screen, (255, 0, 0), (p1.x * (300 / w) + 10, (h-p1.y-1) * (300 / h) + 10), 3)

    pygame.display.update()

    for _u in range(h):
        print(grid[_u])

    puntosAEvitar = set()

    res = input("Evitar puntos en la grilla? S/N: ")
    while res.capitalize() == "S":
        auxP = Punto(int(input("coordenada x del punto ")), int(input("coordenada y del punto ")))
        if auxP == p1:
            print("No puede seleccionar el mismo punto para evitar que el que usa para buscar")
            continue
        puntosAEvitar.add(auxP)
        pygame.draw.circle(screen, (255, 255, 255), (auxP.x * (300 / w) + 10, auxP.y * (300 / h) + 10), 2)
        pygame.display.flip()
        res = input("Continuar? S/N: ")

    buscar_todos_los_triangulos(p1, h, w, setTriangulos, puntosAEvitar)

    f = open("triangulos.txt", "w")
    for t in setTriangulos:
        f.write(str(t))
        f.write('\n')
    f.close()

    _doesExec = input("Continuar? S/N: ")
    if _doesExec.capitalize() != "S":
        _exec = False

pygame.quit()
