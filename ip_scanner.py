import socket
import subprocess
from datetime import datetime

# ports that are common on websites / servers
ports = [21, 22, 80, 443, 3306]

# what usually runs on those ports
services = {
    21: "FTP",
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    3306: "MySQL"
}

timeout = 1


def get_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        print("Could not resolve the domain.")
        exit(1)


def check_ports(ip):
    open_ports = []

    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        if sock.connect_ex((ip, port)) == 0:
            print(f"Port {port} open")
            open_ports.append(port)
        else:
            print(f"Port {port} closed")

        sock.close()

    return open_ports


def nmap_scan(domain):
    result = subprocess.run(
        ["nmap", "-Pn", domain],
        capture_output=True,
        text=True
    )
    return result.stdout


def save_report(domain, ip, open_ports, nmap_result):
    with open("report.txt", "w") as f:
        f.write("Website scan report\n")
        f.write(f"Date: {datetime.now()}\n\n")

        f.write(f"Domain: {domain}\n")
        f.write(f"IP: {ip}\n\n")

        f.write("Open ports:\n")
        if open_ports:
            for port in open_ports:
                name = services.get(port, "Unknown")
                f.write(f"{port} - {name}\n")
        else:
            f.write("None\n")

        f.write("\nNmap result:\n")
        f.write(nmap_result)


def main():
    print("Simple scanner\n")

    domain = input("Domain: ").strip()

    ip = get_ip(domain)
    print(f"IP: {ip}\n")

    open_ports = check_ports(ip)

    print("\nRunning nmap...\n")
    nmap_result = nmap_scan(domain)

    save_report(domain, ip, open_ports, nmap_result)

    print("Done. Check report.txt")


main()
