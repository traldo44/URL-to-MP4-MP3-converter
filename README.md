# URL to MP4/MP3 Converter

Bu program, verilen URL'leri yüksek kalitede MP4 veya MP3 formatına dönüştüren bir Python uygulamasıdır.

## Özellikler

- **Çoklu Format Desteği**: MP4 (video + ses) ve MP3 (sadece ses) formatlarını destekler
- **Yüksek Kalite**: En yüksek çözünürlükte indirme (1080p, 720p, 480p seçenekleri)
- **Kullanıcı Dostu Arayüz**: Tkinter tabanlı modern GUI
- **Çoklu Platform**: Windows, macOS ve Linux desteği
- **Executable**: Tek dosya olarak çalıştırılabilir .exe dosyası

## Kurulum

### Geliştirme Ortamı için

1. Python 3.8+ yükleyin
2. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

3. Programı çalıştırın:
   ```bash
   python converter.py
   ```

### Executable Oluşturma

1. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

2. Executable'ı oluşturun:
   ```bash
   python build_exe.py
   ```

3. Oluşturulan `dist/URLConverter.exe` dosyasını çalıştırın

## Kullanım

1. Programı açın
2. Dönüştürmek istediğiniz URL'yi girin
3. Format seçin (MP4 veya MP3)
4. Kalite seçin (En İyi, 1080p, 720p, 480p)
5. Çıktı klasörünü seçin
6. "Download" butonuna tıklayın

## Desteklenen Platformlar

- YouTube
- Vimeo
- Facebook
- Twitter
- Instagram
- Ve daha fazlası (yt-dlp desteklediği tüm platformlar)

## Gereksinimler

- Python 3.8+
- yt-dlp
- tkinter (Python ile birlikte gelir)
- Pillow
- PyInstaller (executable oluşturmak için)

## Sorun Giderme

- **FFmpeg hatası**: FFmpeg'in sisteminizde yüklü olduğundan emin olun
- **İndirme hatası**: URL'nin geçerli olduğundan ve internet bağlantınızın çalıştığından emin olun
- **Kalite sorunu**: Seçilen kalite mevcut değilse, program otomatik olarak en yüksek mevcut kaliteyi seçer

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

