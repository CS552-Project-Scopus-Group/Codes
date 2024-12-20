### Scopus ve Author için authorlara göre eşleştiririlmiş dosyadaki (ÜNİVERSİTELER İLE TÜM TÜRKİYEDEKİ ÜNİVERSİTELERİ EŞLEŞTİRİP üniversite bilgilerini eşleşmiş dosyaya ekler).

import pandas as pd

# Dosya yolları
file1 = r"C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Eng_Datasets\All_Türkiye_University_List_Eng.xlsx"  # İlk dosya
file2 = r"C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Matched_Informations\matched_data_with_gender.xlsx"  # İkinci dosya
output_file = r"C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Matched_Informations\matched_data_with_gender_city_and_type.xlsx"  # Çıktı dosyası

# İlk dosyayı oku
df1 = pd.read_excel(file1)

# İkinci dosyayı oku
df2 = pd.read_excel(file2)

# Dosyaların ilgili sütunlarını temizle ve eşleştirme için normalize et (örneğin, küçük harfe çevir ve boşlukları kaldır)
df1["University"] = df1["University"].str.strip().str.lower()
df2["University_Name"] = df2["University_Name"].str.strip().str.lower()

# Eşleşme için birleştirme işlemi (merge)
merged_df = pd.merge(
    df2,  # Temel alınacak dosya
    df1[["University", "City", "Type"]],  # Eklenecek bilgiler
    left_on="University_Name",  # İkinci dosyanın eşleşecek sütunu
    right_on="University",  # İlk dosyanın eşleşecek sütunu
    how="left"  # Eşleşmeyenleri de tutmak için "left join"
)

# Gereksiz "University" sütununu kaldır
merged_df = merged_df.drop(columns=["University"])

# Sonuçları yeni bir Excel dosyasına kaydet
merged_df.to_excel(output_file, index=False)

print(f"Birleştirilmiş dosya şu konuma kaydedildi: {output_file}")
