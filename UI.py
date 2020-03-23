from tkinter import *
from tkinter import scrolledtext
from tkinter.ttk import Combobox, Style
import tkinter.font as tkfont
from datetime import *
import time
import threading
import os, signal


class Ui(object):
    def __init__(self, master):
        self.parent = master

        # fontStyle
        self.fontStyle = tkfont.Font(family='JetBrains Mono', size=14)

        # 程序退出标识符
        self.exit = True

        # rootFrame
        self.rootFrame = Frame(self.parent, bg='#2B2B2B', bd=5, relief='groove')

        # receiveFrame
        self.receiveFrame = Frame(self.rootFrame, bg='#ffe4c4', bd=2, relief='groove')

        # sendFrame
        self.sendFrame = Frame(self.rootFrame, bg='#8fbc8f', bd=2, relief='groove')

        # datetime
        self.datetime_value = StringVar()
        self.datetime_Label = Label(self.rootFrame, textvariable=self.datetime_value, fg='#FFCD42', bg='#2B2B2B',
                                    font=self.fontStyle)

        # 消息 文本框
        self.Message_value = StringVar()
        self.Message_Label = Label(self.rootFrame, textvariable=self.Message_value, fg='#FFCD42', bg='#2B2B2B',
                                   font=self.fontStyle)

        # COM Label & 下拉框
        # Label
        self.COM_Label = Label(self.rootFrame, width=10, bd=1, relief='groove', text='COM:',
                               font=self.fontStyle, bg='#2B2B2B', fg='#3E86A0')
        # 下拉框
        self.COM_ComBox_value = StringVar()
        self.COM_ComBox_list = Combobox(self.rootFrame, width=22, textvariable=self.COM_ComBox_value,
                                        font=self.fontStyle, state='readonly')

        # 波特率 Label & 下拉框
        # Label
        self.buteRate_Label = Label(self.rootFrame, width=10, bd=1, relief='groove', text='波特率:',
                                    font=self.fontStyle, bg='#2B2B2B', fg='#3E86A0')
        # 下拉框
        self.buteRate_ComBox_value = StringVar()
        self.buteRate_ComBox_list = Combobox(self.rootFrame, width=22, textvariable=self.buteRate_ComBox_value,
                                             font=self.fontStyle, state='readonly')
        self.buteRate_ComBox_list['value'] = ("1200", "2400", "4800", "9600", "14400", "19200", "38400",
                                              "56000", "576000", "115200")

        # 数据位 Label & 下拉框
        # Label
        self.bitsize_Label = Label(self.rootFrame, width=10, bd=1, relief='groove', text='数据位:',
                                   font=self.fontStyle, bg='#2B2B2B', fg='#3E86A0')
        # 下拉框
        self.bitsize_ComBox_value = StringVar
        self.bitsize_ComBox_list = Combobox(self.rootFrame, width=22, textvariable=self.bitsize_ComBox_value,
                                             font=self.fontStyle, state='readonly')
        self.bitsize_ComBox_list['value'] = ["5", "6", "7", "8"]

        # 校验位 Label & 下拉框
        # Label
        self.bitCheck_Label = Label(self.rootFrame, width=10, bd=1, relief='groove', text='校验位:',
                                    font=self.fontStyle, bg='#2B2B2B', fg='#3E86A0')
        # 下拉框
        self.bitCheck_ComBox_value = StringVar()
        self.bitCheck_ComBox_list = Combobox(self.rootFrame, width=22, textvariable=self.bitCheck_ComBox_value,
                                               font=self.fontStyle, state='readonly')
        self.bitCheck_ComBox_list['value'] = ("Even", "Mark", "None", "Odd", "Space")

        # 停止位 Label & 下拉框
        # Label
        self.stop_Label = Label(self.rootFrame, width=10, bd=1, relief='groove', text='停止位:',
                                    font=self.fontStyle, bg='#2B2B2B', fg='#3E86A0')
        # 下拉框
        self.stop_ComBox_value = StringVar()
        self.stop_ComBox_list = Combobox(self.rootFrame, width=22, textvariable=self.stop_ComBox_value,
                                             font=self.fontStyle, state='readonly')
        self.stop_ComBox_list['value'] = ("One", "Two", "OnePointFive")

        # 打开串口 按钮
        self.openBtn = Button(self.rootFrame, font=self.fontStyle, text='打开串口', bd=1, width=33, relief='groove',
                              background='#F08080')

        # 关闭串口 按钮
        self.closeBtn = Button(self.rootFrame, font=self.fontStyle, text='关闭串口', bd=1, width=33, relief='groove',
                              background='#F08080')

        # 接收 Label
        self.receive_Label = Label(self.receiveFrame, width=33, bd=1, relief='groove', text='接收数据',
                               font=self.fontStyle, bg='#ffe4c4', fg='#3E86A0')

        # 接收 字符表示
        self.receive_view = IntVar()
        self.receiveStr_RadioBtn = Radiobutton(self.receiveFrame, width=8, text='字符显示', variable=self.receive_view,
                                value=1, font=self.fontStyle, bg='#ffe4c4', fg='#3E86A0', activebackground='#ffe4c4')

        # 接收 Hex表示
        self.receiveHex_RadioBtn = Radiobutton(self.receiveFrame, width=9, text='Hex显示', variable=self.receive_view,
                                value=2, font=self.fontStyle, bg='#ffe4c4', fg='#3E86A0', activebackground='#ffe4c4')

        # 清空 按钮
        self.clearBtn = Button(self.receiveFrame, font=self.fontStyle, text='清空', bd=1, width=10, relief='groove',
                               background='#F08080')

        # 接收文本框
        self.receive_text = scrolledtext.ScrolledText(self.receiveFrame, width=31, height=10, bd=1, wrap=WORD, font=self.fontStyle)

        # 发送 Label
        self.sendLabel = Label(self.sendFrame, width=33, bd=1, relief='groove', text='发送数据',
                               font=self.fontStyle, bg='#8fbc8f', fg='#3E86A0')

        # 发送 字符表示
        self.send_view = IntVar()
        self.sendStr_RadioBtn = Radiobutton(self.sendFrame, width=8, text='字符显示', variable=self.send_view,
                                               value=1, font=self.fontStyle, bg='#8fbc8f', fg='#3E86A0',
                                               activebackground='#ffe4c4')

        # 发送 Hex表示
        self.sendHex_RadioBtn = Radiobutton(self.sendFrame, width=9, text='Hex显示', variable=self.send_view,
                                               value=2, font=self.fontStyle, bg='#8fbc8f', fg='#3E86A0',
                                               activebackground='#ffe4c4')

        # 发送 按钮
        self.sendBtn = Button(self.sendFrame, font=self.fontStyle, text='发送', bd=1, width=10, relief='groove',
                               background='#F08080')

        # 接收文本框
        self.send_text = scrolledtext.ScrolledText(self.sendFrame, width=31, height=10, bd=1, wrap=WORD, font=self.fontStyle)

        self.receive_text.tag_config("Date", font=self.fontStyle, foreground='#b8860b')
        self.receive_text.tag_config("Text", font=self.fontStyle, foreground='#d2691e')

        # run
        self.run()


    # run
    def run(self):
        # 程序 title
        self.parent.title("Serial_Port                  -- By dhl -- ")

        # 窗口大小不可变
        self.parent.resizable(0, 0)

        # root pack
        self.rootFrame.grid(column=0, row=0)

        # receive grid
        self.receiveFrame.grid(column=0, row=8, columnspan=3)

        # send grid
        self.sendFrame.grid(column=0, row=12, columnspan=3)

        # option 表格布局
        self.rootFrame.grid(column=0, row=0)

        # datetime 表格布局
        self.datetime_Label.grid(column=0, row=0, columnspan=3)

        # COM 表格布局
        self.COM_Label.grid(column=0, row=1)
        self.COM_ComBox_list.grid(column=1, row=1, columnspan=2)

        # 波特率 表格布局
        self.buteRate_Label.grid(column=0, row=2)
        self.buteRate_ComBox_list.grid(column=1, row=2, columnspan=2)
        self.buteRate_ComBox_list.current(3)

        # 数据位 表格布局
        self.bitsize_Label.grid(column=0, row=3)
        self.bitsize_ComBox_list.grid(column=1, row=3, columnspan=2)
        self.bitsize_ComBox_list.current(3)

        # 校验位 表格布局
        self.bitCheck_Label.grid(column=0, row=4)
        self.bitCheck_ComBox_list.grid(column=1, row=4, columnspan=2)
        self.bitCheck_ComBox_list.current(2)

        # 停止位 表格布局
        self.stop_Label.grid(column=0, row=5)
        self.stop_ComBox_list.grid(column=1, row=5, columnspan=2)
        self.stop_ComBox_list.current(0)

        # 下拉框 颜色
        combostyle = Style()
        combostyle.theme_create('combostyle', parent='alt',
                                settings={'TCombobox':
                                    {'configure':
                                        {
                                            'foreground': '#3E86A0',  # 前景色
                                            'selectforeground': '#ff1493',  # 选择后前景色
                                            'selectbackground': '#2B2B2B',  # 选择后的背景颜色
                                            'fieldbackground': '#2B2B2B',  # 下拉框颜色
                                            'background': '#00ffff',  # 下拉按钮颜色
                                        }}}
                                )
        combostyle.theme_use('combostyle')

        # 打开串口 布局
        self.openBtn.grid(column=0, row=6, columnspan=3)

        # 关闭串口 布局
        self.closeBtn.grid(column=0, row=7, columnspan=3)

        # receive Label
        self.receive_Label.grid(column=0, row=0, columnspan=3)

        # 接收字符 单选框布局
        self.receiveStr_RadioBtn.grid(column=0, row=1)

        # 接收Hex 单选框布局
        self.receiveHex_RadioBtn.grid(column=1, row=1)

        # 清空 按钮布局
        self.clearBtn.grid(column=2, row=1)

        # 接收文本框 布局
        self.receive_text.grid(column=0, row=2, columnspan=3, rowspan=2)

        # 发送 label
        self.sendLabel.grid(column=0, row=0, columnspan=3)

        # 发送字符 单选框布局
        self.sendStr_RadioBtn.grid(column=0, row=1)

        # 发送Hex 单选框布局
        self.sendHex_RadioBtn.grid(column=1, row=1)

        # 发送 按钮布局
        self.sendBtn.grid(column=2, row=1)

        # 发送文本框 布局
        self.send_text.grid(column=0, row=2, columnspan=3, rowspan=2)

        # 消息文本框布局
        self.Message_Label.grid(column=0, row=17, columnspan=3)

        # 动态显示时间的线程
        threading.Thread(target=self.threading_datetime).start()

        # 退出程序时的回调
        self.parent.protocol("WM_DELETE_WINDOW", self.callbackClose)

    # 动态显示时间
    def threading_datetime(self):
        while self.exit:
            self.datetime_value.set(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())))
            time.sleep(1)

    # 退出程序时的回调
    def callbackClose(self):
        self.exit = False
        exit(0)





"""if __name__ == "__main__":
    rt = Tk()
    ui = UI(rt)
    rt.mainloop()"""