# Port Scanner

A simple TCP port range scanner, built two ways to compare approaches:

- **`portscan_socket_method.py`** — pure Python, uses the built-in `socket` module. No external dependencies.
- **`portscan.py`** — wraps [Nmap](https://nmap.org/) via the `python-nmap` library, for richer scan data (service/version detection where available).

Built as a learning project to understand what a port scanner actually does under the hood (raw sockets) versus using an industry-standard tool (Nmap) through Python.

## Why two versions?

The socket version shows the fundamentals — opening a TCP connection and checking if it succeeds. The nmap version shows how to work with a professional scanning engine from Python, which is closer to what's used in real security tooling.

## Setup

### Socket version (no dependencies)
Just needs Python 3.9+ (uses type hints like `tuple[int, int]`).

```bash
python portscan_socket_method.py
```

### Nmap version
Requires Nmap itself to be installed, plus the Python wrapper.

**Windows:**
1. Install Nmap: https://nmap.org/download.html#windows (accept the Npcap prompt during install)
2. `pip install python-nmap`

**Linux (Debian/Kali/Ubuntu):**
```bash
sudo apt install nmap python3-pip
pip install python-nmap
```

Then run:
```bash
python portscan.py
```

## Usage

Both scripts support interactive prompts or command-line flags:

```bash
# Interactive
python portscan_socket_method.py

# With flags
python portscan_socket_method.py -t 10.0.0.5 -p 20-100
python portscan_socket_method.py -t 10.0.0.5 -p 20-100 --timeout 1.0
```

| Flag | Description |
|------|-------------|
| `-t`, `--target` | Target IPv4 address |
| `-p`, `--ports` | Port range as `<low>-<high>`, e.g. `20-100` |
| `--timeout` | (Socket version only) per-port timeout in seconds, default `0.5` |

## Example output

```
Scanning 45.33.32.156 on ports 20-100 (timeout=0.5s)...

  Port    20: closed
  Port    22: open
  Port    80: open
  ...

Done. 2 open port(s): [22, 80]
```

## ⚠️ Legal notice

Only scan systems you own or have explicit permission to test. Scanning networks or hosts without authorization is illegal in most jurisdictions. Good targets for practice:

- `127.0.0.1` (localhost)
- Your own router/LAN devices
- Virtual machines in your own lab (e.g. Metasploitable)
- [scanme.nmap.org](https://nmap.org/) — Nmap's official public test target

## Roadmap / future improvements

- [ ] Multithreading for faster scans across large port ranges
- [ ] Full-range scan support in a single Nmap call instead of per-port loop
- [ ] Export results to CSV/JSON
- [ ] Basic service banner grabbing

## License

See [LICENSE](LICENSE).
