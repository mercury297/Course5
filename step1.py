from bs4 import BeautifulSoup
import requests
import re
import json

response = requests.get('https://www.amazon.in/dp/B07DJHY82F/ref=gbph_img_m-5_d182_b23b14bf?smid=A23AODI1X2CEAE&pf_rd_p=a3a8dc53-aeed-4aa1-88bb-72ce9ddad182&pf_rd_s=merchandised-search-5&pf_rd_t=101&pf_rd_i=1389401031&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_r=P3FSQH2KEB3B5QQ1NQD5')

soup = BeautifulSoup(response.content, 'html.parser')

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


def fix(string):
  string = string.replace('\n','')
  string = string.replace('\t','')
  string = string.replace(u"\xa0", u" ")
  string = string.replace('\s','')
  return string


def for_select(tag ,name):
  temp = soup.select_one(tag).text
  main_dict[name].append(temp)


# title

for_select('span#productTitle','title')

#description

for_select('div#productDescription','description')


# #star rating

for_select('i.a-icon.a-icon-star','rating')

# #no of reviews

for_select('span#acrCustomerReviewText','reviews')


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


# details of product
details_div = soup.find_all('div',class_ = "pdTab")
details =  details_div[0].find_all('tr')

# print(details[1].find_all('td'))

details_dict = {}
for i in details:
  td = i.find_all('td')
  td[0] = fix(td[0].text)
  td[1] = fix(td[1].text)

  if(td[0] == '' or td[1] == '' ):
    continue
  details_dict[td[0]] = td[1]

main_dict['details'] = details_dict

# detail image


allimg = soup.find_all('img',id = 'landingImage')
# print(allimg)

for i in allimg:
  # print(i.attrs)
  temp = dict(i.attrs)
  if 'id' in temp.keys():
    main_dict['img'].append(temp['src'])


#price

price_without = soup.select_one('span#priceblock_ourprice').text

price_with = soup.select_one('span.a-color-price').text
# print(price_with)


main_dict['price'] = [fix(price_without),fix(price_with)]


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

# main_dict['revs'] = revs_list


for i in main_dict:
  if(i == 'details'):
    continue
  temp = main_dict[i]  
  # print(temp)
  if(len(temp)>0):
    string = temp[0]
    string = fix(string)
    temp[0] = string
  # print(temp)
  # break
  # for j in temp:
  #   fix(j)
  #   print(j)
  #   break



# main DS with all fields
print(main_dict)


# print(main_dict['title'][0].replace('\s',''))

out = open('words.json', 'w')

wordsJson = json.dumps(main_dict)

# print(wordsJson)
out.write((wordsJson))

