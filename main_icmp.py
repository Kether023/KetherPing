import random

def mock_snmp_walk(ip, community='public', oid='.1.3.6.1.2.1.1.1.0'):
    # Случайный выбор цифры от 1 до 4
    manufacturer_code = random.randint(1, 4)
    
    # Зависимость от выбранной цифры
    if manufacturer_code == 1:
        manufacturer = 'CISCO'
    elif manufacturer_code == 2:
        manufacturer = 'ELTEX'
    elif manufacturer_code == 3:
        manufacturer = 'LINUX'
    else:
        manufacturer = 'UNKNOWN'

    return manufacturer, ip

def main():
    start_ip = '10.0.94.1'
    end_ip = '10.0.98.254'
    community_string = 'public'

    # Создаем словарь для хранения результатов
    results_dict = {'CISCO': [], 'ELTEX': [], 'LINUX': [], 'UNKNOWN': []}

    for i in range(int(start_ip.split('.')[-1]), int(end_ip.split('.')[-1]) + 1):
        current_ip = f"{start_ip.rsplit('.', 1)[0]}.{i}"
        print(f"Processing {current_ip}...")

        # Получаем результаты
        manufacturer, ip = mock_snmp_walk(current_ip, community_string)

        # Добавляем IP в соответствующий раздел словаря
        results_dict[manufacturer].append(ip)

    # Записываем результаты в файл
    with open('snmp_results.txt', 'w') as file:
        for manufacturer, data in results_dict.items():
            file.write(f"[{manufacturer}]\n")
            for ip in data:
                file.write(f"{ip}\n")
            file.write("\n")

if __name__ == "__main__":
    main()
