import pandas as pd
import os

# Dosya yolları
dosya1_yolu = r"C:\Users\emre.ozturk\Desktop\SCRAP\final_merged_all_univerisities_copy.xlsx"
dosya2_yolu = r"C:\Users\emre.ozturk\Desktop\SCRAP\Scopus_Articles_in_Turkey_1854_2024_V2_eng_karakter.csv"
output_yolu = r"C:\Users\emre.ozturk\Desktop\SCRAP\output_matched.xlsx"

# Ünvanları temizlemek için kullanılacak liste
unvanlar = ["Profesor", "Docent", "Doktor Ogretim Uyesi", "Ogretim Gorevlisi", "Arastirma Gorevlisi"]

def temizle_isim(unvanli_isim):
    """Kişinin ünvanını temizler ve yalnızca isim-soyisim döndürür."""
    if isinstance(unvanli_isim, str):
        for unvan in unvanlar:
            if unvan in unvanli_isim:
                return unvanli_isim.replace(unvan, "").strip()
        return unvanli_isim
    return ""

# 1. dosyayı oku
df1 = pd.read_excel(dosya1_yolu)
df1["Temiz Isimler"] = df1["Title, Name and Surname"].apply(lambda x: [temizle_isim(isim.strip()) for isim in x.split(";")] if isinstance(x, str) else [])

# 2. dosyayı oku
df2 = pd.read_csv(dosya2_yolu)
df2["Temiz Isimler"] = df2["Author full names"].apply(lambda x: [isim.strip() for isim in x.split(";")] if isinstance(x, str) else [])

# Performansı artırmak için df2'yi düzene sok
isim_seti = set(isim for isim_listesi in df2["Temiz Isimler"] for isim in isim_listesi)

# Eşleşmeleri toplu olarak bul
matches = {}
for index, row in df1.iterrows():
    for temiz_isim in row["Temiz Isimler"]:
        if temiz_isim in isim_seti:
            if temiz_isim not in matches:
                matches[temiz_isim] = {
                    "University": row["University"],
                    "Faculty": row["Faculty"],
                    "Department": row["Department"],
                    "Title, Name and Surname": row["Title, Name and Surname"],
                    "Count": 0
                }
            matches[temiz_isim]["Count"] += 1

# Eşleşmeleri DataFrame'e dönüştür
matched_df = pd.DataFrame.from_records([
    {
        "Matched Author Name": key,
        "University": value["University"],
        "Faculty": value["Faculty"],
        "Department": value["Department"],
        "Title, Name and Surname": value["Title, Name and Surname"],
        "Count": value["Count"]
    }
    for key, value in matches.items()
])

# Çıktıyı kaydet
os.makedirs(os.path.dirname(output_yolu), exist_ok=True)
matched_df.to_excel(output_yolu, index=False)

print(f"Eşleşmeler {output_yolu} dosyasına kaydedildi.")