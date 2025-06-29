import time
import random
import requests

NUM_REQUESTS = 10000


def get_user_client():
    """Função para obter o cliente de usuário."""

    url = f"http://localhost:8000/clientes/{random.randint(1, 1000)}"
    return requests.get(url)


def benchmark():
    tempos = []

    inicio_total = time.perf_counter()
    for _ in range(NUM_REQUESTS):
        
        t0 = time.perf_counter()
        response = get_user_client()
        dt = time.perf_counter() - t0

        if response.status_code == 200:
            tempos.append(dt)

    fim_total = time.perf_counter()

    total_time = fim_total - inicio_total
    avg_latency = sum(tempos) / len(tempos)

    print(f"Requests totais: {NUM_REQUESTS}")
    print(f"Throughput: {NUM_REQUESTS / total_time:.2f} req/s")
    print(f"Latência média: {avg_latency * 1000:.2f} ms")


if __name__ == "__main__":
    print("Iniciando benchmark... sincrono\n")
    benchmark()
