import pandas as pd
import os
import glob
import re

# Parantez içindeki numaraları çıkarma fonksiyonu
def remove_numbers_in_parentheses(text):
    if not isinstance(text, str):  # Eğer değer string değilse boş bir string döndür
        return ""
    return re.sub(r"\s*\(.*?\)", "", text).strip()  # Parantez ve içindeki sayıları temizle

# İsimleri soyisim, ikinci isim ve birinci isim olarak ayırma fonksiyonu
def parse_full_name(name):
    if not isinstance(name, str):  # Eğer değer string değilse boş bir string döndür
        return ""
    name_parts = name.split(",")  # Soyisim, İsim formatında ayır
    if len(name_parts) == 2:  # Eğer gerçekten soyisim ve isim varsa
        full_name_parts = name_parts[1].strip().split()  # İsimleri ayır
        surname = name_parts[0].strip()
        if len(full_name_parts) == 1:  # Eğer sadece tek bir isim varsa
            return f"{full_name_parts[0]} {surname}"  # Yalnızca 1 isim ve soyisim
        elif len(full_name_parts) == 2:  # Eğer 2 isim varsa
            return f"{full_name_parts[1]} {full_name_parts[0]} {surname}"  # 2. isim ve soyisim, sonra 1. isim
    return name  # Eğer beklenen formatta değilse olduğu gibi döndür

# 2. Dosya yolu ve sütun adı
file2_path = r"C:\Users\emre.ozturk\Desktop\SCRAP\Scopus_Articles_in_Turkey_1854_2024_V2_eng_karakter.csv"  # İkinci CSV dosyası

# 1. Dosya yolunu al, burada CSV dosyalarını okumaya devam edeceğiz
file1_path = r"C:\Users\emre.ozturk\Desktop\SCRAP\Output\all_cities_data.csv"  # İlk CSV dosyası

# İkinci CSV'yi oku
df2 = pd.read_csv(file2_path)
df2.columns = df2.columns.str.strip()  # Boşlukları temizle

# İkinci CSV'deki isimleri temizle ve ayır
df2["Normalized Author Names"] = df2["Author full names"].apply(remove_numbers_in_parentheses)  # Parantez içini temizle
df2["Normalized Author Names"] = df2["Normalized Author Names"].str.split(";")  # İsimleri ayır
df2 = df2.explode("Normalized Author Names")  # Ayrılan isimleri satırlara aç
df2["Normalized Author Names"] = df2["Normalized Author Names"].apply(parse_full_name)  # İsim formatını düzelt

# 1. CSV dosyasını oku
df1 = pd.read_csv(file1_path)
df1.columns = df1.columns.str.strip()  # Boşlukları temizle

# 1. dosyada "Title, Name and Surname" sütunundan sadece "Name and Surname" kısmını al
titles_to_remove = [
    "Profesor", "Docent", "Ogreti̇m Gorevli̇si̇", "Arastirma Gorevli̇si̇", "Doktor Ogreti̇m Uyesi"
]
pattern = "|".join(titles_to_remove)  # Tüm title'ları bir regex patterni olarak birleştir
df1["Name and Surname"] = df1["Title, Name and Surname"].str.replace(pattern, "", regex=True).str.strip()

# İsimleri eşleştirme işlemi
matched_df = pd.merge(
    df1,
    df2,
    left_on="Name and Surname",  # 1. dosyadaki "Name and Surname" sütunu
    right_on="Normalized Author Names",  # 2. dosyadaki "Normalized Author Names" sütunu
    how="inner"  # Sadece eşleşenleri al
)

# Sadece "Name and Surname" kolonunu al
matched_df = matched_df[["Name and Surname"]]

# Tekrar eden isimleri kaldır
final_matched_df = matched_df.drop_duplicates(subset=["Name and Surname"])

# Elde edilen sonuçları bir CSV dosyasına kaydet
output_path = r"C:\Users\emre.ozturk\Desktop\SCRAP\final_matched_all.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
final_matched_df.to_csv(output_path, index=False)

print(f"Eşleşen veriler {output_path} dosyasına kaydedildi.")
