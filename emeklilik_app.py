import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt

# 1. Sayfa Konfigürasyonu
st.set_page_config(page_title="Emre Orman | Actuarial Suite", layout="wide")

# CSS ile Modern Tasarım
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }
    .stMetric { background-color: #1f2937; padding: 20px; border-radius: 12px; border-bottom: 4px solid #10b981; }
    .main { background-color: #0e1117; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Aktüeryal Emeklilik Projeksiyonu")
st.markdown("---")

# Veri Fonksiyonu
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
with st.sidebar:
    st.header("📊 Model Parametreleri")
    birikim = st.number_input("Hedeflenen Birikim (TL)", min_value=100000, value=5000000, step=100000)
    emeklilik_yasi = st.slider("Emeklilik Yaşı", 45, 85, 65)
    st.markdown("---")
    teknik_faiz = st.slider("Teknik Faiz (%)", 0.0, 15.0, 3.0) / 100
    enflasyon = st.slider("Enflasyon (%)", 0.0, 50.0, 10.0) / 100

# Hesaplama
v = (1 + teknik_faiz) / (1 + enflasyon) - 1
if v == 0: v = 0.00001

df_qx = get_qx_data(emeklilik_yasi)
n = len(df_qx)
hayatta_kalma = (1 - df_qx['qx']).cumprod()
ax = sum(hayatta_kalma * ((1 + v)**-np.arange(n)))
baslangic_maasi = (birikim / ax) / 12

# Metrikler
c1, c2, c3 = st.columns(3)
c1.metric("İlk Maaş (Aylık)", f"{baslangic_maasi:,.2f} TL")
c2.metric("Reel Getiri (v)", f"%{v*100:.2f}")
c3.metric("Projeksiyon Süresi", f"{n} Yıl")

# Grafik
st.subheader("📈 Maaşın Zaman İçindeki Gelişimi (Enflasyon Endeksli)")
gelecek_maaslar = [baslangic_maasi * ((1 + enflasyon)**t) for t in range(n)]

plt.style.use('dark_background')
fig, ax_plot = plt.subplots(figsize=(12, 5))
ax_plot.plot(df_qx['yas'], gelecek_maaslar, color='#10b981', linewidth=3, label="Nominal Maaş")
ax_plot.fill_between(df_qx['yas'], gelecek_maaslar, alpha=0.15, color='#10b981')
ax_plot.set_xlabel("Yaş")
ax_plot.set_ylabel("Maaş (TL)")
ax_plot.grid(alpha=0.1)
st.pyplot(fig)

st.info("Hesaplamalar TRH-2010 mortalite tablosu ve enflasyon projeksiyonuna göre yapılmıştır.")
