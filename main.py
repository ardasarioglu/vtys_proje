import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog, QMessageBox
from PyQt5.uic import loadUi
import sqlite3

# ==========================================
# 1. YENİ MÜŞTERİ EKLEME PENCERESİ SINIFI
# ==========================================
class YeniMusteriDialog(QDialog):
    def __init__(self):
        super(YeniMusteriDialog, self).__init__()
        loadUi("yeni_musteri_dialog.ui", self)
        
        self.ekleekleButton.clicked.connect(self.musteri_kaydet)
        self.ekleiptalButton.clicked.connect(self.close)

    def baglanti_kur(self):
        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()

    def musteri_kaydet(self):
        try:
            self.baglanti_kur()
            ad = self.ekleadLineEdit.text()
            soyad = self.eklesoyadLineEdit.text()
            eposta = self.ekleepostaLineEdit.text()
            telefon = self.ekletelefonLineEdit.text()
            adres = self.ekleadresLineEdit.text()
            dogum_tarihi = self.ekledogumtarihiDateEdit.date().toString("yyyy-MM-dd")
            ehliyet = self.ekleehliyetnoLineEdit.text()

            if not ad or not soyad or not ehliyet:
                QMessageBox.warning(self, "Eksik Bilgi", "Lütfen Ad, Soyad ve Ehliyet No alanlarını doldurunuz!")
                return

            sorgu = "INSERT INTO Musteriler (Ad, Soyad, Eposta, Telefon, Adres, DogumTarihi, EhliyetNo) VALUES (?, ?, ?, ?, ?, ?, ?)"
            self.cursor.execute(sorgu, (ad, soyad, eposta, telefon, adres, dogum_tarihi, ehliyet))
            self.conn.commit()
            
            QMessageBox.information(self, "Başarılı", "Müşteri sisteme başarıyla eklendi.")
            self.accept()

        except sqlite3.IntegrityError:
             QMessageBox.critical(self, "Hata", "Bu E-posta veya Ehliyet No zaten sistemde kayıtlı!")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Kayıt eklenirken hata oluştu: {e}")
        finally:
            if hasattr(self, 'conn'): self.conn.close()

# ==========================================
# 2. YENİ ARAÇ EKLEME PENCERESİ SINIFI (YENİ)
# ==========================================
class YeniAracDialog(QDialog):
    def __init__(self):
        super(YeniAracDialog, self).__init__()
        # Senin tasarladığın araç ekleme dosyasını yüklüyoruz
        loadUi("yeni_arac_dialog.ui", self)
        
        # Buton Bağlantıları
        self.aracekleekleButton.clicked.connect(self.arac_kaydet)
        self.aracekleiptalButton.clicked.connect(self.close)

    def baglanti_kur(self):
        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()

    def arac_kaydet(self):
        try:
            self.baglanti_kur()

            # Verileri Arayüzden Çek
            plaka = self.ekleplakaLineEdit.text().upper() # Plakayı otomatik büyük harf yap
            marka = self.eklemarkaLineEdit.text()
            model = self.eklemodelLineEdit.text()
            yil_text = self.ekleyilLineEdit.text()
            renk = self.eklerenkLineEdit.text()
            km_text = self.eklekilometreLineEdit.text()
            kira_text = self.eklekiraLineEdit.text()

            # --- KONTROLLER ---
            # 1. Boş Alan Kontrolü
            if not plaka or not marka or not model or not kira_text:
                QMessageBox.warning(self, "Eksik Bilgi", "Plaka, Marka, Model ve Kira Bedeli zorunludur!")
                return

            # 2. Sayısal Veri Kontrolü (Yıl, Km, Fiyat sayı olmalı)
            try:
                yil = int(yil_text)          # Yılı tam sayıya çevir
                km = int(km_text)            # Km'yi tam sayıya çevir
                kira = float(kira_text)      # Fiyatı ondalıklı sayıya çevir
            except ValueError:
                QMessageBox.warning(self, "Hatalı Giriş", "Lütfen Yıl, Kilometre ve Kira Bedeli alanlarına sadece sayı giriniz!")
                return

            # --- VERİTABANINA KAYIT ---
            # Durum varsayılan olarak 'Müsait' eklenir
            sorgu = """
                INSERT INTO Araclar (Plaka, Marka, Model, Yil, Renk, Kilometre, GunlukKiraBedeli, Durum)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(sorgu, (plaka, marka, model, yil, renk, km, kira, "Müsait"))
            self.conn.commit()

            QMessageBox.information(self, "Başarılı", "Araç envantere eklendi.")
            self.accept()

        except sqlite3.IntegrityError:
            QMessageBox.critical(self, "Hata", "Bu Plaka zaten sistemde kayıtlı!")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Araç eklenirken hata oluştu: {e}")
        finally:
             if hasattr(self, 'conn'): self.conn.close()


# ==========================================
# 3. ANA PENCERE SINIFI
# ==========================================
class AracKiralamaApp(QMainWindow):
    def __init__(self):
        super(AracKiralamaApp, self).__init__()
        
        try:
            loadUi("main_window.ui", self)
        except FileNotFoundError:
            print("Hata: main_window.ui dosyası bulunamadı!")
            sys.exit(1)

        self.baglanti_kur()
        
        # Başlangıç Listeleme
        self.musterileri_listele() 
        self.araclari_listele()    

        # Arama Sinyalleri
        self.musteriaramaLineEdit.textChanged.connect(self.musterileri_listele)
        self.aracaraLineEdit.textChanged.connect(self.araclari_listele)
        
        # --- BUTON BAĞLANTILARI ---
        # Müşteri Ekle Butonu
        self.musteriyenimusteriButton.clicked.connect(self.yeni_musteri_ekle_penceresi)
        
        # Araç Ekle Butonu (Bunu main_window.ui'da oluşturmuş olman gerekiyor)
        # İsmini 'aracyeniaracButton' olarak varsaydım.
        try:
            self.aracekleButton.clicked.connect(self.yeni_arac_ekle_penceresi)
        except AttributeError:
            print("Uyarı: main_window.ui içinde 'aracyeniaracButton' isminde bir buton bulunamadı!")

    def baglanti_kur(self):
        try:
            self.conn = sqlite3.connect("database.db")
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"Veritabanı hatası: {e}")

    # --- PENCERE AÇMA FONKSİYONLARI ---
    def yeni_musteri_ekle_penceresi(self):
        dialog = YeniMusteriDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.musterileri_listele()

    def yeni_arac_ekle_penceresi(self):
        dialog = YeniAracDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.araclari_listele()

    # --- LİSTELEME FONKSİYONLARI ---
    def musterileri_listele(self):
        try:
            arama_metni = self.musteriaramaLineEdit.text()
            basliklar = ["ID", "Ad", "Soyad", "E-Posta", "Telefon", "Adres", "Doğum Tarihi", "Ehliyet No"]
            self.musterilerTableWidget.setColumnCount(len(basliklar)) 
            self.musterilerTableWidget.setHorizontalHeaderLabels(basliklar)

            if arama_metni == "":
                sorgu = "SELECT * FROM Musteriler"
                self.cursor.execute(sorgu)
            else:
                sorgu = "SELECT * FROM Musteriler WHERE Ad LIKE ? OR Soyad LIKE ? OR EhliyetNo LIKE ?"
                filtre = f"%{arama_metni}%"
                self.cursor.execute(sorgu, (filtre, filtre, filtre))

            kayitlar = self.cursor.fetchall() 
            self.musterilerTableWidget.setRowCount(0)
            for satir_indeks, satir_verisi in enumerate(kayitlar):
                self.musterilerTableWidget.insertRow(satir_indeks)
                for sutun_indeks, veri in enumerate(satir_verisi):
                    self.musterilerTableWidget.setItem(satir_indeks, sutun_indeks, QTableWidgetItem(str(veri)))
        except Exception as e:
            print(f"Müşteri Listeleme hatası: {e}")

    def araclari_listele(self):
        try:
            arama_metni = self.aracaraLineEdit.text()
            basliklar = ["ID","Plaka","Marka","Model","Yıl","Renk","Kilometre","Günlük Kira Bedeli","Durum"]
            self.araclarTableWidget.setColumnCount(len(basliklar))
            self.araclarTableWidget.setHorizontalHeaderLabels(basliklar)

            if arama_metni == "":
                sorgu = "SELECT * FROM Araclar"
                self.cursor.execute(sorgu)
            else:
                sorgu = "SELECT * FROM Araclar WHERE Plaka LIKE ? OR Marka LIKE ? OR Model LIKE ?"
                filtre = f"%{arama_metni}%"
                self.cursor.execute(sorgu, (filtre, filtre, filtre))

            kayitlar = self.cursor.fetchall()
            self.araclarTableWidget.setRowCount(0)
            for satir_indeks, satir_verisi in enumerate(kayitlar):
                self.araclarTableWidget.insertRow(satir_indeks)
                for sutun_indeks, veri in enumerate(satir_verisi):
                    self.araclarTableWidget.setItem(satir_indeks, sutun_indeks, QTableWidgetItem(str(veri)))
        except Exception as e:
            print(f"Araç Listeleme hatası: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = AracKiralamaApp()
    pencere.show()
    sys.exit(app.exec_())