# STOP Sign Detector

OpenCV kullanarak görsellerdeki STOP tabelalarını tespit eden basit bir Python projesi.

## Gereksinimler

```bash
pip install opencv-python numpy
```

## Kullanım

1. `stop_sign_dataset/` klasörüne test edilecek görselleri koyun
2. Scripti çalıştırın:

```bash
python stop_sign_detector.py
```

3. Sonuçlar `detection_results/` klasöründe kaydedilir

## Nasıl Çalışır

- HSV renk uzayında kırmızı bölgeleri tespit eder
- Morfolojik operasyonlarla gürültüyü temizler
- Kare benzeri şekilleri STOP tabelası olarak işaretler
- Tespit edilen tabelaların merkez koordinatlarını yazdırır