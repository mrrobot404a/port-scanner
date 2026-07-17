# Port Scanner

What is a port scanner?
It's a tool that checks which network ports on a host are open, closed or filtered to determine what services are available and accessible

I have made 2 basic versions of a port scanner below:

- **`portscan_socket_method.py`** — pure Python, uses the built-in `socket` module. No external dependencies. Shows how TCP connect scanning works.
- **`portscan.py`** — uses the `python-nmap` library to access the Nmap scanning engine for more in depth scanning and service detection.

This was built to understand what a port scanner does and the difference between one made from scratch compared to another which uses industry-standard tools like Nmap.

## Comparison

| **Feature**               | **Socket Version**   |   **Nmap Version**     |
| :------------------------ | :----------------:   | :------------------:   |
| Built with Python sockets |        ✅ Yes       |         ❌ No          |
| External dependencies     |        None          | Nmap + `python-nmap`   |
| TCP connect scanning      |        ✅ Yes       |         ✅ Yes         |
| Service detection         |        ❌ No        |         ✅ Yes         |
| OS detection              |        ❌ No        |         ✅ Yes         |
| Best for learning         |     ✅ Excellent    |      ❌ Not ideal      |
| Fast scanning             |     ⚠️ Limited      |        ✅ Fast         |


## Setup

### Socket version (no dependencies)
Just needs Python, but i used the latestversion which was 3.9+ (uses type hints like `tuple[int, int]`).

```bash
python portscan_socket_method.py
```

### Nmap version
Requires Nmap itself to be installed, plus the Python wrapper.

**Windows:**
1. Nmap link: https://nmap.org/download.html#windows (accept the Npcap prompt during install)
2. `pip install python-nmap`

**Linux (Debian/Kali/Ubuntu):** (I have not tried this on Linux, so I can't guarantee that it will work)
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
