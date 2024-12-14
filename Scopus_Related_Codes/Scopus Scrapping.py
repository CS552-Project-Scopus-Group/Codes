from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
 
# Chrome seçeneklerini ayarlayın
options = webdriver.ChromeOptions()
options.add_argument(r"--user-data-dir=C:\Users\alibaki.turkoz\AppData\Local\Google\Chrome\User Data\Default")
options.add_argument("--profile-directory=Profile 3")
 
# Chrome WebDriver başlatma
driver = webdriver.Chrome(options=options)
 
# URL'ler
urls = [
"https://www.scopus.com/record/display.uri?eid=2-s2.0-85204581005&origin=resultslist&sort=plf-f&src=s&sid=32f0b224ece73acf734cfbc58c66530e&sot=aff&sdt=aff&s=AF-ID%2860014930%29+AND+SUBJAREA%28ENGI%29&sl=34&sessionSearchId=32f0b224ece73acf734cfbc58c66530e&relpos=0"    # Diğer URL'ler burada devam ediyor...
]
 
# Excel'e kaydedilecek veriler
data = []
 
# URL'leri gezerek verileri toplayalım
for url in urls:
    driver.get(url)
    time.sleep(2)  # Sayfanın yüklenmesi için bekleyin
 
    # Verileri çekmek için XPath'ler
    try:
        # Makale ismini çekme
        article_title = driver.find_element(By.XPATH, '//*[@id="doc-details-page-container"]/article/div[2]/div[2]/section/div[1]/div[1]/div/h2/span').text
       
        # Yazar isimlerini çekme
        authors = driver.find_element(By.XPATH, '//*[@id="doc-details-page-container"]/article/div[2]/div[2]/section/div[1]/div[2]/div/ul').text
       
        # Üniversite adlarını çekme
        affiliations = driver.find_element(By.XPATH, '//*[@id="affiliation-section"]/div/div/ul').text
 
        # Veriyi listeye ekleyelim
        data.append([article_title, authors, affiliations, url])
   
    except Exception as e:
        print(f"Error extracting data from {url}: {e}")
 
# Veriyi DataFrame'e çevirme
df = pd.DataFrame(data, columns=["Article Title", "Authors", "Affiliations", "URL"])
 
# Excel dosyasına kaydetme
file_path = r"C:\Users\alibaki.turkoz\Desktop\scopus_data_deneme.xlsx"
df.to_excel(file_path, index=False)
 
# Tarayıcıyı kapat
driver.quit()
 
print(f"Data has been saved to {file_path}")