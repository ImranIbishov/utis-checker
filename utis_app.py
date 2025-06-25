import streamlit as st
import pandas as pd

# Səhifə başlığı və ikon
st.set_page_config(page_title="UTİS Yoxlama Sistemi", page_icon="✅")
st.title("📘 UTİS Yoxlama Sistemi")
st.markdown("Zəhmət olmasa aşağıya UTİS kodunu daxil edin:")

# Excel faylını oxu
@st.cache_data
def load_data():
    df = pd.read_excel("42_mekteb_qebul.xlsx")  # Fayl adını uyğunlaşdır
    df.columns = df.columns.str.strip()
    df['UTİS kodu'] = df['UTİS kodu'].astype(str).str.strip()
    return df

data = load_data()

# Sessiya dəyişənləri
if "checked_codes" not in st.session_state:
    st.session_state.checked_codes = set()
if "approved_students" not in st.session_state:
    st.session_state.approved_students = []

# UTİS kodu daxil edilən yer
code = st.text_input("🔢 UTİS kodunu daxil edin", max_chars=10)

# Yoxla düyməsi
if st.button("🔍 Yoxla"):
    if not code.strip():
        st.warning("⚠ Zəhmət olmasa UTİS kodunu daxil edin!")
    else:
        result = data[data['UTİS kodu'] == code.strip()]
        if not result.empty:
            student = result.iloc[0]
            info = (
                f"👤 **Ad Soyad:** {student['Ad']} {student['Soyad']}\n"
                f"🧑‍🦱 **Ata adı:** {student['Ata adı']}\n"
                f"🏫 **Sinif:** {student['Sinif']}\n"
                f"📚 **Kitabça dili:** {student['Kitabça dili']}\n"
                f"🏷 **Mərkəz:** {student['Qısa ad']}\n"
                f"📍 **Otaq:** {student['Otaq']}   |   **Yer:** {student['Yer']}"
            )

            st.info(info)

            if code in st.session_state.checked_codes:
                st.warning("⚠ Bu şagird artıq yoxlanılıb.")
            else:
                # Təsdiqlə düyməsi göstər
                if st.button("✅ Təsdiqlə və Siyahıya əlavə et"):
                    st.session_state.checked_codes.add(code)
                    st.session_state.approved_students.append({
                        "Ad": student["Ad"],
                        "Soyad": student["Soyad"],
                        "Sinif": student["Sinif"],
                        "Mərkəz": student["Qısa ad"],
                        "UTİS kodu": code
                    })
                    st.success("✅ Şagird siyahıya əlavə olundu.")
        else:
            st.error("❌ Bu UTİS kodu siyahıda yoxdur.")

# --- Təsdiqlənmiş şagirdlər cədvəli ---
if st.session_state.approved_students:
    st.markdown("---")
    st.subheader("📋 Təsdiqlənmiş Şagirdlər Siyahısı")
    approved_df = pd.DataFrame(st.session_state.approved_students)
    st.dataframe(approved_df, use_container_width=True)

    # Yükləmə imkanı (istəyə görə)
    csv = approved_df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Siyahını Yüklə (CSV)", data=csv, file_name="tesdiqlenmis_sagirdler.csv", mime="text/csv")
