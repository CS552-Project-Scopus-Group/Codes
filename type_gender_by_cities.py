import pandas as pd
import matplotlib.pyplot as plt
import os

# Excel dosyasını oku
file_path = r'C:\Users\emre.ozturk\Desktop\SCRAP\Gender\final_match_with_type_cities.xlsx'
data = pd.read_excel(file_path)

# 'Type' sütunundaki 'Private ' değerlerini 'Private' olarak düzelt
data['Type'] = data['Type'].str.strip()  # Boşlukları temizler

# 'Type' sütunundaki sadece 'Private' ve 'State' olanları al
data = data[data['Type'].isin(['Private', 'State'])]

# 'City' ve 'Gender' sütunlarında şehir ve cinsiyet bilgilerini gruplandır
gender_city_counts = data.groupby(['City', 'Gender']).size().unstack(fill_value=0)

# 'Type' ve 'Gender' sütunlarında tip ve cinsiyet bilgilerini gruplandır
gender_type_counts = data.groupby(['Type', 'Gender']).size().unstack(fill_value=0)

# Çıktıyı bir dosyaya kaydet
output_folder = r'C:\Users\emre.ozturk\Desktop\SCRAP\Gender'
os.makedirs(output_folder, exist_ok=True)

# Çıktıyı Excel dosyasına kaydet
output_file_path = os.path.join(output_folder, 'gender_by_city_counts.xlsx')
gender_city_counts.to_excel(output_file_path)

# Çıktıyı 'Type' ve 'Gender' için de kaydet
output_type_file_path = os.path.join(output_folder, 'gender_by_type_counts.xlsx')
gender_type_counts.to_excel(output_type_file_path)

print(f"Şehir ve cinsiyet sayıları '{output_file_path}' dosyasına kaydedildi.")
print(f"Tip ve cinsiyet sayıları '{output_type_file_path}' dosyasına kaydedildi.")

# Grafik oluştur (City ve Gender)
ax1 = gender_city_counts.plot(kind='bar', stacked=True, figsize=(10, 6), color=['blue', 'pink'])
plt.title('Gender Distribution by City', fontsize=14)
plt.xlabel('City', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.yticks(fontsize=10)

# Grafik üzerine değer ekle (City ve Gender)
for i, city in enumerate(gender_city_counts.index):
    bottom = 0  # Barın tabanını takip et
    for j, gender in enumerate(gender_city_counts.columns):
        value = gender_city_counts.loc[city, gender]
        plt.text(i, bottom + value / 2, str(value), ha='center', va='center', fontsize=9, color='black')
        bottom += value  # Yığınla ilerle

# Grafik kaydet (City ve Gender)
graph_output_path = os.path.join(output_folder, 'gender_distribution_by_city.png')
plt.tight_layout()
plt.savefig(graph_output_path)
plt.close()

print(f"Grafik '{graph_output_path}' konumuna kaydedildi.")

# Grafik oluştur (Type ve Gender)
ax2 = gender_type_counts.plot(kind='bar', stacked=True, figsize=(10, 6), color=['blue', 'pink'])
plt.title('Gender Distribution by Type', fontsize=14)
plt.xlabel('Type', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.yticks(fontsize=10)

# Grafik üzerine değer ekle (Type ve Gender)
for i, _type in enumerate(gender_type_counts.index):
    bottom = 0  # Barın tabanını takip et
    for j, gender in enumerate(gender_type_counts.columns):
        value = gender_type_counts.loc[_type, gender]
        plt.text(i, bottom + value / 2, str(value), ha='center', va='center', fontsize=9, color='black')
        bottom += value  # Yığınla ilerle

# Grafik kaydet (Type ve Gender)
graph_type_output_path = os.path.join(output_folder, 'gender_distribution_by_type.png')
plt.tight_layout()
plt.savefig(graph_type_output_path)
plt.close()

print(f"Grafik '{graph_type_output_path}' konumuna kaydedildi.")
