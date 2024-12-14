import pandas as pd
import matplotlib.pyplot as plt
import os

# Dosya yolunu belirtin
file_path = r"C:\\Users\\emre.ozturk\\Desktop\\SCRAP\\Gender\\final_match_with_type_cities.xlsx"

# Çıktı klasörünü tanımlayın
output_folder = r"C:\\Users\\emre.ozturk\\Desktop\\SCRAP\\Gender"

# Alt klasörler oluşturuluyor
excel_folder = os.path.join(output_folder, 'excel_files')
graph_folder = os.path.join(output_folder, 'graphs')
os.makedirs(excel_folder, exist_ok=True)
os.makedirs(graph_folder, exist_ok=True)

# Veriyi oku
data = pd.read_excel(file_path)

# 'University', 'Faculty' ve 'Count' sütunları üzerinden toplam makale sayısını hesapla
university_faculty_counts = data.groupby(['University', 'Faculty'])['Count'].sum().unstack(fill_value=0)

# Üniversite bazında işlem yapmak için her bir üniversiteyi gruplayalım
for university in university_faculty_counts.index:
    # Üniversiteye ait fakülteleri al
    university_data = university_faculty_counts.loc[university]
    
    # "0" değeri olan fakülteleri kaldır
    university_data = university_data[university_data > 0]

    # Fakülteyi 50'şer satırlık parçalara ayıralım (Büyük chunk_size)
    chunk_size = 50  # Daha büyük bir chunk size kullanıyoruz
    for start_row in range(0, len(university_data), chunk_size):
        chunk = university_data.iloc[start_row:start_row + chunk_size]
        chunk_filename = f'{university}_faculty_count_chunk_{start_row // chunk_size + 1}.xlsx'
        
        # Excel dosyasına kaydet
        chunk.to_excel(os.path.join(excel_folder, chunk_filename))

        # Grafik oluştur (Yatay Bar)
        plt.figure(figsize=(12, 8))
        chunk.plot(kind='barh', stacked=False, colormap='tab20')
        plt.title(f'{university} University Faculty Count Distribution (Part {start_row // chunk_size + 1})')
        plt.xlabel('Total Count of Articles')
        plt.ylabel('Faculty')
        plt.tight_layout()

        # Grafik üzerine değerleri ekleyelim
        for i, value in enumerate(chunk):
            plt.text(value + 0.5, i, str(value), va='center', fontsize=10, color='black')

        # Grafik kaydet
        plt.savefig(os.path.join(graph_folder, f'{university}_faculty_count_chunk_{start_row // chunk_size + 1}.png'))
        plt.close()

        print(f"{university} Üniversitesi için Fakülte ve Count Dağılımının grafiği (Part {start_row // chunk_size + 1}) '{graph_folder}/{university}_faculty_count_chunk_{start_row // chunk_size + 1}.png' konumuna kaydedildi.")

# Üniversite ve Fakülte bazında toplam makale sayısını Excel dosyasına kaydet
university_faculty_excel_path = os.path.join(excel_folder, 'university_faculty_article_count.xlsx')
university_faculty_counts.to_excel(university_faculty_excel_path)

print(f"University ve Faculty bazında toplam makale sayısı '{university_faculty_excel_path}' dosyasına kaydedildi.")
