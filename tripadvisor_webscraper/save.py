import xlsxwriter
import csv
import pandas as pd

def save_to_csv(rstrt_list):
  location=list(rstrt_list.keys())[0]
  filename=location+".csv"
  
  file=open(filename,mode="w")
  writer=csv.writer(file)
  writer.writerow(["name", "rate", "review", "link"])
  for rstrt in list(rstrt_list.get(location)):
    writer.writerow(list(rstrt.values()))
  return filename

def excel_sheet(rstrt_list):
  writer = pd.ExcelWriter('restaurants.xlsx', engine='xlsxwriter')
  for location in rstrt_list:
    filename=save_to_csv(location)
    df = pd.read_csv(filename)
    df.to_excel(writer, sheet_name=filename.strip())
  writer.save()
