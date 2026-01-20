import sqlite3
import pandas as pd
import numpy as np

# 1. Yaşlara göre ölüm olasılıklarını (qx) oluşturalım
# Not: Yaş arttıkça ölüm riski logaritmik olarak artar.
yaslar = np.arange(0, 101)
# Basit bir Gompertz modeli:
olum_olasiliklari = 0.0001 * (1.1 ** yaslar)
olum_olasiliklari = np.clip(olum_olasiliklari, 0, 1) # 1'den büyük olamaz

df_mortalite = pd.DataFrame({
    'yas': yaslar,
    'qx': olum_olasiliklari # qx: o yaşta ölme olasılığı
})

# 2. SQLite Veritabanına Kaydet
conn = sqlite3.connect('hayat_sigortasi.db')
df_mortalite.to_sql('mortalite_tablosu', conn, if_exists='replace', index=False)
conn.close()

print("Mortalite tablosu başarıyla 'hayat_sigortasi.db' içine kaydedildi!")