# 🦾 Robótica Reconfigurable — Dibujo Autónomo con xArm Lite 6

Sistema de control para el brazo robótico **xArm Lite 6** capaz de ejecutar dibujos de forma autónoma mediante archivos G-code. El robot interpreta trayectorias vectoriales e interpola posiciones cartesianas en tiempo real, con calibración dinámica de altura para compensar irregularidades de la superficie.

---

## 📽️ Demo - video demostrativo de como hace ek procedimiento.

> *(https://youtu.be/YhT98m4ahmw)*


## 🧠 ¿Cómo funciona?

El sistema sigue el siguiente flujo:

```
Imagen original
     ↓
Vectorización (Inkscape / herramienta externa)
     ↓
Generación de G-code (.ngc)
     ↓
image_3colors.py — Lectura y parseo de G-code
     ↓
xArm SDK — Envío de comandos de posición cartesiana
     ↓
xArm Lite 6 — Ejecución del dibujo físico
```

1. Una imagen se vectoriza y convierte a archivos `.ngc` (G-code), uno por color (negro, gris, rojo)
2. El script inicializa el robot en posición de home y espera confirmación del usuario
3. El usuario calibra manualmente la altura de contacto con la superficie
4. El script lee el G-code línea por línea, extrae coordenadas X/Y y las convierte a posiciones cartesianas del brazo
5. El robot dibuja cada trazo desplazándose por la trayectoria definida
6. El proceso se repite para cada capa de color

---

## 🛠️ Tech Stack

| Componente | Tecnología |
|---|---|
| Lenguaje | Python 3 |
| Control del robot | xArm Python SDK |
| Formato de trayectorias | G-code (.ngc) |
| Comunicación | TCP/IP (xArm API) |
| Hardware | UFACTORY xArm Lite 6 |

---

## 📁 Estructura del repositorio

```
├── image_3colors.py        # Script principal de control del robot
├── dibujo_negro_0001.ngc   # G-code — capa negra
├── dibujo_gris_0001.ngc    # G-code — capa gris
├── dibujo_rojo_0001.ngc    # G-code — capa roja
├── output_0001.ngc         # G-code de salida general
└── README.md
```

---

## ⚙️ Requisitos

- Python 3.8+
- xArm Python SDK:
  ```bash
  git clone https://github.com/xArm-Developer/xArm-Python-SDK.git
  cd xArm-Python-SDK
  pip install -e .
  ```
- xArm Lite 6 conectado en red local
- Archivo `robot.conf` con la IP del robot:
  ```ini
  [xArm]
  ip = 192.168.X.X
  ```

---

## 🚀 Cómo ejecutar

```bash
# Con IP como argumento
python image_3colors.py 192.168.X.X

# O con archivo de configuración
python image_3colors.py
```

### Flujo de operación

1. El robot se inicializa y va a posición de home
2. Presiona `a` para comenzar el primer dibujo
3. Ajusta la altura de contacto presionando `a` (baja 1mm por presión)
4. Presiona `q` para guardar la altura calibrada y comenzar el dibujo
5. El robot ejecuta la trayectoria completa para cada capa de color
6. Al terminar, presiona `a` para continuar al siguiente color

---

## 🔧 Detalles técnicos

- **Coordenadas:** El sistema convierte coordenadas X/Y del G-code en posiciones cartesianas del robot, con ajuste en el eje Z según la región del dibujo
- **Compensación de altura dinámica:** El script aplica offsets en Z automáticamente dependiendo de la posición Y del trazo para corregir inclinaciones de la superficie
- **Velocidad:** Los movimientos se ejecutan a 100 mm/s con espera síncrona (`wait=True`) para garantizar precisión
- **Modo de operación:** El robot opera en modo posición cartesiana (modo 0) con estado activo (estado 0)

---

## 📐 Posición de trabajo

```
Posición home del dibujo:
  X: 74 mm
  Y: 311 mm  
  Z: 180 mm
  Roll: -180°, Pitch: 0°, Yaw: 130°
```

---

## 📚 Lo que aprendí

- Integración del xArm Python SDK para control cartesiano en tiempo real
- Parseo e interpretación de archivos G-code con Python
- Calibración de espacio de trabajo y compensación de errores de superficie
- Coordinación de movimientos sincrónicos y flujo de trabajo interactivo con hardware real

---

## 👨‍💻 Autor

**Emmanuel Lechuga Arreola**  
Ing. Robótica y Sistemas Digitales — Tecnológico de Monterrey  
[LinkedIn](https://www.linkedin.com/in/emmanuel-lechuga-arreola-7189892bb/) · [GitHub](https://github.com/EmmaLA22)
