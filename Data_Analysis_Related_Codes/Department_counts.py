import pandas as pd
import matplotlib.pyplot as plt
import os

# Dosya yolunu belirtin
file_path = r"C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Matched_Informations\final_match_with_type_cities - Kopya.xlsx"

# Çıktı klasörünü tanımlayın
output_folder = r"C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Data Analysis"
os.makedirs(output_folder, exist_ok=True)

# Veriyi oku
data = pd.read_excel(file_path)

# Department sütunundaki değerleri say
department_counts = data['Department'].value_counts()

# Department grafiğini bölmek için bir grupta 30 değer olacak şekilde ayır
chunk_size = 30
department_chunks = [department_counts[i:i + chunk_size] for i in range(0, len(department_counts), chunk_size)]

# Her bir grup için ayrı grafik oluştur
for idx, chunk in enumerate(department_chunks):
    plt.figure(figsize=(16, 10))
    chunk.plot(kind='barh', color='coral')  # Yatay grafik
    plt.title(f'Department Distribution (Part {idx + 1})', fontsize=14)
    plt.xlabel('Count', fontsize=12)
    plt.ylabel('Department', fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)

    # Her bir çubuğun yanına değer ekle
    for i, count in enumerate(chunk):
        plt.text(count + 0.5, i, str(count), va='center', fontsize=10, color='black')

    # Grafik kaydet
    department_output_path = os.path.join(output_folder, f'department_distribution_part_{idx + 1}.png')
    plt.savefig(department_output_path, bbox_inches='tight')
    plt.close()

    print(f"Department grafiği (Part {idx + 1}) '{department_output_path}' konumuna kaydedildi.")
