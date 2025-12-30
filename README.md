## AdwanceSNI-2.0
AdwanceSNI 2.0 is the enhanced version of the original AdwanceSNI program, designed to provide a comprehensive suite for network scanning and subdomain discovery. It retains the core functionalities of finding subdomains and scanning hosts while introducing new tools for IP extraction, IP generation, and a lite scanner.


<strong><em>AdwanceSNI 2.0 is built using advanced prebuilt tools – FlashScan-Go, normal scanner, and subdomain discovery (API). These tools handle subdomain discovery and host scanning, forming the core of the project.</em></strong>

<strong><em>Credit goes to Ayan Rajput for his valuable contributions🤝.</em></strong>



## Installation commands 🔗
```shell
termux-setup-storage
```
 ```shell
pkg update && pkg upgrade -y
```
 ```shell
pkg install golang -y
```
```shell 
pkg install python-pip -y
```
 ```shell 
pkg install zlib -y
```

```shell
pkg install git
```

# Add Go to PATH

```shell
echo 'PATH="$PATH:$HOME/go/bin"' >> $HOME/.bashrc
source $HOME/.bashrc
```

# Install subfinder and flashscan-go

```shell 
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```

```shell
go install -v github.com/SirYadav1/flashscan-go@latest
```

# Clone the repository

 ```shell 
git clone https://github.com/SirYadav1/AdwanceSNI-2.0
```

## Usage 📌
 
```shell
cd AdwanceSNI-2.0
```
# Install requirements
```shell
bash install.sh
```
# Run program by bash 
```shell
bash run.sh
```

## Author Information

**Author**: YADAV<br>
**Tools**: Normal Scanner, Subdomain API – by Ayan Rajput
**Coded by**: YADAV  
**Design by**: Amith<br>
**Contact**: siryadav025@gamil.com<br>
**Telegram**: [@SirYadav](https://t.me/SirYadav)  
**Version**: 2.0.4
