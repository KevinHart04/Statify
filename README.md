# 

```text
   _____ __        __  _ ___
  / ___// /_____ _/ /_(_) _/_  __
  \__ \/ __/ __ `/ __/ / /_/ / / /
 ___/ / /_/ /_/ / /_/ / __/ /_/ /
/____/\__/\__,_/\__/_/_/  \__, /
                         /____/
```

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![R Base](https://img.shields.io/badge/R-Motor_Estad%C3%ADstico-165CAA?style=for-the-badge&logo=r&logoColor=white)
![TUI](https://img.shields.io/badge/UI-Rich_%2B_Questionary-FF8C00?style=for-the-badge&logo=terminal)

**Statify** es una herramienta de línea de comandos ágil y con una Interfaz de Usuario de Terminal (TUI) diseñada para calcular distribuciones de frecuencias y generar gráficos estadísticos sin salir de la consola. 

Combina la elegancia y la interactividad de **Python** para la interfaz con el poder de cálculo bruto de **R** en el backend. Diseñado para procesar datasets rápidamente y devolver métricas precisas con estilo.

## Características

- **TUI Interactiva:** Olvídate de recordar flags largos. Navega por menús interactivos, selecciona variables y elige gráficos con la barra espaciadora.
- **Soporte Drag & Drop:** Arrastra tus archivos `.csv` o `.xlsx` directamente a la terminal para cargarlos.
- **Tipado Inteligente:** Procesamiento diferenciado para variables **discretas** y **continuas** (con cálculo de amplitud e intervalos por regla de Sturges).
- **Métricas de Centralización:** Cálculo de Media, Mediana y Moda con **interpretación automática de asimetría** empírica.
- **Motor Gráfico Avanzado:** Genera Histogramas, Ojivas, Gráficos de Barras, Polígonos y Sectores (con porcentajes automáticos) usando `ggplot2` y una paleta AMOLED Orange Edition.

## Arquitectura del Proyecto

El proyecto está dividido en un orquestador en Python y módulos funcionales en R:
```text
Statify/
├── tui.py               # Orquestador e Interfaz Interactiva (Python)
├── main.r               # Punto de entrada del backend (R)
└── modules/
    ├── estadistica.r    # Funciones de tabulación y centralización
    └── graficos.r       # Generadores de ggplot2
```

## Dependencias e Instalación

Requiere tener **Python 3** y **R base** instalados en tu sistema.

> [!NOTE]  
> El script de R instalará automáticamente las dependencias de R faltantes (`readxl`, `cli`, `knitr`, `optparse`, `ggplot2`) en su primera ejecución. Ten paciencia, solo ocurre una vez.

**1. Clonar y preparar el entorno de Python:**
```bash
# Se recomienda usar un entorno virtual
python -m venv venv
source venv/bin/activate

# Instalar dependencias visuales de la TUI
pip install questionary rich pyfiglet
```

**2. Dar permisos de ejecución:**
```bash
chmod +x tui.py
```

## Uso

Inicia la interfaz interactiva simplemente ejecutando el orquestador sin argumentos:

```bash
./tui.py
```

Sigue las instrucciones en pantalla para:
1. Cargar tu dataset.
2. Definir tu variable y su naturaleza.
3. Generar las tablas o renderizar los gráficos.

> [!WARNING]  
> Asegúrate de escribir el nombre de la variable de forma **exacta** a como aparece en la cabecera de tu archivo, respetando mayúsculas y minúsculas.

### Uso Clásico (Modo Flags)

Si prefieres el silencio de la terminal pura y dura, o quieres automatizar Statify en un script bash, puedes pasar los argumentos directamente. `tui.py` actuará como un puente (passthrough) hacia R:

```bash
./tui.py -b dataset.xlsx -v SALARIO -t continua -g histograma,ojiva
```

| Flag | Descripción |
|------|-------------|
| `-b` | Ruta del archivo de datos (`.csv` o `.xlsx`) |
| `-v` | Nombre exacto de la variable a analizar |
| `-t` | Tipo de variable (`discreta` o `continua`) |
| `-g` | Gráficos a generar separados por coma, o `all` |
| `-c` | Mostrar solo medidas de centralización e interpretación |

> [!TIP]  
> **Para los entusiastas de la terminal:** Puedes visualizar los gráficos PNG generados directamente en la consola usando `kitty +kitten icat archivo.png` o herramientas como `chafa archivo.png`. ¡Ideal si tu entorno es un Window Manager como Hyprland!
```
