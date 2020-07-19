import requests
from bs4 import BeautifulSoup
from decimal import Decimal
location_list=[]
location_url_list=[]

final_list=[]


def last_page(url):
  result=requests.get(url)
  soup=BeautifulSoup(result.text,"html.parser")
  pages=soup.find("div",{"class":"pageNumbers"}).find_all("a")
  last_page=pages[-1].get_text(strip=True)
  return int(last_page)

def rstrt_last_page(url):
  result=requests.get(url)
  soup=BeautifulSoup(result.text,"html.parser")
  pages=soup.find_all("a",{"class":"pageNum taLnk"})
  last_page=pages[-1].get_text(strip=True)
  return int(last_page)


def extract_locations(): 
  
  url=f"https://www.tripadvisor.co.kr/Restaurants-g293910-Taiwan.html#LOCATION_LISTl"
  last=last_page(url)

  for i in range(last):
    number=i*20

    print("scrapping location page: ",i+1)
 
    result=requests.get(f"https://www.tripadvisor.co.kr/Restaurants-g293910-oa{number}-Taiwan.html#LOCATION_LISTl")
    soup=BeautifulSoup(result.text,"html.parser")
    if number==0:
      locations=soup.find_all("div",{"class":"geo_name"})
    else:
       locations=soup.find("ul",{"class":"geoList"}).find_all("li")
       
    if locations:
      for loc in locations:
          loc=loc.find("a")
          location_list.append(loc.get_text(strip=True)[0:-4]) 
          location_url_list.append("https://tripadvisor.co.kr"+loc['href'])
  return 0

def extract_rstrt(last_page,location_url):
  rstrt_list=[]
  for i in range(last_page):
    tag_list=[]
    tag_with_rstrt_link=[]
    
    url=""
    print("Scraping Resturant page: ",i+1)

    first=location_url.split("-")[0]
    second=location_url.split("-")[1:]
    end=""
    for sec in second:
      end=end+sec+"-"
    url=first+f"-oa{30*i}-"+end[0:-1]
    result=requests.get(url)
    soup=BeautifulSoup(result.text,"html.parser")
    tag_with_rstrt_link=soup.find_all("a",{"class":"_15_ydu6b"})
    tag_list+=tag_with_rstrt_link
    
    rstrt_url_list=[]
    print("len(tag_list): ",len(tag_list))

    for tag in tag_list:
      url="https://tripadvisor.co.kr"+tag['href']
      rstrt_url_list.append(url)
      
    for rstrt_url in rstrt_url_list:
      result=requests.get(rstrt_url)
      soup=BeautifulSoup(result.text,"html.parser")
      rstrt_name=soup.find("h1").get_text(strip=True).split(",")[0]
      
      rates=soup.find_all("span",{"class":"row_num"})
      star=5
      rstrt_rate=0#식당의 평균평점
      count=0 #총 리뷰 개수
      for rate in rates:
        rate=int(rate.get_text(strip=True))#별점당 평점개수
        rstrt_rate+=star*rate
        count+=rate
        star=star-1
        if (star<1):
          break
      if (count!=0):
        rstrt_rate=float(Decimal(rstrt_rate/count))
        rstrt_rate=round(rstrt_rate,1)
      else:
        rstrt_rate=0

      rstrt_review_count=count
  
      rstrt_list.append(
      {"name":rstrt_name,
      "rate":rstrt_rate,
      "review":rstrt_review_count,
      "link":rstrt_url})
    print("len(rstrt_list): ",len(rstrt_list))

  return rstrt_list

def extract_rstrts():
  extract_locations()
  for i in range(0,len(location_list)):#각 지역별로 링크 탐색
    print("< Location: ",location_list[i],">")
    last_page=rstrt_last_page(location_url_list[i])#그지역음식점 마지막페이지
    print("rstrt_last_page: ",last_page)

    rstrt_list=extract_rstrt(last_page,location_url_list[i])
    final_list.append({location_list[i]:rstrt_list})
  return final_list

