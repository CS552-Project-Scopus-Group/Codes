import pandas as pd
import matplotlib.pyplot as plt

# Excel dosyalarını oku
df1 = pd.read_excel(r'C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Eng_Datasets\Scopus_articles_in_Türkiye_2016_2024.xlsx')
df2 = pd.read_excel(r'C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Eng_Datasets\Scopus_articles_in_Türkiye_1854_2015.xlsx')

# Dataframeleri birleştir
combined_df = pd.concat([df1, df2])
print("Combined DataFrame: ")
print(combined_df.head())

# City sütunundaki ; ile ayrılmış şehirleri ayır ve satırları çoğalt
def split_cities(row):
    if pd.isna(row['City']):
        return pd.DataFrame()  # NaN olanları tamamen çıkar
    cities = row['City'].split('; ')
    return pd.DataFrame({'Year': [row['Year']] * len(cities), 'City': cities})

expanded_df = pd.concat([split_cities(row) for _, row in combined_df.iterrows()], ignore_index=True)
print("Expanded DataFrame: ")
print(expanded_df.head(15))

# City ve Year bazında gruplama yaparak makale sayılarını hesapla
article_counts = expanded_df.groupby(['Year', 'City']).size().reset_index(name='Article_Count')
print("Article Counts Grouped by Year and City: ")
print(article_counts.head(15))

# Unknown olanları çıkar
article_counts = article_counts[article_counts['City'] != 'Unknown']

# CSV olarak kaydet
article_counts.to_csv(r'C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Data Analysis\CSV\article_counts.csv', index=False)

# Her yıl için ayrı grafik çiz ve kaydet
unique_years = article_counts['Year'].unique()
for year in unique_years:
    yearly_data = article_counts[article_counts['Year'] == year]
    
    plt.figure(figsize=(12, 6))
    plt.bar(yearly_data['City'], yearly_data['Article_Count'], color='skyblue')
    plt.xticks(rotation=45, ha='right')
    plt.title(f'{year} Yılı - Şehir Bazlı Makale Sayıları')
    plt.xlabel('Şehir')
    plt.ylabel('Makale Sayısı')
    plt.tight_layout()
    plt.savefig(rf'C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Data Analysis\PNG\{year}_article_counts.png')
    plt.close()
