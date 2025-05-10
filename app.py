import streamlit as st
import pickle
import pandas as pd

# Başlık ve açıklama
st.set_page_config(page_title="Kira Tahmin Uygulaması", layout="centered")
st.title("🏠 İstanbul Kira Tahmini")
st.markdown("Lütfen aşağıdaki alanları eksiksiz ve **Türkçe karakter kullanmadan** doldurunuz.")

# Modeli yükle (pipeline dahil)
model = pickle.load(open("kira_modeli.pkl", "rb"))

# Kullanıcıdan veri alma
st.subheader("📌 Girdi Bilgileri")

district = st.text_input("İlçe (ornek: Besiktas)", max_chars=30)
neighborhood = st.text_input("Mahalle (ornek: Levent)", max_chars=30)
room = st.number_input("Oda Sayısı", min_value=0, max_value=10, step=1)
living_room = st.number_input("Salon Sayısı", min_value=0, max_value=5, step=1)
area = st.number_input("Metrekare (m²)", min_value=10, max_value=1000, step=5)
age = st.number_input("Bina Yaşı", min_value=0, max_value=100, step=1)
floor = st.number_input("Bulunduğu Kat", min_value=-5, max_value=50, step=1)

# Türkçe karakter uyarısı
def contains_turkish(text):
    return any(char in "çğıöşüÇĞİÖŞÜ" for char in text)

if st.button("Kira Tahmin Et"):
    if contains_turkish(district) or contains_turkish(neighborhood):
        st.error("❌ Lütfen ilçe ve mahalle isimlerinde **Türkçe karakter** kullanmayınız!")
    else:
        # Modelin beklediği sütunlara uygun şekilde veri çerçevesi oluştur
        input_df = pd.DataFrame([{
            "district": district,
            "neighborhood": neighborhood,
            "room": room,
            "living_room": living_room,
            "area": area,
            "age": age,
            "floor": floor
        }])
        
        # Tahmin yap
        prediction = model.predict(input_df)
        st.success(f"💸 Tahmini Kira: {int(prediction[0])} TL")
