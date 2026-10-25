#Filosofos Comelones
#Leonel Figueroa Jauregui


# ===============================================================
# PARTE 1: LOGICA (hilos, semaforos y tenedores)
# ===============================================================

#Librerias
import time
import random
import threading #libreria de semaforo en python

#Creacion de filosofos y tenedores 
# El filosofo n usa el tenedor n (derecho) y el tenedor n+1 (izquierdo)
estados = ["pensando"] * 5                               # solo 2 estados: pensando o comiendo
hambre = [False] * 5                                     # True = ya quiere comer y esta esperando sus tenedores
tenedores = [None] * 5                                   # None = libre, o el numero del filosofo que lo tiene
mutex = threading.Lock()                                 # protege tenedores y estados (evita la condicion de carrera)
semaforos = [threading.Semaphore(0) for i in range(5)]   # SEMAFOROS: cada filosofo espera aqui hasta que sus 2 tenedores esten libres


# Revisa si el filosofo n puede comer: quiere comer y sus 2 tenedores estan libres
def probar(n):
    derecho = n
    izquierdo = (n + 1) % 5
    if hambre[n] and tenedores[derecho] is None and tenedores[izquierdo] is None:
        tenedores[derecho] = n      # agarra primero el derecho
        tenedores[izquierdo] = n    # luego el izquierdo
        hambre[n] = False
        estados[n] = "comiendo"
        semaforos[n].release()      # lo despierta para que coma


#Funcion pensar
def pensar(n):
    time.sleep(random.randint(1, 2))


#Funcion comer
def comer(n):
    with mutex:
        hambre[n] = True            # ya quiere comer
        probar(n)                   # si sus 2 tenedores estan libres, come de una vez

    semaforos[n].acquire()          # si no pudo, espera aqui hasta que le toque

    time.sleep(3)                   # esta comiendo

    with mutex:
        estados[n] = "pensando"
        tenedores[n] = None         # suelta los 2 tenedores
        tenedores[(n + 1) % 5] = None
        probar((n + 4) % 5)         # los vecinos que esperaban comen directo
        probar((n + 1) % 5)


# Vida de cada filosofo (se repite siempre hasta cerrar la ventana)
def filosofo(n):
    while True:
        pensar(n)
        comer(n)

# ==============================================================================================================================


# ===============================================================
# PARTE 2: VISUAL (tkinter)
# ===============================================================

#Librerias
import math
import tkinter as tk

#Configuracion del dibujo
ESCALA = 1.2                     # tamano de todo el dibujo (1.0 = chico, 1.2 = grande, 1.4 = mas grande)

TAMANO = int(760 * ESCALA)       # tamano de la ventana
CX, CY = TAMANO / 2, TAMANO / 2  # centro de la mesa
RADIO_MESA = 340 * ESCALA
R_FILOSOFO = 240 * ESCALA        # distancia de los filosofos al centro
RADIO_FILOSOFO = 52 * ESCALA
R_REPOSO = 215 * ESCALA          # tenedor libre: en el hueco entre dos filosofos
R_MANO = 158 * ESCALA            # tenedor ocupado: junto a su filosofo

COLOR_PENSANDO = "#5dade2"       # azul
COLOR_COMIENDO = "#2ecc71"       # verde
COLOR_TENEDOR_LIBRE = "#4a4a4a"  # gris
COLOR_TENEDOR_OCUPADO = "#f1c40f"  # amarillo

# angulo de cada filosofo (el 0 arriba y luego en el sentido del reloj)
ANG_FILOSOFO = [math.radians(-90 + 72 * n) for n in range(5)]

# el tenedor i esta entre el filosofo i-1 y el filosofo i
reposo = []
for i in range(5):
    ang = ANG_FILOSOFO[i] - math.radians(36)
    reposo.append((CX + R_REPOSO * math.cos(ang), CY + R_REPOSO * math.sin(ang)))

posicion = [list(p) for p in reposo]   # posicion actual de cada tenedor (se va moviendo)

#Creacion de la ventana
ventana = tk.Tk()
ventana.title("Filosofos Comelones - Leonel Figueroa Jauregui")
ventana.resizable(False, False)
lienzo = tk.Canvas(ventana, width=TAMANO, height=TAMANO, bg="#1e1e2e", highlightthickness=0)
lienzo.pack()


# Dibuja un tenedor en (x, y) apuntando hacia el centro de la mesa
def dibujar_tenedor(x, y, color):
    e = ESCALA
    ang = math.atan2(y - CY, x - CX)
    ux, uy = math.cos(ang), math.sin(ang)      # hacia afuera
    px, py = -uy, ux                           # de lado
    bx, by = x - ux * 5 * e, y - uy * 5 * e    # base de las puas
    lienzo.create_line(x + ux * 27 * e, y + uy * 27 * e, bx, by, fill=color, width=int(5 * e), capstyle="round")   # mango
    lienzo.create_line(bx - px * 7 * e, by - py * 7 * e, bx + px * 7 * e, by + py * 7 * e, fill=color, width=int(3 * e))   # base
    for lado in (-7, 0, 7):                                                                                        # 3 puas
        lienzo.create_line(bx + px * lado * e, by + py * lado * e,
                           bx + px * lado * e - ux * 22 * e, by + py * lado * e - uy * 22 * e,
                           fill=color, width=int(3 * e))


# Dibuja la mesa, los filosofos y los tenedores (se repite cada 30 ms)
def dibujar():
    lienzo.delete("all")

    # mesa grande
    lienzo.create_oval(CX - RADIO_MESA, CY - RADIO_MESA, CX + RADIO_MESA, CY + RADIO_MESA,
                       fill="#c8a165", outline="#8b5a2b", width=int(8 * ESCALA))
    lienzo.create_text(CX, CY, text="FILÓSOFOS\nCOMELONES",
                       font=("Arial", int(18 * ESCALA), "bold"), fill="#5b3a1a", justify="center")

    # filosofos (circulos que cambian de color)
    for n in range(5):
        x = CX + R_FILOSOFO * math.cos(ANG_FILOSOFO[n])
        y = CY + R_FILOSOFO * math.sin(ANG_FILOSOFO[n])
        color = COLOR_PENSANDO if estados[n] == "pensando" else COLOR_COMIENDO
        lienzo.create_oval(x - RADIO_FILOSOFO, y - RADIO_FILOSOFO, x + RADIO_FILOSOFO, y + RADIO_FILOSOFO,
                           fill=color, outline="#222222", width=int(3 * ESCALA))
        lienzo.create_text(x, y, text=f"F{n}\n{estados[n]}",
                           font=("Arial", int(13 * ESCALA), "bold"), fill="#111111", justify="center")

    # tenedores (se mueven suave hacia donde les toca)
    for i in range(5):
        dueno = tenedores[i]
        if dueno is None:
            objetivo = reposo[i]
            color = COLOR_TENEDOR_LIBRE
        else:
            # el tenedor derecho queda de un lado del plato y el izquierdo del otro
            if i == dueno:
                ang = ANG_FILOSOFO[dueno] - math.radians(11)
            else:
                ang = ANG_FILOSOFO[dueno] + math.radians(11)
            objetivo = (CX + R_MANO * math.cos(ang), CY + R_MANO * math.sin(ang))
            color = COLOR_TENEDOR_OCUPADO
        posicion[i][0] += (objetivo[0] - posicion[i][0]) * 0.2
        posicion[i][1] += (objetivo[1] - posicion[i][1]) * 0.2
        dibujar_tenedor(posicion[i][0], posicion[i][1], color)

    ventana.after(30, dibujar)      # se vuelve a dibujar cada 30 ms


#Programa principal
for n in range(5):
    threading.Thread(target=filosofo, args=(n,), daemon=True).start()   # arranca los 5 filosofos (parte 1)

dibujar()
ventana.mainloop()