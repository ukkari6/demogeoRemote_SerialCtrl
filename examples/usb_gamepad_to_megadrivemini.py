#!/usr/bin/env python3
#デモジオリモート　USBコントローラー　→　メガドライブミニブリッジコード
#FT232RLのドライバが必要です
#USBコントローラーの読み取りにPygameを使用していますので、ライブラリのインストールが必要です。
#pip3 install pygame
#このコードはXubuntu 24.04.5 LTSで書いています。
#
#これはネオジオミニに挿すだけでデモ機能を実現するUSBデバイス
# demogeoRemote（デモジオリモート）
#用のUSBコントローラー　→　メガドラミニモード用ブリッジコードです。
#USBコントローラーの入力をメガドラミニに橋渡し（ブリッジ）します。
#
#様々な種類のUSBコントローラーに対応出来るように、このコード起動時に
#A,B,C,X,Y,Z,START,MODE
#の割り当てをするようにしています。
#
#フルスピードで動かすとCPUに負担が掛かるので、
#pygame.time.wait(5)
#でウェイトを入れていますが、ジョイスティックがガクつく場合は値を小さくしてください。


import serial
import time
import sys
import pygame
from base_megadrivemini import set_button_state, update_axis_state_digital, send_data


NUM_BUTTONS = 8 #割り当てるボタン数



#ボタン割り当て設定
def buttons_config():
  buttons = []
  # USBコントローラーボタン総数取得
  num_buttons = joystick.get_numbuttons()

  print(" ")
  print(" ")
  print(" ")
  print("*********************************")
  print("  割り当てたいボタンを ")
  print("  A　B　C　X　Y　Z　START　MODE  ")
  print("  の順番で押してください  ")
  print("*********************************")

  # イベントループ
  while len(buttons) < NUM_BUTTONS:
    for event in pygame.event.get():
      if event.type == pygame.JOYBUTTONDOWN:
        button_index = event.button  # 押されたボタンの番号
        print(f"ボタン {button_index} が押されました。")
        buttons.append(button_index)

  return buttons




if __name__ == "__main__":
    # シリアルポートの設定
    serial_port = '/dev/ttyUSB0'  # 実行環境で変更する
    baud_rate = 115200

    #デモジオに送るボタン変数 button0 = 0
    button0 = 0
    button1 = 0
    axis_x = 0x7F #0=左,0x7F=中央,0xFF=右
    axis_y = 0x7F #0=上,0x7F=中央,0xFF=下
    
    with serial.Serial(serial_port, baud_rate, timeout=1) as ser:


      # pygameを初期化
      pygame.init()
      # ジョイスティックを初期化
      pygame.joystick.init()
      # 接続されているジョイスティックの数を取得
      joystick_count = pygame.joystick.get_count()

      if joystick_count == 0:
        print("ジョイスティックが見つかりません。")
        sys.exit()

      # 最初のジョイスティックを使用
      joystick = pygame.joystick.Joystick(0)
      joystick.init()

      # ボタン、軸、ハットスイッチの数を取得
      num_buttons = joystick.get_numbuttons()
      num_axes = joystick.get_numaxes()
      num_hats = joystick.get_numhats()

      # 割り当てるボタン名
      button_names = ["BUTTON_A", "BUTTON_B", "BUTTON_C", "BUTTON_X", "BUTTON_Y", "BUTTON_Z", "BUTTON_START", "BUTTON_MODE"]

      #ボタン割り当て設定
      buttons = buttons_config()

      # メインループ
      running = True
      while running:
        # イベントを取得
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            running = False

          #ジョイスティックの状態を更新
          if event.type == pygame.JOYAXISMOTION:
            axis_y = int((joystick.get_axis(1) + 1.0 ) / 2.0 * 256)
            axis_x = int((joystick.get_axis(0) + 1.0 ) / 2.0 * 256)
          #ジョイスティックの状態がハット操作に干渉するので削除
          #ハット操作をジョイスティック操作に反映させる
          #elif event.type == pygame.JOYHATMOTION:
            #x,y = joystick.get_hat(0)
            #print("x")
            #print(x)
            #print("y")
            #print(y)
          #  y = -y  #ハットの上下1と-1がAXISと逆なので反転
            #axis_y = int((x + 1.0 ) / 2.0 * 255)  #ハットの-1,0,1を0,0x7F,0xFFに変換
            #converted_value = int((y + 1))
            #axis_x = int((x + 1.0 ) / 2.0 * 255)
            #y = -y
            #axis_y = int((y + 1.0 ) / 2.0 * 255)

            #print("converted_value")
            #print(converted_value)
            #print("axis_y")
            #print(axis_y)
            #print("axis_x")
            #print(axis_x)


          #ボタンの状態を更新
          for i, button_name in enumerate(button_names):
            if joystick.get_button(buttons[i]) == 1:
              button0, button1 = set_button_state(button_name, "ON", button0, button1)
            else:
              button0, button1 = set_button_state(button_name, "OFF", button0, button1)

          send_data(ser, button0, button1, axis_y, axis_x)  #デモジオにボタン状態を送信
          pygame.time.wait(1) #フルスピードで動かすとCPUに負担が掛かるためウェイト

