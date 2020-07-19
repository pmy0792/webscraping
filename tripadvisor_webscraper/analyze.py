import numpy as np
import matplotlib.pyplot as plt


def analyze_one_location(li):
  plt.clf()
  one,two,three,four,five=0,0,0,0,0,
  
  restaurants=list(li.values())[0]
  for restaurant in restaurants:
    rate=float(restaurant.get("rate"))
    if (1<=rate<2):
      one+=1
    elif (2<=rate<3):
      two+=1
    elif (3<=rate<4):
      three+=1
    elif (4<=rate<5):
      four+=1
    elif (rate==5):
      five+=1

  rate = [one, two, three, four, five]
  bars = ('1', '2', '3', '4', '5')
  y_pos = np.arange(len(bars))
  plt.barh(y_pos, rate)
  plt.yticks(y_pos, bars)
  return plt

def show_analyze_result(final_list):
  for li in final_list:
    result=analyze_one_location(li)
    imagename= '/home/runner/webscraper3/image/'+ str(list(li.keys())[0]) 
    result.savefig(imagename)


