#!/usr/bin/env python3
#
#デモジオリモート　VID/PID書き換えコード
#FT232RLのドライバが必要です
#2024年12月以降に購入された本体はFT232RLからCH340Nに変更しています。
#このコードはXubuntu 22.04.5 LTSで書いています。
#
#これはネオジオミニに挿すだけでデモ機能を実現するUSBデバイス
# demogeoRemote（デモジオリモート）
#のリモートモードのVID/PIDを書き換えるコードです。
#
#VID/PIDを書き換えることで、
#デモジオリモートを任意のUSBデバイスとして動作させることができます。
#
#VID/PIDを書き換えるとパソコン側が正常なUSBデバイスとして認識できなくなったり、
#USB周りの設定をリセットしなきゃいけなく面倒なことになるので
#このコードの実行は完全自己責任でお願いします。
#
#出荷時デフォルト値
#ネオジオミニ
#VID = 0x04d8;
#PID = 0xee12;
#XINPUT
#VID = 0x045E;
#PID = 0x028E;
#DIRECTINPUT
#VID = 0x2563;
#PID = 0x0575;
#例えば、以下の値を書き込むと以下のアレのように認識されます。
#HORI HORIPAD for Nintendo Switch
#0x0f0d, 0x00c1

import serial
import time
import random
import sys


def rewrite_vid_pid():
  VID = input("VIDを入力してください（例：0xFFFF）： ")
  try:
      data = int(VID, 16) 
      if data < 0 or data > 0xFFFF:
          raise ValueError("0x0000から0xFFFFの範囲で入力してください")
      VID_H = (data >> 8) & 0xFF  # 上位バイト
      VID_L= data & 0xFF          # 下位バイト
  except ValueError as e:
      print("エラー：正しい16進数の形式で入力してください")
      sys.exit()  # プログラムを終了

  PID = input("PIDを入力してください（例：0xFFFF）： ")
  try:
      data = int(PID, 16) 
      if data < 0 or data > 0xFFFF:
          raise ValueError("0x0000から0xFFFFの範囲で入力してください")
      PID_H = (data >> 8) & 0xFF  # 上位バイト
      PID_L= data & 0xFF          # 下位バイト
  except ValueError as e:
      print("エラー：正しい16進数の形式で入力してください")
      sys.exit()  # プログラムを終了

  head0 = 0xfe
  head1 = 0xf0

  ser.write(bytes([head0, head1, VID_H, VID_L, PID_H, PID_L]))
  print("書き換え完了しました。デモジオリモートを差し直してください。")







# シリアルポートの設定
serial_port = '/dev/ttyUSB0'
baud_rate = 115200  # ボーレートは適宜設定してください

# シリアルポートを開く
with serial.Serial(serial_port, baud_rate, timeout=1) as ser:
  for i in range(100):
    ser.write(bytes(0))
  print("------------------------------------------")
  print("demogeoRemote VID/PID　書き換えプログラム")
  print("------------------------------------------")
  print("VID/PIDを書き換えるとUSBデバイスの認識が不完全になったり、最悪の場合USBの機能が利用できなくなる場合があります。")
  user_input = input("よろしいですか？ (Y/N): ").strip().upper()
  if user_input == 'Y':
    rewrite_vid_pid()
    sys.exit()
  elif user_input == 'N':
    sys.exit()
  else:
    print("無効な入力です。YまたはNを入力してください。")
    sys.exit()
