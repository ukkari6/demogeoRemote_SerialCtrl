#!/usr/bin/env python3
#
#デモジオリモート　リモート機能のDIRECT INPUTモード基本コード
#FT232RLのドライバが必要です
#2024年12月以降に購入された本体はFT232RLからCH340Nに変更しています。
#このコードはXubuntu 22.04.5 LTSで書いています。
#
#これはネオジオミニに挿すだけでデモ機能を実現するUSBデバイス
# demogeoRemote（デモジオリモート）
#向けのリモート機能用基本コードです。
#
#このコードはDIRECT INPUTモード用の基本コードです。
#ネオジオミニでは動作しません。
#

import serial
import time
import sys
import random



# ボタンのビットマスク
BUTTONS = {
    'BUTTON_1': 0b00000001,
    'BUTTON_2': 0b00000010,
    'BUTTON_3': 0b00000100,
    'BUTTON_4': 0b00001000,
    'BUTTON_5': 0b00010000,
    'BUTTON_6': 0b00100000,
    'BUTTON_7': 0b01000000,
    'BUTTON_8': 0b10000000,

    'BUTTON_9': 0b00000001,
    'BUTTON_10': 0b00000010,
    'BUTTON_11': 0b00000100,
    'BUTTON_12': 0b00001000,
    'BUTTON_13': 0b00010000,
    'BUTTON_14': 0b00100000,
    'BUTTON_15': 0b01000000,
    'BUTTON_16': 0b10000000,
}



#シリアルに送信するパケットの生成
def gen_packet(button0, button1, axis1_x, axis1_y, axis2_x, axis2_y, l_trigger, r_trigger, hat):
    header1 = 0xa5
    header2 = 0x5a
    
    data = [header1, header2, button0, button1, axis1_x, axis1_y, axis2_x, axis2_y, l_trigger, r_trigger, hat, 0]
    return bytes(data)


#ボタンの状態を変更
def set_button_state(button_name, state, button0, button1):

  button = BUTTONS.get(button_name)  # ボタンのビットマスクを取得
  if button is None:
    print(f"Invalid button name: {button_name}")
    return

  if button_name in ['BUTTON_1','BUTTON_2','BUTTON_3','BUTTON_4',\
                    'BUTTON_5','BUTTON_6','BUTTON_7','BUTTON_8']:  # button0
    if state == "ON":
        button0 |= button
    else:
        button0 &= ~button
  elif button_name in ['BUTTON_9', 'BUTTON_10','BUTTON_11','BUTTON_12',\
                      'BUTTON_13', 'BUTTON_14','BUTTON_15','BUTTON_16']:  # button1
    if state == "ON":
        button1 |= button
    else:
        button1 &= ~button

  return button0, button1


#軸の状態更新
def update_axis_state_digital(state, axis_x, axis_y):

    if state == "UP":
        axis_y = 0x00  # 上
    elif state == "DOWN":
        axis_y = 0xFF  # 下
    elif state == "LEFT":
        axis_x = 0x00  # 左
    elif state == "RIGHT":
        axis_x = 0xFF  # 右
    else:
        axis_x = 0x7F  # 中央
        axis_y = 0x7F  # 中央

    return axis_x, axis_y

#ハットの状態を更新
def update_hat_state(state, hat):
    if state == "UP":
        hat = 0
    elif state == "UP-RIGHT":
        hat = 1
    elif state == "RIGHT":
        hat = 2
    elif state == "DOWN-RIGHT":
        hat = 3
    elif state == "DOWN":
        hat = 4
    elif state == "DOWN-LEFT":
        hat = 5
    elif state == "LEFT":
        hat = 6
    elif state == "UP-LEFT":
        hat = 7
    else:
        hat = 8   #中央

    return hat

#シリアルに送信するパケットを生成し、シリアルポートにバイナリデータを書き込む
def send_data(ser, button0, button1, axis1_x, axis1_y, axis2_x, axis2_y, l_trigger, r_trigger, hat):
    data = gen_packet(button0, button1, axis1_x, axis1_y, axis2_x, axis2_y, l_trigger, r_trigger, hat)
    ser.write(data)
    print(f"Sent: {data}")   #送信データの表示


if __name__ == "__main__":
    # シリアルポートの設定
    serial_port = '/dev/ttyUSB0'  # 実行環境で変更する
    baud_rate = 115200

    #デモジオに送るボタン変数
    button0 = 0
    button1 = 0
    axis1_x = 0x7F #0=左,0x7F=中央,0xFF=右、だいたい左スティック割り当て
    axis1_y = 0x7F #0=上,0x7F=中央,0xFF=下、だいたい左スティック割り当て
    axis2_x = 0x7F #0=左,0x7F=中央,0xFF=右、だいたい右スティック割り当て 
    axis2_y = 0x7F #0=上,0x7F=中央,0xFF=下、だいたい右スティック割り当て
    l_trigger = 0 #0から0xFFまで
    r_trigger = 0 #0から0xFFまで
    hat = 8       #0から8まで
    with serial.Serial(serial_port, baud_rate, timeout=1) as ser:

      while True:
        #右、左、ボタン１、ボタン２を繰り返すコード
        #axis1_x, axis1_y = update_axis_state_digital("RIGHT", axis1_x, axis1_y)  #だいたい左
        #axis2_x, axis2_y = update_axis_state_digital("RIGHT", axis2_x, axis2_y)  #たいだい右
        #button0, button1 = set_button_state("BUTTON_16", "ON", button0, button1) #ボタンの状態を更新、1から16まで
        #hat = update_hat_state("UP", hat)  #ハットの状態を更新,UP,UP-RIGHT,RIGHT,DOWN-RIGHT,DOWN,DOWN-LEFT,LEFT,UP-LEFT

        #send_data(ser, button0, button1, axis1_x, axis1_y, axis2_x, axis2_y, l_trigger, r_trigger, hat)
        #axis1_x, axis1_y, axis2_x, axis2_y, l_trigger, r_trigger, hatの割り当てはVID/PIDやOSや環境によって変化します。
        #環境によって右スティックとして動かなかったりhatとして動かない場合があります。


        axis1_x, axis1_y = update_axis_state_digital("RIGHT", axis1_x, axis1_y)  #だいたい左
        send_data(ser, button0, button1, axis1_x, axis1_y, axis2_x, axis2_y, l_trigger, r_trigger, hat)  #デモジオにボタン状態を送信
        time.sleep(0.1)

        axis1_x, axis1_y = update_axis_state_digital("LEFT", axis1_x, axis1_y)  #だいたい左
        send_data(ser, button0, button1, axis1_x, axis1_y, axis2_x, axis2_y, l_trigger, r_trigger, hat)  #デモジオにボタン状態を送信
        time.sleep(0.1)

        axis1_x, axis1_y = update_axis_state_digital("CENTER", axis1_x, axis1_y)  #だいたい左
        send_data(ser, button0, button1, axis1_x, axis1_y, axis2_x, axis2_y, l_trigger, r_trigger, hat)  #デモジオにボタン状態を送信
        time.sleep(0.1)

        button0, button1 = set_button_state("BUTTON_1", "ON", button0, button1) #ボタンの状態を更新、1から16まで
        send_data(ser, button0, button1, axis1_x, axis1_y, axis2_x, axis2_y, l_trigger, r_trigger, hat)  #デモジオにボタン状態を送信
        time.sleep(0.1)

        button0, button1 = set_button_state("BUTTON_1", "OFF", button0, button1) #ボタンの状態を更新、1から16まで
        send_data(ser, button0, button1, axis1_x, axis1_y, axis2_x, axis2_y, l_trigger, r_trigger, hat)  #デモジオにボタン状態を送信
        time.sleep(0.1)

        button0, button1 = set_button_state("BUTTON_2", "ON", button0, button1) #ボタンの状態を更新、1から16まで
        send_data(ser, button0, button1, axis1_x, axis1_y, axis2_x, axis2_y, l_trigger, r_trigger, hat)  #デモジオにボタン状態を送信
        time.sleep(0.1)

        button0, button1 = set_button_state("BUTTON_2", "OFF", button0, button1) #ボタンの状態を更新、1から16まで
        send_data(ser, button0, button1, axis1_x, axis1_y, axis2_x, axis2_y, l_trigger, r_trigger, hat)  #デモジオにボタン状態を送信
        time.sleep(0.1)
