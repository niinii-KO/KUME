import numpy as np
import numpy.random as rd
import pandas as pd
from scipy.stats import truncnorm
import random

skip = False
nega = 0
light = 0
med = 0
heavy =0
hhh =0

ChildorAdult =  rd.choice(2, 15000, p=[0.334,0.666]) #0子供、1大人
Childp = [0.334, 0.666]  #疾患、非疾患
Adultp = [0.1, 0.9]
p = [Childp, Adultp]
sigmas = [3.5,7]
mus =[12,70]
low=[0,19]
high = [18,100]
tall = lambda CorA,Age,Sex: round([[5.433,4.3198],[0,0]][CorA][Sex]*(Age-4) + [[106.69,110.51],[163.1,149.4]][CorA][Sex] + 10 * rd.randn(),2)
#=rd.choice(2, 5, p=) # 4が出る確率が高い
table = []
c_cri = [[100,80,40,20],[0.7,1,1.2,2],[0.3,1,2,4],["なし", "焦点性", "全般性"],[0.5,2,3,3.4], [0.5,2,3,3.4],[0.5,2,3,3.4],[35,15,10,8.5],[150,110,60,45],[25,18,15,13]]
a_cri = [[100,80,40,20],[0.3,1,2,4],["なし", "漏出性", "滲出性"],["なし", "漏出性", "滲出性"],["なし", "I型", "II型"],[5,20,30,34], [8],[40,18,15,13]]
cri = [c_cri, a_cri]

def num_maker(CorA,Age,cri,tb):
  critb = cri[CorA]
  lislis = []
  if CorA == 0:
    if Age > 1 and Age<13:
      l = [0,2,3,4,5]
    else:
      l = [1,2,3,4,5]
    
    if Age == 0:
      l = l + [6]
    elif Age < 12:
      l = l + [7]
    else:
      l = l + [8]
  else:
    l = [0,1,2 + rd.choice(2),4 + rd.choice(2),6,7]
  
  j=0
  for i in l:
    #print(i)
    if critb[i] ==[8]:
      a = rd.choice(3) + 1
      a = 10**tb[j] * a
    elif len(critb[i]) == 3:
      a = critb[i][tb[i]]
    else:
      #print(critb[i])
      #print(tb)
      a = round(random.uniform(critb[i][tb[j]], critb[i][tb[j]+1]),2)
    lislis = lislis + [a]
    j=j+1
  return l + lislis

def num_maker2(f, mu, sigma,roundn=2):
  TF = False
  i=0
  while TF == False:
    i=i+1
    n = np.random.normal(mu, sigma)
    if f(n):
      TF = True
      TTF = round(n,roundn)
      if TTF is None:
        print(n)
      else:
        if i>100:
          print(i)
        return TTF
    else:
      if i>100:
        return round(mu+rd.choice(2, 1)[0],roundn)
kk =0
TF = False
for CorA in ChildorAdult:
  kk = kk+1
  Age = round(truncnorm.rvs((low[CorA] - mus[CorA]) / sigmas[CorA],  (high[CorA] - mus[CorA]) / sigmas[CorA], loc=mus[CorA], scale=sigmas[CorA]))
  Sex = rd.choice(2) #0male ,1female
  tb = rd.choice(3, 6, p=[0.4,0.3,0.3])

  lislis = [Age,Sex, tall(CorA,Age,Sex)] + [tb.tolist(), sum(tb)>5]
  l =num_maker(CorA,Age,cri,tb.tolist())
  lislis2 = lislis + l
  #print(lislis2)

  MF = ["男","女"]
  lislis3 = [lislis[0], MF[lislis[1]], lislis[2]]   #Age, Sex, Tall, 血清Cr, Weight, U_Cr, S_Na, U_Na, 
  if CorA == 0:
    #血清Cr
    if l[0] == 0:
      lislis3.append(round(0.35*lislis[2]/l[6],2))
      GFR = l[6]
    else:
      if Age > 10 and Sex == 0:
        if Age <16:
          a = 1
        else:
          a = 2
      else:
        a = 0
      lislis3.append(round([0.4+0.1*Age/5, 0.6+0.2*(Age-10)/5, 0.4+0.1*Age/5 + 0.1][a] * l[6],2))
      GFR = 80
    
    #体重
    if Age <1:
      lislis3.append(round(l[11]*lislis[2]**2/10000,3))
    elif Age <12:
      lislis3.append(round(l[11]*(lislis[2]/100)**3/10,1))
    else:
      lislis3.append(round(l[11]*(lislis[2]/100)**2,1))

    #U_Cr
    lislis3.append(round(GFR * lislis3[3] * (5.99 * np.sqrt(l[11]*lislis3[4])/10000)/(700/24/60 * 1.73),2))

    #S_Na
    lislis3.append(round(np.random.normal(140, 1.5),2))

    #U_Na
    lislis3.append(round(l[7]/100*lislis3[5]*lislis3[6]/lislis3[3],2))

    #てんかん
    ll = [["小児欠神てんかん","若年ミオクロニーてんかん"], ["ローランドてんかん"]]
    if l[8] == "焦点性":
      lislis3.append(ll[1][0])
    elif l[8] == "全般性":
      lislis3.append(ll[0][rd.choice(2)])
    else:
      lislis3.append("")
   

    #呼吸数
    if Age == 0:
      a=0
    elif Age==1:
      a =1
    elif Age<12:
      a =2
    else:
      a =3
    lislis3.append(round([40,30,30-5*(np.log2(Age/3)+1),15][a] * l[9],2))

    #血圧
    lislis3.append(round((70+2*Age)*l[10],2))
    lislis3 = lislis3+["","","","","","","","",""]
    #print(lislis3)
    #Age, Sex, Tall, 血清Cr, Weight, U_Cr, S_Na, U_Na,てんかん、呼吸数、血圧
  else:
    #SCr
    lislis3.append(round((l[6]/(Age**(-0.287)*194*[1,0.739][Sex]))**(-1/1.094),2))
    GFR=l[6]

    #Weight
    lislis3.append(round(l[11]*(lislis[2]/100)**2,1))

    #UCr
    lislis3.append(round(GFR * lislis3[3] * (5.99 * np.sqrt(l[11]*lislis3[4])/10000)/(22*lislis3[4]/24/60 * 1.73),2))
    
    #SNa
    lislis3.append(round(np.random.normal(148, 5),2))

    #UNa
    lislis3.append(round(l[7]/100*lislis3[5]*lislis3[6]/lislis3[3],2))


    PElis = [[num_maker2(lambda a: a <160, 80, 5),num_maker2(lambda a: a >160, 160, 5)]]
    PElis.append([num_maker2(lambda a: PElis[0][0]/a < 0.6, 210, 10),num_maker2(lambda a: PElis[0][0]/a > 0.6, 210, 50)])
    PElis.append([np.random.normal(7, 0.8)])
    PElis.append([num_maker2(lambda a: a/PElis[2][0] < 0.5, 3, 0.5),num_maker2(lambda a: a/PElis[2][0] > 0.5, 3, 3)])
    if l[2] ==2:
      #胸水
      #3胸水LDH,2血清LDH, 1血清タンパク質、 1胸水タンパク質
      if l[8] == "なし":
        lislis3 = lislis3 + ["",PElis[1][0],round(PElis[2][0],2),""]
      elif l[8] == "漏出性":
        lislis3 = lislis3 + [round(PElis[i][0],2) for i in range(4)]
      else:
        PE = rd.choice(2, 3)
        PE = PE.tolist()
        PE = PE[0:2] + [0]+ [PE[2]]
        lislis3 = lislis3 + [round(PElis[i][PE[i]],2) for i in range(4)]

      lislis3 = lislis3 + [round(np.random.normal(5, 0.8),2),""]  #腹水項目
    else:
      #腹水
      lislis3 = lislis3 + ["",round(PElis[1][0],2),round(PElis[2][0],2),""]

      #血清アルブミン
      lislis3.append(round(np.random.normal(5, 0.8),2))

      #腹水アルブミン
      if l[8] == "なし":
        lislis3.append("")
      elif l[8] == "漏出性":
        lislis3.append(round(lislis3[12]-num_maker2(lambda a: a>1.1, 1.5, 2),2))
      else:
        lislis3.append(round(lislis3[12]-num_maker2(lambda a: a<1.1, 1.0, 2),2))
      
    
    if l[3]==4:
      if l[9] == "なし":
        #PaO2, PaCo2
        lislis3 = lislis3 + [num_maker2(lambda a: a >60, 60, 5), num_maker2(lambda a: a <45, 40, 5)]
      elif l[9] == "I型":
        lislis3 = lislis3 + [num_maker2(lambda a: a <60, 60, 5), num_maker2(lambda a: a <45, 40, 5)]
      else:
        lislis3 = lislis3 + [num_maker2(lambda a: a <60, 60, 5), num_maker2(lambda a: a >45, 45, 5)]
    else:
      CO2 = num_maker2(lambda a: a <45, 40, 5)
      lislis3 = lislis3 + [round(150-CO2/0.8-l[9],2), CO2]
    lislis3.append(l[10])
    lislis3 = lislis3[0:7] +["","",""] +lislis3[7:]
    #print(kk)
  lislis3.append(sum(lislis2[3]))
  lislis3.append(np.random.normal(sum(lislis2[3]), num_maker2(lambda a: a>0, 0.25, 0.7)))
import numpy as np
import numpy.random as rd
import pandas as pd
from scipy.stats import truncnorm
import random

skip = False
nega = 0
light = 0
med = 0
heavy =0
hhh =0

ChildorAdult =  rd.choice(2, 15000, p=[0.334,0.666]) #0子供、1大人
Childp = [0.334, 0.666]  #疾患、非疾患
Adultp = [0.1, 0.9]
p = [Childp, Adultp]
sigmas = [3.5,7]
mus =[12,70]
low=[0,19]
high = [18,100]
tall = lambda CorA,Age,Sex: round([[5.433,4.3198],[0,0]][CorA][Sex]*(Age-4) + [[106.69,110.51],[163.1,149.4]][CorA][Sex] + 10 * rd.randn(),2)
#=rd.choice(2, 5, p=) # 4が出る確率が高い
table = []
c_cri = [[100,80,40,20],[0.7,1,1.2,2],[0.3,1,2,4],["なし", "焦点性", "全般性"],[0.5,2,3,3.4], [0.5,2,3,3.4],[35,15,10,8.5],[150,110,60,45],[25,18,15,13]]
a_cri = [[100,80,40,20],[0.3,1,2,4],["なし", "漏出性", "滲出性"],["なし", "漏出性", "滲出性"],["なし", "I型", "II型"],[5,20,30,34], [8],[40,18,15,13]]
cri = [c_cri, a_cri]

def num_maker(CorA,Age,cri,tb):
  critb = cri[CorA]
  lislis = []
  if CorA == 0:
    if Age > 1 and Age<13:
      l = [0,2,3,4,5]
    else:
      l = [1,2,3,4,5]
    
    if Age == 0:
      l = l + [6]
    elif Age < 12:
      l = l + [7]
    else:
      l = l + [8]
  else:
    l = [0,1,2 + rd.choice(2),4 + rd.choice(2),6,7]
  
  j=0
  for i in l:
    #print(i)
    if critb[i] ==[8]:
      a = rd.choice(3) + 1
      a = 10**tb[j] * a
    elif len(critb[i]) == 3:
      a = critb[i][tb[i]]
    else:
      #print(critb[i])
      #print(tb)
      a = round(random.uniform(critb[i][tb[j]], critb[i][tb[j]+1]),2)
    lislis = lislis + [a]
    j=j+1
  return l + lislis

def num_maker2(f, mu, sigma,roundn=2):
  TF = False
  i=0
  while TF == False:
    i=i+1
    n = np.random.normal(mu, sigma)
    if f(n):
      TF = True
      TTF = round(n,roundn)
      if TTF is None:
        print(n)
      else:
        if i>100:
          print(i)
        return TTF
    else:
      if i>100:
        return round(mu+rd.choice(2, 1)[0],roundn)
kk =0
TF = False
for CorA in ChildorAdult:
  kk = kk+1
  Age = round(truncnorm.rvs((low[CorA] - mus[CorA]) / sigmas[CorA],  (high[CorA] - mus[CorA]) / sigmas[CorA], loc=mus[CorA], scale=sigmas[CorA]))
  Sex = rd.choice(2) #0male ,1female
  tb = rd.choice(3, 6, p=[0.4,0.3,0.3])

  lislis = [Age,Sex, tall(CorA,Age,Sex)] + [tb.tolist(), sum(tb)>5]
  l =num_maker(CorA,Age,cri,tb.tolist())
  lislis2 = lislis + l
  #print([Age] + l)

  MF = ["男","女"]
  lislis3 = [lislis[0], MF[lislis[1]], lislis[2]]   #Age, Sex, Tall, 血清Cr, Weight, U_Cr, S_Na, U_Na, 
  if CorA == 0:
    #血清Cr
    if l[0] == 0:
      lislis3.append(round(0.35*lislis[2]/l[6],2))
      GFR = l[6]
    else:
      if Age > 10 and Sex == 0:
        if Age <16:
          a = 1
        else:
          a = 2
      else:
        a = 0
      lislis3.append(round([0.4+0.1*Age/5, 0.6+0.2*(Age-10)/5, 0.4+0.1*Age/5 + 0.1][a] * l[6],2))
      GFR = 80
    
    #体重
    if Age <1:
      lislis3.append(round(l[11]*lislis[2]**2/10000,3))
    elif Age <12:
      lislis3.append(round(l[11]*(lislis[2]/100)**3/10,1))
    else:
      lislis3.append(round(l[11]*(lislis[2]/100)**2,1))

    #U_Cr
    lislis3.append(round(GFR * lislis3[3] * (5.99 * np.sqrt(l[11]*lislis3[4])/10000)/(700/24/60 * 1.73),2))

    #S_Na
    lislis3.append(round(np.random.normal(140, 1.5),2))

    #U_Na
    lislis3.append(round(l[7]/100*lislis3[5]*lislis3[6]/lislis3[3],2))

    #てんかん
    ll = [["小児欠神てんかん","若年ミオクロニーてんかん"], ["ローランドてんかん"]]
    if l[8] == "焦点性":
      lislis3.append(ll[1][0])
    elif l[8] == "全般性":
      lislis3.append(ll[0][rd.choice(2)])
    else:
      lislis3.append("")
   

    #呼吸数
    if Age == 0:
      a=0
    elif Age==1:
      a =1
    elif Age<12:
      a =2
    else:
      a =3
    lislis3.append(round([40,30,30-5*(np.log2(Age/3)+1),15][a] * l[9],2))

    #血圧
    lislis3.append(round((70+2*Age)*l[10],2))
    lislis3 = lislis3+["","","","","","","","",""]
    #print(lislis3)
    #Age, Sex, Tall, 血清Cr, Weight, U_Cr, S_Na, U_Na,てんかん、呼吸数、血圧
  else:
    #SCr
    lislis3.append(round((l[6]/(Age**(-0.287)*194*[1,0.739][Sex]))**(-1/1.094),2))
    GFR=l[6]

    #Weight
    lislis3.append(round(l[11]*(lislis[2]/100)**2,1))

    #UCr
    lislis3.append(round(GFR * lislis3[3] * (5.99 * np.sqrt(l[11]*lislis3[4])/10000)/(22*lislis3[4]/24/60 * 1.73),2))
    
    #SNa
    lislis3.append(round(np.random.normal(148, 5),2))

    #UNa
    lislis3.append(round(l[7]/100*lislis3[5]*lislis3[6]/lislis3[3],2))


    PElis = [[num_maker2(lambda a: a <160, 80, 5),num_maker2(lambda a: a >160, 160, 5)]]
    PElis.append([num_maker2(lambda a: PElis[0][0]/a < 0.6, 210, 10),num_maker2(lambda a: PElis[0][0]/a > 0.6, 210, 50)])
    PElis.append([np.random.normal(7, 0.8)])
    PElis.append([num_maker2(lambda a: a/PElis[2][0] < 0.5, 3, 0.5),num_maker2(lambda a: a/PElis[2][0] > 0.5, 3, 3)])
    if l[2] ==2:
      #胸水
      #3胸水LDH,2血清LDH, 1血清タンパク質、 1胸水タンパク質
      if l[8] == "なし":
        lislis3 = lislis3 + ["",PElis[1][0],round(PElis[2][0],2),""]
      elif l[8] == "漏出性":
        lislis3 = lislis3 + [round(PElis[i][0],2) for i in range(4)]
      else:
        PE = rd.choice(2, 3)
        PE = PE.tolist()
        PE = PE[0:2] + [0]+ [PE[2]]
        lislis3 = lislis3 + [round(PElis[i][PE[i]],2) for i in range(4)]

      lislis3 = lislis3 + [round(np.random.normal(5, 0.8),2),""]  #腹水項目
    else:
      #腹水
      lislis3 = lislis3 + ["",round(PElis[1][0],2),round(PElis[2][0],2),""]

      #血清アルブミン
      lislis3.append(round(np.random.normal(5, 0.8),2))

      #腹水アルブミン
      if l[8] == "なし":
        lislis3.append("")
      elif l[8] == "漏出性":
        lislis3.append(round(lislis3[12]-num_maker2(lambda a: a>1.1, 1.5, 2),2))
      else:
        lislis3.append(round(lislis3[12]-num_maker2(lambda a: a<1.1, 1.0, 2),2))
      
    
    if l[3]==4:
      if l[9] == "なし":
        #PaO2, PaCo2
        lislis3 = lislis3 + [num_maker2(lambda a: a >60, 60, 5), num_maker2(lambda a: a <45, 40, 5)]
      elif l[9] == "I型":
        lislis3 = lislis3 + [num_maker2(lambda a: a <60, 60, 5), num_maker2(lambda a: a <45, 40, 5)]
      else:
        lislis3 = lislis3 + [num_maker2(lambda a: a <60, 60, 5), num_maker2(lambda a: a >45, 45, 5)]
    else:
      CO2 = num_maker2(lambda a: a <45, 40, 5)
      lislis3 = lislis3 + [round(150-CO2/0.8-l[9],2), CO2]
    lislis3.append(l[10])
    lislis3 = lislis3[0:8] +["","",""] +lislis3[8:]
    #print(kk)
  lislis3.append(sum(lislis2[3]))
  lislis3.append(np.random.normal(sum(lislis2[3]), num_maker2(lambda a: a>0, 0.25, 0.7)))

  if lislis3[-1] <6:
    lislis3.append("陰性")
    nega = nega +1
  elif lislis3[-1] < 8:
    lislis3.append("軽症")
    light = light +1
  elif lislis3[-1] < 11:
    lislis3.append("中等症")
    med = med+1
  elif lislis3[-1] < 12:
    lislis3.append("重症")
    heavy = heavy +1
  else:
    lislis3.append("超重症")
    hhh = hhh +1
  #print("aa"+str(kk))
    #Age, Sex, Tall, 血清Cr, Weight, U_Cr, S_Na, U_Na,てんかん、呼吸数、血圧, Score, real_Score, リスク
    #Age, Sex, Tall, SCr, Weight, UCr,SNa,UNa,胸水LDH、血清LDH、血清蛋白、胸水蛋白、血清Alb,腹水Alb、PaO2,PaCo2,JCS,Score, Real_score, リスク
  #print(lislis3)
  lislis3 = lislis3 +\
  [round(np.random.normal(num_maker2(lambda a: a>1, 10 * lislis3[-2] + 20, 5),num_maker2(lambda a: a>0.2, 0.3, 1)),2),\
   round(np.random.normal(num_maker2(lambda a: a>1, 11 * lislis3[-2] + 0.2, 2), num_maker2(lambda a: a>0.4, 0.5, num_maker2(lambda a: a>0, 0.25, 1))),2),\
   round(np.random.normal(num_maker2(lambda a: a>10, 22 * lislis3[-2] + 145, 20), num_maker2(lambda a: a>0, num_maker2(lambda a: a>0, 10, 10), 6)),2),\
   round(np.random.normal(0.5 * lislis3[-2] + 20, num_maker2(lambda a: a>0, 0.2, 0.3)),3),\
   num_maker2(lambda a: a>0, 22 * lislis3[-2] + 13, num_maker2(lambda a: a>0, 22, 12))]
  #print("bb"+str(kk))
  
  
  if not TF:
    arra = np.array([lislis3])
    TF = True
  else:
    arra = np.append(arra, [lislis3], axis=0)
print(nega,light,med,heavy,hhh)

df = pd.DataFrame(arra,
                  columns=['年齢', '性別', '身長', '血清Cr', '体重', '尿中Cr', '血清Na', '尿中Na','てんかん','呼吸数','血圧',
                           '胸水LDH','血清LDH','血清蛋白','胸水蛋白','血清Alb', '腹水Alb','PaO2','PaCo2','JCS', 'Score', 'real_Score',
                           'リスク', 'Doukaku Ag', '陽光過敏症', 'Snapdragon Antibody', 'Witch scent負荷試験','Possession sign'])
#print(df)
#print (df.columns)
#df2 = df[['年齢', '性別', '身長', '血清Cr', '体重', '尿中Cr', '血清Na', '尿中Na','てんかん','呼吸数','血圧','胸水LDH','血清LDH','血清蛋白','胸水蛋白']]
df2 = df[['年齢', '性別', '身長', '血清Cr', '体重', '尿中Cr', '血清Na', '尿中Na','てんかん','呼吸数','血圧','胸水LDH','血清LDH','血清蛋白','胸水蛋白','血清Alb','腹水Alb','PaO2','PaCo2','JCS', 'Doukaku Ag', '陽光過敏症', 'Snapdragon Antibody', 'Witch scent負荷試験','Possession sign']]


df3 = df2.reindex(columns=['年齢', '性別', '身長', '体重','呼吸数','血圧', '血清Cr','血清Na','血清LDH','血清蛋白','血清Alb','PaO2','PaCo2','JCS',  '尿中Cr', '尿中Na','胸水LDH','胸水蛋白','腹水Alb','てんかん',  'Doukaku Ag', '陽光過敏症', 'Snapdragon Antibody', 'Witch scent負荷試験','Possession sign'])

df3.to_csv('D-aureus新検査薬治験.csv',encoding = "shift-jis")
"""if not skip:
  !pip install japanize-matplotlib
import seaborn
import matplotlib.pyplot as plt
import japanize_matplotlib

%matplotlib inline
for jj in ['Doukaku Ag', '陽光過敏症', 'Snapdragon Antibody', 'Witch scent負荷試験','Possession sign']:
  #print(df[jj].astype(np.float32))
  seaborn.violinplot(  x=df['リスク'], y=df[jj].astype(np.float32), inner="quartile", color="0.85"  )
  seaborn.swarmplot( x=df['リスク'], y=df[jj].astype(np.float32))
  plt.show()"""


import statistics
infection = [0] * 31
for date in range(31):
  infection[date] = random.gammavariate(3.5, 1.3)

infsum = sum(infection)
infp = [i/infsum for i in infection]
infdate = rd.choice(31, 1000, p=infp)
TF = False
for date in infdate:
  lislis4 = ["1月" + str(date+1)+"日", int(num_maker2(lambda a: a>0, rd.choice(2, 1)[0]*30+30, 20, roundn=0)), ["男","女"][rd.choice(2, 1)[0]], ["D.aureus", "D.aeruginosa", "D. douma", "D.goblin", "D.jougo", "D.malum"][rd.choice(6, 1)[0]]]
  if not TF:
    arra = np.array([lislis4])
    TF = True
  else:
    arra = np.append(arra, [lislis4], axis=0)


df4 = pd.DataFrame(arra, columns=['日付', '年齢', '性別','subtype'])
df4.to_csv('１ヶ月の感染状況.csv',encoding = "shift-jis")
number = [1000,200,10,20,20,9]

TF = False
for year in range(1950, 2023):
  cut = [max(number)*1.5, sum(number)/len(number),max(number)/100, min(number)/2, statistics.median(number),min(number)/10]
  number = [int(num_maker2(lambda a: a>cut[i] and a<200000, number[i] ,abs(cut[i]-number[i]+1), roundn=0)) for i in range(6)]
  lislis5 = [int(year)] + number
  if not TF:
    arra = np.array([lislis5])
    TF = True
  else:
    arra = np.append(arra, [lislis5], axis=0)

df5 = pd.DataFrame(arra, columns=['年', "D.aureus", "D.aeruginosa", "D. douma", "D.goblin", "D.jougo", "D.malum"])
df5.to_csv('subtypeの感染状況.csv',encoding = "shift-jis")
