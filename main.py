import datetime

import serial

port = 'COM1'
baudrate = 115200
bytesize = serial.EIGHTBITS
parity = serial.PARITY_NONE
stopbits = serial.STOPBITS_ONE

with serial.Serial(
        port=port,
        baudrate=baudrate,
        bytesize=bytesize,
        parity=parity,
        stopbits=stopbits
) as ser, open('./log.txt', 'ab+') as f:
    while True:
        b = ser.read()
        # if b == b'\x00':
        #     break

        s = b.decode()
        print(s, end='')

        f.write(b)
        if s == '\n':
            now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f'^[{now_str}]\n'.encode())
        f.flush()
