import asyncio
import random
import time
import httpx
import requests

NUM_REQUESTS = 10000


def get_server_metrics():
    response = requests.get("http://localhost:8000/metrics")

    if not response.ok:
        return print("Erro ao obter métricas do servidor.") or []

    metrics = response.json()
    return metrics.get("message", [])


def clear_server_metrics():
    response = requests.put("http://localhost:8000/clean-metrics")

    if not response.ok:
        return print("Erro ao limpar métricas do servidor.") or False

    return print(response.json().get("message", ""))


async def fetch(client: httpx.AsyncClient, sem: asyncio.Semaphore) -> int:
    url = f"http://localhost:8000/clientes/{random.randint(1, 1000)}"

    async with sem:
        resp = await client.get(url, timeout=10.0)
        return resp.status_code


async def benchmark():
    # Limits hardware concurrency to 40
    sem = asyncio.Semaphore(40)

    async with httpx.AsyncClient(timeout=10.0) as client:
        inicio_total = time.perf_counter()

        tasks = [asyncio.create_task(fetch(client, sem)) for _ in range(NUM_REQUESTS)]
        await asyncio.gather(*tasks)

        fim_total = time.perf_counter()
        total_time = fim_total - inicio_total

    print(f"Requests totais : {NUM_REQUESTS}")
    print(f"Throughput      : {NUM_REQUESTS / total_time:.2f} req/s")

    latencies = get_server_metrics()
    avg_latency = sum(latencies) / len(latencies)
    print(f"Latência média  : {avg_latency * 1000:.2f} ms")


if __name__ == "__main__":
    print("Iniciando benchmark... assíncrono\n")
    asyncio.run(benchmark())
