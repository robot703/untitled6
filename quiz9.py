import sqlite3
import turtle
import random
from tkinter.simpledialog import *

## 전역 변수 선언 부분 ##
swidth, sheight = 300, 300
lineID = 0
order_line = 0


def drawing():
    global X, Y, r, g, b

    global lineID, order_line

    order_line = 0
    turtle.pendown()

    try:
        con = sqlite3.connect(
            "C:/sqlite-tools-win32-x86-3320000/naverDB")  # DB가 저장된 폴더까지 지정
        cur = con.cursor()
    except:
        print("DB연결 오류")

    lineID += 1

    for i in range(0, 5, 1):
        order_line += 1

        X = random.randrange(-swidth / 2, swidth / 2)  # -150~ 150
        Y = random.randrange(-sheight / 2, sheight / 2)
        r = round(random.random(), 1)
        g = round(random.random(), 1)
        b = round(random.random(), 1)

        turtle.pencolor((r, g, b))
        turtle.goto(X, Y)

        try:
            sql = "INSERT INTO turtle VALUES('" + str[lineID] + "','" + str[r] + "','" + str[g] + "','" \
                  + str[b]+ "','" + str[order_line] + "','" + str[X] + "','" + str[Y] + "')"
            cur.execute(sql)
            con.commit()

        except:
            print("DB오류(SQL)")

    con.close()
    turtle.penup()
    turtle.goto(0, 0)



def drawing_reverse():
    global X, Y, r, g, b
    line = -1
    try:
        con = sqlite3.connect(
            "C:/sqlite-tools-win32-x86-3320000/naverDB")  # DB가 저장된 폴더까지 지정
        cur = con.cursor()
    except:
        print("DB연결 오류")

    try:
        cur.execute(
            " select * from turtleTable order by lineID desc, line_order desc")  # line ID 내림차순 후 lineorder 내립차순으로가져오기
    except:
        print("DB오류(SQL)")

    while (True):
        row = cur.fetchone()
        if row == None:
            turtle.pencolor(r, g, b)
            turtle.goto(0, 0)
            break;

        if int(row[0]) != line:
            turtle.goto(0, 0)
            line = int(row[0])

            r = row[1]
            g = row[2]
            b = row[3]
            X = row[5]
            Y = row[6]
            turtle.pencolor((r, g, b))
            turtle.penup()
            turtle.goto(X, Y)

        else:
            X = row[5]
            Y = row[6]
            turtle.pendown()
            turtle.goto(X, Y)  #좌표 현재값 색상 전값 그리고 색상 저장
            r = row[1]
            g = row[2]
            b = row[3]
            turtle.pencolor((r, g, b))

    con.close()


def resetDisplay():
    turtle.reset()
    turtle.width(3)

def deleteData():
    try:
        con = sqlite3.connect(
            "C:/sqlite-tools-win32-x86-3320000/naverDB")  # DB가 저장된 폴더까지 지정
        cur = con.cursor()
    except:
        print("DB연결 오류")

    try:
        sql = "delete from turtleTable"
        cur.execute(sql)
        con.commit()

    except:
        print("DB오류(SQL)")
    con.close()


## 메인 코드 부분 ##
if __name__ == "__main__":
    turtle.title('거북거북')
    turtle.shape('turtle')
    turtle.setup(width=swidth + 50, height=sheight + 50)
    turtle.width(3)
    turtle.screensize(swidth, sheight)
    drawing()  # first
    drawing()  # second
    resetDisplay()
    drawing_reverse()
    deleteData() #한번 기능을 하고 데이터 베이스에 데이터가 쌓이는 것을 막기위해 모든 레코드를 삭제.

    turtle.done()
