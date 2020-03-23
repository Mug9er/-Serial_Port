import UI
import Serial_Operation
from tkinter import *
import time
import serial
import threading
import base64
import binascii
import re


class Ui_Operator(object):
    def __init__(self, master):
        self.parent = master
        self.ui = UI.Ui(self.parent)
        self.view_time = 0
        self.run()
        self.ser = serial.Serial()

    def run(self):
        threading.Thread(target=self.threading_scan_com).start()
        self.ui.openBtn.bind('<Button-1>', self.open_port)
        self.ui.sendBtn.bind('<Button-1>', self.send_message)
        self.ui.closeBtn.bind('<Button-1>', self.close_port)

    def threading_scan_com(self):
        # self.view_time = 0
        while self.ui.exit:
            com_list = Serial_Operation.scan_COM()
            if len(com_list) != len(self.ui.COM_ComBox_list['value']):
                print(com_list)
                self.ui.COM_ComBox_list['value'] = com_list
                self.ui.Message_value.set("[新消息]:串口列表发生变化")
                self.view_time = 0
            time.sleep(0.1)
            # self.view_time += 1
            # if self.view_time == 10:
            #    self.ui.Message_value.set("")

    def open_port(self, event):
        get_com = self.ui.COM_ComBox_list.get()
        get_bute = self.ui.buteRate_ComBox_list.get()
        get_bit = self.ui.bitsize_ComBox_list.get()
        get_check = self.ui.bitCheck_ComBox_list.get()
        get_stop = self.ui.stop_ComBox_list.get()
        self.ser = Serial_Operation.select_port(get_com, get_bute, int(get_bit), get_check, get_stop, 0.05)
        if self.ser.isOpen():
            self.view_time = 0
            threading.Thread(target=self.threading_recv_data).start()
            self.ui.Message_value.set("端口%s已经打开" % get_com)
        else:
            self.view_time = 0
            self.ui.Message_value.set("端口%s打开失败" % get_com)

    def send_message_value(self, data):
        if self.ui.send_view.get() == 1:
            return data.encode("utf-8")
        else:
            data = base64.b16decode(data)
            return data

    def receive_message_value(self, data):
        rec_data = StringVar()
        try:
            rec_data = data.decode('utf-8')
        except UnicodeDecodeError:
            rec_data = base64.b16encode(data).decode('utf-8')
        if self.ui.receive_view.get() == 1:
            return rec_data
        else:
            rec_data = rec_data.encode('utf-8')
            return rec_data.hex()

    def threading_recv_data(self):
        while self.ui.exit and self.ser.isOpen():
            data = self.ser.read_all()
            if data != b'':
                self.ui.receive_text.insert(END, time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())) + ":\n"
                                            , 'Date')
                self.ui.receive_text.see(END)
                self.ui.receive_text.insert(END, self.receive_message_value(data) + '\n',
                                            'Text')
                self.ui.receive_text.see(END)

            time.sleep(0.1)

    def send_message(self, event):
        data = self.ui.send_text.get('0.0', END)
        rec = re.findall(r'(.*?)\n', data, re.S)
        data = self.send_message_value(rec[0])
        self.ser.write(data)

    def close_port(self, event):
        self.ser.close()
        if self.ser.isOpen():
            self.ui.Message_value.set("端口关闭失败")
        else:
            self.ui.Message_value.set("端口关闭成功")


if __name__ == '__main__':
    rt = Tk()
    ui = Ui_Operator(rt)
    rt.mainloop()
