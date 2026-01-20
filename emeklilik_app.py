import streamlit as st
import pandas as pd
import sqlite3
import numpy as np
import matplotlib.pyplot as plt

# Sayfa Yapılandırması
st.set_page_config(page_title="Emre Orman | Aktueryal Emeklilik", layout="wide")

def emeklilik_motoru(emeklilik_yasi, birikim, teknik_faiz):
    conn = sqlite3.connect('hayat_sigortasi.db')
    query = f"SELECT yas, qx FROM mortalite_tablosu WHERE yas >= {emeklilik_yasi}"
    df = pd.read_sql(query, conn)
    conn.close()
    
    bugunku_deger = 0
    hayatta_kalma_ihtimali = 1.0
    projeksiyon = []
    
    for i, row in df.iterrows():
        t = i
        iskonto = 1 / ((1 + teknik_faiz) ** t)
        bugunku_deger += hayatta_kalma_ihtimali * iskonto
        
        # Grafik için verileri topla
        projeksiyon.append({
            'Yas': row['yas'],
            'Hayatta_Kalma_%': hayatta_kalma_ihtimali * 100,
            'Paranin_Degeri': iskonto
        })
        hayatta_kalma_ihtimali *= (1 - row['qx'])
        
    return bugunku_deger, pd.DataFrame(projeksiyon)

# --- ARAYÜZ ---
st.title("🛡️ Aktüeryal Emeklilik ve Yaşam Planlayıcı")
st.markdown("Bu sistem, **TRH-2010 Mortalite Tablosu** verilerini kullanarak finansal gelecek tahmini yapar.")

with st.sidebar:
    st.header("Parametreler")
    mevcut_yas = st.slider("Mevcut Yaşınız", 18, 60, 30)
    emeklilik_yasi = st.slider("Emeklilik Hedef Yaşı", 55, 80, 65)
    birikim = st.number_input("Hedeflenen Toplam Birikim (TL)", 100000, 10000000, 1000000, step=50000)
    teknik_faiz = st.slider("Yıllık Teknik Faiz (%)", 1.0, 10.0, 4.0) / 100

if st.button("Emeklilik Planını Oluştur"):
    katsayi, df_grafik = emeklilik_motoru(emeklilik_yasi, birikim, teknik_faiz)
    yillik_maas = birikim / katsayi
    aylik_maas = yillik_maas / 12
    
    # Metrikler
    c1, c2, c3 = st.columns(3)
    c1.metric("Anüite Katsayısı", f"{katsayi:.2f}")
    c2.metric("Tahmini Aylık Maaş", f"{aylik_maas:,.2f} TL")
    c3.metric("Yaşam Beklentisi (Emeklilikten Sonra)", f"{len(df_grafik)} Yıl")
    
    st.divider()
    
    # Grafikler
    col_sol, col_sag = st.columns(2)
    
    with col_sol:
        st.subheader("⏳ Yaşlandıkça Hayatta Kalma Olasılığı")
        st.line_chart(df_grafik.set_index('Yas')['Hayatta_Kalma_%'])
        st.caption("Bu grafik, seçtiğiniz emeklilik yaşından itibaren yaşam olasılığınızın azalışını gösterir.")
        
    with col_sag:
        st.subheader("📉 Paranın Zaman Değeri (İskonto)")
        st.area_chart(df_grafik.set_index('Yas')['Paranin_Degeri'])
        st.caption("Gelecekteki 1 TL'nin bugün aslında ne kadar ettiğini gösteren finansal değer kaybı.")

    st.success(f"Analiz Tamamlandı: {emeklilik_yasi} yaşında emekli olursanız, paranın zaman değerine ve mortalite riskine göre aylık net maaşınız hesaplanmıştır.")