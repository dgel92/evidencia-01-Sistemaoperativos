import multiprocessing
import time
import os

def cpu_stress(n):
    # Cálculo intensivo para ocupar la CPU
    count = 0
    for i in range(2, n):
        for j in range(2, int(i**0.5) + 1):
            if i % j == 0:
                break
        else:
            count += 1
    return count

def memory_stress(size_mb):
    print(f"Intentando asignar {size_mb} MB de RAM...")
    data = bytearray(size_mb * 1024 * 1024)
    print("Memoria asignada con éxito.")
    return data

if __name__ == "__main__":
    print(f"--- Iniciando Experimento en PID: {os.getpid()} ---")
    start_time = time.time()

    # 1. Prueba de CPU (Multiprocessing)
    cores = multiprocessing.cpu_count()
    print(f"Detectados {cores} núcleos. Iniciando procesos...")
    with multiprocessing.Pool(processes=cores) as pool:
        pool.map(cpu_stress, [20000] * cores)

    # 2. Prueba de RAM
    # Intentamos usar 400MB (Ajustalo según el límite que pongas en Docker)
    dummy_data = memory_stress(400) 

    end_time = time.time()
    print(f"--- Experimento Finalizado en {end_time - start_time:.2f} segundos ---")