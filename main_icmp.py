import asyncio
from scapy.all import srp, Ether, ICMP, IP

async def icmp_scan(target_ip):
    packet = Ether(dst="ff:ff:ff:ff:ff:ff") / IP(dst=target_ip) / ICMP()
    result = srp(packet, timeout=3, verbose=0)[0]

    devices = []
    for sent, received in result:
        devices.append({'ip': received[IP].src, 'mac': received[Ether].src})
    return devices

async def main():
    target_ip = "192.168.1.1/24"
    devices = await icmp_scan(target_ip)

    active_ips = [device['ip'] for device in devices]

    with open('active_ip.txt', 'w') as file:
        file.write('\n'.join(active_ips))

    print("Активные IP-адреса записаны в active_ip.txt")

if __name__ == "__main__":
    asyncio.run(main())
