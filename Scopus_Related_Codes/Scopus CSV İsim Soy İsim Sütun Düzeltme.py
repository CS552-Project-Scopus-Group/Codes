import pandas as pd
import re
from unidecode import unidecode

# CSV dosyasını yükle
csv_path = r"C:\Users\alibaki.turkoz\Desktop\Ozyegin\CS_552_Python_ile_Veri_Bilimi\CS552 Project\CS552_Project_Çalışma Dosyası\Scopus Articles 1854-2015\scopus_articles_in_Türkiye_2024_1854.csv"  # Buraya kendi dosya yolunu yaz
df = pd.read_csv(csv_path)

def duzelt_author_names(author_full_names):
    if pd.isna(author_full_names):
        return ""
    # Yazar isimlerini ";" ile ayır
    authors = author_full_names.split(";")
    duzeltmis_authors = []
    for author in authors:
        # Parantez içindeki numaraları kaldır
        author = re.sub(r"\s*\(\d+\)", "", author).strip()
        # İsimleri "Soyad, Ad" formatından "Ad Soyad" formatına çevir
        soyad_ad = author.split(", ")
        if len(soyad_ad) == 2:
            ad_soyad = f"{soyad_ad[1]} {soyad_ad[0]}"
            # Türkçe karakterleri İngilizce karakterlere çevir
            ad_soyad = unidecode(ad_soyad)
            duzeltmis_authors.append(ad_soyad)
        else:
            duzeltmis_authors.append(unidecode(author))
    # Düzeltilmiş isimleri ";" ile birleştir
    return "; ".join(duzeltmis_authors)

# "Author full names" sütununu düzenle
df["Author full names"] = df["Author full names"].apply(duzelt_author_names)

# Düzenlenmiş dosyayı kaydet
output_path = r"C:\Users\alibaki.turkoz\Desktop\Ozyegin\CS_552_Python_ile_Veri_Bilimi\CS552 Project\CS552_Project_Çalışma Dosyası\Scopus Articles 1854-2015\duzenlenmis_dosya.csv"
df.to_csv(output_path, index=False)

print(f"Düzenlenmiş dosya kaydedildi: {output_path}")
