from bs4 import BeautifulSoup
import requests
import re

response = requests.get('https://www.amazon.in/dp/B07DJHY82F/ref=gbph_img_m-5_d182_b23b14bf?smid=A23AODI1X2CEAE&pf_rd_p=a3a8dc53-aeed-4aa1-88bb-72ce9ddad182&pf_rd_s=merchandised-search-5&pf_rd_t=101&pf_rd_i=1389401031&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_r=P3FSQH2KEB3B5QQ1NQD5')

soup = BeautifulSoup(response.content, 'html.parser')
# soup = soup.prettify()
# f = open('out.txt','w')
# f.write(str(soup))
# print(soup.prettify())

main_dict = {}

main_dict = {
  'title' : [],
  'description' : [],
  'price' : [],
  'colors': [],
  'reviews' : [],
  'rating' : [],
  'details':[],
  'img':[],
  'revs':[]
  }


# title
title = soup.select_one('span#productTitle').text
main_dict['title'].append(title)

#description
description = soup.select_one('div#productDescription').text
main_dict['description'].append(description)

#star rating
rating = soup.select_one('i.a-icon.a-icon-star').text
main_dict['rating'].append(rating)

#colors
colors = soup.find_all('li')
for i in colors:
  # print(i.attrs)
  temp = dict(i.attrs)
  if 'title' in temp.keys():
    if('GB' in temp['title']):
      continue
    else:
      # print(temp['title'])
      temp['title'] = temp['title'].replace('Click to select','')
      main_dict['colors'].append(temp['title'])  
      # print(temp['title'])

#no of reviews
reviews = soup.select_one('span#acrCustomerReviewText').text
main_dict['reviews'].append(reviews)

# details of product
details_div = soup.find_all('div',class_ = "pdTab")
details =  details_div[0].find_all('tr')

# print(details[1].find_all('td'))

details_dict = {}
for i in details:
  td = i.find_all('td')
  details_dict[td[0].text] = td[1].text 

main_dict['details'] = details_dict

# detail image


allimg = soup.find_all('img')
# print(allimg.attrs)

for i in allimg:
  # print(i.attrs)
  temp = dict(i.attrs)
  if 'id' in temp.keys():
    if(temp['id'] == 'detailImage'):
      main_dict['img'].append(temp['src'])


#price

# price_without = soup.select_one('span.a-section.a-spacing-none.a-padding-none')

# print(price_without)



# reviews text
revs_list = []
cnt = 0
for i in range(10):
  string = 'https://www.amazon.in/OnePlus-Midnight-Black-128GB-Storage/product-reviews/B07DJHY82F/ref=cm_cr_getr_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber'
  string += '='+str(i+1)
  # print(string)
  response = requests.get(string)
  soup = BeautifulSoup(response.content, 'html.parser')
  revs = soup.find_all('a' , class_ = 'review-title')
  for i in revs:
    temp = i.find_all('span')
    # print(temp[0].text)
    revs_list.append(temp[0].text)
    cnt +=1

print(cnt)
print(revs_list)

# revs = soup.find_all('a' , class_ = 'review-title') 

# for i in revs:
#   print(i.find_all('span'))



# main DS with all fields
print(main_dict)


