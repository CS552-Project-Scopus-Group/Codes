import pandas as pd
import unidecode

# Türkçe karakterleri İngilizce'ye çeviren fonksiyon
def convert_to_english(text):
    return unidecode.unidecode(text)

# CSV dosyasının yolu
file_path = r"C:\Users\emre.ozturk\Desktop\SCRAP\Scopus_Articles_in_Türkiye_1854_2024_V2 (1).csv"

# CSV dosyasını oku
df = pd.read_csv(file_path)

# Tüm sütun ve satırlardaki Türkçe karakterleri İngilizce'ye çevir
df = df.applymap(lambda x: convert_to_english(str(x)) if isinstance(x, str) else x)

# Çıktı dosya yolunu belirle
output_file_path = r"C:\Users\emre.ozturk\Desktop\SCRAP\Scopus_Articles_in_Turkey_1854_2024_V2_eng_karakter.csv"

# Düzeltilmiş CSV dosyasını kaydet
df.to_csv(output_file_path, index=False)

print(f"Processed and saved file: {output_file_path}")
