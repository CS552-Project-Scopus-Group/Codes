import pandas as pd
import matplotlib.pyplot as plt
import re

# CSV dosyasının yolu
dosya_yolu = r"C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Eng_Datasets\Scopus_Articles_in_Turkey_1854_2024_V2_eng_karakter.csv"

# CSV dosyasını oku
df = pd.read_csv(dosya_yolu)

# 'Year' sütunu olup olmadığını kontrol et ve 1990'dan sonrasını filtrele
if 'Year' in df.columns:
    df = df[df['Year'] >= 1990]

# Fakülte ve Departman bilgilerini çıkaran fonksiyonlar
def extract_faculty(affiliations):
    if pd.isna(affiliations):
        return []
    try:
        # Faculty of ... kısmını yakalamak için regex kullan
        faculty_match = re.findall(r'Faculty of ([^,]*)', affiliations)
        return faculty_match if faculty_match else []
    except:
        return []

def extract_department(affiliations):
    if pd.isna(affiliations):
        return []
    try:
        # Department of ... kısmını yakalamak için regex kullan
        department_match = re.findall(r'Department of ([^,]*)', affiliations)
        return department_match if department_match else []
    except:
        return []

# Affiliations sütununu kontrol et
affiliations_sutunlari = [sutun for sutun in df.columns if 'affiliation' in sutun.lower()]

if affiliations_sutunlari:
    affiliations_sutunu = affiliations_sutunlari[0]
    
    # Fakülte ve Departman bilgilerini çıkarmak için yeni sütunlar ekle
    df['Faculties'] = df[affiliations_sutunu].apply(extract_faculty)
    df['Departments'] = df[affiliations_sutunu].apply(extract_department)

    # Fakültelere göre makale sayısı (yıllara göre)
    faculty_article_count = {}
    for _, row in df.iterrows():
        faculties = row['Faculties']
        year = row['Year']
        for faculty in faculties:
            if faculty not in faculty_article_count:
                faculty_article_count[faculty] = {}
            if year not in faculty_article_count[faculty]:
                faculty_article_count[faculty][year] = 0
            faculty_article_count[faculty][year] += 1

    # Departmanlara göre makale sayısı (yıllara göre)
    department_article_count = {}
    for _, row in df.iterrows():
        departments = row['Departments']
        year = row['Year']
        for department in departments:
            if department not in department_article_count:
                department_article_count[department] = {}
            if year not in department_article_count[department]:
                department_article_count[department][year] = 0
            department_article_count[department][year] += 1

    # Fakültelere ait yıllara göre makale sayısı grafik oluşturma
    if faculty_article_count:
        for faculty, yearly_data in faculty_article_count.items():
            years = sorted(yearly_data.keys())
            article_counts = [yearly_data[year] for year in years]

            plt.figure(figsize=(12, 6))
            plt.plot(years, article_counts, marker='o', color='skyblue')
            plt.title(f"Number of Articles by Faculty: {faculty} (Post 1990)")
            plt.xlabel("Year")
            plt.ylabel("Number of Articles")
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Fakültelere ait yıllık grafik kaydetme
            kayit_yolu_faculty_year_png = rf"C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Data Analysis\Faculty_Based\{faculty.replace(' ', '_')}_Faculty_Yearly_Article_Count.png"
            plt.savefig(kayit_yolu_faculty_year_png, format='png')
            print(f"Graph for Faculty ({faculty}) has been saved to: {kayit_yolu_faculty_year_png}")

            plt.close()

    # Departmanlara ait yıllara göre makale sayısı grafik oluşturma
    if department_article_count:
        for department, yearly_data in department_article_count.items():
            years = sorted(yearly_data.keys())
            article_counts = [yearly_data[year] for year in years]

            plt.figure(figsize=(12, 6))
            plt.plot(years, article_counts, marker='o', color='lightgreen')
            plt.title(f"Number of Articles by Department: {department} (Post 1990)")
            plt.xlabel("Year")
            plt.ylabel("Number of Articles")
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Departmanlara ait yıllık grafik kaydetme
            kayit_yolu_department_year_png = rf"C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Data Analysis\Department_Based\{department.replace(' ', '_')}_Department_Yearly_Article_Count.png"
            plt.savefig(kayit_yolu_department_year_png, format='png')
            print(f"Graph for Department ({department}) has been saved to: {kayit_yolu_department_year_png}")

            plt.close()

else:
    print("Error: Required column for 'Affiliations' analysis not found.")
