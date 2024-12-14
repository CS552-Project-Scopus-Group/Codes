import pandas as pd

# Excel dosyasını yükleyin
dosya_adi = r"C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ - Kopya\İzmir\İzmir Yüksek Teknoloji Üniversitesi\İzmir_Yüksek_Teknoloji_University_academic_staff.xlsx"  # Dosya yolu
df = pd.read_excel(dosya_adi)

# İkinci sütundaki bilgileri '/' ile ayır ve ilk üç kısmı al
df[['University', 'Faculty', 'Department']] = df.iloc[:, 1].str.split('/', n=3, expand=True).iloc[:, :3]

# Türkçe karakterlere uygun baş harfi büyük, diğerleri küçük formatlama fonksiyonu
def format_turkish_text(text):
    if isinstance(text, str):  # Sadece metinler için düzenleme yap
        return ' '.join([word.capitalize() for word in text.strip().split()])  # Her kelimenin ilk harfi büyük
    return text

# Sütunları formatla
df['University'] = df['University'].apply(format_turkish_text)
df['Faculty'] = df['Faculty'].apply(format_turkish_text)
df['Department'] = df['Department'].apply(format_turkish_text)

# İlk sütunu da baş harf büyük, diğer harf küçük olacak şekilde düzenle
df['Title, Name and Surname'] = df.iloc[:, 0].apply(format_turkish_text)

# Sütunları yeniden düzenle: University, Faculty, Department, Title, Name and Surname
df = df[['University', 'Faculty', 'Department', 'Title, Name and Surname']]

# Düzenlenmiş dosyayı aynı isimle kaydet
df.to_excel(dosya_adi, index=False)

print(f"Excel dosyası başarıyla güncellendi: {dosya_adi}")
