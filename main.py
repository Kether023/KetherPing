import asyncio
import subprocess

async def ping(ip):
    process = await asyncio.create_subprocess_exec(
        'ping', '-c', '4', ip,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    await process.wait()
    return ip if process.returncode == 0 else None

async def ping_ips(ips):
    tasks = [ping(ip) for ip in ips]
    done, _ = await asyncio.wait(tasks)
    return [task.result() for task in done if task.result() is not None]

async def main():
    base_ip = "192.168.1."
    num_ips = 258
    ips_to_ping = [base_ip + str(i) for i in range(1, num_ips + 1)]

    # Разделяем IP-адреса на группы по 10
    group_size = 10
    grouped_ips = [ips_to_ping[i:i+group_size] for i in range(0, len(ips_to_ping), group_size)]

    # Пингуем IP-адреса группами
    active_ips = []
    for group in grouped_ips:
        active_ips.extend(await ping_ips(group))

    # Записываем активные IP-адреса в файл
    with open('active_ip.txt', 'w') as file:
        file.write('\n'.join(active_ips))

    print("Активные IP-адреса записаны в active_ip.txt")

if __name__ == "__main__":
    asyncio.run(main())
