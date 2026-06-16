<p align="center">
  <h1 align="center">AdwanceSNI 2.0</h1>
  <p align="center">Next-gen network scanning & subdomain discovery suite</p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Go-1.20+-00ADD8?style=flat-square&logo=go&logoColor=white" alt="Go">
  <img src="https://img.shields.io/badge/Platform-Termux%20|%20Linux-00ff41?style=flat-square" alt="Platform">
  <img src="https://img.shields.io/badge/Version-2.0.4-red?style=flat-square" alt="Version">
</p>

---

### Overview

Enhanced evolution of AdwanceSNI. Integrates powerful engines and API-based subdomain discovery for bug bounty and network security.

### Features

- **Fast Subdomain Discovery** — Hybrid approach using APIs and Subfinder
- **Host Scanning** — Deep scanning with core modules
- **IP/Domain Extraction** — Clean and parse IP ranges
- **File Splitting** — Handle large datasets easily
- **Cross-Platform** — Optimized for Termux and Linux

### Installation

```bash
pkg update && pkg upgrade -y
pkg install git python golang zlib -y
```

```bash
echo 'export PATH="$PATH:$HOME/go/bin"' >> $HOME/.bashrc
source $HOME/.bashrc
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/SirYadav1/flashscan-go@latest
```

```bash
git clone https://github.com/SirYadav1/AdwanceSNI-2.0
cd AdwanceSNI-2.0
bash install.sh
```

### Usage

```bash
adwance
```

Or manually:

```bash
cd AdwanceSNI-2.0
bash run.sh
```

---

### Credits

| Role | Name |
|------|------|
| **Core Developer** | [YADAV](https://github.com/SirYadav1) |
| **Contributor** | Ayan Rajput |
| **Design** | Amith |

---

### Contact

- **Telegram:** [@SirYadav](https://t.me/SirYadav)
- **Email:** [siryadav025@gmail.com](mailto:siryadav025@gmail.com)
