import pandas as pd
from unidecode import unidecode
 
# İlk harfleri büyük yapma fonksiyonu
def capitalize_words(text):
    if pd.isna(text):  # NaN değerler varsa kontrol et
        return text
    return ' '.join(word.capitalize() for word in unidecode(text).lower().split())
 
# CSV dosyasının yolu
input_file = r"C:\Users\alibaki.turkoz\Downloads\all_universities_academics.csv"
output_file = r"C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Eng_Datasets\organized_universities_academics.xlsx"
 
# CSV dosyasını oku
df = pd.read_csv(input_file, header=None)
 
# Sütun isimlerini ekle
df.columns = ["University Name", "Academic Name", "Title", "Details"]
 
# 4. satırdan başlayarak son 5 satırı hariç tut
df = df.iloc[3:-5].reset_index(drop=True)
 
# "University Name" sütununda yalnızca üniversite adını bırak ve baş harflerini büyük yap
df["University Name"] = df["University Name"].str.extract(r"(.*?ÜNİVERSİTESİ)")
df["University Name"] = df["University Name"].apply(lambda x: capitalize_words(x) if pd.notna(x) else x)
 
# "Details" sütunundan fakülte ve bölüm bilgilerini al
# "Faculty" ve "Major" sütunlarını oluştur
def handle_faculty_and_major(details):
    if pd.isna(details):
        return None, None
 
    # "FAKÜLTESİ" içeren kısmı Faculty olarak al
    if "FAKÜLTESİ" in details:
        faculty = details.split('/')[1]  # "FAKÜLTESİ" kısmını al
    else:
        # REKTÖRLÜK veya YÜKSEKOKULU içeren kısmı al
        faculty_parts = [part for part in details.split('/') if "REKTÖRLÜK" in part or "YÜKSEKOKULU" in part]
        faculty = faculty_parts[0] if faculty_parts else None
   
    # Major kısmı "BÖLÜMÜ" veya "ANABİLİM DALI" sonrası olacak
    if "BÖLÜMÜ" in details:
        major = details.split('/')[2]  # BÖLÜMÜ kısmını al
    elif "ANABİLİM DALI" in details:
        major = details.split('/')[2]  # ANABİLİM DALI kısmını al
    else:
        major = None
 
    return faculty, major
 
# Apply the function to split "Details" into "Faculty" and "Major"
df["Faculty"], df["Major"] = zip(*df["Details"].apply(lambda x: handle_faculty_and_major(x)))
 
# Apply capitalization for Faculty and Major
df["Faculty"] = df["Faculty"].apply(lambda x: capitalize_words(x) if pd.notna(x) else x)
df["Major"] = df["Major"].apply(lambda x: capitalize_words(x) if pd.notna(x) else x)
 
# "Academic Name" ve "Title" sütunlarını düzenle
df["Academic Name"] = df["Academic Name"].apply(lambda x: capitalize_words(x.strip()) if pd.notna(x) else x)
df["Title"] = df["Title"].apply(lambda x: capitalize_words(x.strip()) if pd.notna(x) else x)
 
# "Details" sütununu kaldır
df = df.drop(columns=["Details"])
 
# Sonuçları Excel olarak kaydet
df.to_excel(output_file, index=False)
 
print(f"Düzenlenmiş dosya şu konuma kaydedildi: {output_file}")