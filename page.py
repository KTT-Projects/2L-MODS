import sys
from tkinter import *
import requests

root = Tk()

#ウィンドウ
root.title('ネットワーク接続')

root.geometry('1000x1000')

#入力したデータの送信
def send_data():
    network_name = network_name_entry.get()
    password = password_entry.get()

    if not network_name or not password:
        result_Label.config(text='ネットワーク名とパスワードを入力してください')
        return

    data = {
        'network_name':network_name,
        'password':password
    }

    try:
        response = requests.post('/home/developer/2L-MODS/request.php', data=data)
        result_Label.config(text=response.text)
    except Exception as e:
        result_Label.config(text=f"エラーが発生しました:{e}")



#パスワードの表示非表示の切り替え
def switch_password():
    if show_password_var.get():
        password_entry.config(show='')
    else:
        password_entry.config(show='*')

#タイトルと説明文
title_label = Label(
    root,
    text='ネットワークを検出して接続します',
    font=('Helvetica', 14, 'bold')
)
title_label.pack(pady=(10,5))

description_label = Label(
    root,
    text='接続したいネットワークの名前とパスワードを入力します'
)
description_label.pack(pady=(0,15))

#ネットワーク名の入力フィールド
network_name_label = Label(
    root,
    text='ネットワーク名：'
)
network_name_label.pack(anchor='w', padx=10)

network_name_entry = Entry(
    root
)
network_name_entry.pack(fill='x', padx=10, pady=(0,10))

#セキュリティ　放置
#Static4 = Label(text=u'セキュリティ：')
#Static4.pack()
#Entry2 = Entry(width=50)
#Entry2.pack()

#パスワードの入力フィールド
password_label = Label(
    root,
    text='パスワード：'
)
password_label.pack(anchor='w', padx=10)

password_entry = Entry(
    root,
    show='*'
)
password_entry.pack(fill='x', padx=10, pady=(0, 10))

#パスワードを表示させる
show_password_var = IntVar()
show_password = Checkbutton(
    root,
    text=u'パスワードを表示',
    variable = show_password_var,
    command = switch_password,
)
show_password.pack(anchor='w', padx=10, pady=(0,20))

#キャンセルと接続ボタン
button_frame = Frame(root)
button_frame.pack(pady=10, padx=10, fill="x")

cancel_button = Button(
    button_frame,
    text='キャンセル'
)
cancel_button.pack(side='left', padx=(0, 5), expand=True,)

conect_button = Button(
    button_frame,
    text='接続',
)

conect_button.pack()#side='right', expand=True)

#結果表示
result_Label = Label(root, text="")
result_Label.pack(pady=(10, 0))

root.mainloop()

# Layer処理開始
print ('aaa')
