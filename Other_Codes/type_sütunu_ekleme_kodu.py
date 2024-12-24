import pandas as pd

# Dosyaları yükle
final_scopus = pd.read_excel(r'C:\Users\emre.ozturk\Desktop\Yeni_Analiz_scrap\Scopus_articles_in_Türkiye_2016_2024.xlsx')
university_data = pd.read_excel(r'C:\Users\emre.ozturk\Desktop\Yeni_Analiz_scrap\university_data.xlsx')

# "Affiliations" sütunundaki her üniversiteyi ";" ile ayırarak listeye çeviriyoruz
final_scopus['Affiliations'] = final_scopus['Affiliations'].apply(lambda x: [aff.strip() for aff in str(x).split(';')] if pd.notnull(x) else [])

# "Type" bilgilerini maplemek için bir fonksiyon yazıyoruz
def get_university_type(affiliations):
    seen_affiliations = set()  # Daha önce eklenen üniversiteleri takip etmek için bir set
    types = []  # Tür bilgilerini saklamak için bir liste
    
    for affiliation in affiliations:
        if affiliation not in seen_affiliations:  # Eğer üniversite daha önce eklenmediyse
            seen_affiliations.add(affiliation)  # Üniversiteyi işaretle
            # Her üniversite için karşılık gelen "Type" değerini bul
            matching_rows = university_data[university_data['University Name'].str.contains(affiliation, case=False, na=False)]
            university_types = matching_rows['Type'].tolist()
            
            if university_types:
                types.append(university_types[0])  # İlk eşleşen türü ekle
            else:
                types.append("Unknown")  # Eşleşme yoksa "Unknown" ekle
    
    # Türleri sırasıyla birleştir ve döndür
    return '; '.join(types)

# "Type" sütununu oluştur
final_scopus['Type'] = final_scopus['Affiliations'].apply(get_university_type)

# Yeni DataFrame'i Excel'e kaydet
final_scopus.to_excel(r'C:\Users\emre.ozturk\Desktop\Yeni_Analiz_scrap\final_scopus_with_type_2016_2024.xlsx', index=False)

print("İşlem tamamlandı ve yeni dosya kaydedildi.")
