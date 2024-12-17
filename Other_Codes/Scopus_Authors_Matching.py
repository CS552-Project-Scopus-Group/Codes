import pandas as pd
 
# Dosya yolları
file1_path = r"C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Eng_Datasets\organized_universities_academics.xlsx"
file2_path = r"C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Eng_Datasets\Scopus_Articles_in_Turkey_1854_2024_V2_eng_karakter.csv"
 
# Dosyaları oku
df1 = pd.read_excel(file1_path)  # Excel dosyasını oku
df2 = pd.read_csv(file2_path)  # CSV dosyasını oku
 
# Author full names sütununu ve Academic Name sütununu al
df2['Author full names'] = df2['Author full names'].str.split(';')  # Author full names'leri split et
df2 = df2.explode('Author full names')  # Listeleri satırlara ayır
 
# 1. dosyada "Academic Name" ve 2. dosyada "Author full names" eşleşmesi
matched = pd.merge(df1, df2, left_on='Academic Name', right_on='Author full names', how='inner')
 
# Gereksiz sütunları sil
columns_to_drop = ['Affiliations', 'Document Type', 'Author full names', 'Title_y']
matched = matched.drop(columns=columns_to_drop)
 
# "Academic Name" bazında "Number of Articles", "Years", "University Name", "Title_x", "Faculty" ve "Major" sütunlarını oluştur
grouped = matched.groupby('Academic Name').agg(
    Number_of_Articles=('Academic Name', 'size'),
    Years=('Year', lambda x: ', '.join(map(str, sorted(x.unique())))),
    University_Name=('University Name', 'first'),
    Title_x=('Title_x', 'first'),
    Faculty=('Faculty', 'first'),
    Major=('Major', 'first')
).reset_index()
 
# Çıktı dosyasının kaydedileceği klasör ve dosya adı
output_folder = r"C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Eng_Datasets"
output_file = f"{output_folder}\\matched_data.xlsx"
 
# Eşleşen verileri Excel dosyasına kaydet
grouped.to_excel(output_file, index=False)
print(f"Eşleşen veriler {output_file} dosyasına kaydedildi.")