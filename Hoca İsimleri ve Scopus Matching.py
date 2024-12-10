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

# Ana klasör yolu
main_folder_path = r"C:\Users\alibaki.turkoz\Desktop\Ozyegin\CS_552_Python_ile_Veri_Bilimi\CS552 Project\CS552_Project_Çalışma Dosyası\All_Universities"  # Excel dosyalarının bulunduğu ana klasör
file2_path = r"C:\Users\alibaki.turkoz\Desktop\Ozyegin\CS_552_Python_ile_Veri_Bilimi\CS552 Project\CS552_Project_Çalışma Dosyası\Scopus Articles 1854-2015\scopus_articles_in_Türkiye_2024_1854.csv"  # İkinci CSV dosyası

# Ana klasördeki tüm Excel dosyalarını bul
excel_files = glob.glob(os.path.join(main_folder_path, "*.xlsx"))

# İkinci CSV dosyasını oku
df2 = pd.read_csv(file2_path)
df2.columns = df2.columns.str.strip()  # Boşlukları temizle

# İkinci CSV'deki isimleri temizle ve ayır
df2["Normalized Author Names"] = df2["Author full names"].apply(remove_numbers_in_parentheses)  # Parantez içini temizle
df2["Normalized Author Names"] = df2["Normalized Author Names"].str.split(";")  # İsimleri ayır
df2 = df2.explode("Normalized Author Names")  # Ayrılan isimleri satırlara aç
df2["Normalized Author Names"] = df2["Normalized Author Names"].apply(parse_full_name)  # İsim formatını düzelt

# Eşleşen veriler için birleştirme işlemi
matched_df_list = []

for file in excel_files:
    if "~$" in file:  # Geçici dosyaları atla
        print(f"Atlandı: {file}, geçici dosya.")
        continue

    print(f"İşleniyor: {file}")
    df1 = pd.read_excel(file)  # Ana klasördeki bir Excel dosyasını oku
    df1.columns = df1.columns.str.strip()  # Boşlukları temizle

    # Eğer gerekli sütun mevcut değilse, dosyayı atla
    if "Title, Name and Surname" not in df1.columns:
        print(f"Atlandı: {file}, gerekli sütun yok.")
        continue

    # İlk Excel dosyasındaki "Title, Name and Surname" sütunundan sadece "Name and Surname" kısmını ayır
    titles_to_remove = [
        "Profesör", "Doçent", "Öğreti̇m Görevli̇si̇", "Araştirma Görevli̇si̇", "Doktor Öğreti̇m Üyesi"
    ]
    pattern = "|".join(titles_to_remove)  # Tüm title'ları bir regex patterni olarak birleştir
    df1["Name and Surname"] = df1["Title, Name and Surname"].str.replace(pattern, "", regex=True).str.strip()

    # İsimleri eşleştirme işlemi
    matched_df = pd.merge(
        df1,
        df2,
        left_on="Name and Surname",  # İsim ve soy isim sütunu
        right_on="Normalized Author Names",  # Temizlenmiş isim sütunu
        how="inner"  # Sadece eşleşenleri al
    )

    # Sadece "Name and Surname" kolonunu al
    matched_df = matched_df[["Name and Surname"]]
    matched_df_list.append(matched_df)

# Tüm eşleşen verileri birleştir
final_matched_df = pd.concat(matched_df_list, ignore_index=True)

# Tekrar eden isimleri kaldır
final_matched_df = final_matched_df.drop_duplicates(subset=["Name and Surname"])

# Elde edilen sonuçları bir Excel dosyasına kaydet
output_path = r"C:\Users\alibaki.turkoz\Desktop\Ozyegin\CS_552_Python_ile_Veri_Bilimi\CS552 Project\CS552_Project_Çalışma Dosyası\Matched_Authors\matched_results2.xlsx"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
final_matched_df.to_excel(output_path, index=False)

print(f"Eşleşen veriler {output_path} dosyasına kaydedildi.")
