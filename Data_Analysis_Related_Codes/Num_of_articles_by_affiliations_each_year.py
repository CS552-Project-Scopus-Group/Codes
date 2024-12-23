import pandas as pd
import matplotlib.pyplot as plt
import math

# Excel dosyalarını oku
df1 = pd.read_excel(r'C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Eng_Datasets\Scopus_articles_in_Türkiye_2016_2024.xlsx')
df2 = pd.read_excel(r'C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Eng_Datasets\Scopus_articles_in_Türkiye_1854_2015.xlsx')

# Türkiye'deki üniversitelerin listesi
uni_list = pd.read_excel(r'C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Eng_Datasets\All_Türkiye_University_List_Eng.xlsx')

# Üniversite isimlerini küçük harfe çevirip boşlukları temizle (eşleştirme kolaylığı için)
uni_list['University'] = uni_list['University'].str.strip().str.lower()

# Dataframeleri birleştir
combined_df = pd.concat([df1, df2])

# Affiliations sütunundaki ; ile ayrılmış üniversiteleri ayır ve satırları çoğalt
def split_affiliations(row):
    if pd.isna(row['Affiliations']):
        return pd.DataFrame()  # NaN olanları tamamen çıkar
    affiliations = row['Affiliations'].split('; ')
    return pd.DataFrame({'Year': [row['Year']] * len(affiliations), 'Affiliation': affiliations})

expanded_df = pd.concat([split_affiliations(row) for _, row in combined_df.iterrows()], ignore_index=True)

# Üniversite isimlerini küçük harfe çevir
expanded_df['Affiliation'] = expanded_df['Affiliation'].str.strip().str.lower()

# Sadece listedeki üniversiteleri filtrele
filtered_df = expanded_df[expanded_df['Affiliation'].isin(uni_list['University'])]

# Üniversite ve yıl bazında makale sayısını hesapla
affiliation_counts = filtered_df.groupby(['Year', 'Affiliation']).size().reset_index(name='Article_Count')

# CSV olarak kaydet
affiliation_counts.to_excel(r'C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Data Analysis\CSV\filtered_affiliation_counts.xlsx', index=False)

# Her yıl için üniversiteleri gruplayarak grafik oluştur
unique_years = affiliation_counts['Year'].unique()
universities_per_plot = 30  # Bir subplot'ta 35 üniversite göster

for year in unique_years:
    yearly_data = affiliation_counts[affiliation_counts['Year'] == year]
    yearly_data = yearly_data.sort_values(by='Article_Count', ascending=False)
    
    num_universities = len(yearly_data)
    num_plots = math.ceil(num_universities / universities_per_plot)

    # Subplot düzeni (3 sütun x 2 satır)
    rows = math.ceil(num_plots / 3)
    fig, axes = plt.subplots(rows, 3, figsize=(18, 6 * rows))
    axes = axes.flatten()

    # Üniversite verilerini döngüyle ekle
    for i in range(num_plots):
        start_idx = i * universities_per_plot
        end_idx = start_idx + universities_per_plot
        subset_data = yearly_data[start_idx:end_idx]
        
        ax = axes[i]
        ax.bar(subset_data['Affiliation'], subset_data['Article_Count'], color='skyblue')
        ax.set_xticks(range(len(subset_data)))
        ax.set_xticklabels(subset_data['Affiliation'], rotation=45, ha='right')
        ax.set_title(f'{year} Yılı - {start_idx+1}-{min(end_idx, num_universities)} Üniversiteler')
        ax.set_ylabel('Makale Sayısı')

    # Boş grafikleri kaldır
    for j in range(num_plots, len(axes)):
        fig.delaxes(axes[j])

    # Genel başlık ve düzenleme
    plt.suptitle(f'{year} Yılı - Üniversite Bazlı Makale Sayıları')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Grafiklerin kaydedileceği dosya yolu
    plt.savefig(rf'C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Data Analysis\PNG\Num_of_articles_by_universities_each_year\{year}_affiliation_counts.png')
    plt.close()
