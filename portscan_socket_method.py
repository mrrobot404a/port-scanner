#!/usr/bin/env python3
"""
portscan_socket_method.py - basic TCP port range scanner using raw sockets.
 
No external dependencies - works on Windows, Linux, or macOS as long as
you have Python 3 installed. Nothing extra to pip install.
 
Usage:
    python portscan_socket_method.py
    python portscan_socket_method.py -t 10.0.0.5 -p 20-100
"""
 
import argparse
import re
import socket
import sys
 
IP_PATTERN = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$")
PORT_RANGE_PATTERN = re.compile(r"^(\d+)-(\d+)$")
 
BANNER = r"""
 ____            _   ____                  
|  _ \ ___  _ __| |_/ ___|  ___ __ _ _ __  
| |_) / _ \| '__| __\___ \ / __/ _` | '_ \ 
|  __/ (_) | |  | |_ ___) | (_| (_| | | | |
|_|   \___/|_|   \__|____/ \___\__,_|_| |_|
 
  Brahmjot's Port Scanner - raw socket edition
"""
 
 
def prompt_ip() -> str:
    """Keep asking until a valid IPv4 address is entered."""
    while True:
        ip = input("Target IP address: ").strip()
        if IP_PATTERN.match(ip):
            return ip
        print("That doesn't look like a valid IPv4 address, try again.")
 
 
def prompt_port_range() -> tuple[int, int]:
    """Keep asking until a valid <low>-<high> port range is entered."""
    while True:
        raw = input("Port range (e.g. 20-100): ").strip().replace(" ", "")
        match = PORT_RANGE_PATTERN.match(raw)
        if not match:
            print("Format must be <int>-<int>, e.g. 60-120.")
            continue
        low, high = int(match.group(1)), int(match.group(2))
        if 0 <= low <= high <= 65535:
            return low, high
        print("Ports must be between 0-65535, with low <= high.")
 
 
def scan_port(target: str, port: int, timeout: float = 0.5) -> str:
    """
    Attempt a TCP connection to a single port.
    Returns 'open', 'closed', or 'filtered' (timed out / unreachable).
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        try:
            result = sock.connect_ex((target, port))
            return "open" if result == 0 else "closed"
        except socket.timeout:
            return "filtered"
        except OSError as exc:
            print(f"  [!] Error on port {port}: {exc}", file=sys.stderr)
            return "error"
 
 
def scan_range(target: str, port_min: int, port_max: int, timeout: float = 0.5) -> dict:
    """
    Scan a single target across [port_min, port_max] inclusive.
    Returns a dict of {port: state}.
    """
    results = {}
    for port in range(port_min, port_max + 1):
        state = scan_port(target, port, timeout)
        results[port] = state
        print(f"  Port {port:>5}: {state}")
    return results
 
 
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Basic TCP port range scanner (raw socket version).")
    parser.add_argument("-t", "--target", help="Target IPv4 address")
    parser.add_argument("-p", "--ports", help="Port range as <low>-<high>, e.g. 20-100")
    parser.add_argument(
        "--timeout",
        type=float,
        default=0.5,
        help="Per-port connection timeout in seconds (default: 0.5)",
    )
    return parser.parse_args()
 
 
def main() -> None:
    print(BANNER)
    args = parse_args()
 
    target = args.target if args.target and IP_PATTERN.match(args.target) else prompt_ip()
 
    if args.ports and PORT_RANGE_PATTERN.match(args.ports.replace(" ", "")):
        low_str, high_str = PORT_RANGE_PATTERN.match(args.ports.replace(" ", "")).groups()
        port_min, port_max = int(low_str), int(high_str)
    else:
        port_min, port_max = prompt_port_range()
 
    print(f"\nScanning {target} on ports {port_min}-{port_max} (timeout={args.timeout}s)...\n")
    results = scan_range(target, port_min, port_max, args.timeout)
 
    open_ports = [p for p, s in results.items() if s == "open"]
    print(f"\nDone. {len(open_ports)} open port(s): {open_ports if open_ports else 'none'}")
 
 
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScan interrupted by user.")
        sys.exit(1)