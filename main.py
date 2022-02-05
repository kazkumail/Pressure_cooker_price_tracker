import requests
from bs4 import BeautifulSoup
import smtplib
import lxml

URL = "https://www.amazon.com/Instant-Pot-Pressure-Steamer-Sterilizer/dp/B08PQ2KWHS/ref=dp_fod_1?pd_rd_i=B08PQ2KWHS&th=1"
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}

HTML_page_amazon = requests.get(URL, headers=header)

soup = BeautifulSoup(HTML_page_amazon.content, "lxml")
price = soup.find(class_="a-offscreen").get_text()
price_without_sign = price.split("$")[1]
print(price_without_sign)

title = soup.find(id="productTitle").get_text().strip()
print(title)

if int(price_without_sign) < 100:
    message = f"{title} is now {price}"

    with smtplib.SMTP(EMAIL, port=587) as connection:
        connection.starttls()
        result = connection.login(EMAIL, PASSWORD)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=EMAIL,
            msg=f"Subject: Amazon Price Alert!\n\n {message}\n {URL}"
        )
