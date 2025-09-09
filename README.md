# 🎬 URL to MP4/MP3 Converter

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

---

## 🇺🇸 English

This program is a modern Python application that converts given URLs to high-quality MP4 or MP3 format.

### ✨ Features

- **🎥 Multi-Format Support**: Supports MP4 (video + audio) and MP3 (audio only) formats
- **📺 High Quality**: Download in highest resolution (1080p, 720p, 480p options)
- **🎨 Modern Interface**: Tkinter-based glassmorphic GUI design
- **🖥️ Multi-Platform**: Windows, macOS and Linux support
- **📦 Executable**: Single file runnable .exe file
- **📊 Progress Tracking**: Download percentage and speed display
- **💾 Persistent Settings**: Selected download path is automatically saved
- **🔴 Visual Feedback**: Selected buttons have red borders

### 🚀 Installation

#### For Development Environment

1. Install Python 3.8+
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the program:
   ```bash
   python converter.py
   ```

#### Creating Executable

1. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Create executable:
   ```bash
   python build_exe.py
   ```

3. Run the created `dist/URLConverter.exe` file

### 📖 Usage

1. Open the program
2. Enter the URL you want to convert
3. Select format (MP4 or MP3)
4. Select quality (1080p, 720p, 480p options)
5. Select output folder (displayed in top right)
6. Click "📥 DOWNLOAD" button

### 🌐 Supported Platforms

- ✅ YouTube
- ✅ Vimeo
- ✅ Facebook
- ✅ Twitter
- ✅ Instagram
- ✅ TikTok
- ✅ And more (all platforms supported by yt-dlp)

### 📋 Requirements

- Python 3.8+
- yt-dlp
- tkinter (comes with Python)
- Pillow
- PyInstaller (for creating executable)

### 🔧 Troubleshooting

#### Common Issues and Solutions

**SSL Connection Errors:**
- The program now includes automatic SSL retry mechanism
- If you still get SSL errors, try running as administrator
- Check your antivirus/firewall settings
- Disable VPN temporarily if you're using one

**Download Errors:**
- Make sure the URL is valid and your internet connection is working
- The program will automatically retry failed downloads up to 3 times
- Check if the video is available in your region

**FFmpeg Issues:**
- FFmpeg will be downloaded automatically if not found
- If download fails, check your internet connection
- Temporarily disable antivirus during FFmpeg download

**Quality Issues:**
- If selected quality is not available, the program automatically selects the highest available quality
- Try different quality options if download fails


---

## 🇹🇷 Türkçe

Bu program, verilen URL'leri yüksek kalitede MP4 veya MP3 formatına dönüştüren modern bir Python uygulamasıdır.

### ✨ Özellikler

- **🎥 Çoklu Format Desteği**: MP4 (video + ses) ve MP3 (sadece ses) formatlarını destekler
- **📺 Yüksek Kalite**: En yüksek çözünürlükte indirme (1080p, 720p, 480p seçenekleri)
- **🎨 Modern Arayüz**: Tkinter tabanlı glassmorphic GUI tasarımı
- **🖥️ Çoklu Platform**: Windows, macOS ve Linux desteği
- **📦 Executable**: Tek dosya olarak çalıştırılabilir .exe dosyası
- **📊 Progress Tracking**: İndirme yüzdesi ve hız gösterimi
- **💾 Kalıcı Ayarlar**: Seçilen indirme yolu otomatik kaydedilir
- **🔴 Görsel Geri Bildirim**: Seçili butonlar kırmızı çerçeveli

### 🚀 Kurulum

#### Geliştirme Ortamı için

1. Python 3.8+ yükleyin
2. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

3. Programı çalıştırın:
   ```bash
   python converter.py
   ```

#### Executable Oluşturma

1. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

2. Executable'ı oluşturun:
   ```bash
   python build_exe.py
   ```

3. Oluşturulan `dist/URLConverter.exe` dosyasını çalıştırın

### 📖 Kullanım

1. Programı açın
2. Dönüştürmek istediğiniz URL'yi girin
3. Format seçin (MP4 veya MP3)
4. Kalite seçin (1080p, 720p, 480p seçenekleri)
5. Çıktı klasörünü seçin (sağ üstte görünür)
6. "📥 DOWNLOAD" butonuna tıklayın

### 🌐 Desteklenen Platformlar

- ✅ YouTube
- ✅ Vimeo
- ✅ Facebook
- ✅ Twitter
- ✅ Instagram
- ✅ TikTok
- ✅ Ve daha fazlası (yt-dlp desteklediği tüm platformlar)

### 📋 Gereksinimler

- Python 3.8+
- yt-dlp
- tkinter (Python ile birlikte gelir)
- Pillow
- PyInstaller (executable oluşturmak için)

### 🔧 Sorun Giderme

#### Yaygın Sorunlar ve Çözümleri

**SSL Bağlantı Hataları:**
- Program artık otomatik SSL yeniden deneme mekanizması içeriyor
- Hala SSL hatası alıyorsanız, programı yönetici olarak çalıştırmayı deneyin
- Antivirus/firewall ayarlarınızı kontrol edin
- VPN kullanıyorsanız geçici olarak kapatmayı deneyin

**İndirme Hataları:**
- URL'nin geçerli olduğundan ve internet bağlantınızın çalıştığından emin olun
- Program başarısız indirmeleri otomatik olarak 3 kez yeniden deneyecek
- Videoyu bölgenizde mevcut olup olmadığını kontrol edin

**FFmpeg Sorunları:**
- FFmpeg bulunamazsa otomatik olarak indirilecek
- İndirme başarısız olursa internet bağlantınızı kontrol edin
- FFmpeg indirme sırasında antivirus programınızı geçici olarak kapatın

**Kalite Sorunları:**
- Seçilen kalite mevcut değilse, program otomatik olarak en yüksek mevcut kaliteyi seçer
- İndirme başarısız olursa farklı kalite seçeneklerini deneyin


---

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Developer

**Mert Aydıngüneş**  
**Version:** 1.0.0  
**Date:** 2024

