import pandas as pd
import matplotlib.pyplot as plt

# CSV dosyasının yolu
dosya_yolu = r"C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Eng_Datasets\Scopus_Articles_in_Turkey_1854_2024_V2_eng_karakter.csv"

# CSV dosyasını oku
df = pd.read_csv(dosya_yolu)

# Tüm sütun isimlerini görüntüle
print("Columns in CSV File:")
print(df.columns)

# 'year' sütununu kontrol et
year_sutunlari = [sutun for sutun in df.columns if 'year' in sutun.lower()]
if year_sutunlari:
    print(f"Column(s) containing Year information: {year_sutunlari}")
    # İlk sütunu kullanarak yıl analizini yapalım
    year_sutunu = year_sutunlari[0]
    print(f"\n'{year_sutunu}' Unique year values ​​in column:")
    print(df[year_sutunu].dropna().unique())

    # Yıllara göre makale sayısını hesapla
    makale_sayisi = df[year_sutunu].value_counts().sort_index()

    # Tüm veriyi CSV'ye kaydetme
    kayit_yolu_csv = r"C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Data Analysis\Year-Number_of_Articles.csv"
    makale_sayisi.to_csv(kayit_yolu_csv, index=True, header=['Number of Articles'])
    print(f"\nAll Year Data has been saved to: {kayit_yolu_csv}")

    # 1970'ten itibaren olan verileri filtrele
    makale_sayisi_1970 = makale_sayisi[makale_sayisi.index >= 1970]

    # 1970'ten itibaren grafiğini oluşturma ve PNG olarak kaydetme
    plt.figure(figsize=(12, 6))
    makale_sayisi_1970.plot(kind='bar', title='Number of Articles by Year (1970 and onwards)', ylabel='Number of Articles', xlabel='Year')
    plt.tight_layout()

    # PNG kaydetme yolu
    kayit_yolu_png = r"C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Data Analysis\Year-Number_of_Articles.png"
    plt.savefig(kayit_yolu_png, format='png')
    print(f"Graph (1970 and onwards) has been saved as PNG to: {kayit_yolu_png}")

    plt.show()
else:
    print("Error: No column containing 'year' information found.")
