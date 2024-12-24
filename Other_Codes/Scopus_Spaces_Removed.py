import pandas as pd
import re

# Dosya yolu
file_path = r'C:\Users\alibaki.turkoz\Desktop\CS552_Project_Ali_Baki_TÜRKÖZ_Github\Eng_Datasets\final_scopus_with_type_1854_2015.xlsx'

# Excel dosyasını oku
df = pd.read_excel(file_path)

# Noktalama işaretlerinin etrafındaki boşlukları kaldıran fonksiyon
def clean_punctuation_spaces(text):
    if isinstance(text, str):
        # Noktalama işaretlerinden önceki ve sonraki boşlukları kaldır
        text = re.sub(r'\s*([.,;:!?])\s*', r'\1', text)
    return text

# Tüm DataFrame için uygulanacak
df = df.applymap(clean_punctuation_spaces)

# Temizlenmiş veriyi tekrar kaydet
output_path = file_path.replace('.xlsx', '_cleaned.xlsx')
df.to_excel(output_path, index=False)

print(f'Temizlik tamamlandı. Dosya {output_path} olarak kaydedildi.')
