import os
from selenium import webdriver

# from pyvirtualdisplay import Display

cur_path = os.path.dirname(os.path.abspath(__file__))

# display = Display(
#     visible=0,
#     size=(1024, 768),
# )
# display.start()

driver = webdriver.Chrome(executable_path=f"{cur_path}/chromedriver")
# url = "https://www.google.com"
url = "https://genelife.asia/"
driver.get(url)

reval = driver.find_elements_by_css_selector(
    "#wrap_ > div:nth-child(1) > section > section.home__performance.inner.inner--90.home__section.pos_rel.bg > div.home__section__inner.home__performance__inner > p.home__performance__num.odometer.odometer-auto-theme > div"
)

print(reval[0].get_property())
