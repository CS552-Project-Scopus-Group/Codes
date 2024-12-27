import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# Dosyanın yolu (Dosyanın doğru yolunu burada güncelleyin)
file_path = r'C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Data Analysis\Yearly_university_article_count.xlsx'

# Veriyi yükle
df = pd.read_excel(file_path)

# Grafik klasörleri oluştur
output_folder_yearly = r'C:\Users\alibaki.turkoz\Desktop\Graphs\Yearly'
output_folder_university = r'C:\Users\alibaki.turkoz\Desktop\Graphs\University'
os.makedirs(output_folder_yearly, exist_ok=True)
os.makedirs(output_folder_university, exist_ok=True)

# Yılları al
years = df['Year'].unique()

# Üniversiteleri al
universities = df['University'].unique()

# Yıllara göre grafikler
for year in years:
    # Her yıl için veriyi filtrele
    df_year = df[df['Year'] == year]

    # Üniversitelere göre sırala
    df_year_sorted = df_year.sort_values(by='Number of Articles', ascending=False)

    # Üniversiteleri 30'luk gruplara böl
    num_universities = len(df_year_sorted)
    groups = [df_year_sorted[i:i + 30] for i in range(0, num_universities, 30)]

    # Alt grafik boyutu hesaplama
    num_groups = len(groups)
    cols = 2  # Her satırda 3 grafik
    rows = (num_groups // cols) + (1 if num_groups % cols else 0)

    # Tüm grupları tek bir PNG'ye koy
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 6, rows * 4))
    axes = axes.flatten()

    for idx, group in enumerate(groups):
        ax = axes[idx]
        sns.barplot(data=group, x='University', y='Number of Articles', color='skyblue', ax=ax)
        ax.set_title(f'Group {idx + 1}')
        ax.set_xticklabels(group['University'], rotation=45, ha='right', fontsize=8)
        ax.set_ylabel('Number of Articles')
        ax.set_xlabel('University')

    # Boş eksenleri kaldır
    for idx in range(len(groups), len(axes)):
        fig.delaxes(axes[idx])

    plt.tight_layout()
    year_output_path = os.path.join(output_folder_yearly, f'{year}_university_article_counts.png')
    plt.savefig(year_output_path)
    plt.close()

# Üniversitelere göre grafikler
for university in universities:
    # Her üniversite için veriyi filtrele
    df_university = df[df['University'] == university].sort_values(by='Year')

    # Grafik oluştur
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_university, x='Year', y='Number of Articles', color='skyblue')
    plt.title(f'{university} - Articles per Year')
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.ylabel('Number of Articles')
    plt.xlabel('Year')
    plt.tight_layout()

    # Grafiği kaydet
    university_output_path = os.path.join(output_folder_university, f'{university}_articles_per_year.png')
    plt.savefig(university_output_path)
    plt.close()
