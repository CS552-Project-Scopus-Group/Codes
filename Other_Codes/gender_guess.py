import pandas as pd
import gender_guesser.detector as gender

# İsim tespit edici oluştur
d = gender.Detector()

# Excel dosyasını oku
file_path = r"C:\Users\emre.ozturk\Desktop\SCRAP\final_matched_all.xlsx"
output_file = r"C:\Users\emre.ozturk\Desktop\SCRAP\fina_match_with_genders.xlsx"

df = pd.read_excel(file_path)

# İsim sütunundan tahmin et
def predict_gender(name):
    if pd.isnull(name):
        return "Unknown"
    first_name = name.split()[0]  # İlk adı al
    guess = d.get_gender(first_name)
    # Gender-guesser sonuçlarını daha anlaşılır hale getir
    if guess in ["male", "mostly_male"]:
        return "Male"
    elif guess in ["female", "mostly_female"]:
        return "Female"
    else:
        return "Unknown"

# 'Name and Surname' sütunundan cinsiyet tahmini yap
df['Gender'] = df['Matched Author Name'].apply(predict_gender)

# Ek sütunlar oluştur
df['Male'] = (df['Gender'] == 'Male').astype(int)  # Erkekler için 1, diğerleri için 0
df['Female'] = (df['Gender'] == 'Female').astype(int)  # Kadınlar için 1, diğerleri için 0
df['Unknown'] = (df['Gender'] == 'Unknown').astype(int)  # Bilinmeyenler için 1, diğerleri için 0

# Yeni Excel dosyasına kaydet
df.to_excel(output_file, index=False)

print(f"Cinsiyet tahmini tamamlandı. Sonuçlar {output_file} dosyasına kaydedildi.")
