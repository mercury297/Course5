from afinn import Afinn
import json


data = []
with open("classified.json", "r") as read_file:
    data = json.load(read_file)

afinn = Afinn()

buckets = ['Battery Life','Picture Quality','Value for Money','Sound Quality','Fingerprint']

score = {}

# for i in range(5):
#     score.update({i:[]})

# print(score[0])

for i in data:
    temp = data[i]
    t = []
    for j in temp:
        tot = afinn.score(j)
        t.append(tot)
    score[i] = t
    # print(i, tot/len(temp))
cnt = 0
for i in score:
    temp = score[i]
    l = len(temp)
    pos , neg , nuet = 0,0,0
    for j in temp:
        if(j<0):
            neg+= 1
        elif(j>0):
            pos += 1
        else:
            nuet += 1
    print('for ',buckets[cnt])
    print('\n positive % is',(pos/l)*100,end='\t')
    print('negative % is',(neg/l)*100,end='\t')
    print('neutral % is', (nuet / l) * 100)
    print()
    cnt += 1


