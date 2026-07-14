#!/usr/bin/env python3
"""
portscan.py - Simple TCP port range scanner using python-nmap.

Setup (Kali/Debian-based):
    sudo apt install python3-pip
    pip install python-nmap

Usage:
    python3 portscan.py
    python3 portscan.py -t 10.0.0.5 -p 20-100
"""

import argparse
import re
import sys

import nmap
print(nmap.__version__)

IP_PATTERN = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$")
PORT_RANGE_PATTERN = re.compile(r"^(\d+)-(\d+)$")

BANNER = r"""
 ____            _   ____                  
|  _ \ ___  _ __| |_/ ___|  ___ __ _ _ __  
| |_) / _ \| '__| __\___ \ / __/ _` | '_ \ 
|  __/ (_) | |  | |_ ___) | (_| (_| | | | |
|_|   \___/|_|   \__|____/ \___\__,_|_| |_|

  Brahmjot's Port Scanner - built on python-nmap
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


def scan_range(target: str, port_min: int, port_max: int) -> dict:
    """
    Scan a single target across [port_min, port_max] inclusive.
    Returns a dict of {port: state}. Ports that couldn't be read
    (filtered/no response/parse issue) are marked 'unknown'.
    """
    scanner = nmap.PortScanner()
    results = {}

    for port in range(port_min, port_max + 1):
        try:
            scan_result = scanner.scan(target, str(port))
            state = scan_result["scan"][target]["tcp"][port]["state"]
        except KeyError:
            # Host didn't return data for this port (commonly filtered/no reply)
            state = "unknown"
        except Exception as exc:
            print(f"  [!] Error scanning port {port}: {exc}", file=sys.stderr)
            state = "error"

        results[port] = state
        print(f"  Port {port:>5}: {state}")

    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Basic TCP port range scanner (python-nmap wrapper).")
    parser.add_argument("-t", "--target", help="Target IPv4 address")
    parser.add_argument("-p", "--ports", help="Port range as <low>-<high>, e.g. 20-100")
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

    print(f"\nScanning {target} on ports {port_min}-{port_max}...\n")
    results = scan_range(target, port_min, port_max)

    open_ports = [p for p, s in results.items() if s == "open"]
    print(f"\nDone. {len(open_ports)} open port(s): {open_ports if open_ports else 'none'}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScan interrupted by user.")
        sys.exit(1)
