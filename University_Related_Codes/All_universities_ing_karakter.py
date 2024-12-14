import os
import pandas as pd
import unidecode

# Türkçe karakterleri İngilizce'ye çeviren fonksiyon
def convert_to_english(text):
    return unidecode.unidecode(text)

# Klasör yolu
root_dir = r"C:\Users\emre.ozturk\Desktop\SCRAP\All_universities"
output_dir = r"C:\Users\emre.ozturk\Desktop\SCRAP\Output"

# Alt klasörler
cities = ["Ankara", "İzmir", "Antalya", "Gaziantep", "Kayseri", "Konya", "Bursa"]

# Eğer çıktı klasörü yoksa oluştur
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Tüm şehirler için veri birleştirilecek
all_data = []

# Dosyaları alıp işlem yapma
for city in cities:
    city_path = os.path.join(root_dir, city)
    city_data = []  # Her şehir için verileri topla
    
    # Klasör içindeki tüm alt klasörleri ve dosyaları dolaş
    for subdir, _, files in os.walk(city_path):
        for file in files:
            # Ankara, Kayseri, Konya için 'güncellenmiş_dosya.xlsx' dosyasını işle
            if city in ["Ankara", "Kayseri", "Konya"] and file == "güncellenmiş_dosya.xlsx":
                file_path = os.path.join(subdir, file)
                # Excel dosyasını oku
                df = pd.read_excel(file_path)
                # Tüm sütun ve satırlardaki Türkçe karakterleri İngilizce'ye çevir
                df = df.applymap(lambda x: convert_to_english(str(x)) if isinstance(x, str) else x)
                city_data.append(df)  # Şehir verisini birleştir
                print(f"Processed file: {file_path}")
            
            # İzmir, Antalya, Gaziantep, Bursa için 'academic_staff.xlsx' dosyasını işle
            elif city in ["İzmir", "Antalya", "Gaziantep", "Bursa"] and file.endswith("academic_staff.xlsx"):
                file_path = os.path.join(subdir, file)
                # Excel dosyasını oku
                df = pd.read_excel(file_path)
                # Tüm sütun ve satırlardaki Türkçe karakterleri İngilizce'ye çevir
                df = df.applymap(lambda x: convert_to_english(str(x)) if isinstance(x, str) else x)
                city_data.append(df)  # Şehir verisini birleştir
                print(f"Processed file: {file_path}")
    
    # Şehirdeki tüm dosyaları birleştir
    if city_data:
        city_df = pd.concat(city_data, ignore_index=True)
        # Çıktı dosya yolu
        output_file_path = os.path.join(output_dir, f"{city}_data.csv")
        # Düzeltilmiş CSV dosyasını kaydet
        city_df.to_csv(output_file_path, index=False)
        print(f"Saved city data: {output_file_path}")
        
        # Tüm şehir verilerini birleştir
        all_data.append(city_df)

# Tüm şehirlerin verilerini birleştirip tek bir dosya olarak kaydet
if all_data:
    all_cities_df = pd.concat(all_data, ignore_index=True)
    output_file_path_all = os.path.join(output_dir, "all_cities_data.csv")
    all_cities_df.to_csv(output_file_path_all, index=False)
    print(f"Saved all cities data: {output_file_path_all}")
