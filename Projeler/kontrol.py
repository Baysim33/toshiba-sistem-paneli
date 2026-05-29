import os
import psutil
import requests
import time

# Renk kodları (Terminali canlandırmak için)
YESIL = '\033[92m'
SARI = '\033[93m'
KIRMIZI = '\033[91m'
MAVI = '\033[94m'
SIFIRLA = '\033[0m'

def bar_ciz(yuzde):
    # %100'lük sistemi 20 blokluk bir çubuğa indirgiyoruz
    blok_sayisi = int(yuzde / 5)
    bar = '■' * blok_sayisi + ' ' * (20 - blok_sayisi)
    
    # Kullanım oranına göre renk belirleme
    if yuzde < 50:
        renk = YESIL
    elif yuzde < 80:
        renk = SARI
    else:
        renk = KIRMIZI
        
    return f"[{renk}{bar}{SIFIRLA}] %{yuzde}"

# Dış IP'yi her saniye sorgulamamak için döngünün dışında bir kere çekiyoruz
try:
    ip_bul = requests.get("https://api.ipify.org", timeout=5).text
except:
    ip_bul = "Bağlantı Yok / Engellendi"

# Anlık Port Taraması Fonksiyonu
def port_kontrol():
    import socket
    kritik_portlar = [21, 22, 80, 443, 8080]
    aciklar = []
    for port in kritik_portlar:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.2)
        if s.connect_ex(('127.0.0.1', port)) == 0:
            aciklar.append(port)
        s.close()
    return aciklar

# CANLI DÖNGÜ BAŞLIYOR (Ctrl + C ile durdurana kadar döner)
try:
    while True:
        print("\033[H", end="") # İmleci en üste taşır
        
        print(f"{MAVI}============================================={SIFIRLA}")
        print(f"{MAVI}       TOSHIBA CANLI SİSTEM PANELİ           {SIFIRLA}")
        print(f"{MAVI}============================================={SIFIRLA}\n")
        
        islemci = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory().percent
        
        print(f"İşlemci Yükü : {bar_ciz(islemci)}")
        print(f"RAM Kullanımı: {bar_ciz(ram)}")
        print(f"\nGüvenli IP   : {YESIL}{ip_bul}{SIFIRLA}")
        
        print(f"\n{MAVI}---------------------------------------------{SIFIRLA}")
        acik_portlar = port_kontrol()
        if acik_portlar:
            print(f"{KIRMIZI}UYARI: Açık Portlar Yakalandı! -> {acik_portlar}{SIFIRLA}")
        else:
            print(f"Siber Kalkan : {YESIL}AKTİF (Kritik Portlar Kapalı){SIFIRLA}")
        print(f"{MAVI}---------------------------------------------{SIFIRLA}")
        print("\n[Paneli kapatmak için Ctrl + C tuşlarına bas]")
        
        time.sleep(2)

except KeyboardInterrupt:
    print(f"\n{SARI}Panelden çıkış yapıldı. Güvenli günler reis!{SIFIRLA}")
