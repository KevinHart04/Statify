#  Frecuencia.R - Analizador Estadístico CLI

Una herramienta de línea de comandos ágil y directa para calcular tablas de frecuencias y generar gráficos estadísticos sin salir de la terminal. Diseñado para procesar datasets rápidamente y devolver métricas precisas con estilo.

## Características

- **Tablas de Frecuencias:** Calcula frecuencias absolutas, relativas y acumuladas al instante.
- **Soporte Multiformato:** Lee archivos `.csv` y `.xlsx` de forma transparente.
- **Gráficos Opcionales:** Genera histogramas y gráficos de barras listos para visualizar con una paleta de colores optimizada (AMOLED Orange Edition).
- **Output Elegante:** Tablas formateadas en Markdown (`knitr`) y alertas visuales (`cli`).

## Dependencias

El script instalará automáticamente las dependencias faltantes en su primera ejecución, pero requiere R base instalado en tu sistema.

Librerías utilizadas:
- `readxl`
- `cli`
- `knitr`
- `optparse`
- `ggplot2`

## Uso

Dale permisos de ejecución al script si aún no lo has hecho:
`chmod +x frecuencia.R`

### Sintaxis Básica
`./frecuencia.R -b <archivo> -v <variable> [-g <graficos>]`

### Argumentos
| Flag | Nombre | Descripción | Requerido |
|------|--------|-------------|-----------|
| `-b` | `--base` | Ruta del archivo de datos (`.csv` o `.xlsx`) | **Sí** |
| `-v` | `--var` | Nombre exacto de la variable a analizar | **Sí** |
| `-g` | `--graph`| Gráficos opcionales separados por coma (`histograma`, `barras`) | No |

## Ejemplos

**1. Solo generar la tabla de frecuencias:**
`./frecuencia.R -b dataset.xlsx -v EDAD`

**2. Generar tabla y exportar un histograma y un gráfico de barras:**
`./frecuencia.R -b dataset.csv -v SALARIO -g histograma,barras`

> **Pro-Tip para usuarios de terminal:** Puedes visualizar los gráficos PNG generados directamente en la consola usando `kitty +kitten icat archivo.png` o `chafa archivo.png`.

---
