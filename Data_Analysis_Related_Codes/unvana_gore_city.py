import pandas as pd
import matplotlib.pyplot as plt
import os
import re

# Dosya yolunu belirtin
file_path = r"C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Matched_Informations\final_match_with_type_cities - Kopya.xlsx"

# Çıktı klasörünü tanımlayın
output_folder = r"C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Data Analysis"
os.makedirs(output_folder, exist_ok=True)

# Veriyi oku
data = pd.read_excel(file_path)

# 'Title, Name and Surname' sütunundan unvanları çek
unvan_pattern = r"^(Arastirma Gorevlisi|Docent|Profesor|Doktor Ogretim Uyesi|Ogretim Gorevlisi)"
data['Unvan'] = data['Title, Name and Surname'].str.extract(unvan_pattern)

# 'Unvan' ve 'City' sütunlarına göre her kombinasyonun sayısını hesapla
unvan_city_counts = data.groupby(['Unvan', 'City']).size().unstack(fill_value=0)

# Unvan ve City'e göre sayıları yazdır
print(unvan_city_counts)

# Unvan ve City'e göre sayıları gösteren grafik oluştur
plt.figure(figsize=(12, 8))
unvan_city_counts.plot(kind='bar', stacked=True, figsize=(12, 8), colormap='tab20')

# Başlık ve etiketler
plt.title('Number of People by Title and City', fontsize=14)
plt.xlabel('Title', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.yticks(fontsize=10)

# Grafik üzerine değer ekle
for i, unvan in enumerate(unvan_city_counts.index):
    bottom = 0  # Barın tabanını takip et
    for j, city in enumerate(unvan_city_counts.columns):
        value = unvan_city_counts.loc[unvan, city]
        plt.text(i, bottom + value / 2, str(value), ha='center', va='center', fontsize=9, color='black')
        bottom += value  # Yığınla ilerle

# Grafik kaydet
unvan_city_output_path = os.path.join(output_folder, 'number_by_title_and_city.png')
plt.tight_layout()
plt.savefig(unvan_city_output_path)
plt.close()

print(f"Unvanlara ve şehirlere göre sayıların grafiği '{unvan_city_output_path}' konumuna kaydedildi.")

# Unvan ve City'e göre sayıları Excel dosyasına kaydet
unvan_city_excel_path = os.path.join(output_folder, 'number_by_title_and_city.xlsx')
unvan_city_counts.to_excel(unvan_city_excel_path)

print(f"Unvanlara ve şehirlere göre sayılar '{unvan_city_excel_path}' dosyasına kaydedildi.")
