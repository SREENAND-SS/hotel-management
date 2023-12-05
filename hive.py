import mysql.connector
import time
import sys
f=0
r_type = []
rent = []



#f-1
def staff():
    
    for i in range(5):
        usr=input('ENTER USERNAME :')# DEFAULT >>> ADMIN
        pswd=input('ENTER PASSWORD :')#DEFAULT >>> PASSWORD
        if usr=='ADMIN' and pswd=='PASSWORD':
            print('LOGIN SUCCESSFUL !\n')
            home_st() #>>f-3
            break
        elif i==3:
            print('last try')
        else:
            print('invalid credentials')


#f-2
def guest():
    for i in range(5):

        usr = input('ENTER USERNAME :')  # DEFAULT >>> GUEST
        pswd = input('ENTER PASSWORD :')  # DEFAULT >>> GUEST
        if usr=='GUEST' and pswd=='GUEST':
            print('LOGIN SUCCESSFUL !')
            home_cust() #>>f-4
            break
        elif i==3:
            print('last try')
        else:
            print('invalid credentials')


#f-3
def home_st():

    print('''\n\tOPTONS\n''','='*18,'''\n1.SHOW AVAILABLE ROOMS
2.SHOW OCCUPIED ROOMS
3.SHOW BOOKED ROOMS
4.SHOW RENTS
5.OCCUPY A ROOM
6.GENERATE INVOICE
7.FORWARD TO GUEST PORTAL
8.CHECK OUT
9.CUSTOMER DETAILS
10.EXIT''')
    c = int(input('enter a choice :'))
    global m
    global ik
    if c == 1:
        available()
        time.sleep(1)
        home_st()
    elif c == 2:
        u=0
        m.execute("select room_no,status from rooms where status='OCCUPIED';")
        v = m.fetchall()
        print("ROOM NO")
        for i in v:
            print(i[0])
            u+=1
        print("NO OF OCCUPIED ROOMS",u)
        time.sleep(1)
        home_st()
    elif c == 3:
        u = 0
        m.execute("select room_no,status from rooms where status='BOOKED';")
        v = m.fetchall()
        print("ROOM NO")
        for i in v:
            print(i[0])
            u += 1
            print("NO OF BOOKED ROOMS", u)
        home_st()
    elif c == 4:
        rents()
        time.sleep(1)
        home_st()
    elif c == 5:
        book()
        time.sleep(1)
        home_st()
    elif c == 6:
        bill()
        time.sleep(1)
        home_st()
    elif c == 7:
        print("FORWARDING TO GUEST PORTAL")
        time.sleep(1)
        home_cust()
    elif c == 8:
        check_out()
        time.sleep(1)
        home_st()
    elif c == 9:
        cust_details()
        home_st()
    elif c == 10:
        print("logging out...")
        quit()


#f-4
def home_cust():
    print('''\n\tOPTONS\n''','='*18,'''\n1.SHOW AVAILABLE ROOMS
2.SHOW RENTS
3.BOOK A ROOM
4.RESTURANT MENU CARD
5.GENERATE BILL
6.CANCEL BOOKING
7.UPDATE STATUS
8.EXIT''')
    c = int(input('enter a choice :'))
    if c == 1:
        available()
        time.sleep(1)

        home_cust()
    elif c == 2:
        rents()
        time.sleep(1)
        home_cust()
    elif c == 3:
        book() #>>f-5
        time.sleep(1)
        home_cust()
    elif c == 4:
        resturant() #>>f-12
        time.sleep(1)
        home_cust()
    elif c == 5:
        bill()#>>f-6
        time.sleep(1)
        home_cust()
    elif c == 6:
        cancel() #>>f-10
        time.sleep(1)
        home_cust()
    elif c == 7:
        update_status()
        time.sleep(2)
        home_cust()
    elif c == 8:
        print('LOGGING OUT ...')
        time.sleep(3)
        print('THANK YOU! VISIT AGAIN')
#f-5
def book():
    rent=0
    cust_name = input('enter customer name:')
    cust_add = input("customer's address :")
    cust_age = int(input("enter customer's age:"))
    id_proof = input("id proof submitted:")
    cust_contact = input("enter customer's contact:")
    total_no_of_persons = int(input('''enter no of  persons
occupying the room (max=4persons/room):'''))
    z=r_data(total_no_of_persons)
    r_typecust=z[0]
    ch_in_date = input('Enter check in date (FORMAT :YYYY/MM/DD):')
    ch_in_time = input('Enter check in time format(HH:MM:SS)')
    cust_id = ct_id()
    rno=room_no(r_typecust)
    n=[cust_id,cust_name,cust_add,cust_age,id_proof,
       cust_contact,total_no_of_persons,ch_in_date,ch_in_time,
       r_typecust,rno]
    if " " in n:
        print("required feild is blank !\nplease fill it")
    sql = '''insert into room_check_in(customer_id,customer_name,
address,age,id_proof_submitted,contact,
total_no_of_person,check_in_date,check_in_time,
room_type,room_no)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
    m.execute(sql, n)
    d.commit()
    print("BOOKING SUCCESSFUL!!")
    print("your customer id is :",cust_id)
    print("your room number is ",rno)
    m.execute("INSERT INTO RESTURANT (customer_id) values(%s)",(cust_id,))
    if f==2:
        home_cust()
    elif f==1:
        home_st()


#f-6
def bill():
    c = input('enter customer_id:')
    m.execute("SELECT * FROM room_check_in r,room_check_out o WHERE o.customer_id = %s and r.customer_id=o.customer_id", (c,))
    v = m.fetchone()
    hi=v[10]
    m.execute("select no_of_days_after_check_in * rent from rooms, room_check_out where customer_id = %s and room_no = %s;",(c,hi))
    g = m.fetchall()
    m.execute("SELECT BILL_PRICE FROM RESTURANT WHERE CUSTOMER_ID=%s",(c,))
    s=m.fetchall()
    print("\n\n --------------------------------")
    print("           Hotel MASOT")
    print(" --------------------------------")
    print("              Bill")
    print(" --------------------------------")
    print(" Name: ", v[1], "\t\n Phone No.: ", v[5], "\t\n Address: ", v[2], "\t")
    print("\n Check-In: ", v[7], "\t\n Check-Out: ", v[13], "\t")
    print("\n Room Type: ", v[9], "\t\n Room Charges: ", g[0][0], "\t")
    print(" Restaurant Charges:" ,s[0][0],"\t", )
    print(" --------------------------------")
    print("\n Total Amount: ", s[0][0]+g[0][0], "\t")
    print(" --------------------------------")
    print("          Thank You")
    print("          Visit Again :)")
    print(" --------------------------------\n")
# f-7
def r_typ(n):
    global rent
    global r_type

    # r_type = input('enter room type :')
    if  n == 1:
        r_type = ['single non-AC','single AC','single luxury suite']
        rent = [1500,1750,3000]
    elif n == 2:
        r_type=['double non-AC','double AC','double luxury suite']
        rent = [2250,2500,4750]
    elif n == 3:
        r_type = ['deluxe non-AC','deluxe AC','deluxe luxury suite']
        rent = [3000,3250,5000]
    r_list=[r_type, rent]
    return r_list
#f-8
def r_data(k):
    r_det=[]

    p=r_typ(k)
    for i in range (len(p)+1):
        print(i+1,'.',p[0][i])
    f=int(input('enter your choice:'))
    if f == 1 :
        r_det=[p[0][0],p[1][0]]
    elif f == 2:
        r_det = [p[0][1], p[1][1]]
    elif f == 3:
        r_det = [p[0][2], p[1][2]]

    return r_det
#loading
def b():
    print("Loading:")
    #animation = ["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"]
    animation = ["[■□□□□□□□□□]","[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]",
                 "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]",
                 "[■■■■■■■■■□]", "[■■■■■■■■■■]"]
    for i in range(len(animation)):
        time.sleep(0.2)
        sys.stdout.write("\r" + animation[i % len(animation)])
        sys.stdout.flush()
    print("\n")


# f-9

def ct_id():
    cust_id=[]
    c_us=[]
    cust = ''
    for i in range (0,500):
        cust = 'C'+str(i+100)
        cust_id.append(cust)

    m.execute("select customer_id from room_check_in;")
    v=m.fetchall()
    for j in v:
        for v1 in j:
            c_us.append(v1)
    for k in range(len(cust_id)):
        if cust_id[k] not in c_us:
            return cust_id[k]
 # f-10
def cancel():
    f=input('enter  customer id :')
    i=input("enter customer name :")
    m.execute("select customer_id,customer_name,room_no from room_check_in")
    v=m.fetchall()
    for j in v:
        if j[0] == f and j[1] == i:
            m.execute("update rooms set status='vacant' where room_no=%s",(j[2],))
            print("booking cancelled succesfully!!")
    d.commit()

# f-11
def room_no(r_typecust):
    global m
    m.execute("SELECT room_no FROM rooms WHERE room_type = %s and status='vacant'", (r_typecust,))
    v = m.fetchall()

    k=0
    for i in range(len(v)-1,-1,-1):
        k= v[i][0]
    if f==2:
        m.execute("update rooms set status='BOOKED' where room_no=%s",(k,))
    elif f==1:
        m.execute("UPDATE ROOMS SET STATUS='OCCUPIED' WHERE ROOM_NO =%s",(k,))
    d.commit()
    return k



# f-12
def resturant():
    rc=[]
    r = 0
    f=input('enter customer id:')
    m.execute("select customer_id from resturant")
    v=m.fetchall()
    if v==():
        m.execute("insert into resturant (customer_id) values(%s)",(f,))
    m.execute("select customer_id from room_check_in;")
    v=m.fetchall()
    for i in v:

        if f == i[0]:
            print("-------------------------------------------------------------------------")
            print("                           Hotel MASCOT")
            print("-------------------------------------------------------------------------")
            print("                            Menu Card")
            print("-------------------------------------------------------------------------")
            print("                            MAIN DISHES")
            print("       -----------------------------------------------------")
            print("STARTERS                                     BREADS")
            print("-------------------                          -------------------")
            print("1 HONEY CHILLI VEGETABLE....80.00            28 PAROTTA.................10.00")
            print("2 CHICKEN LOLLIPOP..........160.00           29 CHAPATHI................10.00")
            print("3 CHICKEN TIKKA BITES.......160.00           30 NOOLAPPAM................8.00")
            print("                                             31 APPAM....................8.00\nSOUPS")
            print("-------------------                          32 ARI PATHRI...............8.00")
            print("4 CREAM OF TOMATO...........60.00            33 OROTTI...................8.00")
            print("5 CREAM OF VEGETABLE........60.00            34 TANDOOR ROTI............16.00")
            print("6 SWEET CORN SOUP...........60.00            35 PLAIN NAN...............20.00")
            print("7 SWEET CORN CHICKEN........70.00            36 BUTTER NAN..............25.00")
            print("8 MEAT BALL SOUP............70.00            37 WHEAT PAROTTA...........14.00")
            print("9 MUTTON SOUP...............70.00            38 NOOL PAROTTA............12.00")
            print("\nSALADS                                      NON-VEG DISHES")
            print("-------------------                          -------------------")
            print("10 CUCUMBER SALAD...........40.00            39 CHICKEN DRY FRY.........155.00")
            print("11 GREEN SALAD..............50.00            40 CHICKEN KADAI...........170.00")
            print("12 HAWALIAN CHICKEN SALAD...65.00            41 CHILLI CHICKEN..........195.00")
            print("                                             42 BUTTER CHICKEN........ .200.00")
            print("VEGGIE                                       43 CHICKEN 65..............220.00")
            print("-------------------                          44 CHICKEN PEPPER DRY......250.00")
            print("13 GREEN PEAS MASALA........65.00            ")
            print("14 TOMATO FRY...............75.00            45 MUTTON CHOPS............160.00")
            print("15 DHAL FRY.................75.00            46 MUTTON DRY FRY..........170.00")
            print("16 VEGETABLE KHURMA.........85.00            47 MUTTON ROAST............175.00")
            print("17 ALOO MASALA..............90.00")
            print("18 VEGETABLE STEW...........90.00            48 BEEF DRY FRY............120.00")
            print("19 GOBI MANCHURIAN.........100.00            49 BEEF ROAST..............135.00")
            print("20 PANEER BUTTER MASALA....105.00            50 CHILLI BEEF.............150.00")
            print("21 PANEER CHILLI...........105.00            51 BEEF KANTHARI FRY.......165.00")
            print("22 PALAK PANEER............120.00            ")
            print("\nDOSA CHART                                  BIRYANI")
            print("-------------------                          -------------------")
            print("23 PLAIN DOSA...............45.00            52 CHICKEN DHUM BIRYANI....165.00")
            print("24 MASALA DOSA..............55.00            53 MUTTON DHUM BIRYANI.....180.00")
            print("25 GHEE ROAST...............60.00            54 FISH BIRYANI............175.00")
            print("26 PAPER ROAST..............70.00            55 EGG BIRYANI.............150.00")
            print("27 OOTHAPPPAM...............65.00            56 BEEF BIRYANI............200.00")
            print("\n                  MILKSHAKES,ICE CREAM AND FALOODA")
            print("           ------------------------------------------------")
            print("MILKSHAKES                                   ICE CREAMS & FALOODA")
            print("---------------------                        ---------------------------")
            print("57 ROSE MILK................70.00            65 VANILLA..................35.00")
            print("58 VANILLA SHAKE............75.00            66 STRAWBERRY...............35.00")
            print("59 CHOCOLATE SHAKE..........75.00            67 CHOCOLATE................40.00")
            print("60 MANGO SHAKE..............75.00            68 PISTA....................40.00")
            print("61 STRAWBERRY SHAKE.........75.00            69 BUTTERSCOTCH.............40.00")
            print("62 BUTTERSCOTCH SHAKE.......75.00            70 FRUIT SALAD..............90.00")
            print("63 PISTA SHAKE..............75.00            71 DRY FRUIT SALAD..........95.00")
            print("64 BADAM SHAKE..............75.00            72 FALOODA..................95.00")
            print("\n                             BEVERAGES")
            print("           ------------------------------------------------")
            print("HOT BEVERAGES                                FRESH JUICES")
            print("-----------------                            ------------------")
            print("73 BLACK TEA................8.00             80 FRESH LIME(SODA/WATER)..25.00")
            print("74 TEA.....................10.00             81 PINEAPPLE...............45.00")
            print("75 LIME TEA................10.00             82 GRAPES..................50.00")
            print("76 BLACK COFFEE............15.00             83 ORANGE..................50.00")
            print("77 COFFEE..................20.00             84 MUSAMBI.................55.00")
            print("78 MASALA TEA..............18.00             85 MANGO...................60.00")
            print("79 GREEN TEA...............19.00             86 WATERMELON..............60.00")
            print("SELECT THE FOOD YOU WANT ")
            time.sleep(1)
            c = input('press enter to continue')
            print("Press 0 -to end and show bill ")
            ch = 1
            while (ch != 0):
                ch = int(input(" -> "))

                # if-elif-conditions to assign item
                # prices listed in menu card
                if ch == 1:
                    rs = 80
                    r = r + rs
                elif ch == 2 or ch == 3 or ch == 45:
                    rs = 160
                    r = r + rs
                elif ch >= 4 and ch <= 6 or ch == 25 or ch == 86:
                    rs = 60
                    r = r + rs
                elif ch >= 7 and ch <= 9 or ch == 57:
                    rs = 70
                    r = r + rs
                elif ch == 10 or (ch >= 67 and ch <= 69):
                    rs = 40
                    r = r + rs
                elif ch == 11 or ch == 82 or ch == 83:
                    rs = 50
                    r = r + rs
                elif ch == 12 or ch == 13 or ch == 27:
                    rs = 65
                    r = r + rs
                elif ch == 14 or ch == 15 or (ch >= 58 and ch <= 64):
                    rs = 75
                    r = r + rs
                elif ch == 16:
                    rs = 85
                    r = r + rs
                elif ch == 17 or ch == 18 or ch == 70:
                    rs = 90
                    r = r + rs
                elif ch == 19:
                    rs = 100
                    r = r + rs
                elif ch == 20 or ch == 21:
                    rs = 105
                    r = r + rs
                elif ch == 22 or ch == 48:
                    rs = 120
                    r = r + rs
                elif ch == 23 or ch == 81:
                    rs = 45
                    r = r + rs
                elif ch == 24 or ch == 84:
                    rs = 55
                    r = r + rs
                elif ch == 28 or ch == 29 or ch == 74 or ch == 75:
                    rs = 10
                    r = r + rs
                elif ch == 73 or (ch >= 30 and ch <= 33):
                    rs = 8
                    r = r + rs
                elif ch == 34:
                    rs = 16
                    r = r + rs
                elif ch == 35 or ch == 77:
                    rs = 20
                    r = r + rs
                elif ch == 36 or ch == 80:
                    rs = 25
                    r = r + rs
                elif ch == 37:
                    rs = 14
                    r = r + rs
                elif ch == 38:
                    rs = 12
                    r = r + rs
                elif ch == 39:
                    rs = 155
                    r = r + rs
                elif ch == 40 or ch == 46:
                    rs = 170
                    r = r + rs
                elif ch == 41:
                    rs = 195
                    r = r + rs
                elif ch == 42 or ch == 56:
                    rs = 200
                    r = r + rs
                elif ch == 43:
                    rs = 220
                    r = r + rs
                elif ch == 44:
                    rs = 250
                    r = r + rs
                elif ch == 47 or ch == 54:
                    rs = 175
                    r = r + rs
                elif ch == 49:
                    rs = 135
                    r = r + rs
                elif ch == 50 or ch == 55:
                    rs = 150
                    r = r + rs
                elif ch == 51 or ch == 52:
                    rs = 165
                    r = r + rs
                elif ch == 65 or ch == 66:
                    rs = 35
                    r = r + rs
                elif ch == 71 or ch == 72:
                    rs = 95
                    r = r + rs
                elif ch == 76:
                    rs = 15
                    r = r + rs
                elif ch == 78:
                    rs = 18
                    r = r + rs
                elif ch == 79:
                    rs = 19
                    r = r + rs
                elif ch == 0:

                    print("Total Bill: ", r)

        m.execute("UPDATE RESTURANT SET BILL_PRICE=BILL_PRICE+%s WHERE CUSTOMER_ID=%s",(r,f))
        d.commit()
# f-13
def check_out():
    g = input('enter customer id :')
    s = input("number days of stay :")
    h = input("enter check out date (YYYY/MM/DD) :")
    z = input("enter check out time (HH:MM:SS) :")
    k=[g,s,h,z]
    sql="insert into room_check_out (customer_id,no_of_days_after_check_in,check_out_date,check_out_time) values(%s,%s,%s,%s)"
    m.execute(sql,k)
    m.execute("select room_no from room_check_in where customer_id=%s",(g,))
    v=m.fetchone()
    l=v[0]
    print(l)
    m.execute("update rooms set status ='vacant' where room_no=%s", (l,))
    d.commit()
#f-14
def rents():
    m.execute("select distinct(room_type),rent from rooms;")
    v = m.fetchall()
    print("room type \t\t\t rent")
    print("-" * 15, '\t\t', "-" * 15)
    for i in range(len(v)):
        if i <= 5:
            print(v[i][0], '\t\t\t', v[i][1])
        elif i > 5:
            print(v[i][0], '\t\t', v[i][1])
# f-15
def available():
    ik = 0
    m.execute("select room_no,room_type from rooms where status='vacant';")
    v = m.fetchall()
    print("room number \t\t room type")
    print("-" * 15, '\t', "-" * 15)
    for i in v:
        ik += 1
        print(i[0], '\t\t\t', i[1])
    print("no ; of available rooms", ik)

# f-16
def cust_details():
    di=0
    m.execute("select customer_id,customer_name,contact from room_check_in")
    v=m.fetchall()
    print("CUSTOMER ID \t CUSTOMER NAME \t CONTACT")
    print("--------------------------------------------")
    for i in v:
        di+=1
        print(i[0],'\t\t',i[1],'\t\t',i[2])

#f-17
def update_status():
    f = input('enter customer id:')
    m.execute("select customer_id from room_check_in;")
    v = m.fetchall()
    for i in v:
        if f == i[0]:
            m.execute("select room_no from room_check_in where customer_id=%s", (f,))
            r1 = m.fetchall()
            print(r1[0][0])
            x=int(input("enter room_no :"))
            print(x)
            if r1[0][0] == x:
                m.execute("update rooms set status='OCCUPIED' where room_no=%s",(x,))
                print("DONE!!!")
        d.commit()

sta=input(" start ")
if sta is not None:


    d = mysql.connector.connect(host='localhost', user='root', passwd='123456')
    m = d.cursor()
    m.execute('create database if not exists hotel;')
    m.execute('use hotel;')
    m.execute('''create table if not exists  rooms(room_no int,
              room_type varchar(30),status varchar(20) default 'vacant',rent int);''')
    m.execute('''create table if not exists room_check_in
(customer_id char(5) primary key ,customer_name varchar(30),address varchar(40),
age int,id_proof_submitted varchar(30),contact varchar(20),total_no_of_person int,
check_in_date date,check_in_time time,room_type varchar(25),room_no int);''')
    m.execute('''create table if not exists room_check_out(customer_id varchar(25),
              no_of_days_after_check_in int,check_out_date date,check_out_time time);''')
    m.execute("create table if not exists resturant (customer_id char(5),bill_price int)")
    sql = "insert into rooms (room_no,room_type,rent)values(%s,%s,%s)"
    g = input("do you want to add datas(ignore if exist)[y/n] :")
    if g == 'y':
        for k in range(201):
            global n
            room_no = 100 + k
            if room_no <= 120:
                n = [room_no, 'single NON-AC', 1500]
                m.execute(sql, n)
            elif room_no > 120 and room_no <= 140:
                n = [room_no, 'double NON-AC', 2250]
                m.execute(sql, n)
            elif room_no > 140 and room_no <= 160:
                n = [room_no, 'deluxe NON-AC', 3000]
                m.execute(sql, n)
            elif room_no > 160 and room_no <= 180:
                n = [room_no, 'single AC', 1750]
                m.execute(sql, n)
            elif room_no > 180 and room_no <= 200:
                n = [room_no, 'double AC', 2500]
                m.execute(sql, n)
            elif room_no > 200 and room_no <= 220:
                n = [room_no, 'deluxe AC', 3250]
                m.execute(sql, n)
            elif room_no > 220 and room_no <= 240:
                n = [room_no, 'single luxury suite', 3000]
                m.execute(sql, n)
            elif room_no > 240 and room_no <= 270:
                n = [room_no, 'double luxury suite', 4750]
                m.execute(sql, n)
            elif room_no > 270 and room_no <= 300:
                n = [room_no, 'deluxe luxury suite', 5000]
                m.execute(sql, n)
        d.commit()
    else:
        pass


    print("SETUP IS DONE \n ")
    i = input("press ENTER to continue")
    print("")

    print('-'*30)
    print('WELCOME TO MASCOT HOTEL')
    print('-'*30)
    print('*'*30)
    print('\tLOGIN')
    print('*'*30)
    soc=input('LOGIN AS STAFF OR GUEST :')
    if soc == 'staff' or soc == 'STAFF':
        f+=1
        print(' FORWARDING TO STAFF PORTAL ')
        b()
        staff() #>>f-1
    if soc=='guest' or soc == 'GUEST':
        f+=2
        print('FORWARDING TO GUEST PORTAL')
        b()
        guest() #>>f-2


