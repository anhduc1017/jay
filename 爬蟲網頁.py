import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

# 啟動 Chrome 瀏覽器（自動下載驅動 )
# 前往 Google 搜尋頁
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.toysrus.com.tw/zh-tw/")

# 模擬滾動頁面載入內容
for _ in range(3):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# 取得完整 HTML 原始碼
page_source = driver.page_source
soup = BeautifulSoup(page_source, "html.parser")

# 抓取所有分類 banner 區塊
banners = soup.find_all("div", class_="banner")

print(f"共找到 {len(banners)} 個分類\n")

for banner in banners:
    # 連結
    link_tag = banner.find("a", class_="link")
    link = link_tag["href"] if link_tag and link_tag.has_attr("href") else ""

    # 圖片連結
    img_tag = banner.find("img")
    img_src = img_tag["src"] if img_tag and img_tag.has_attr("src") else ""

    # 名稱：從圖片 URL 中猜名稱（圖片檔名）
    if img_src:
        filename = img_src.split("/")[-1]  # 取圖片名稱
        name = filename.split("-")[0].replace("%22", "").replace("%20", "").capitalize()
    else:
        name = "未知"

    print(f"類別名稱: {name}")
    print(f"連結: {link}")
    print(f"圖片: {img_src}")
    print("\n")

driver.quit()

