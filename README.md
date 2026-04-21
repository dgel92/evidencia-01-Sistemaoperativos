# Proyecto ABP: Análisis de Rendimiento y Gestión de Recursos del SO

## 📝 Introducción
Este proyecto se desarrolla bajo el enfoque de Aprendizaje Basado en Proyectos (ABP) para la materia Sistemas Operativos. El objetivo es analizar cómo el **Kernel de Linux** gestiona los procesos, la planificación de CPU y los límites críticos de memoria utilizando contenedores Docker sobre un host con **Arch Linux**.

## 🧠 Marco Teórico

### 1. Planificación de CPU (Scheduler)
El **Scheduler** es el componente del SO encargado de asignar tiempo de procesador a los procesos. En Linux (CFS - Completely Fair Scheduler), cuando la demanda de hilos supera los núcleos disponibles, se produce el **Context Switching** (cambio de contexto), donde el SO debe guardar y cargar estados de registros constantemente, penalizando el rendimiento total.

### 2. Gestión de Memoria y Cgroups
Docker utiliza **Control Groups (cgroups)** para imponer límites de hardware. Cuando un proceso intenta exceder su cuota de RAM y no hay espacio en la Swap, el Kernel activa el **OOM Killer** (Out Of Memory Killer), un mecanismo de protección que finaliza procesos para preservar la estabilidad del sistema host.

## 🚀 Metodología del Experimento

Se utilizó un script de estrés en Python (`prueba1.py`) con las siguientes capacidades:
- **Carga de CPU:** Cálculo de números primos mediante `multiprocessing`.
- **Carga de RAM:** Asignación de un `bytearray` de 400 MB.

### Escenarios de Prueba:
1.  **Escenario A (Libre):** Sin restricciones. Uso total de los 16 núcleos del host.
2.  **Escenario B (CPU Limitada):** Restricción a 1.0 CPU (`--cpus="1.0"`).
3.  **Escenario C (RAM Limitada):** Restricción estricta de memoria (`--memory="410m"`).

## 📊 Resultados Obtenidos

| Escenario | Configuración | Tiempo (seg) | Resultado / Estado |
| :--- | :--- | :--- | :--- |
| **Control** | Sin límites | **0.15s** | Ejecución óptima (16 núcleos) |
| **CPU Stress** | 1.0 Core | **0.42s** | Degradación por Context Switching |
| **RAM Stress** | 410 MB | **N/A** | Finalizado por **OOM Killer** |

## 🔍 Análisis Técnico

- **Impacto en CPU:** Al limitar el contenedor a un solo core, el tiempo de ejecución aumentó un **180%**. Aunque el script lanzó 16 procesos, el SO los obligó a turnarse en un solo núcleo, evidenciando el costo operativo del scheduler.
- **Umbral de Memoria:** Se determinó un punto de quiebre en **414 MB**. Con 413 MB o menos, el proceso es aniquilado por el SO. Esto demuestra que el "overhead" (costo de funcionamiento) del runtime de Python y el contenedor es de aproximadamente **14 MB (3.5%)** adicionales a los datos procesados.

## 🛠️ Instrucciones de Uso y Replicación

### 1. Construcción de la Imagen
Desde la terminal en la carpeta del proyecto:
```bash

### 1. Prueba de CPU.
docker run --name cont-cpu --rm --cpus="1.0" experimento-abp > experimento_cpu.log 2>&1

### 2. Prueba de RAM.
docker run --name cont-ram --rm --memory="410m" --memory-swap="410m" experimento-abp > experimento_ram.log 2>&1


### Verificar evidencia.
cat experimento_cpu.log
docker build -t experimento-abp .
