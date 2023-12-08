#====Railway Ticket Booking System=====#

#impImorting modules
import os
try:
    from kivy.uix.screenmanager import ScreenManager
    from kivymd.app import MDApp
    from kivy.lang import Builder
    from kivy.core.window import Window
    from kivymd.uix.dialog import MDDialog
    import pandas as pd
    from kivymd.uix.button import MDFlatButton
    from kivymd.uix.pickers import MDDatePicker
    from kivy.properties import StringProperty
    from stationdet import stationdata,spl,exp,garibrath,no_seats
    from kivymd.uix.list import ThreeLineListItem
    import re
    import datetime
    from geopy.geocoders import Nominatim
    from geopy.distance import geodesic
    import random
except ImportError:
    os.system('pip install kivymd')
    os.system('pip install kivy')
    os.system('pip install lxml')
    os.system('pip install pandas')
    os.system('pip install geopy')
    from kivy.uix.screenmanager import ScreenManager
    from kivymd.app import MDApp
    from kivy.lang import Builder
    from kivy.core.window import Window
    from kivymd.uix.dialog import MDDialog
    import pandas as pd
    from kivymd.uix.button import MDFlatButton
    from kivymd.uix.pickers import MDDatePicker
    from kivy.properties import StringProperty
    from stationdet import stationdata, spl, exp, garibrath, no_seats
    from kivymd.uix.list import ThreeLineListItem
    import re
    import datetime
    from geopy.geocoders import Nominatim
    from geopy.distance import geodesic
    import random
geolocator = Nominatim(user_agent="MyApp")

#===========================

#Window config
def big_screen():
    Window.size = (1080,720)
    Window.top = 60
    Window.left = 200
def small_screen():
    Window.size = (620,720)
    Window.top = 60
    Window.left = 200
#===========================
#datetime

import time
currentDate = time.strftime("%Y-%m-%d")
#===========================
#main app building
class UI(ScreenManager):
    def set_list_md_icons(self, text="", search=False):
        #Builds a list of icons for the screen MDIcons.

        def add_icon_item(name_icon , asv):
            self.ids.rv.data.append(
                {
                    "viewclass": "TwoLineListItem",
                    "text": name_icon,
                    'secondary_text': asv,
                    'font_size': '18sp'

                }
            )

        self.ids.rv.data = []
        if self.ids.search_field.text == '':
            self.ids.rv.data = []
        else:
            for name_icon in stationdata.keys():
                if search:
                    if text in name_icon:
                        add_icon_item(name_icon.upper(),stationdata[name_icon])
                else:
                    add_icon_item(name_icon.upper(),stationdata[name_icon])

class Rail(MDApp):
    #loads kivy string

    def build(self):
        Builder.load_file('lime.kv')
        return UI()
    def on_start(self):
        self.root.ids.currdate.text = currentDate
        small_screen()

    def create_acc(self): #========================create new user
        cs = pd.read_csv('userinfo.csv')
        if self.root.ids.new_username.text in list(cs['username']):
            self.wrong_dbox(obj='' , txt='Username Already Exists')
        elif self.root.ids.new_name.text=='' or self.root.ids.new_email.text=='' or self.root.ids.new_mobno.text =='' or self.root.ids.new_username.text=='' or self.root.ids.new_pass.text == '' or self.root.ids.re_new_pass.text == '':
            self.wrong_dbox(obj='' , txt = 'Fields Can not be Empty')
        else:
            if self.root.ids.new_pass.text == self.root.ids.re_new_pass.text:
                ndf = pd.DataFrame({'username':[self.root.ids.new_username.text] ,
                                    'password': [self.root.ids.new_pass.text],
                      'name':[self.root.ids.new_name.text],'mobno':[self.root.ids.new_mobno.text],
                      'email':[self.root.ids.new_email.text]})
                cs = pd.concat([cs,ndf] , ignore_index=True)
                cs.to_csv('userinfo.csv' , index=False)
                self.wrong_dbox(obj = '',txt = "User successfully Registered")
                self.root.current = 'loginpage'
            else:
                self.wrong_dbox(obj = '' , txt = 'Recheck Password')
    #functions
    def login_pro(self):    #=========================================login button
        uname = self.root.ids.username.text
        passwd = self.root.ids.password.text
        cs = pd.read_csv('userinfo.csv')
        if uname in list(cs['username']):
            c = 0
            for i in range(0,cs.shape[0]):
                if list(cs['username'])[i] == uname:
                    break
                else:
                    c=c+1

            if passwd == str(cs['password'][c]):
                self.wrong_dbox(obj = '',txt = "login Successful")
                self.root.ids.innername.text = f'Welcome {cs["name"][c]}'
                big_screen()
                self.root.current = 'homepg'
                self.cc = False
            else:
                self.wrong_dbox(obj = '' , txt = 'Wrong Password')
        else:
            self.wrong_dbox(obj='' , txt = 'User Does not Exists')

    def viewpass(self):     #=========================================eye button
        if self.root.ids.password.password:
            self.root.ids.password.password = False
            self.root.ids.passbutt.icon = "eye-off"
        elif not self.root.ids.password.password:
            self.root.ids.password.password = True
            self.root.ids.passbutt.icon = "eye"

    def viewpass1(self):    #=========================================eye button
        if self.root.ids.re_new_pass.password:
            self.root.ids.re_new_pass.password = False
            self.root.ids.passbutt1.icon = "eye-off"
        elif not self.root.ids.re_new_pass.password:
            self.root.ids.re_new_pass.password = True
            self.root.ids.passbutt1.icon = "eye"

    def new_usr(self):      #=========================================new user
        small_screen()
        self.root.ids.re_new_pass.text = ''
        self.root.ids.new_pass.text = ''
        self.root.ids.new_username.text = ''
        self.root.ids.new_name.text = ''
        self.root.ids.new_mobno.text = ''
        self.root.ids.new_email.text = ''
        self.root.current = 'new_usr'

    def alrdyacc(self):     #=========================================already account
        small_screen()
        self.root.ids.username.text = ''
        self.root.ids.password.text = ''
        self.root.current = 'loginpage'



    def contact_us(self , obj):
        button_close = MDFlatButton(text='Close', on_release=self.close_dilog)
        self.dbox = MDDialog(title="Information", text="""Customer Care Numbers : 14646 OR 0755-6610661 / 0755-4090600
I-tickets/e-tickets : care@irctc.co.in
For Cancellation E-tickets : etickets@irctc.co.in
Address :
Indian Railway Catering and Tourism Corporation Ltd.,
B-148, 11th Floor, Statesman House,
Barakhamba Road, New Delhi 110001.""", buttons=[button_close])
        self.dbox.open()

    def close_dilog(self, obj): #=================================Close dialog box
        self.dbox.dismiss()

    def tr_bw_st(self):         #==================================Train Search Main
        self.root.current = 'trainsearch'

    # ==================================calender butt
    def on_save(self , instance , value , date_range):
        self.root.ids.caldate.text = str(value)

    def clndr(self):
        dt_dilg = MDDatePicker()
        dt_dilg.bind(on_save=self.on_save)
        dt_dilg.open()

    def on_save1(self , instance , value , date_range):
        self.root.ids.book_caldate.text = str(value)

    def clndr1(self):
        dt_dilg = MDDatePicker()
        dt_dilg.bind(on_save=self.on_save1)
        dt_dilg.open()

    def book_ticket(self):
        self.root.ids.book_from.text = ''
        self.root.ids.book_to.text = ''
        self.root.ids.book_caldate.text = ''
        self.root.current = 'book_train'

    def search(self , search=False):       #=============================================search trains
        self.from_serch = self.root.ids.from_serch.text.upper()
        self.from_to = self.root.ids.from_to.text.upper()
        self.caldate = self.root.ids.caldate.text
        print(self.from_serch,self.from_to,self.caldate,sep='\n')
        cont = 'Yes'
        if self.from_serch=='' or self.from_to=='':
            cont = 'No'
        elif self.caldate=="":
            tr_data = f'https://etrain.info/trains/{self.from_serch}-to-{self.from_to}'
            tr_data=pd.read_html(tr_data)[1]
        else:
            date69 = self.caldate.replace('-' , '')
            tr_data = f'https://etrain.info/trains/{self.from_serch}-to-{self.from_to}?date={date69}'
            tr_data=pd.read_html(tr_data)[1]


        def add_train_data(trdet , classes='' , days=''):
            self.root.ids.trdata.data.append(
                {
                    "viewclass": "ThreeLineListItem",
                    "text": trdet,
                    'secondary_text': classes,
                    'tertiary_text':days,
                    'font_size': '18sp',
                }
            )
        def comptrdat():
            self.root.ids.trdata.data = []
            for i in range(tr_data.shape[0]):
                xxxx = ''
                for j in range(len(tr_data[14][i])):
                    if j == 0:
                        pass
                    elif j % 2 == 0:
                        xxxx = xxxx + '-'
                    xxxx = xxxx + tr_data[14][i][j]
                day = 'Running Days - '
                if tr_data[7][i] == 'Y':
                    day = day + 'Su'
                if tr_data[8][i] == 'Y':
                    day = day + 'M'
                if tr_data[9][i] == 'Y':
                    day = day + 'T'
                if tr_data[10][i] == 'Y':
                    day = day + 'W'
                if tr_data[11][i] == 'Y':
                    day = day + 'Th'
                if tr_data[12][i] == 'Y':
                    day = day + 'F'
                if tr_data[13][i] == 'Y':
                    day = day + 'S'
                if day == 'Running Days - SuMTWThFS':
                    day = 'Running Days - Everyday'

                if search:
                    add_train_data(
                        f'{tr_data[0][i]}-{tr_data[1][i]} ({tr_data[2][i]}-{tr_data[4][i]})({tr_data[3][i]}-{tr_data[5][i]})',
                        f'Seats Available {xxxx}', day)
                else:
                    add_train_data(
                        f'{tr_data[0][i]}-{tr_data[1][i]} ({tr_data[2][i]}-{tr_data[4][i]})({tr_data[3][i]}-{tr_data[5][i]})',
                        f'Seats Available {xxxx}', day)
        if cont == 'No':
            self.root.ids.trdata.data = []
            add_train_data('No Results Found')
        else:
            comptrdat()


    def wrong_dbox(self, obj , txt ): #======================================================dbox
        button_close = MDFlatButton(text='Close', on_release=self.close_dilog)
        self.dbox = MDDialog(title="Information", text=txt, buttons=[button_close])
        self.dbox.open()

    def dilbox(self, obj , txt ,title): #======================================================dbox
        button_close = MDFlatButton(text='Close', on_release=self.close_dilog)
        self.dbox = MDDialog(title=title, text=txt, buttons=[button_close])
        self.dbox.open()
    def preview(self): #============================================================ticket privew
        try:
            x = pd.read_html(f'https://etrain.info/train/{self.root.ids.trno.text}/schedule')
            self.tr = x[0][1][0]
        except:
            self.root.ids.seatclass.text = 'No train found'
            x=''
        try:
            st = list()
            for i in x[5]['S.No.CODE']:
                st.append(re.sub(r'[0-9]', '', i))
            print(st)
            if self.root.ids.book_from.text.upper() not in st or self.root.ids.book_to.text.upper() not in st or self.root.ids.clas.text.upper() not in x[0][1][2].upper():
                self.wrong_dbox(obj='', txt="Wrong Source/Destinaiton Code or Class")
                self.check1 = None
            else:
                self.check1 = True
            day = datetime.datetime.strptime(self.root.ids.book_caldate.text, '%Y-%m-%d')
            self.day = day.strftime('%a').upper()
            y = x[0][1][1].upper()
            if 'DAILY' in y or self.day in y:
                self.check2 = True
            else:
                self.wrong_dbox(obj='', txt='Train Does not Run on Selected Date')
                self.check2 = None
            try:
                noofpeop= int(self.root.ids.no_seats.text)
                self.check3 = True
            except:
                self.wrong_dbox(obj='' , txt = 'No of people should be integer')
                self.check3 = False
                noofpeop=None
            print(self.check3,self.check2,self.check1)
            if self.check1 == True and self.check2 == True and self.check3==True:
                if 'GARIBRATH' in x[0][1][0].upper() or 'GARIB RATH' in x[0][1][0].upper():
                    cost = garibrath
                elif 'RAJDHANI' in x[0][1][0].upper() or 'DURONTO' in x[0][1][0].upper() or 'SHATABDI' in x[0][1][
                    0].upper():
                    cost = spl
                else:
                    cost = exp
                print(cost[self.root.ids.clas.text])
                st1 = [i for i in stationdata if stationdata[i] == self.root.ids.book_from.text.upper()]
                st2 = [j for j in stationdata if stationdata[j] == self.root.ids.book_to.text.upper()]
                print(st1,st2)
                l1 = geolocator.geocode(st1[0])
                l2 = geolocator.geocode(st2[0])
                dist = geodesic((l1.latitude, l1.longitude), (l2.latitude, l2.longitude))
                print(dist)
                print(cost[self.root.ids.clas.text])
                print(noofpeop)
                tot_cost = dist*cost[self.root.ids.clas.text]*noofpeop
                tot_cost=str(tot_cost)
                tot_cost = list(tot_cost)
                for i in range(3):
                    tot_cost.pop(-1)
                totcost = ''
                for i in tot_cost:
                    totcost+=i
                tot_cost = float(totcost)
                tot_cost = round(tot_cost)
                self.root.ids.trname.text = self.tr
                self.trno = self.root.ids.trno.text
                self.cost = str(tot_cost)
                self.from_q = str(st1[0]).upper()
                self.to = str(st2[0]).upper()
                self.date = str(self.root.ids.book_caldate.text).upper()
                self.namepr = self.root.ids.book_name.text.upper()
                self.seats = self.root.ids.no_seats.text.upper()
                self.clas = self.root.ids.clas.text.upper()
                self.noofpeop = int(self.root.ids.no_seats.text)
                self.cost = 'INR - ' + self.cost
                self.root.ids.cost.text = self.cost
                self.check4=True

        except:
            self.wrong_dbox(obj='' , txt='Something Went Wrong')
            self.check4=False


    def book_tr(self):
        if self.check4:
            try:
                pnr_dat = pd.read_csv('pnr.csv')
                loop = True
                while loop:
                    pnr = random.randint(1000000000, 9999999999)
                    if str(pnr) in list(pnr_dat['pnr']):
                        loop = True
                    else:
                        nw_pnr = pnr
                        loop = False
                        cho = {'1A': ['H1', 'HA1'],
                               '2A': ['A1', 'A2', 'A3', 'A4', 'A5'],
                               '3A': ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9'],
                               'SL': ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10'],
                               'EC': ['E1', 'E2'], 'CC': ['C1', 'C2', 'C3', 'C4', 'C5', 'C6'],
                               '2S': ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8']
                               }
                        seats = random.choice(cho[self.clas])
                        r_set = random.randint(1, no_seats[self.clas] - int(self.noofpeop))
                        r_seat = ''
                        for j in range(0,int(self.noofpeop)):
                            r_set = r_set + j
                            r_seat = r_seat + f' {r_set}'

                        dataf = pd.DataFrame(
                            {'pnr': [nw_pnr, ], 'train': [self.tr, ],
                             'name': [self.namepr, ], 'person': [self.noofpeop, ],
                             'class': [self.clas, ], 'seats': [r_seat, ], 'coach': [seats, ],
                             'date': [self.date, ], 'from': [self.from_q, ],
                             'to': [self.to, ], 'cost': [self.cost, ]})
                        pnr = pd.concat([pnr_dat, dataf], ignore_index=True)
                        pnr.to_csv('pnr.csv', index=False)
                        self.dilbox(obj='', title='Booked',
                                    txt=f'PNR : {nw_pnr}\nTRAIN : {self.tr.upper()}\nNAME : {self.namepr}\nFROM : {self.from_q}\nTO : {self.to}\nDOJ : {self.date}\nCOACH : {seats} {r_seat}\nCOST : {self.cost}')
            except:
               self.dilbox(obj='', txt='Unable To Book Train', title='Please Try Again')
        else:
            self.dilbox(obj='', txt='Unable To Book Train\nFirstly View Preview', title='Please Try Again')

    def pnr_page(self):
        small_screen()
        self.root.current='pnr'
    def bck_home(self):
        big_screen()
        self.root.current='homepg'

    def see_pnr(self):
        pnr=pd.read_csv('pnr.csv' , dtype='object')
        try:
            if self.root.ids.pnr.text not in list(pnr['pnr']):
                self.dilbox(obj = '' , title='PNR Does Not Exsist' , txt = 'Enter Registered PNR')
            else:
                ind = 0
                for i in list(pnr['pnr']):
                    if i == self.root.ids.pnr.text:
                        break
                    else:
                        ind+=1
                self.root.ids.pnr_trname.text = pnr['train'][ind]
                self.root.ids.pnr_from.text = pnr['from'][ind]
                self.root.ids.pnr_to.text = pnr['to'][ind]
                self.root.ids.pnr_doj.text = pnr['date'][ind]
                self.root.ids.pnr_name.text = pnr['name'][ind]
                self.root.ids.pnr_coach.text = pnr['coach'][ind]
                self.root.ids.pnr_seats.text = pnr['seats'][ind]
                self.cc = True
        except:
            self.wrong_dbox(obj='' , txt='Something Went Wrong')
            self.cc=False
    def canc_dbox(self):
        pnr = pd.read_csv('pnr.csv', dtype='object')
        if self.cc and self.root.ids.pnr.text in list(pnr['pnr']):
            button_close = MDFlatButton(text='No', on_release=self.close_dilog)
            button_conf = MDFlatButton(text='Yes', on_release=self.cancel)
            self.dbox = MDDialog(title='Confirmation', text='Are you sure you want to cancel PNR?', buttons=[button_close , button_conf])
            self.dbox.open()
        else:
            self.dilbox(title='' , obj='' , txt = 'Please Enter Correct PNR')

    def cancel(self,obj):
        self.close_dilog(obj='')
        try:
            if self.cc:
                pnr = pd.read_csv('pnr.csv', dtype='object')
                ind = 0
                for i in list(pnr['pnr']):
                    if i == self.root.ids.pnr.text:
                        break
                    else:
                        ind += 1
                pnr.drop(ind,axis=0,inplace=True)
                pnr.to_csv('pnr.csv' , index=False)
                self.dilbox(obj='', title='Cancellation Successful ', txt='PNR Cancelled Successfully')
                self.root.ids.pnr_trname.text = ''
                self.root.ids.pnr_from.text = ''
                self.root.ids.pnr_to.text = ''
                self.root.ids.pnr_doj.text = ''
                self.root.ids.pnr_name.text = ''
                self.root.ids.pnr_coach.text = ''
                self.root.ids.pnr_seats.text = ''
                self.cc = False

            else:
                self.wrong_dbox(obj='', txt='First View PNR Details')
        except:
            self.wrong_dbox(obj='', txt='Something Went Wrong')


if __name__ == '__main__':
    Rail().run()