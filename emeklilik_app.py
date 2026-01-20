import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt

st.set_page_config(page_title="Emre Orman - Emeklilik Modeli", layout="wide")
st.title("📈 Aktüeryal Emeklilik Projeksiyonu")

# Veritabanı Bağlantısı
def get_qx_data(yas):
    try:
        conn = sqlite3.connect('hayat_sigortasi.db')
        query = f"SELECT yas, qx FROM trh2010 WHERE yas >= {yas}"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except:
        return pd.DataFrame({'yas': range(yas, 101), 'qx': [0.01] * (101-yas)})

# Sidebar
st.sidebar.header("Parametreler")
birikim = st.sidebar.number_input("Hedeflenen Birikim (TL)", min_value=100000, value=5000000, step=100000)
emeklilik_yasi = st.sidebar.slider("Emeklilik Yaşı", 45, 85, 65)
teknik_faiz = st.sidebar.slider("Yıllık Teknik Faiz (%)", 0.0, 15.0, 3.0) / 100
enflasyon = st.sidebar.slider("Beklenen Yıllık Enflasyon (%)", 0.0, 50.0, 10.0) / 100

# Aktüeryal Hesaplama
v = (1 + teknik_faiz) / (1 + enflasyon) - 1
if v == 0: v = 0.00001

df_qx = get_qx_data(emeklilik_yasi)
n = len(df_qx)
yillar = np.arange(n)
hayatta_kalma = (1 - df_qx['qx']).cumprod()
ax = sum(hayatta_kalma * ((1 + v)**-yillar))

baslangic_maasi = (birikim / ax) / 12

# Metrikler
col1, col2 = st.columns(2)
col1.metric("İlk Emekli Maaşı (Aylık)", f"{baslangic_maasi:,.2f} TL")
col2.metric("Reel Faiz Oranı", f"%{v*100:.2f}")

# ZAMAN ETKİSİ GRAFİĞİ
st.subheader("📊 Zamanın Etkisi: Enflasyon Altında Maaş Seyri")
gelecek_maaslar = [baslangic_maasi * ((1 + enflasyon)**t) for t in range(n)]

fig, ax_plot = plt.subplots(figsize=(10, 4))
ax_plot.plot(df_qx['yas'], gelecek_maaslar, color='#2ecc71', linewidth=2)
ax_plot.fill_between(df_qx['yas'], gelecek_maaslar, alpha=0.2, color='#2ecc71')
ax_plot.set_xlabel("Yaş")
ax_plot.set_ylabel("Maaş (TL)")
st.pyplot(fig)

st.info("Bu modelde maaşınız her yıl enflasyon oranında artırılarak alım gücünüz korunmaktadır.")
