# URL to MP4/MP3 Converter

Video ve ses bağlantılarını MP4 veya MP3 olarak indiren masaüstü uygulaması. Python, Tkinter ve yt-dlp ile geliştirildi; Windows için tek dosyalık `.exe` olarak paketlenebilir.

[English](#english)

## Özellikler

- **MP4:** 1080p odaklı altı kalite seçeneği. Seçilen kalite yoksa uygun en iyi sürüm denenir.
- **MP3:** 64 ile 320 kbps arasında altı kalite seçeneği.
- **İlerleme takibi:** İndirme yüzdesi ve hız gösterimi.
- **Otomatik FFmpeg:** Sistemde bulunamazsa uygulama kendisi indirir.
- **Yeniden deneme:** Bağlantı hatalarında indirme otomatik tekrarlanır.
- **Kalıcı ayarlar:** Seçtiğiniz indirme klasörü hatırlanır.

## Kurulum

Python 3.8 veya üzeri gerekir.

```bash
git clone https://github.com/traldo44/URL-to-MP4-MP3-converter.git
cd URL-to-MP4-MP3-converter
pip install -r requirements.txt
python converter.py
```

Video siteleri sık değiştiği için indirme çalışmazsa yt-dlp'yi güncelleyin:

```bash
pip install -U yt-dlp
```

### Windows için .exe oluşturma

```bash
python build_exe.py
```

Çıktı `dist/URLConverter.exe` dosyasıdır.

## Kullanım

1. Uygulamayı açın ve bağlantıyı yapıştırın.
2. MP4 veya MP3 biçimini seçin.
3. Kaliteyi ve indirme klasörünü seçin.
4. **DOWNLOAD** düğmesine basın.

yt-dlp'nin desteklediği siteler kullanılabilir: [desteklenen siteler](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).

## Sorun giderme

| Sorun | Çözüm |
| --- | --- |
| SSL veya bağlantı hatası | VPN, vekil sunucu ve güvenlik duvarı ayarlarını kontrol edin. |
| İndirme başlamıyor | Bağlantının geçerli ve bölgenizde erişilebilir olduğunu doğrulayın, yt-dlp'yi güncelleyin. |
| FFmpeg indirilemiyor | İnternet bağlantınızı kontrol edin veya FFmpeg'i kendiniz kurun. |

Yalnızca indirme hakkına sahip olduğunuz içerikler için kullanın.

## English

A desktop app that downloads video and audio links as MP4 or MP3, built with Python, Tkinter and yt-dlp. It offers quality presets for both formats, shows progress, downloads FFmpeg when it is missing and remembers your output folder.

```bash
pip install -r requirements.txt
python converter.py
```

Run `python build_exe.py` to build a single-file Windows executable. Only download content you have the right to use.

## Lisans

MIT

**Geliştirici:** Mert Aydıngüneş
