import asyncio
import random
import time
import httpx

NUM_REQUESTS = 10000  # total de requisições


async def fetch(client: httpx.AsyncClient, sem: asyncio.Semaphore, latencies, tempos) -> int:
    url = f"http://localhost:8000/clientes/{random.randint(1, 1000)}"
    async with sem:
        start = time.perf_counter()
        resp = await client.get(url, timeout=10.0)
        elapsed = time.perf_counter() - start
        latencies.append(elapsed)
        
        if resp.status_code == 200:
            tempos.append(elapsed)
        
        return resp.status_code


async def benchmark():
    tempos, latencies, sucesso = [], [], 0

    limits = httpx.Limits(max_connections=100, max_keepalive_connections=20)
    async with httpx.AsyncClient(timeout=10.0, limits=limits) as client:
        inicio_total = time.perf_counter()

        sem = asyncio.Semaphore(100)
        tasks = [
            asyncio.create_task(fetch(client, sem, latencies, tempos))
            for _ in range(NUM_REQUESTS)
        ]
        await asyncio.gather(*tasks)

        fim_total = time.perf_counter()

    total_time = fim_total - inicio_total
    avg_latency = sum(tempos) / len(tempos) if tempos else 0

    print(f"Requests totais : {NUM_REQUESTS}")
    print(f"Sucessos (200)  : {NUM_REQUESTS}")
    print(f"Throughput      : {NUM_REQUESTS / total_time:.2f} req/s")
    print(f"Latência média  : {avg_latency * 1000:.2f} ms")


if __name__ == "__main__":
    print("Iniciando benchmark... assíncrono\n")
    asyncio.run(benchmark())
