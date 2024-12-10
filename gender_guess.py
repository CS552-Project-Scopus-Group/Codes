import pandas as pd
import gender_guesser.detector as gender

# İsim tespit edici oluştur
d = gender.Detector()

# CSV dosyasını oku
file_path = r"C:\Users\emre.ozturk\Desktop\SCRAP\final_matched_all.csv"
output_file = r"C:\Users\emre.ozturk\Desktop\SCRAP\names_with_gender.csv"

df = pd.read_csv(file_path)

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

# 'Author full names' sütunundan cinsiyet tahmini yap
df['Gender'] = df['Name and Surname'].apply(predict_gender)

# Yeni CSV'ye kaydet
df.to_csv(output_file, index=False)

print(f"Cinsiyet tahmini tamamlandı. Sonuçlar {output_file} dosyasına kaydedildi.")