'''
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
geolocator = Nominatim(user_agent="MyApp")
l1 = geolocator.geocode('Patna junction')
l2 = geolocator.geocode('New Delhi')
print(l1)
print(l2)
print((l1.latitude, l1.longitude), (l2.latitude, l2.longitude),sep='\n')
dist = geodesic((l1.latitude, l1.longitude), (l2.latitude, l2.longitude))
dist = str(dist)
ldist = list(dist)
for i in range(3):
    ldist.pop(-1)
dsd = ""
for i in ldist:
    dsd += i
dsd = float(dsd)
dsd = round(dsd)
print(type(dsd))
'''
import pandas as pd
import time
#d = {'roll':[] , 'name':[] , 'class':[] , 'sec':[] , 'school':[] , 'attempted':[] , 'wrong':[] , 'unattepted':[]}
#df = pd.DataFrame(d)
#df.to_csv('testdata.csv')
#pd.DataFrame({'qno':[] , 'qn':[] , 'opa':[] , 'opb':[] , 'opc':[] , 'opd':[] , 'crop':[]}).to_csv('question.csv')
def test():
    roll_no = input('Enter Your Roll.No:')
    name = input('Enter Your Name:')
    clas = input('Enter Your Class:')
    section = input('Enter Your Section:')
    schl = input('Enter Your School:')
    print('Lets Start Quiz👍')
    time.sleep(1)
    for i in range(3,0,-1):
        print(i)
        time.sleep(1)
    response = list()
    df = pd.read_csv('question.csv')
    dt = pd.read_csv('testdata.csv')
    for i in range(df.shape[0]):
        print(f'Q{df["qno"][i]} {df["qn"][i]}.\na){df["opa"][i]}\nb){df["opb"][i]}\nc){df["opc"][i]}\nd){df["opd"][i]}')
        res = input('Enter Your Ans:')
        res = res.lower()
        if res not in list('abcd'):
            response.append('u')
        elif res == df['crop'][i]:
            response.append('c')
        else:
            response.append('w')
    cor=0
    wro=0
    unat=0
    for i in response:
        if 'c'==i:
            cor+=1
        elif 'w'==i:
            wro+=1
        elif 'u'==i:
            unat+=1
        else:
            pass
    print(f'Correct:{cor}\nWrong:{wro}\nUnattempted:{unat}')
    print(f'Your Score:{(cor*4)-(wro*1)}')
    da = {'roll':[roll_no,] , 'name':[name,] , 'class':[clas,] , 'sec':[section,] , 'school':[schl,] , 'attempted':[cor,] , 'wrong':[wro,] , 'unattepted':[unat,] , 'marks':[(cor*4)-(wro*1),]}
    da = pd.DataFrame(da)
    da = pd.concat([dt,da] , ignore_index=True)
print('Instructions:\nEvery correct ans marks +4\nEvery incorrect ans marks for -1 and,\n Every unattempted will be marked for 0')
ok = input('Are You Ready(Y for yes):')
if ok.upper()!='Y':
    quit()
else:
    test()
    print('ThankYou!')
