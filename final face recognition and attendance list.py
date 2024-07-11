"""
#FOTOĞRAFLARI KIYASLIYOR
import cv2
import face_recognition

# Elon Musk'ın resmini yükle ve renk formatını BGR'den RGB'ye dönüştür
imgElon = face_recognition.load_image_file('ImagesBasic/Elon Musk.jpg')
imgElon = cv2.cvtColor(imgElon, cv2.COLOR_BGR2RGB)

# Test resmini yükle ve renk formatını BGR'den RGB'ye dönüştür
imgTest = face_recognition.load_image_file('ImagesBasic/1.jpg')
imgTest = cv2.cvtColor(imgTest, cv2.COLOR_BGR2RGB)

# Elon Musk'ın yüzünü bul ve dikdörtgen içine al
faceLoc = face_recognition.face_locations(imgElon)[0]
encodeElon = face_recognition.face_encodings(imgElon)[0]
cv2.rectangle(imgElon, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 0, 255), 2)

# Test resmindeki yüzü bul ve dikdörtgen içine al
faceLocTest = face_recognition.face_locations(imgTest)[0]
encodeTest = face_recognition.face_encodings(imgTest)[0]
cv2.rectangle(imgTest, (faceLocTest[3], faceLocTest[0]), (faceLocTest[1], faceLocTest[2]), (255, 0, 255), 2)

# Yüzleri karşılaştır ve sonuçları ve yüz uzaklığını ekrana yazdır
results = face_recognition.compare_faces([encodeElon], encodeTest)
faceDis = face_recognition.face_distance([encodeElon], encodeTest)
print(results, faceDis)

# Sonuçları ve yüz uzaklığını test resminin üstüne yazdır
cv2.putText(imgTest, f'{results} {round(faceDis[0], 2)}', (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

# Resimleri göster
cv2.imshow('Elon Musk', imgElon)
cv2.imshow('Elon Test', imgTest)
cv2.waitKey(0)
"""
"""
#YOKLAMA LİSTESİ OLUŞTURUP KAMERADAN YOKLAMA ALIYOR
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pandas as pd

# 'ImagesAttendance' klasöründeki resimlerin yolları ve isimleri
path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
    print(classNames)

# Resimlerin yüz tanıma kodlamalarını bulan fonksiyon
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Resmi RGB formatına dönüştürme
        encodes = face_recognition.face_encodings(img)
        if len(encodes) > 0:  # Eğer resimde yüz kodlaması varsa
            encode = encodes[0]
            encodeList.append(encode)
    return encodeList

# Katılım listesini güncelleyen fonksiyon
def markAttendance(name):
    # Dosya mevcut değilse oluştur ve başlık ekle
    if not os.path.exists('Attendance.csv'):
        with open('Attendance.csv', 'w') as f:
            f.writelines('Name,Time\n')
    
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

# Yüz kodlamalarını bul
encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)  # Resmi %25 boyutuna küçültme
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)  # Resmi RGB formatına dönüştürme
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
    
    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)
        
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Yüz çevresine dikdörtgen çizme
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)  # İsim kutusunu doldurma
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)  # İsmi yazma
            markAttendance(name)
    
    cv2.imshow('Webcam', img)

    # 'q' tuşuna basıldığında döngüyü ve programı durdurma
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()  # Kamerayı serbest bırakma
cv2.destroyAllWindows()  # Tüm pencereleri kapatma

# Attendance.csv dosyasını gösterme
if os.path.exists('Attendance.csv'):
    attendance_df = pd.read_csv('Attendance.csv')
    print(attendance_df)
else:
    print("Attendance.csv dosyası mevcut değil.")
"""
#unkownK KİŞİ GÜNCELLEMESİ
"""
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pandas as pd

# 'ImagesAttendance' klasöründeki resimlerin yolları ve isimleri
path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
    print(classNames)

# Resimlerin yüz tanıma kodlamalarını bulan fonksiyon
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Resmi RGB formatına dönüştürme
        encodes = face_recognition.face_encodings(img)
        if len(encodes) > 0:  # Eğer resimde yüz kodlaması varsa
            encode = encodes[0]
            encodeList.append(encode)
    return encodeList

# Katılım listesini güncelleyen fonksiyon
def markAttendance(name):
    # Dosya mevcut değilse oluştur ve başlık ekle
    if not os.path.exists('Attendance.csv'):
        with open('Attendance.csv', 'w') as f:
            f.writelines('Name,Time\n')
    
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

# Yüz kodlamalarını bul
encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)  # Resmi %25 boyutuna küçültme
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)  # Resmi RGB formatına dönüştürme
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
    
    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)
        
        if faceDis[matchIndex] < 0.50:  # Eğer en yakın yüzün uzaklığı 0.50'den küçükse
            name = classNames[matchIndex].upper()
            markAttendance(name)
        else:
            name = 'Unknown'
        
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Yüz çevresine dikdörtgen çizme
        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)  # İsim kutusunu doldurma
        cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)  # İsmi yazma
    
    cv2.imshow('Webcam', img)

    # 'q' tuşuna basıldığında döngüyü ve programı durdurma
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()  # Kamerayı serbest bırakma
cv2.destroyAllWindows()  # Tüm pencereleri kapatma

# Attendance.csv dosyasını gösterme
if os.path.exists('Attendance.csv'):
    attendance_df = pd.read_csv('Attendance.csv')
    print(attendance_df)
else:
    print("Attendance.csv dosyası mevcut değil.")
"""
#unkown KİŞİLERİN YOKLAMAYA EKLENMİŞ HALİ
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pandas as pd

# 'ImagesAttendance' klasöründeki resimlerin yolları ve isimleri
path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
    print(classNames)

# Kaydedilen katılım bilgilerini tutmak için set kullanılacak
attendance_set = set()

# Resimlerin yüz tanıma kodlamalarını bulan fonksiyon
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Resmi RGB formatına dönüştürme
        encodes = face_recognition.face_encodings(img)
        if len(encodes) > 0:  # Eğer resimde yüz kodlaması varsa
            encode = encodes[0]
            encodeList.append(encode)
    return encodeList

# Katılım listesini güncelleyen fonksiyon
def markAttendance(name):
    # Dosya mevcut değilse oluştur ve başlık ekle
    if not os.path.exists('Attendance.csv'):
        with open('Attendance.csv', 'w') as f:
            f.writelines('Name,Time\n')
    
    now = datetime.now()
    dtString = now.strftime('%H:%M:%S')
    
    # Eğer isim zaten listedeyse tekrar eklemeyelim
    if name not in attendance_set:
        with open('Attendance.csv', 'a') as f:
            f.writelines(f'\n{name},{dtString}')
        attendance_set.add(name)

# Yüz kodlamalarını bul
encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)
#Videodan yüzleri tam algılayamıyor uzak geliyor, webcam düzeyinde yakın olmalı amx verim için

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)  # Resmi %25 boyutuna küçültme
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)  # Resmi RGB formatına dönüştürme
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
    
    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)
        
        if faceDis[matchIndex] < 0.50:  # Eğer en yakın yüzün uzaklığı 0.50'den küçükse
            name = classNames[matchIndex].upper()
        else:
            name = 'Unknown'
        
        markAttendance(name)
        
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Yüz çevresine dikdörtgen çizme
        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)  # İsim kutusunu doldurma
        cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)  # İsmi yazma
    
    cv2.imshow('Webcam', img)

    # 'q' tuşuna basıldığında döngüyü ve programı durdurma
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()  # Kamerayı serbest bırakma
cv2.destroyAllWindows()  # Tüm pencereleri kapatma

# Attendance.csv dosyasını gösterme
if os.path.exists('Attendance.csv'):
    attendance_df = pd.read_csv('Attendance.csv')
    print(attendance_df)
else:
    print("Attendance.csv dosyası mevcut değil.")

#İNPUTLA unkownU TANIMA VE SON HALİ
#HATALI
#ÇÜNKÜ SÜREKLİ BOŞ OKUDUĞUNDA unkown KAYDETMEYİ İSTİYO VE KAMERA DONUYOR
"""
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pandas as pd

# 'ImagesAttendance' klasöründeki resimlerin yolları ve isimleri
path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
    print(classNames)

# Kaydedilen katılım bilgilerini tutmak için set kullanılacak
attendance_set = set()

# Resimlerin yüz tanıma kodlamalarını bulan fonksiyon
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Resmi RGB formatına dönüştürme
        encodes = face_recognition.face_encodings(img)
        if len(encodes) > 0:  # Eğer resimde yüz kodlaması varsa
            encode = encodes[0]
            encodeList.append(encode)
    return encodeList

# Katılım listesini güncelleyen fonksiyon
def markAttendance(name):
    # Dosya mevcut değilse oluştur ve başlık ekle
    if not os.path.exists('Attendance.csv'):
        with open('Attendance.csv', 'w') as f:
            f.writelines('Name,Time\n')
    
    now = datetime.now()
    dtString = now.strftime('%H:%M:%S')
    
    # Eğer isim zaten listedeyse tekrar eklemeyelim
    if name not in attendance_set:
        with open('Attendance.csv', 'a') as f:
            f.writelines(f'\n{name},{dtString}')
        attendance_set.add(name)

# Yüz kodlamalarını bul
encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)
start_time = datetime.now()

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)  # Resmi %25 boyutuna küçültme
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)  # Resmi RGB formatına dönüştürme
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
    
    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)
        
        if faceDis[matchIndex] < 0.50:  # Eğer en yakın yüzün uzaklığı 0.50'den küçükse
            name = classNames[matchIndex].upper()
        else:
            if (datetime.now() - start_time).seconds > 10:  # 10 saniyeden fazla süre geçtiyse
                name = 'Unknown'
            else:
                # İlk 10 saniye içinde isim girilmesini bekleyelim
                cv2.putText(img, "Enter name:", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.imshow('Webcam', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                continue
        
        if name == 'Unknown':
            # Unknown olarak tanınan kişinin ismini input olarak al
            cv2.putText(img, "Enter name:", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow('Webcam', img)
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                break
            elif key & 0xFF == ord('x'):
                if os.path.exists('Attendance.csv'):
                    os.remove('Attendance.csv')
                    attendance_set.clear()  # attendance_set'i temizleme
                    print("Attendance.csv dosyası temizlendi.")
                else:
                    print("Attendance.csv dosyası mevcut değil.")
            else:
                name = input("Enter the name of the unknown person: ")
                if name:
                    # Yeni kişiyi tanımlama ve kaydetme
                    cv2.imwrite(f"{path}/{name}.jpg", img)
                    classNames.append(name)
                    encodeListKnown = findEncodings(images + [img])  # Yeni resmi ekleyerek yeniden kodlamaları bulma
                    markAttendance(name)
                else:
                    name = 'Unknown'
        
        markAttendance(name)
        
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Yüz çevresine dikdörtgen çizme
        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)  # İsim kutusunu doldurma
        cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)  # İsmi yazma
    
    cv2.imshow('Webcam', img)

    # 'q' tuşuna basıldığında döngüyü ve programı durdurma
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # 'x' tuşuna basıldığında Attendance.csv dosyasını temizleme
    if cv2.waitKey(1) & 0xFF == ord('x'):
        if os.path.exists('Attendance.csv'):
            os.remove('Attendance.csv')
            attendance_set.clear()  # attendance_set'i temizleme
            print("Attendance.csv dosyası temizlendi.")
        else:
            print("Attendance.csv dosyası mevcut değil.")
    
cap.release()  # Kamerayı serbest bırakma
cv2.destroyAllWindows()  # Tüm pencereleri kapatma

# Attendance.csv dosyasını gösterme
if os.path.exists('Attendance.csv'):
    attendance_df = pd.read_csv('Attendance.csv')
    print(attendance_df)
else:
    print("Attendance.csv dosyası mevcut değil.")"""

"""
#X TUşUNA BASINCA YOKLAMAYI TEMİZLİYO VE SON HALİ
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pandas as pd

# 'ImagesAttendance' klasöründeki resimlerin yolları ve isimleri
path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
    print(classNames)

# Kaydedilen katılım bilgilerini tutmak için set kullanılacak
attendance_set = set()

# Resimlerin yüz tanıma kodlamalarını bulan fonksiyon
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Resmi RGB formatına dönüştürme
        encodes = face_recognition.face_encodings(img)
        if len(encodes) > 0:  # Eğer resimde yüz kodlaması varsa
            encode = encodes[0]
            encodeList.append(encode)
    return encodeList

# Katılım listesini güncelleyen fonksiyon
def markAttendance(name):
    # Dosya mevcut değilse oluştur ve başlık ekle
    if not os.path.exists('Attendance.csv'):
        with open('Attendance.csv', 'w') as f:
            f.writelines('Name,Time\n')
    
    now = datetime.now()
    dtString = now.strftime('%H:%M:%S')
    
    # Eğer isim zaten listedeyse tekrar eklemeyelim
    if name not in attendance_set:
        with open('Attendance.csv', 'a') as f:
            f.writelines(f'\n{name},{dtString}')
        attendance_set.add(name)

# Yüz kodlamalarını bul
encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)  # Resmi %25 boyutuna küçültme
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)  # Resmi RGB formatına dönüştürme
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
    
    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)
        
        if faceDis[matchIndex] < 0.50:  # Eğer en yakın yüzün uzaklığı 0.50'den küçükse
            name = classNames[matchIndex].upper()
        else:
            name = 'Unknown'
        
        markAttendance(name)
        
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Yüz çevresine dikdörtgen çizme
        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)  # İsim kutusunu doldurma
        cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)  # İsmi yazma
    
    cv2.imshow('Webcam', img)

    # 'q' tuşuna basıldığında döngüyü ve programı durdurma
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # 'x' tuşuna basıldığında Attendance.csv dosyasını temizleme
    if cv2.waitKey(1) & 0xFF == ord('x'):
        if os.path.exists('Attendance.csv'):
            os.remove('Attendance.csv')
            attendance_set.clear()  # attendance_set'i temizleme
            print("Attendance.csv dosyası temizlendi.")
        else:
            print("Attendance.csv dosyası mevcut değil.")
    
cap.release()  # Kamerayı serbest bırakma
cv2.destroyAllWindows()  # Tüm pencereleri kapatma

# Attendance.csv dosyasını gösterme
if os.path.exists('Attendance.csv'):
    attendance_df = pd.read_csv('Attendance.csv')
    print(attendance_df)
else:
    print("Attendance.csv dosyası mevcut değil.")
"""
#BİLİNMEYEN KİŞİYİ INPUT AL VE KAYDET VEYA 5 SN SONRA DEVAM ET VE GÜNCEL SON HALİ
#Ama HATALI donuyor kamera
"""
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime, timedelta
import pandas as pd

# 'ImagesAttendance' klasöründeki resimlerin yolları ve isimleri
path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
    print(classNames)

# Kaydedilen katılım bilgilerini tutmak için set kullanılacak
attendance_set = set()

# Resimlerin yüz tanıma kodlamalarını bulan fonksiyon
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Resmi RGB formatına dönüştürme
        encodes = face_recognition.face_encodings(img)
        if len(encodes) > 0:  # Eğer resimde yüz kodlaması varsa
            encode = encodes[0]
            encodeList.append(encode)
    return encodeList

# Katılım listesini güncelleyen fonksiyon
def markAttendance(name):
    # Dosya mevcut değilse oluştur ve başlık ekle
    if not os.path.exists('Attendance.csv'):
        with open('Attendance.csv', 'w') as f:
            f.writelines('Name,Time\n')
    
    now = datetime.now()
    dtString = now.strftime('%H:%M:%S')
    
    # Eğer isim zaten listedeyse tekrar eklemeyelim
    if name not in attendance_set:
        with open('Attendance.csv', 'a') as f:
            f.writelines(f'\n{name},{dtString}')
        attendance_set.add(name)

# Yüz kodlamalarını bul
encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)
start_time = datetime.now()

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)  # Resmi %25 boyutuna küçültme
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)  # Resmi RGB formatına dönüştürme
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
    
    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)
        
        if faceDis[matchIndex] < 0.50:  # Eğer en yakın yüzün uzaklığı 0.50'den küçükse
            name = classNames[matchIndex].upper()
        else:
            if (datetime.now() - start_time) > timedelta(seconds=5):  # 5 saniyeden fazla süre geçtiyse
                name = 'Unknown'
            else:
                # İlk 5 saniye içinde isim girilmesini bekleyelim
                cv2.putText(img, "Enter name:", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.imshow('Webcam', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                continue
        
        if name == 'Unknown':
            # Unknown olarak tanınan kişinin ismini input olarak al
            cv2.putText(img, "Enter name:", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow('Webcam', img)
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                break
            elif key & 0xFF == ord('x'):
                if os.path.exists('Attendance.csv'):
                    os.remove('Attendance.csv')
                    attendance_set.clear()  # attendance_set'i temizleme
                    print("Attendance.csv dosyası temizlendi.")
                else:
                    print("Attendance.csv dosyası mevcut değil.")
            else:
                name = input("Enter the name of the unknown person: ")
                if name:
                    # Yeni kişiyi tanımlama ve kaydetme
                    cv2.imwrite(f"{path}/{name}.jpg", img)
                    classNames.append(name)
                    encodeListKnown = findEncodings(images + [img])  # Yeni resmi ekleyerek yeniden kodlamaları bulma
                    markAttendance(name)
                else:
                    name = 'Unknown'
                    markAttendance(name)
        
        markAttendance(name)
        
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Yüz çevresine dikdörtgen çizme
        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)  # İsim kutusunu doldurma
        cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)  # İsmi yazma
    
    cv2.imshow('Webcam', img)

    # 'q' tuşuna basıldığında döngüyü ve programı durdurma
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # 'x' tuşuna basıldığında Attendance.csv dosyasını temizleme
    if cv2.waitKey(1) & 0xFF == ord('x'):
        if os.path.exists('Attendance.csv'):
            os.remove('Attendance.csv')
            attendance_set.clear()  # attendance_set'i temizleme
            print("Attendance.csv dosyası temizlendi.")
        else:
            print("Attendance.csv dosyası mevcut değil.")
    
cap.release()  # Kamerayı serbest bırakma
cv2.destroyAllWindows()  # Tüm pencereleri kapatma

# Attendance.csv dosyasını gösterme
if os.path.exists('Attendance.csv'):
    attendance_df = pd.read_csv('Attendance.csv')
    print(attendance_df)
else:
    print("Attendance.csv dosyası mevcut değil.")"""
