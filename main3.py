import requests
import sqlite3
import os
from io import BytesIO
from PIL import Image


if __name__ == "__main__":
    urls = "http://localhost:8000/"
    login = {'srvno': '', 'password': '', 'device_id': ''}
    res1 = requests.post(url=urls+'Accounts/login/', json=login)
    token = res1.json()['data']['token']
    header = {'Authorization': 'jwt ' + token}
    con = sqlite3.connect('db.sqlite3')
    c = con.cursor()
    c1 = con.cursor()
    base_path = 'C:/Users/User/Desktop/선박이미지/'
    if not (os.path.isdir(base_path)):
        os.makedirs(os.path.join(base_path))
    while True:
        _ship_id = input('합칠 선박 ID 입력 : ')
        ship_id = input('선박 ID 입력 : ')
        c.execute("SELECT id, name FROM NormalShip WHERE id={}".format(ship_id))
        ship_data = c.fetchone()
        if ship_data is None:
            print('존재하지 않는 선박입니다\n')
            continue
        if not (os.path.isdir(base_path + str(ship_data[0]))):
            os.makedirs(os.path.join(base_path + str(ship_data[0])))
        c1.execute("SELECT img FROM NormalImage WHERE n_name_id={}".format(ship_data[0]))
        url = 'http://211.236.124.151:2162/media/'
        img_idx = 0
        for img_url in c1.fetchall():
            try:
                res = requests.get(url + img_url[0])
                img_data = BytesIO(res.content)
                img = Image.open(img_data)
                img_name = base_path + str(ship_data[0]) + '/' + str(ship_data[1]) + "_" + str(img_idx) + '.jpg'
                img.save(img_name)
                print("{0} 선박 {1} 번째 이미지 저장".format(ship_data[0], img_idx))
                img_idx = img_idx + 1
            except Exception as e:
                continue
        data = {'id': int(_ship_id)}
        for img in os.listdir(base_path + str(ship_data[0])):
            image = {'image_data': open(base_path + str(ship_data[0]) + '/' + img, 'rb')}
            status = requests.post(url=urls+'Ships/image/normal/', headers=header, data=data,
                                   files=image)
        print("{0} <-> {1} 합병 완료".format(_ship_id, ship_id))