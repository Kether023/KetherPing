import logging
import asyncio
import subprocess
import ipaddress
from puresnmp import get

logging.basicConfig(filename='snmp_errors.log', level=logging.ERROR, format='%(asctime)s [%(levelname)s]: %(message)s')

async def ping(ip):
    try:
        process = await asyncio.create_subprocess_exec(
            'ping', ip,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        await process.wait()
        return ip if process.returncode == 0 else None
    except Exception as e:
        logging.error(f"Error while pinging {ip}: {e}")
        return None

async def ping_ips(ips):
    results = []
    for ip in ips:
        try:
            result = await ping(ip)
            if result is not None:
                results.append(result)
        except Exception as e:
            logging.error(f"Error while processing {ip} in ping_ips: {e}")
    return results

# async def snmp_walk(ip, community='public', base_oid='.1.3.6.1.2.1'):
#     try:
#         full_oid_list = await get(ip, community, base_oid)
#         return [oid[0] for oid in full_oid_list]
#     except Exception as e:
#         logging.error(f"Error for {ip} in SNMP walk: {e}")
#         return None

async def get_all_oid(ip, community='public', base_oid='.1.3.6.1.2.1'):
    try:
        full_oid_list = await get(ip, community, base_oid)
        return [oid[0] for oid in full_oid_list]
    except Exception as e:
        logging.error(f"Error for {ip} in getting all OID: {e}")
        return None

async def main():
    start_ip = ipaddress.IPv4Address('10.0.94.1')
    end_ip = ipaddress.IPv4Address('10.0.98.255')
    ips_to_ping = [str(ip) for ip in range(int(start_ip), int(end_ip) + 1)]
    group_size = 10
    grouped_ips = [ips_to_ping[i:i + group_size] for i in range(0, len(ips_to_ping), group_size)]

    active_ips = []
    for group in grouped_ips:
        print(f"Pinging group: {group}")
        try:
            results = await ping_ips(group)
            active_ips.extend(results)
        except Exception as e:
            logging.error(f"Error while processing group {group} in main: {e}")

    with open('active_ip.txt', 'w') as active_file:
        active_file.write('\n'.join(filter(None, active_ips)))

    community_string = 'public'
    results_dict = {'CISCO': [], 'ELTEX': [], 'LINUX': [], 'UNKNOWN': []}

    for i in active_ips:
        current_ip = str(ipaddress.IPv4Address(i))
        print(f"Processing {current_ip}...")
        try:
            base_oid = '.1.3.6.1.2.1' 
            full_oid_list = await get_all_oid(current_ip, community_string, base_oid)
            print(f"Full OID list for {current_ip}: {full_oid_list}")

            grouped_oid_list = [full_oid_list[i:i + group_size] for i in range(0, len(full_oid_list), group_size)]

            for group_index, group in enumerate(grouped_oid_list):
                print(f"Processing group {group_index + 1} of OID for {current_ip}...")
                manufacturer = 'UNKNOWN'
                for oid in group:
                    last_digit = int(oid.split('.')[-1])
                    if 1 <= last_digit <= 3:
                        manufacturer = 'CISCO'
                    elif 4 <= last_digit <= 6:
                        manufacturer = 'ELTEX'
                    elif 7 <= last_digit <= 9:
                        manufacturer = 'LINUX'
                results_dict[manufacturer].append(current_ip)
        except Exception as e:
            logging.error(f"Error while processing {current_ip} in main: {e}")

    with open('snmp_results.txt', 'w') as file:
        for manufacturer, data in results_dict.items():
            file.write(f"[{manufacturer}]\n")
            for ip in data:
                file.write(f"{ip}\n")
            file.write("\n")

if __name__ == "__main__":
    asyncio.run(main())
