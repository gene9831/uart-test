import datetime
import time
import serial

port = 'COM4'
baudrate = 28800
bytesize = serial.EIGHTBITS
parity = serial.PARITY_NONE
stopbits = serial.STOPBITS_ONE


cc_flag = False


def get_log_file_name(dt: datetime.datetime):
    return f'log-{dt.strftime("%Y-%m-%d-%H.%M")}.txt'


log_file_name = get_log_file_name(datetime.datetime.now())
# print(log_file_name)
print('\033[1;31m' + '*' * 50)
print('\033[1;31m请勿关闭此程序。因操作不当导致数据丢失，后果自负！\033[0m')
print('\033[1;31m' + '*' * 50 + '\033[0m')
# exit()


while True:
    try:
        with serial.Serial(
                port=port,
                baudrate=baudrate,
                bytesize=bytesize,
                parity=parity,
                stopbits=stopbits
        ) as ser:
            while True:
                while True:
                    with open(f'./{log_file_name}', 'a+', encoding='utf8') as f:
                        bs = ser.read()

                        if bs == b'\xcc':
                            cc_flag = True
                            continue
                        elif cc_flag and bs == b'\xdd':
                            now = datetime.datetime.now()
                            # 遇到 cc dd 换行
                            f.write(
                                f'\n[{now.strftime("%Y-%m-%d %H:%M:%S")}]\n')
                            f.write('cc dd ')

                            # if now.minute % 1 == 0 and now.second == 0:
                            if now.hour % 4 == 0 and now.minute == 0 and now.second == 0:
                                # 每4小时更换log file的名称
                                tmp_log_file_name = get_log_file_name(now)
                                if tmp_log_file_name != log_file_name:
                                    log_file_name = tmp_log_file_name
                                    break
                                else:
                                    continue
                            else:
                                continue

                        for b in bs:
                            f.write(f'{b:02x} ')

                        f.flush()
    except serial.SerialException as e:
        print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {e}')
        time.sleep(3)
