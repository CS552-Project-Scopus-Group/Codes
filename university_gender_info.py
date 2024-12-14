import pandas as pd
import matplotlib.pyplot as plt
import os

# Dosya yolunu belirtin
file_path = r"C:\\Users\\emre.ozturk\\Desktop\\SCRAP\\Gender\\final_match_with_genders_copy.xlsx"

# Çıktı klasörünü tanımlayın
output_folder = r"C:\\Users\\emre.ozturk\\Desktop\\SCRAP\\Gender"
os.makedirs(output_folder, exist_ok=True)

# Veriyi oku
data = pd.read_excel(file_path)

# 'University' ve 'Gender' sütunlarındaki verileri gruplayarak say
university_gender_counts = data.groupby('University')['Gender'].value_counts().unstack(fill_value=0)

# Grafiklerin toplu olarak kaydedilmesi için chunk boyutu
chunk_size = 10  # Her seferinde 10 üniversiteyi işle

# Üniversiteleri gruplara ayır
university_chunks = [university_gender_counts.iloc[i:i + chunk_size] for i in range(0, len(university_gender_counts), chunk_size)]

# Her bir grup için grafik oluştur ve kaydet
for idx, chunk in enumerate(university_chunks):
    # Grafik oluştur
    ax = chunk.plot(kind='bar', stacked=True, figsize=(12, 8), width=0.8, 
                    color=['#1f77b4', '#d62728'])  # Mavi (erkek) ve kırmızı (kadın) renkleri kullan
    
    # Grafik başlığı ve etiketleri
    plt.title(f"Gender Distribution for Universities (Part {idx + 1})", fontsize=16)
    plt.xlabel('University', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    
    # Cinsiyet sayısını her çubuğun üzerine ekle
    for i, (university, gender_counts) in enumerate(chunk.iterrows()):
        plt.text(i, gender_counts[0] + gender_counts[1] + 1,  # Yerleşim yeri, en üst kısıma ekle
                 f"{gender_counts[0]} - {gender_counts[1]}", 
                 ha='center', fontsize=10, color='black')

    # Lejant (legend) ekle
    plt.legend(title="Gender", fontsize=10, loc='upper left', bbox_to_anchor=(1.05, 1))

    # Grafik kaydet
    university_graph_path = os.path.join(output_folder, f"gender_distribution_part_{idx + 1}.png")
    plt.savefig(university_graph_path, bbox_inches='tight')
    plt.close()  # Grafik kapat

    print(f"Part {idx + 1} grafikleri kaydedildi.")

print("Tüm grafikler kaydedildi.")
