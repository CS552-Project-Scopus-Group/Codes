import pandas as pd
import matplotlib.pyplot as plt
import os
import re

# Dosya yolunu belirtin
file_path = r"C:\\Users\\emre.ozturk\\Desktop\\SCRAP\\Gender\\final_match_with_genders_copy.xlsx"

# Çıktı klasörünü tanımlayın
output_folder = r"C:\\Users\\emre.ozturk\\Desktop\\SCRAP\\Gender\\Genders"
os.makedirs(output_folder, exist_ok=True)

# Veriyi oku
data = pd.read_excel(file_path)

# Gender sütunundaki değerleri say
counts = data['Gender'].value_counts()

# Grafik oluştur
plt.figure(figsize=(8, 6))
bar_plot = counts.plot(kind='bar', color=['blue', 'pink'])
plt.title('Gender Distribution', fontsize=14)
plt.xlabel('Gender', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.xticks(rotation=0, fontsize=10)
plt.yticks(fontsize=10)

# Her bir sütunun üzerine değer ekle
for i, count in enumerate(counts):
    plt.text(i, count + 0.5, str(count), ha='center', fontsize=20, color='black')

# Grafik kaydet
output_path = os.path.join(output_folder, 'gender_distribution.png')
plt.savefig(output_path)
plt.close()

print(f"Grafik '{output_path}' konumuna kaydedildi.")

# Title, Name and Surname sütunundan sadece unvanları çek
unvan_pattern = r"^(Arastirma Gorevlisi|Docent|Profesor|Doktor Ogretim Uyesi|Ogretim Gorevlisi)"
data['Unvan'] = data['Title, Name and Surname'].str.extract(unvan_pattern)

# Unvan sütunundaki değerleri say
unvan_counts = data['Unvan'].value_counts()

# Unvan grafiği oluştur
plt.figure(figsize=(8, 6))
unvan_counts.plot(kind='bar', color='skyblue')
plt.title('Title Distribution', fontsize=14)
plt.xlabel('Title', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)

# Her bir sütunun üzerine değer ekle
for i, count in enumerate(unvan_counts):
    plt.text(i, count + 0.5, str(count), ha='center', fontsize=10, color='black')

# Grafik kaydet
unvan_output_path = os.path.join(output_folder, 'title_distribution.png')
plt.savefig(unvan_output_path)
plt.close()

print(f"Unvan grafiği '{unvan_output_path}' konumuna kaydedildi.")

# Unvanlara göre Count sütunundaki toplam değerleri hesapla
unvan_count_totals = data.groupby('Unvan')['Count'].sum()

# Unvanların Count toplamlarını gösteren grafik oluştur
plt.figure(figsize=(8, 6))
unvan_count_totals.plot(kind='bar', color='lightgreen')
plt.title('Total Count by Title', fontsize=14)
plt.xlabel('Title', fontsize=12)
plt.ylabel('Total Count', fontsize=12)
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)
plt.tight_layout()

# Her bir sütunun üzerine değer ekle
for i, total in enumerate(unvan_count_totals):
    plt.text(i, total + 0.5, str(total), ha='center', fontsize=10, color='black')

# Grafik kaydet
unvan_count_output_path = os.path.join(output_folder, 'title_total_count_distribution.png')
plt.savefig(unvan_count_output_path)
plt.close()

print(f"Unvanlara göre Count toplamlarının grafiği '{unvan_count_output_path}' konumuna kaydedildi.")



# Department sütunundaki değerleri say
department_counts = data['Department'].value_counts()

# Department grafiği oluştur
plt.figure(figsize=(16, 10))
department_counts.plot(kind='bar', color='coral')
plt.title('Department Distribution', fontsize=14)
plt.xlabel('Department', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.xticks(rotation=45, fontsize=10, ha='right')
plt.yticks(fontsize=10)

# Her bir sütunun üzerine değer ekle
for i, count in enumerate(department_counts):
    plt.text(i, count + 0.5, str(count), ha='center', fontsize=10, color='black')

# Grafik kaydet
department_output_path = os.path.join(output_folder, 'department_distribution.png')
plt.savefig(department_output_path, bbox_inches='tight')
plt.close()

print(f"Department grafiği '{department_output_path}' konumuna kaydedildi.")