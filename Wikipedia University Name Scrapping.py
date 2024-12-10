from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Chrome seçeneklerini ayarlayın
options = webdriver.ChromeOptions()
options.add_argument(r"--user-data-dir=C:\Users\alibaki.turkoz\AppData\Local\Google\Chrome\User Data\Default")
options.add_argument("--profile-directory=Profile 2")

# Chrome WebDriver başlatma
driver = webdriver.Chrome(options=options)

# Kullanıcıdan URL alın
url = input("Enter the Wikipedia URL for the city: ")

# Excel'e kaydedilecek veriler
data = []

# URL'yi açalım
driver.get(url)
time.sleep(2)  # Sayfanın yüklenmesi için bekleyin

try:
    # Şehir adını başlıktan al ve ekleri temizle
    raw_city_name = driver.find_element(By.XPATH, '//*[@id="firstHeading"]').text
    city_name = raw_city_name.split("'")[0].strip()  # "'daki" veya "'deki" gibi ekleri temizler

    # Üniversiteler tablosundaki satırları bul
    rows = driver.find_elements(By.XPATH, '//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr')

    for row in rows:
        try:
            # Üniversite adını al
            university_name = row.find_element(By.XPATH, './td[1]/a').text.strip()
            data.append([city_name, university_name])
        except Exception as e:
            print(f"Error processing row: {e}")

    print(f"Data collected for {city_name} from {url}")

except Exception as e:
    print(f"Error extracting data from {url}: {e}")

# Veriyi DataFrame'e çevirme
df = pd.DataFrame(data, columns=["City", "University Name"])

# Excel dosyasına kaydetme
file_path = rf"C:\Users\alibaki.turkoz\Desktop\universities_in_{city_name}.xlsx"
df.to_excel(file_path, index=False)

# Tarayıcıyı kapat
driver.quit()

print(f"Data has been saved to {file_path}")
