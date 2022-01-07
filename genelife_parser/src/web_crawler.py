import requests
from bs4 import BeautifulSoup

url = "https://genelife.asia/"

response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    sub_num = soup.select_one(
        "#wrap_ > div:nth-child(1) > section > section.home__performance.inner.inner--90.home__section.pos_rel.bg > div.home__section__inner.home__performance__inner > p.home__performance__num.odometer.odometer-auto-theme > div"
    )
    print(sub_num)
else:
    print(response.status_code)
