import pandas as pd
import matplotlib.pyplot as plt
import re

# Türkiye illeri listesi
turkiye_illeri = [
    "Adana", "Adiyaman", "Afyonkarahisar", "Agri", "Aksaray", "Amasya", "Ankara",
    "Antalya", "Ardahan", "Artvin", "Aydin", "Balikesir", "Bartin", "Batman",
    "Bayburt", "Bilecik", "Bingol", "Bitlis", "Bolu", "Burdur", "Bursa", "Canakkale",
    "Cankiri", "Corum", "Denizli", "Diyarbakir", "Duzce", "Edirne", "Elazig", "Erzincan",
    "Erzurum", "Eskisehir", "Gaziantep", "Giresun", "Gumushane", "Hakkari", "Hatay",
    "Igdir", "Isparta", "Istanbul", "Izmir", "Kahramanmaras", "Karabuk", "Karaman",
    "Kars", "Kastamonu", "Kayseri", "Kilis", "Kirikale", "Kirkareli", "Kirsehir",
    "Kocaeli", "Konya", "Kutahya", "Malatya", "Manisa", "Mardin", "Mersin", "Mugla",
    "Mus", "Nevsehir", "Nigde", "Ordu", "Osmaniye", "Rize", "Sakarya", "Samsun",
    "Sanliurfa", "Siirt", "Sinop", "Sirnak", "Sivas", "Tekirdag", "Tokat", "Trabzon",
    "Tunceli", "Usak", "Van", "Yalova", "Yozgat", "Zonguldak"
]

# CSV dosyasının yolu
dosya_yolu = r"C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Eng_Datasets\Scopus_Articles_in_Turkey_1854_2024_V2_eng_karakter.csv"

# CSV dosyasını oku
df = pd.read_csv(dosya_yolu)

# Affiliations sütunundaki şehir bilgisini çıkaran bir fonksiyon
def extract_city(affiliations):
    if pd.isna(affiliations):
        return []
    try:
        # Şehirleri çıkar, her bir şehir bir kelime olarak algılanır
        city_match = re.findall(r'\b(' + '|'.join(turkiye_illeri) + r')\b', affiliations)
        return city_match if city_match else []
    except:
        return []

# Affiliations sütununu kontrol et
affiliations_sutunlari = [sutun for sutun in df.columns if 'affiliation' in sutun.lower()]
year_sutunlari = [sutun for sutun in df.columns if 'year' in sutun.lower()]

if affiliations_sutunlari and year_sutunlari:
    year_sutunu = year_sutunlari[0]
    affiliations_sutunu = affiliations_sutunlari[0]
    
    # Şehir bilgisini çıkarmak için yeni sütun ekle
    df['Cities'] = df[affiliations_sutunu].apply(extract_city)

    # Şehirlerin sadece bir kez sayılması için City listesinde tekrarları kaldır
    # Eğer bir satırda aynı şehirden birden fazla varsa, her biri bir kez sayılır.
    df['Cities'] = df['Cities'].apply(lambda x: list(set(x)))

    # Yıllara ve şehirlere göre grupla
    yil_sehir_makale_sayisi = {}

    for _, row in df.iterrows():
        yil = row[year_sutunu]
        if pd.isna(yil):
            continue
        
        # Şehir listesine göre işlem yapalım
        for city in row['Cities']:
            if city and city in turkiye_illeri:
                if yil not in yil_sehir_makale_sayisi:
                    yil_sehir_makale_sayisi[yil] = {}
                if city not in yil_sehir_makale_sayisi[yil]:
                    yil_sehir_makale_sayisi[yil][city] = 0
                yil_sehir_makale_sayisi[yil][city] += 1

    # Veriyi bir DataFrame'e çevir
    data = []
    for yil, sehir_dict in yil_sehir_makale_sayisi.items():
        for sehir, sayi in sehir_dict.items():
            data.append([yil, sehir, sayi])

    makale_sayisi_df = pd.DataFrame(data, columns=[year_sutunu, 'City', 'Article Count'])

    # Sonuçları ekrana yazdır
    print("\nNumber of Articles by Year and City:")
    print(makale_sayisi_df)

    # Sonuçları CSV olarak kaydetme
    kayit_yolu_csv = r"C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Data Analysis\Year_City_Article_Count.csv"
    makale_sayisi_df.to_csv(kayit_yolu_csv, index=False)
    print(f"\nData has been saved to: {kayit_yolu_csv}")

    # Her şehir için ayrı grafikler oluşturuluyor ve PNG olarak kaydediliyor
    for city in turkiye_illeri:
        city_data = makale_sayisi_df[makale_sayisi_df['City'] == city]
        
        if not city_data.empty:
            # Grafik oluşturma
            plt.figure(figsize=(10, 6))
            plt.bar(city_data[year_sutunu], city_data['Article Count'], color='skyblue')
            plt.title(f"Number of Articles by Year for {city}")
            plt.xlabel("Year")
            plt.ylabel("Number of Articles")
            plt.xticks(rotation=45)
            plt.tight_layout()

            # PNG olarak kaydetme
            kayit_yolu_png = rf"C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Data Analysis\{city}_Year_Article_Count.png"
            plt.savefig(kayit_yolu_png, format='png')
            print(f"Graph for {city} has been saved to: {kayit_yolu_png}")

            plt.close()
else:
    print("Error: Required columns for 'Year' and 'Affiliations' analysis not found.")
