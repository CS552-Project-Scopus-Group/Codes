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

    # Fakültelere göre makale sayısı
    faculty_article_count = {}
    for _, row in df.iterrows():
        faculties = row['Faculties']
        for faculty in faculties:
            if faculty not in faculty_article_count:
                faculty_article_count[faculty] = {}
            if row['Year'] not in faculty_article_count[faculty]:
                faculty_article_count[faculty][row['Year']] = 0
            faculty_article_count[faculty][row['Year']] += 1

    # Departmanlara göre makale sayısı
    department_article_count = {}
    for _, row in df.iterrows():
        departments = row['Departments']
        for department in departments:
            if department not in department_article_count:
                department_article_count[department] = {}
            if row['Year'] not in department_article_count[department]:
                department_article_count[department][row['Year']] = 0
            department_article_count[department][row['Year']] += 1

    # Fakültelere ait makale sayısını DataFrame'e çevir
    faculty_df = pd.DataFrame(faculty_article_count.items(), columns=['Faculty', 'Yearly Article Count'])
    department_df = pd.DataFrame(department_article_count.items(), columns=['Department', 'Yearly Article Count'])

    # Toplam makale sayısını ekleyin
    faculty_df['Article Count'] = faculty_df['Yearly Article Count'].apply(lambda x: sum(x.values()))
    department_df['Article Count'] = department_df['Yearly Article Count'].apply(lambda x: sum(x.values()))

    # 500'den az olanları filtrele
    faculty_df = faculty_df[faculty_df['Article Count'] >= 500]
    department_df = department_df[department_df['Article Count'] >= 3000]

    # Sonuçları ekrana yazdır
    print("\nNumber of Articles by Faculty:")
    print(faculty_df)
    print("\nNumber of Articles by Department:")
    print(department_df)

    # Sonuçları CSV olarak kaydetme
    kayit_yolu_faculty_csv = r"C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Data Analysis\Faculty_Article_Count_Post_1990_Filtered.csv"
    faculty_df.to_csv(kayit_yolu_faculty_csv, index=False)
    kayit_yolu_department_csv = r"C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Data Analysis\Department_Article_Count_Post_1990_Filtered.csv"
    department_df.to_csv(kayit_yolu_department_csv, index=False)

    print(f"\nFaculty data has been saved to: {kayit_yolu_faculty_csv}")
    print(f"\nDepartment data has been saved to: {kayit_yolu_department_csv}")

    # Fakültelere ait toplam makale sayısı grafik oluşturma
    if not faculty_df.empty:
        plt.figure(figsize=(12, 6))
        faculty_df = faculty_df.sort_values(by='Article Count', ascending=False)
        plt.bar(faculty_df['Faculty'], faculty_df['Article Count'], color='skyblue')
        plt.title("Number of Articles by Faculty (Post 1990 - >=500 Filtered)")
        plt.xlabel("Faculty")
        plt.ylabel("Number of Articles")
        plt.xticks(rotation=90)
        plt.tight_layout()

        # Fakültelere ait toplam makale sayısı grafik kaydetme
        kayit_yolu_faculty_total_png = r"C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Data Analysis\Faculty_Article_Count_Post_1990_Filtered.png"
        plt.savefig(kayit_yolu_faculty_total_png, format='png')
        print(f"Graph for Faculty Total has been saved to: {kayit_yolu_faculty_total_png}")

        plt.close()

    # Departmanlara ait toplam makale sayısı grafik oluşturma
    if not department_df.empty:
        plt.figure(figsize=(12, 6))
        department_df = department_df.sort_values(by='Article Count', ascending=False)
        plt.bar(department_df['Department'], department_df['Article Count'], color='lightgreen')
        plt.title("Number of Articles by Department (Post 1990 - >=3000 Filtered)")
        plt.xlabel("Department")
        plt.ylabel("Number of Articles")
        plt.xticks(rotation=90)
        plt.tight_layout()

        # Departmanlara ait toplam makale sayısı grafik kaydetme
        kayit_yolu_department_total_png = r"C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Data Analysis\Department_Article_Count_Post_1990_Filtered.png"
        plt.savefig(kayit_yolu_department_total_png, format='png')
        print(f"Graph for Department Total has been saved to: {kayit_yolu_department_total_png}")

        plt.close()

else:
    print("Error: Required column for 'Affiliations' analysis not found.")
