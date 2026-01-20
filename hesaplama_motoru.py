import numpy as np
import pandas as pd

def hayatta_kalma_olasiligi(su_an_yas, hedef_yas):
    # Basit bir aktüeryal varsayım: Her yıl ölüm riski yaşla birlikte %1 artar
    # (Gerçekte bu tablolar resmi kurumlarca yayınlanır)
    yillar = hedef_yas - su_an_yas
    olasilik = 1.0
    for i in range(yillar):
        # Yaşlandıkça hayatta kalma ihtimali azalıyor
        risk = (su_an_yas + i) / 120 
        olasilik *= (1 - risk)
    return olasilik

# Örnek: 30 yaşındaki birinin 65 yaşına kadar hayatta kalma ihtimali
yas30 = 30
emeklilik_yasi = 65
sans = hayatta_kalma_olasiligi(yas30, emeklilik_yasi)

print(f"{yas30} yasindaki birinin {emeklilik_yasi} yasina kadar hayatta kalma ihtimali: %{sans*100:.2f}")