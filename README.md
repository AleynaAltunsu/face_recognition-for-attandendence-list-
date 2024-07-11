# face_recognition-for-attandendence-list-

ÖNEMLİ NOT: koda dair tüm açıklamalar ve versiyonlar yorum satırları içinde açıklanmıştır.

---

## Yüz Tanıma ve Yoklama Uygulaması

Bu proje, Python ve OpenCV kütüphaneleri kullanılarak geliştirilmiş bir yüz tanıma ve yoklama uygulamasıdır. Kullanıcılar, belirli kişilerin yüzlerini tanıyan ve katılımı kaydeden bir sistem üzerinde çalışabilirler.

### Özellikler

- **Yüz Tanıma:** Uygulama, kaydedilmiş resimlerdeki yüzleri tanıyabilir ve ekranda işaretleyebilir.
- **Yoklama Kaydı:** Tanınan kişilerin katılım zamanlarını otomatik olarak kaydeder.
- **Görüntü İşleme:** OpenCV kullanılarak görüntü işleme teknikleri uygulanır.

### Nasıl Kullanılır

1. **Gereksinimler**
   - Python 3.x
   - OpenCV ve face_recognition kütüphaneleri (`pip install opencv-python face-recognition`)

2. **Başlatma**
   - Terminal veya komut istemcisinde proje dizinine gidin.
   - `python main.py` komutunu çalıştırarak uygulamayı başlatın.

3. **Yüz Tanıma**
   - Kameranızı veya bir video dosyasını kullanarak yüz tanımayı test edin.
   - Tanınan yüzler otomatik olarak işaretlenecek ve ekranda adları gösterilecektir.

4. **Yoklama Kaydı**
   - Tanılan kişilerin adları ve katılım zamanları `Attendance.csv` dosyasına kaydedilecektir.
   - Katılım listesini `Attendance.csv` dosyasından takip edebilirsiniz.

### Örnek Kod Parçaları

```python
import cv2
import face_recognition
import numpy as np
import pandas as pd
from datetime import datetime

# Gerekli fonksiyonlar buraya eklenecek
```

### Katkıda Bulunma

- Bu proje açık kaynaklıdır ve her türlü katkıya açıktır.
- Geliştirme sürecine katılmak için GitHub profilimi ziyaret edebilirsiniz: (https://github.com/AleynaAltunsu).

  
