import pandas as pd

# Excel dosyasının yolu
file_path = r'C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\yearly_university_article_count.xlsx'

# Excel dosyasını oku
df = pd.read_excel(file_path)

# Üniversite isimlerini düzenleme eşleşmeleri
replace_dict = {
    'Ostim Teknik University': 'OSTIM Technical University',
    'Ostim Technical University': 'OSTIM Technical University',
    'Istanbul Teknik University': 'Istanbul Technical University',
    'Gebze Teknik University': 'Gebze Technical University',
    'Konya Teknik University': 'Konya Technical University',
    'Iskenderun Teknik University': 'Iskenderun Technical University',
    'Karadeniz Teknik University': 'Karadeniz Technical University',
    'Malatya Turgut ozal University': 'Malatya Turgut Ozal University',
    'Acibadem Mehmet Ali Aydinlar University': 'Acibadem University',
    'Cappadocia University': 'Kapadokya University',
    'Istanbul Commerce University': 'Istanbul Ticaret University',
    'Sakarya Applied Sciences University': 'Sakarya Uygulamali Bilimler University',
    'Isparta Applied Sciences University': 'Isparta Uygulamali Bilimler University',
    'Bilecik seyh Edebali University': 'Bilecik Seyh Edebali University',
    'Nigde omer Halisdemir University': 'Nigde Omer Halisdemir University',
    'Agri Ibrahim cecen University': 'Agri Ibrahim Cecen University',
    'Artvin coruh University': 'Artvin Coruh University',
    'Middle Eastern Technical University': 'Middle East Technical University',
    'Saglik Bilimleri University': 'Health Sciences University',
    'Afyonkarahisar Saglik Bilimleri University': 'Afyonkarahisar Health Sciences University',
    'Kutahya Saglik Bilimleri University': 'Kutahya Health Sciences University',
    'Antalya Science University': 'Antalya Bilim University',
    'Gaziantep Islamic Science and Technology University': 'Gaziantep Islam Science and Technology University',
    'Ankara Bilim University': 'Ankara Science University',
    'Ankara Sosyal Bilimler University': 'Ankara Social Sciences University',
    'Yildiz Teknik University' : 'Yildiz Technical University',
    'Orta Dogu Teknik University' : 'Middle East Technical University',
    'Yildiz Teknik University' : 'Yildiz Technical University',
    'Bursa Teknik University' : 'Bursa Technical University',
    'Erzurum Teknik University' : 'Erzurum Technical University',
    'Eskisehir Teknik University' : 'Eskisehir Technical University',
    'Izmir Democracy University' : 'Izmir Demokrasi University',
    'Ihsan Dogramaci Bilkent University' : 'Bilkent University',
    'Izmir Economics University' : 'Izmir Ekonomi University'

}

# Üniversite isimlerini düzenle
df['University'] = df['University'].replace(replace_dict)

# Makale sayılarını birleştir (Year ve University bazında)
df = df.groupby(['Year', 'University'], as_index=False).agg({'Number of Articles': 'sum'})

# Sonuçları kaydet
output_path = r'C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\cleaned_yearly_university_article_count.xlsx'
df.to_excel(output_path, index=False)

print(f'İşlem tamamlandı. Dosya {output_path} olarak kaydedildi.')
