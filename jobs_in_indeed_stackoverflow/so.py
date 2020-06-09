import requests
from bs4 import BeautifulSoup
URL=f"https://stackoverflow.com/jobs?q=python"


def get_last_page():
  result=requests.get(URL)
  soup=BeautifulSoup(result.text,"html.parser")
  pages=soup.find("div",{"class":"s-pagination"}).find_all("a")
  last_page=pages[-2].get_text(strip=True)
  return int(last_page)


def extract_jobs(last_page):
  jobs=[]
  for page in range(last_page):
    print(f"Scrapping page in StackOverflow #{page}")
    result=requests.get(f"{URL}&pg={page}")
    soup=BeautifulSoup(result.text,"html.parser")

    results=soup.find_all("div",{"class":"-job"})
    for result in results:
      job=extract_job(result)
      jobs.append(job)
  return jobs  

def extract_job(result):
  title=result.find("a",{"class":"s-link stretched-link"})["title"].strip()
  company=result.find("h3",{"class":"fc-black-700"}).find("span").string
  if company:
    company=company.strip()
  else:
    company=None
    
  location=result.find("span",{"class":"fc-black-500"}).string
  if location:
    location=location.strip()
  else:
    location=None

  job_id=result["data-jobid"]

  return {
    "title":title,"company":company,"location":location,
    "link":f"https://stackoverflow.com/jobs/{job_id}"}

def get_jobs():
  last_page=get_last_page()
  jobs=extract_jobs(last_page)
  return jobs