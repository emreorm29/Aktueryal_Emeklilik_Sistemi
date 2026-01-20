import sqlite3
import pandas as pd

def emeklilik_maas_katsayisi(emeklilik_yasi, teknik_faiz=0.04):
    """
    Bu fonksiyon, emeklilikten sonraki her 1 TL'lik maaşın 
    bugünkü maliyetini hesaplar (Aktüeryal Anüite).
    """
    conn = sqlite3.connect('hayat_sigortasi.db')
    # Emeklilik yaşından 100 yaşına kadar olan riskleri çek
    query = f"SELECT yas, qx FROM mortalite_tablosu WHERE yas >= {emeklilik_yasi}"
    df = pd.read_sql(query, conn)
    conn.close()
    
    bugunku_deger = 0
    hayatta_kalma_ihtimale = 1.0
    
    for i, row in df.iterrows():
        t = i # Emeklilikten sonra geçen yıl sayısı
        # Gelecekteki parayı bugüne indirge (Finansal Matematik)
        iskonto_faktoru = 1 / ((1 + teknik_faiz) ** t)
        
        # O yıl maaş alabilmesi için hayatta olması lazım
        bugunku_deger += hayatta_kalma_ihtimale * iskonto_faktoru
        
        # Bir sonraki yıl için hayatta kalma ihtimalini güncelle
        hayatta_kalma_ihtimale *= (1 - row['qx'])
        
    return bugunku_deger

# --- TEST PANELİ ---
birikim = 1000000 # Diyelim ki 1 Milyon TL biriktirdin
emeklilik_yasi = 65

katsayi = emeklilik_maas_katsayisi(emeklilik_yasi)
yillik_maas = birikim / katsayi

print(f"--- EMEKLİLİK PROJEKSİYONU ---")
print(f"Toplam Birikim: {birikim:,.2f} TL")
print(f"Emeklilik Yaşı: {emeklilik_yasi}")
print(f"Alabileceğiniz Yıllık Maaş: {yillik_maas:,.2f} TL")
print(f"Aylık Maaş Karşılığı: {yillik_maas/12:,.2f} TL")