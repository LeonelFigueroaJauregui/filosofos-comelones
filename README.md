# 🍝 Filósofos Comelones

Simulación visual del clásico problema de sincronización **"La cena de los filósofos"**, hecha en **Python** con **hilos, semáforos y mutex**, y una interfaz gráfica animada con **tkinter**.

**Autor:** Leonel Figueroa Jauregui

---

## 📖 El problema

Cinco filósofos están sentados alrededor de una mesa. Entre cada par de filósofos hay un tenedor (5 en total). Cada filósofo alterna entre dos estados:

- **Pensando** 🔵
- **Comiendo** 🟢

Para comer, un filósofo necesita **los dos tenedores** que tiene a su lado. Si todos agarraran un tenedor al mismo tiempo y esperaran el otro, nadie podría comer (**interbloqueo / deadlock**). Este proyecto resuelve el problema evitando ese caso y sin que ningún filósofo se quede esperando para siempre.

## ⚙️ Cómo funciona

El código está dividido en dos partes:

### Parte 1: Lógica (concurrencia)

- Cada filósofo corre en su **propio hilo** (`threading.Thread`).
- Un **mutex** (`threading.Lock`) protege los estados y los tenedores para evitar condiciones de carrera.
- Cada filósofo tiene su propio **semáforo** (`threading.Semaphore(0)`) donde espera hasta que sus dos tenedores estén libres.
- La función `probar(n)` revisa si el filósofo `n` tiene hambre y si sus dos tenedores están libres; si es así, los toma de forma atómica y lo despierta con `release()`.
- Al terminar de comer, el filósofo suelta sus tenedores y prueba a despertar a sus vecinos que estaban esperando.

Como los dos tenedores se toman **juntos** dentro de la sección crítica, nunca se queda un filósofo con un solo tenedor, por lo que no hay deadlock.

### Parte 2: Visual (tkinter)

- Una ventana con una mesa circular y los 5 filósofos.
- El color de cada filósofo indica su estado:

| Elemento | Color | Significado |
|---|---|---|
| Filósofo | 🔵 Azul | Pensando |
| Filósofo | 🟢 Verde | Comiendo |
| Tenedor | ⚫ Gris | Libre (en la mesa) |
| Tenedor | 🟡 Amarillo | En uso (junto a su filósofo) |

- Los tenedores se **mueven con animación suave** hacia el filósofo que los toma.
- La pantalla se redibuja cada 30 ms.
- Se puede cambiar el tamaño de todo el dibujo con la constante `ESCALA`.

## 🛠️ Tecnologías

- Python 3
- `threading` (hilos, `Lock`, `Semaphore`)
- `tkinter` (interfaz gráfica)
- `math`, `time`, `random`

## 🚀 Cómo ejecutarlo

### 1. Requisitos

Necesitas tener Python 3 instalado. En Ubuntu/Debian, `tkinter` puede requerir instalarse aparte:

```bash
sudo apt install python3 python3-tk
```

En Windows y macOS normalmente ya viene incluido con Python.

### 2. Clonar el repositorio

```bash
git clone https://github.com/<tu-usuario>/<nombre-del-repositorio>.git
cd <nombre-del-repositorio>
```

### 3. Ejecutar

```bash
python3 "Filosofos Comelones.py"
```

Se abrirá la ventana con la simulación. Para terminarla, solo cierra la ventana (los hilos son *daemon* y se detienen solos).

## 🎛️ Configuración rápida

Al inicio de la **Parte 2** del código puedes ajustar:

| Constante | Descripción |
|---|---|
| `ESCALA` | Tamaño del dibujo (`1.0` chico, `1.2` grande, `1.4` más grande) |
| `COLOR_*` | Colores de filósofos y tenedores |

Y en la **Parte 1**, los tiempos:

- `pensar()` → entre 1 y 2 segundos
- `comer()` → 3 segundos

## 📸 Captura

Agrega aquí una captura de pantalla de la simulación, por ejemplo:

```markdown
![Simulación](captura.png)
```

## 📚 Conceptos que se practican

- Concurrencia con hilos
- Exclusión mutua (mutex)
- Semáforos
- Condiciones de carrera
- Interbloqueo (deadlock) e inanición (starvation)
- Animación con `tkinter.Canvas`

## 👤 Autor

**Leonel Figueroa Jauregui**
Estudiante de Ingeniería en Computación, CUAltos.
