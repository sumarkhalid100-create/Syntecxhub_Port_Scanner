import socket
import threading
import os

open_ports = []


def scan_port(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((host, port))

        if result == 0:
            print(f"[+] Port {port}: OPEN")
            open_ports.append(port)

        s.close()
    except Exception:
        pass


def start_scan(host, start_port, end_port):
    print(f"\nStarting scan on host: {host}")
    print(f"Scanning ports {start_port} through {end_port}...\n")

    threads = []
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(host, port))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


if __name__ == "__main__":
    target_host = input("Enter the IP address to scan (e.g., 127.0.0.1): ")

    start_p = int(input("Start Port (e.g., 1): "))
    end_p = int(input("End Port (e.g., 50): "))

    start_scan(target_host, start_p, end_p)
    print("\nScan complete.")

    # --- FIND AND SAVE THE FILE ---
    file_location = os.path.abspath("scan_results.txt")

    print(f"\nSaving results EXACTLY here:\n---> {file_location}")

    with open(file_location, "w") as file:
        file.write(f"Scan Results for IP: {target_host}\n")
        file.write("-" * 30 + "\n")
        if open_ports:
            for p in open_ports:
                file.write(f"Port {p}: OPEN\n")
        else:
            file.write("No open ports found.\n")

    print("\nResults saved successfully!")