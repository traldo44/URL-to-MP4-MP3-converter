# 🎬 All Video Downloader - Kullanım Talimatları

## ⚠️ Windows SmartScreen Uyarısı Çözümü

Executable'ı ilk kez çalıştırdığınızda Windows SmartScreen uyarısı çıkabilir. Bu normal bir durumdur ve güvenlik önlemidir.

### 🔧 Çözüm Adımları:

1. **"Ek bilgi" (More info) linkine tıklayın**
2. **"Yine de çalıştır" (Run anyway) butonuna tıklayın**
3. Program açılacaktır

### 📋 Alternatif Çözümler:

#### Yöntem 1: Sağ Tık ile Çalıştırma
- Executable'a **sağ tıklayın**
- **"Yönetici olarak çalıştır"** seçin
- Uyarı çıkmayacaktır

#### Yöntem 2: Windows Defender'dan İstisna Ekleme
1. **Windows Güvenlik** açın
2. **Virüs ve tehdit koruması** → **Ayarları yönet**
3. **İstisnalar** → **İstisna ekle**
4. **Dosya** seçin ve `URLConverter.exe` dosyasını seçin

#### Yöntem 3: PowerShell ile Çalıştırma
```powershell
# Executable'ın bulunduğu klasörde:
Unblock-File -Path "URLConverter.exe"
.\URLConverter.exe
```

## 🎯 Program Özellikleri

### ✨ Ana Özellikler:
- **1920x1080 Full HD** video indirme
- **MP3 audio** indirme (320k kalite)
- **Sağ tık yapıştır** desteği
- **Kırmızı çerçeveli** seçim sistemi
- **Modern arayüz** tasarımı
- **Klasör seçimi** ile kolay indirme

### 🎬 Desteklenen Platformlar:
- ✅ YouTube
- ✅ Vimeo
- ✅ Facebook
- ✅ Twitter
- ✅ Instagram
- ✅ Ve daha fazlası...

### 📁 Sistem Gereksinimleri:
- **Windows 10/11** (64-bit)
- **İnternet bağlantısı**
- **Disk alanı** (video boyutuna göre)

## 🚀 Kullanım

1. **URL girin** - Video linkini yapıştırın
2. **Format seçin** - MP4 (video) veya MP3 (ses)
3. **Kalite seçin** - 1080p seçeneklerinden birini seçin
4. **Klasör seçin** - İndirme yerini belirleyin
5. **📥 DOWNLOAD** - İndirme başlar

## 🔧 Sorun Giderme

### Video İndirilmiyor:
- İnternet bağlantınızı kontrol edin
- URL'nin doğru olduğundan emin olun
- Antivirus programınızı geçici olarak kapatın

### Düşük Kalite:
- FFmpeg kurulumu yapın (opsiyonel)
- Daha yüksek kalite seçeneği seçin

### Program Açılmıyor:
- Windows Defender'dan istisna ekleyin
- Yönetici olarak çalıştırın

## 📞 Destek

**Geliştirici:** Mert Aydıngüneş  
**Versiyon:** 1.0.0  
**Tarih:** 2024

---

**Not:** Bu program tamamen güvenlidir ve sadece video indirme işlemi yapar. Hiçbir kişisel veri toplamaz veya göndermez.



