'''
    创建初衷：
        方便处理数据
        更加快捷的对数据库进行插入操作
        前提：已经清洗好了数据
'''

import pymysql
import time
import tkinter, tkinter.messagebox, tkinter.filedialog, tkinter.simpledialog


# 数据库登录，创建一个窗体
def frame():
    global tk
    tk = tkinter.Tk()
    tk.title("数据库页面")
    tk.geometry('250x300+650+250')  # 窗体大小  宽，高，+x,+y坐标
    tk.resizable(False, False)  # 窗体不可变
    # 左上角图标 (只接收ico后缀)
    tk.iconbitmap(default="1.ico")

    hostTitle = tkinter.Label(tk, text="地址：")
    hostTitle.place(x=30, y=25)

    global hostText
    hostText = tkinter.Entry(tk)
    hostText.place(x=80, y=25)

    portTitle = tkinter.Label(tk, text="端口号：")
    portTitle.place(x=30, y=55)

    global portText
    portText = tkinter.Entry(tk)
    portText.place(x=80, y=55)

    userTitle = tkinter.Label(tk, text="用户名：")
    userTitle.place(x=30, y=80)

    global userText
    userText = tkinter.Entry(tk)
    userText.place(x=80, y=80)

    passwdTitle = tkinter.Label(tk, text="密码：")
    passwdTitle.place(x=30, y=105)

    global passwdText
    passwdText = tkinter.Entry(tk, show="*")
    passwdText.place(x=80, y=105)

    dbTitle = tkinter.Label(tk, text="数据库：")
    dbTitle.place(x=30, y=135)

    global dbText
    dbText = tkinter.Entry(tk)
    dbText.place(x=80, y=135)

    tableTitle = tkinter.Label(tk, text="表名：")
    tableTitle.place(x=30, y=165)

    global tableText
    tableText = tkinter.Entry(tk)
    tableText.place(x=80, y=165)

    submitButton = tkinter.Button(tk, fg="red", text="连接", command=checkConnect)
    submitButton.place(x=30, y=195)

    tk.mainloop()


# 数据库连接
def mysqlConect(host, port, user, password, db):
    global conn
    conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db)
    # 游标对象
    global cursor
    cursor = conn.cursor()


# 询问窗体
def askFrame():
    global askTk
    askTk = tkinter.Tk()
    askTk.title("数据库详情页面")
    askTk.geometry('250x300+650+250')  # 窗体大小  宽，高，+x,+y坐标
    askTk.resizable(False, False)  # 窗体不可变
    # 左上角图标 (只接收ico后缀)
    askTk.iconbitmap(default="1.ico")

    totalTitle = tkinter.Label(askTk, text="插入数据条数(整数)：")
    totalTitle.place(x=30, y=25)

    # 获取插入条数
    global totalText
    totalText = tkinter.Entry(askTk)
    totalText.place(x=30, y=55)

    columnT = tkinter.Label(askTk, text="插入数据列数(column)：")
    columnT.place(x=30, y=85)

    # 获取插入列数
    global columnTotal
    columnTotal = tkinter.Entry(askTk)
    columnTotal.place(x=30, y=105)

    columnTitle = tkinter.Label(askTk, text="插入数据的字段名(用','隔开)：")
    columnTitle.place(x=30, y=135)

    # 获取插入字段名
    global columnText
    columnText = tkinter.Entry(askTk)
    columnText.place(x=30, y=160)

    submitButton = tkinter.Button(askTk, fg="red", text="提交", command=checkData)
    submitButton.place(x=30, y=185)

    askTk.mainloop()


def checkData():
    try:
        # 插入总条数
        global total
        total = int(totalText.get())
        # 插入总列数
        global columnT
        columnT = int(columnTotal.get())
        # 获取插入字段名
        global columns
        columns = columnText.get()
        # 列数
        global col
        col = len(columns.split(","))
        print("字段数：", col)
        if col != columnT:
            tkinter.messagebox.showinfo("提示", "输入的字段名和总列数不一致")
        else:
            # 字段名类型单独进行判断
            # isinstance判断数据类型
            if isinstance(total, int) and total > 0 and isinstance(columnT, int) and columnT > 0:
                print("*" * 30)
                print("插入总条数：", total)
                print("插入总列数：", columnT)
                print("字段名：", columns)
                askTk.destroy()
                print("询问界面消失")
                print("*" * 30)
                mainFrame()
            else:
                tkinter.messagebox.showinfo("提示内", "数据类型异常，请重新输入！！！")

    except:
        tkinter.messagebox.showinfo("提示外", "数据类型异常，请重新输入！！！")


# 主体
def mainFrame():
    global root
    root = tkinter.Tk()
    root.title("数据清洗页面")
    root.geometry('350x500+650+250')  # 窗体大小  宽，高，+x,+y坐标
    # root.resizable(False, False)  # 窗体不可变
    # 左上角图标 (只接收ico后缀)
    root.iconbitmap(default="1.ico")

    mainTitle = tkinter.Label(root, text="上传数据的完整路径：\n(C:\\Users\\admin\\Desktop\\goods.txt)：")
    mainTitle.place(x=30, y=25)

    submitButton = tkinter.Button(root, fg="red", text="提交", command=fileOperation)
    submitButton.place(x=260, y=35)

    # 保存所有文件路径
    global paths
    paths = []
    for i in range(col):
        paths.append("mainText" + str(i))

    for i in range(1, col + 1):
        paths[i - 1] = tkinter.Entry(root)
        paths[i - 1].place(x=80, y=70 * i)

    root.mainloop()


def insert(ls):
    # mysql操作
    l = columns.split(",")
    array = []
    for i in l:
        array.append(i.replace(i, "%s"))
    l = ",".join(array)
    sql = 'insert into ' + table + '(' + columns + ') VALUES(' + l + ')'
    print("数据库操作语句：", sql)
    args = []
    try:
        args = list(zip(*ls))
        print(list(zip(*ls)))
    except Exception as e:
        tkinter.messagebox.showwarning("警告", e)
    # 数据类型：[(1, '展示', 13), (1, '展示', 13), (1, '展示', 13), (1, '展示', 13)]
    # args必须是一个列表包含元组
    try:
        cursor.executemany(sql, args)
        print("*" * 30)
        print("数据库插入操作开始")
        conn.commit()
        conn.close()
        print('*' * 30)
        print("数据库插入操作结束")
        time.sleep(3)
        tkinter.messagebox.showinfo("提示", "写入成功!!!")
        root.destroy()
    except Exception as e:
        tkinter.messagebox.showwarning("警告", e)


def fileOperation():
    print("**********进入文件清洗**********")
    ls = []
    for i in range(columnT):
        ls.append("ls" + str(i + 1))
    print(ls)
    try:
        for i in range(len(paths)):
            print(paths[i].get())
            with open(file=paths[i].get(), mode="r", encoding='utf-8') as f:
                t1 = []
                for row in range(total):
                    # 读取全部
                    # f.read().split("\n")
                    t1.append(f.readline().replace("\n",""))
                ls[i] = t1
        # 数据库插入操作
        print(ls)
        insert(ls)
    except Exception as e:
        tkinter.messagebox.showwarning("警告", e)


def checkConnect():
    host = hostText.get()
    port = int(portText.get())
    user = userText.get()
    passwd = passwdText.get()
    db = dbText.get()
    global table
    table = tableText.get()
    print("*" * 30)
    print("主机地址为：", host)
    print("端口号为：", port)
    print("用户名为：", user)
    print("密码为：", passwd)
    print("数据库为：", db)
    print("数据库表名：", table)
    try:
        mysqlConect(host, port, user, passwd, db)
        tkinter.messagebox.showinfo("提示", "数据库连接成功")
        tk.destroy()
        print("数据库登录界面消失")
        print("*" * 30)
        askFrame()
    except:
        tkinter.messagebox.showinfo("提示", "输入错误")


def main():
    frame()


if __name__ == '__main__':
    main()

# num = 1
# title = ["日常Java练习题", "日常Python练习题", "Android日常练习题", "计算机基础"]
# image = "http://baidu.com/video/v"
# publis = ["2021-10-22", "2021-10-24", "2020-11-11", "2020-10-21"]
# user = ["春天来了", "夏天走了", "秋天散了", "冬天冷了"]
# click = 0
# print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
#
# ls1, ls3, ls4 = [], [], []
#
# for i in range(1, 9):
#     ls1.append(i)
#     ls3.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
#     ls4.append("轮播图")
# print(ls1, ls2, ls3, ls4)
