import asyncio
import subprocess

async def ping(ip):
    process = await asyncio.create_subprocess_exec(
        'ping', ip,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    await process.wait()
    return ip if process.returncode == 0 else None

async def ping_ips(ips):
    tasks = [ping(ip) for ip in ips]
    results = await asyncio.gather(*tasks)
    return results

async def main():
    base_ip = "192.168.1."
    num_ips = 20
    ips_to_ping = [base_ip + str(i) for i in range(1, num_ips + 1)]

    group_size = 10
    grouped_ips = [ips_to_ping[i:i+group_size] for i in range(0, len(ips_to_ping), group_size)]

    active_ips = []

    for group in grouped_ips:
        print(f"Pinging group: {group}")
        results = await ping_ips(group)
        active_ips.extend([ip for ip in results if ip is not None])

    with open('active_ip.txt', 'w') as active_file:
        active_file.write('\n'.join(filter(None, active_ips)))

    print("Активные IP-адреса записаны в active_ip.txt")

if __name__ == "__main__":
    asyncio.run(main())
