import serial
import binascii
import time


def scan_COM():
    ser = serial.Serial()
    port_name = []
    i = 1
    while i < 100:
        name = 'COM' + str(i)
        #ser.open
        try:
            ser.is_open
            ser = serial.Serial(name)
            port_name.append(name)
        except serial.serialutil.SerialException as e:
            pass
        i += 1
    return port_name


def select_port(port, baudrate, bytesize, parity, stopbits, timeout):
    # serparity 检验位
    serparity = serial.PARITY_NONE
    if parity == 'Even':
        serparity = serial.PARITY_EVEN
    elif parity == 'Mark':
        serparity = serial.PARITY_MARK
    elif parity == 'Odd':
        serparity = serial.PARITY_ODD
    # serstop停止位
    serstop = serial.STOPBITS_ONE
    if stopbits == 'OnePointFive':
        serstop = serial.STOPBITS_ONE_POINT_FIVE
    elif stopbits == 'Two':
        serstop = serial.STOPBITS_TWO
    # ser 代表打开的串口信息
    try:
        ser = serial.Serial(port, baudrate, bytesize, serparity, serstop, timeout)
    except serial.serialutil.SerialException:
        ser.close()
        ser = serial.Serial(port, baudrate, bytesize, serparity, serstop, timeout)
    return ser


# while死循环接收信息
def recv(ser):
    data = ser.read_all()
    return data


def send_message(data):
    serial.write(data.encode('utf-8'))


# 转成字符串
def distinguish_data_to_Str(data):
    # 字符串码解码转字符串
    print(data)
    data = bytes(data).decode('utf-8')
    return data


# 转成HEX
def distinguish_data_to_hex(data):
    # 字符串转16进制
    senorlist = []
    # [2:-1]截取掉这个字符串的前两位和最后一位
    data = str(binascii.b2a_hex(data))[2:-1]

    # 如果len<28说明信息不完整
    if len(data) < 28:
        senorlist.append("ERROR")
    else:
        # 完整信息
        senorlist.append(data)
        # 传感器种类
        senorlist.append(data[4]+data[5])
        # 传送的数据
        senorlist.append(data[10: -6])
    # 返回一个列表
    return senorlist


def hex_to_str(s):
    return ''.join([chr(i) for i in [int(b, 16) for b in s.split(' ')]])


def str_to_hex(s):
    return ' '.join([hex(ord(c)).replace('0x', '') for c in s])


def str_to_hexStr(string):
    str_bin = string.encode('utf-8')
    print(str_bin)
    return binascii.hexlify(str_bin).decode('utf-8')


def hexStr_to_str(hex_str):
    hexadecimal = hex_str.encode('utf-8')
    str_bin = binascii.unhexlify(hexadecimal)
    return str_bin.decode('utf-8')
"""
str = "中"
encode_str = str.encode('utf-8')
decode_str = encode_str.decode('utf-8')

print(str)
print(encode_str)
print(decode_str)"""

'''
发送端， Hex和字符都转成16进制b''



'''