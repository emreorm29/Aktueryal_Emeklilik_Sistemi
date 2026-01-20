# Aktüeryal Emeklilik Hesaplayıcı 📈
Bu proje, Arch Linux üzerinde Python ve Streamlit kullanılarak geliştirilmiş bir emeklilik projeksiyonu uygulamasıdır.

## Özellikler
- **TRH-2010 Mortalite Tablosu:** SQLite veritabanı üzerinden gerçek ölüm olasılıkları kullanılır.
- **Teknik Faiz Analizi:** Paranın zaman değerine göre maaş hesaplaması.
- **İhtiyatlılık İlkesi:** Düşük riskli teknik faiz varsayımları ile güvenli emeklilik planlaması.

## Kurulum
1. `python -m venv venv`
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`
4. `streamlit run emeklilik_app.py`
