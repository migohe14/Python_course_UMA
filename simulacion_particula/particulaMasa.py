from particula import *
class ParticulaMasa(Particula):
    def __init__(self):
        super().__init__()
        self.masa = 0

    def setValores(self, pPos, pVel, pAcc, pMasa):
        super().setValores(pPos, pVel, pAcc)
        self.masa = pMasa

    def initRandom(self):
        self.setValores(np.array([random(), random(), random() ]), np.array([random(), random(), random()]),
          np.array( [random(), random(), random()]), random())

    def muestra(self):
        super().muestra()
        print("   La masa es: ", self.masa)

    def aceleracionCero(self):
        self.acc=np.array([0.0,0.0,0.0])
    
    def aceleracionGravitatoria(self, otra):
        softening = 1e-6
        distancia = self.distancia (otra)
        if distancia < softening:
            distancia = softening
        distanciaInv = 1.0 / distancia
        delta = otra.pos - self.pos
        self.acc += delta* G * otra.masa * distanciaInv ** 3