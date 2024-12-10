from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re  # Regular expression kullanacağız
 
# Chrome seçeneklerini ayarlayın
options = webdriver.ChromeOptions()
options.add_argument(r"--user-data-dir=C:\Users\alibaki.turkoz\AppData\Local\Google\Chrome\User Data\Default")
options.add_argument("--profile-directory=Profile 2")
 
# Chrome WebDriver başlatma
driver = webdriver.Chrome(options=options)
 
# Düzeltilmiş URL
url = "https://yokatlas.yok.gov.tr/lisans-univ.php?u=2077"
 
# Excel'e kaydedilecek veriler
data = set()  # Set kullanarak benzersiz veriler tutalım
 
# URL'yi açalım
driver.get(url)
time.sleep(2)  # Sayfanın yüklenmesi için bekleyin
 
# Veriyi çekmek için XPath
try:
    # Belirttiğiniz XPath kullanarak veriyi çekelim
    element_xpath = '/html/body/div[1]/div[2]/div[2]/div'
 
    # Veriyi bul ve metni al
    element = driver.find_element(By.XPATH, element_xpath)
    rows = element.text.strip().split('\n')  # Satırlara ayıralım
 
    # EA, SAY, DİL, SÖZ kelimelerini ve parantez içeriğini hariç tutarak verileri ekleyelim
    for row in rows:
        if not any(keyword in row for keyword in ["EA", "SAY", "DİL", "SÖZ", "KKTC"]):
            # Parantez içindeki metni çıkaralım
            row_cleaned = re.sub(r'\(.*?\)', '', row)  # Parantez içindekileri temizle
            data.add(row_cleaned.strip())  # Satırı set'e ekleyelim (benzersiz olacak)
 
    print(f"Data collected from {url}")
 
except Exception as e:
    print(f"Error extracting data from {url}: {e}")
 
# Veriyi DataFrame'e çevirme
df = pd.DataFrame(list(data), columns=["Departments"])
 
# Excel dosyasına kaydetme
file_path = r"C:\Users\alibaki.turkoz\Desktop\Gaziantep_Sanko_University_Departments.xlsx"
df.to_excel(file_path, index=False, header=True)
 
# Tarayıcıyı kapat
driver.quit()
 
print(f"Data has been saved to {file_path}")