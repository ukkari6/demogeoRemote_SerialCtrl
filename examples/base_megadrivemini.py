#!/usr/bin/env python3
#
#デモジオリモート　リモート機能のメガドラミニモード用基本コード
#FT232RLのドライバが必要です
#このコードはXubuntu 22.04.5 LTSで書いています。
#
#これはネオジオミニに挿すだけでデモ機能を実現するUSBデバイス
# demogeoRemote（デモジオリモート）
#向けのリモート機能用基本コードです。
#
#このコードはネオジオミニモード用のコードです。
#A,B,C,X,Y,Z,スタート,モード、十字キー操作がPythonから出来るようになっています。
#
#ジョイスティックを右に送り続けるコードのみ実装していますが、
#キーボード入力やUSBパッドのボタンを読み取ってデモジオリモートに送るだけで
#ゲームの操作が可能です。
#
#また、キーボード入力やUSBパッドの状態から特定のパターンを読み出すことで
#強力なマクロとしても動作出来ます。

import serial
import time
import sys
import random



# ボタンのビットマスク
BUTTONS = {
    'BUTTON_A': 0b00000100,  # button0の0ビット目
    'BUTTON_B': 0b00000010,  # button0の1ビット目
    'BUTTON_C': 0b00100000,  # button0の3ビット目
    'BUTTON_X': 0b00001000,
    'BUTTON_Y': 0b00000001,
    'BUTTON_Z': 0b00010000,
    'BUTTON_START':0b00000010,  # button1の3ビット目
    'BUTTON_MODE': 0b00000001,   # button1の3ビット目
}


#シリアルに送信するパケットの生成
def gen_packet(button0, button1, axis_x, axis_y):
    header1 = 0xa5
    header2 = 0x5a
    
    data = [header1, header2, button0, button1, axis_y, axis_x, 0, 0, 0, 0, 0, 0]
    return bytes(data)


#ボタンの状態を変更
#set_button_state("BUTTON_A", "ON") のように使う
#BUTTON_A
#BUTTON_B
#BUTTON_C
#BUTTON_X
#BUTTON_Y
#BUTTON_Z
#BUTTON_START
#BUTTON_MODE
def set_button_state(button_name, state, button0, button1):

  button = BUTTONS.get(button_name)  # ボタンのビットマスクを取得
  if button is None:
    print(f"Invalid button name: {button_name}")
    return

  if button_name in ['BUTTON_A', 'BUTTON_B', 'BUTTON_C', 'BUTTON_X', 'BUTTON_Y', 'BUTTON_Z', ]:  # button0
    if state == "ON":
        button0 |= button
    else:
        button0 &= ~button
  elif button_name in ['BUTTON_START', 'BUTTON_MODE']:  # button1
    if state == "ON":
        button1 |= button
    else:
        button1 &= ~button

  return button0, button1


#軸の状態更新（デジタル）
def update_axis_state_digital(state, axis_x, axis_y):
    if state == "UP":
        axis_x = 0x00  # 上
        axis_y = 0x7F
    elif state == "DOWN":
        axis_x = 0xFF  # 下
        axis_y = 0x7F
    elif state == "LEFT":
        axis_x = 0x7F
        axis_y = 0x00  # 左
    elif state == "RIGHT":
        axis_x = 0x7F
        axis_y = 0xFF  # 右
    else:
        axis_x = 0x7F  # 中央
        axis_y = 0x7F  # 中央

    return axis_x, axis_y


#シリアルに送信するパケットを生成し、シリアルポートにバイナリデータを書き込む
def send_data(ser, button0, button1, axis_x, axis_y):
    data = gen_packet(button0, button1, axis_x, axis_y)
    ser.write(data)
    print(f"Sent: {data}")   #送信データの表示


if __name__ == "__main__":
    # シリアルポートの設定
    serial_port = '/dev/ttyUSB0'  # 実行環境で変更する
    baud_rate = 115200

    #デモジオに送るボタン変数
    button0 = 0
    button1 = 0
    axis_x = 0x7F #0=左,0x7F=中央,0xFF=右
    axis_y = 0x7F #0=上,0x7F=中央,0xFF=下
    with serial.Serial(serial_port, baud_rate, timeout=1) as ser:

      while True:
        #ジョイスティックを右に送り続けるサンプルコード
        #axis_x, axis_y = update_axis_state_digital("RIGHT", axis_x, axis_y)  #ジョイスティックの状態を更新
        #button0, button1 = set_button_state("BUTTON_SELECT", "OFF", button0, button1) #ボタンの状態を更新

        axis_x, axis_y = update_axis_state_digital("RIGHT", axis_x, axis_y)  #ジョイスティックの状態を更新
        #button0, button1 = set_button_state("BUTTON_START", "ON", button0, button1) #ボタンの状態を更新
        send_data(ser, button0, button1, axis_x, axis_y)  #デモジオにボタン状態を送信
        time.sleep(0.1)

        axis_x, axis_y = update_axis_state_digital("CENTER", axis_x, axis_y)  #ジョイスティックの状態を更新
        #button0, button1 = set_button_state("BUTTON_START", "OFF", button0, button1) #ボタンの状態を更新
        send_data(ser, button0, button1, axis_x, axis_y)  #デモジオにボタン状態を送信
        time.sleep(0.5)
