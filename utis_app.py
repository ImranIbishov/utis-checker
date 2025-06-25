import streamlit as st
import pandas as pd

# Başlıq
st.set_page_config(page_title="UTİS Yoxlama Sistemi", page_icon="✅")
st.title("📘 UTİS Yoxlama Sistemi")
st.markdown("Zəhmət olmasa UTİS kodunu daxil edin:")

# Faylı yüklə
@st.cache_data
def load_data():
    df = pd.read_excel("42 nömrəli məktəb_lisey qebul.xlsx")
    df.columns = df.columns.str.strip()
    df['UTİS kodu'] = df['UTİS kodu'].astype(str).str.strip()
    return df

data = load_data()

# Kod daxil etmə
code = st.text_input("UTİS kodu", max_chars=10)

# Sessiyada saxlanılan yoxlanmış kodlar
if "checked_codes" not in st.session_state:
    st.session_state.checked_codes = set()

# Yoxla düyməsi
if st.button("Yoxla ✅"):
    if not code.strip():
        st.warning("Zəhmət olmasa UTİS kodunu daxil edin!")
    else:
        result = data[data['UTİS kodu'] == code.strip()]
        if not result.empty:
            student = result.iloc[0]
            info = (
                f"**👤 Ad Soyad:** {student['Ad']} {student['Soyad']}\n\n"
                f"**🧑‍🦱 Ata adı:** {student['Ata adı']}\n\n"
                f"**🏫 Sinif:** {student['Sinif']}\n"
                f"**📚 Kitabça dili:** {student['Kitabça dili']}\n"
                f"**🏷️ Mərkəz:** {student['Qısa ad']}\n"
                f"**📍 Otaq:** {student['Otaq']}, **Yer:** {student['Yer']}"
            )
            if code in st.session_state.checked_codes:
                st.error("⚠ Bu şagird artıq yoxlanılıb!")
                st.info(info)
            else:
                st.session_state.checked_codes.add(code)
                st.success("✅ Şagird tapıldı!")
                st.info(info)
        else:
            st.error("❌ Bu UTİS kodu siyahıda yoxdur.")
