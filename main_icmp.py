import logging
from pysnmp.hlapi import SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity, getCmd

# Configure the logging module
logging.basicConfig(filename='snmp_errors.log', level=logging.ERROR, format='%(asctime)s [%(levelname)s]: %(message)s')

def snmp_walk(ip, community='public', oid='.1.3.6.1.2.1.1.1.0'):
    results = []
    try:
        error_indication, error_status, error_index, var_binds = next(
            getCmd(SnmpEngine(),
                CommunityData(community),
                UdpTransportTarget((ip, 161)),
                ContextData(),
                ObjectType(ObjectIdentity(oid)),
                ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))
        )

        if error_indication:
            raise Exception(f"Error: {error_indication}")
        elif error_status:
            raise Exception(f"Error: {error_status.prettyPrint()}")
        else:
            for var_bind in var_binds:
                results.append((var_bind[0].prettyPrint(), var_bind[1].prettyPrint()))

    except Exception as e:
        logging.error(f"Error processing {ip}: {str(e)}")
    
    return results

def mock_snmp_walk(ip, community='public', oid='.1.3.6.1.2.1.1.1.0'):
    mock_results = [
        ('1.3.6.1.2.1.1.1.0', 'Mock System Description'),
        ('1.3.6.1.2.1.2.2.1.2.1', 'Mock Interface 1 Description'),
    ]
    return mock_results

def main():
    start_ip = '10.0.94.1'
    end_ip = '10.0.98.254'
    community_string = 'public'

    with open('snmp_results.txt', 'w') as file:
        for i in range(int(start_ip.split('.')[-1]), int(end_ip.split('.')[-1]) + 1):
            current_ip = f"{start_ip.rsplit('.', 1)[0]}.{i}"
            print(f"Processing {current_ip}...")

            # results = snmp_walk(current_ip, community_string)
            results = mock_snmp_walk(current_ip, community_string)

            file.write(f"Results for {current_ip}:\n")
            for oid, value in results:
                file.write(f"OID: {oid}, Value: {value}\n")
            file.write("\n")

if __name__ == "__main__":
    main()
