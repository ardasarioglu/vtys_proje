import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDate 
import sqlite3
from datetime import datetime

# ==========================================
# 1. YENİ MÜŞTERİ EKLEME PENCERESİ
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
# 2. MÜŞTERİ GÜNCELLEME PENCERESİ
# ==========================================
class GuncelleMusteriDialog(QDialog):
    def __init__(self):
        super(GuncelleMusteriDialog, self).__init__()
        loadUi("guncelle_musteri_dialog.ui", self)
        self.guncelleguncelleButton.clicked.connect(self.guncelle_kaydet)
        self.guncelleiptalButton.clicked.connect(self.close)
        self.musteri_id = None

    def baglanti_kur(self):
        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()

    def bilgileri_doldur(self, kayit_verisi):
        self.musteri_id = kayit_verisi[0]
        self.guncelleadLineEdit.setText(kayit_verisi[1])
        self.guncellesoyadLineEdit.setText(kayit_verisi[2])
        self.guncelleepostaLineEdit.setText(kayit_verisi[3])
        self.guncelletelefonLineEdit.setText(kayit_verisi[4])
        self.guncelleadresLineEdit.setText(kayit_verisi[5])
        tarih_string = kayit_verisi[6]
        q_tarih = QDate.fromString(tarih_string, "yyyy-MM-dd")
        self.guncelledogumtarihiDateEdit.setDate(q_tarih)
        self.guncelleehliyetnoLineEdit.setText(kayit_verisi[7])

    def guncelle_kaydet(self):
        try:
            self.baglanti_kur()
            ad = self.guncelleadLineEdit.text()
            soyad = self.guncellesoyadLineEdit.text()
            eposta = self.guncelleepostaLineEdit.text()
            telefon = self.guncelletelefonLineEdit.text()
            adres = self.guncelleadresLineEdit.text()
            dogum_tarihi = self.guncelledogumtarihiDateEdit.date().toString("yyyy-MM-dd")
            ehliyet = self.guncelleehliyetnoLineEdit.text()

            if not ad or not soyad or not ehliyet:
                QMessageBox.warning(self, "Eksik Bilgi", "Ad, Soyad ve Ehliyet alanları boş bırakılamaz!")
                return

            sorgu = "UPDATE Musteriler SET Ad=?, Soyad=?, Eposta=?, Telefon=?, Adres=?, DogumTarihi=?, EhliyetNo=? WHERE MusteriID=?"
            self.cursor.execute(sorgu, (ad, soyad, eposta, telefon, adres, dogum_tarihi, ehliyet, self.musteri_id))
            self.conn.commit()
            QMessageBox.information(self, "Başarılı", "Müşteri bilgileri güncellendi.")
            self.accept()
        except sqlite3.IntegrityError:
            QMessageBox.critical(self, "Hata", "Bu E-posta veya Ehliyet No başka bir müşteriye ait!")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Güncelleme hatası: {e}")
        finally:
            if hasattr(self, 'conn'): self.conn.close()

# ==========================================
# 3. MÜŞTERİ FİLTRELEME PENCERESİ
# ==========================================
class MusteriFiltreDialog(QDialog):
    def __init__(self):
        super(MusteriFiltreDialog, self).__init__()
        loadUi("musteri_filtre_dialog.ui", self)
        self.date_filtre_baslangic.setDate(QDate(1950, 1, 1))
        self.date_filtre_bitis.setDate(QDate.currentDate())
        self.btn_filtre_uygula.clicked.connect(self.accept)
        self.btn_filtre_iptal.clicked.connect(self.close)

# ==========================================
# 4. YENİ ARAÇ EKLEME PENCERESİ
# ==========================================
class YeniAracDialog(QDialog):
    def __init__(self):
        super(YeniAracDialog, self).__init__()
        loadUi("yeni_arac_dialog.ui", self)
        self.aracekleekleButton.clicked.connect(self.arac_kaydet)
        self.aracekleiptalButton.clicked.connect(self.close)

    def baglanti_kur(self):
        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()

    def arac_kaydet(self):
        try:
            self.baglanti_kur()
            plaka = self.ekleplakaLineEdit.text().upper() 
            marka = self.eklemarkaLineEdit.text()
            model = self.eklemodelLineEdit.text()
            yil_text = self.ekleyilLineEdit.text()
            renk = self.eklerenkLineEdit.text()
            km_text = self.eklekilometreLineEdit.text()
            kira_text = self.eklekiraLineEdit.text()

            if not plaka or not marka or not model or not kira_text:
                QMessageBox.warning(self, "Eksik Bilgi", "Plaka, Marka, Model ve Kira Bedeli zorunludur!")
                return
            try:
                yil = int(yil_text)
                km = int(km_text) 
                kira = float(kira_text)
            except ValueError:
                QMessageBox.warning(self, "Hatalı Giriş", "Lütfen sayısal alanları kontrol ediniz!")
                return

            sorgu = "INSERT INTO Araclar (Plaka, Marka, Model, Yil, Renk, Kilometre, GunlukKiraBedeli, Durum) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
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
# 5. ARAÇ GÜNCELLEME PENCERESİ
# ==========================================
class GuncelleAracDialog(QDialog):
    def __init__(self):
        super(GuncelleAracDialog, self).__init__()
        loadUi("guncelle_arac_dialog.ui", self)
        self.aracguncelleguncelleButton.clicked.connect(self.guncelle_kaydet)
        self.aracguncelleiptalButton.clicked.connect(self.close)
        self.arac_id = None

    def baglanti_kur(self):
        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()

    def bilgileri_doldur(self, kayit_verisi):
        self.arac_id = kayit_verisi[0]
        self.guncelleplakaLineEdit.setText(kayit_verisi[1])
        self.guncellemarkaLineEdit.setText(kayit_verisi[2])
        self.guncellemodelLineEdit.setText(kayit_verisi[3])
        self.guncelleyilLineEdit.setText(kayit_verisi[4])
        self.guncellerenkLineEdit.setText(kayit_verisi[5])
        self.guncellekilometreLineEdit.setText(kayit_verisi[6])
        self.guncellekiraLineEdit.setText(kayit_verisi[7])
        mevcut_durum = kayit_verisi[8]
        self.aracguncelledurumComboBox.setCurrentText(mevcut_durum)

    def guncelle_kaydet(self):
        try:
            self.baglanti_kur()
            plaka = self.guncelleplakaLineEdit.text().upper()
            marka = self.guncellemarkaLineEdit.text()
            model = self.guncellemodelLineEdit.text()
            yil_text = self.guncelleyilLineEdit.text()
            renk = self.guncellerenkLineEdit.text()
            km_text = self.guncellekilometreLineEdit.text()
            kira_text = self.guncellekiraLineEdit.text()
            durum = self.aracguncelledurumComboBox.currentText()

            if not plaka or not marka or not model or not kira_text:
                 QMessageBox.warning(self, "Eksik Bilgi", "Plaka, Marka, Model ve Kira alanları zorunludur!")
                 return
            try:
                yil = int(yil_text)
                km = int(km_text)
                kira = float(kira_text)
            except ValueError:
                QMessageBox.warning(self, "Hata", "Yıl, Kilometre ve Kira Bedeli sayısal olmalıdır!")
                return

            sorgu = "UPDATE Araclar SET Plaka=?, Marka=?, Model=?, Yil=?, Renk=?, Kilometre=?, GunlukKiraBedeli=?, Durum=? WHERE AracID=?"
            self.cursor.execute(sorgu, (plaka, marka, model, yil, renk, km, kira, durum, self.arac_id))
            self.conn.commit()
            QMessageBox.information(self, "Başarılı", "Araç bilgileri güncellendi.")
            self.accept()
        except sqlite3.IntegrityError:
            QMessageBox.critical(self, "Hata", "Bu Plaka zaten sistemde kayıtlı!")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Güncelleme hatası: {e}")
        finally:
            if hasattr(self, 'conn'): self.conn.close()

# ==========================================
# 6. ARAÇ FİLTRELEME PENCERESİ
# ==========================================
class AracFiltreDialog(QDialog):
    def __init__(self):
        super(AracFiltreDialog, self).__init__()
        loadUi("arac_filtre_dialog.ui", self)
        
        self.spin_filtre_fiyat_min.setMaximum(1000000.00)
        self.spin_filtre_fiyat_max.setMaximum(1000000.00)
        self.spin_filtre_fiyat_max.setValue(100000.00)

        self.spin_filtre_yil_min.setRange(1900, 2100)
        self.spin_filtre_yil_min.setValue(1990)

        self.spin_filtre_yil_max.setRange(1900, 2100)
        self.spin_filtre_yil_max.setValue(2030)

        self.spin_filtre_kilometre_min.setMaximum(1000000) 
        self.spin_filtre_kilometre_max.setMaximum(1000000)
        self.spin_filtre_kilometre_max.setValue(1000000)

        self.btn_arac_filtre_uygula.clicked.connect(self.accept)
        self.btn_arac_filtre_iptal.clicked.connect(self.close)


# ==========================================
# 7. ANA PENCERE SINIFI
# ==========================================
class AracKiralamaApp(QMainWindow):
    def __init__(self):
        super(AracKiralamaApp, self).__init__()
        loadUi("main_window.ui", self)
        self.baglanti_kur()
        
        # --- BAŞLANGIÇ YÜKLEMELERİ ---
        self.musterileri_listele() 
        self.araclari_listele()
        self.kiralamalari_yukle()
        self.raporlari_yukle()

        # --- SİNYALLER (Müşteri & Araç) ---
        self.musteriaramaLineEdit.textChanged.connect(self.musterileri_listele)
        self.aracaraLineEdit.textChanged.connect(self.araclari_listele)
        
        self.musteriyenimusteriButton.clicked.connect(self.yeni_musteri_ekle_penceresi)
        self.musterisilButton.clicked.connect(self.musteri_sil)
        self.musteriguncelleButton.clicked.connect(self.musteri_guncelle_penceresi)
        self.musteritemizleButton.clicked.connect(self.musteri_filtre_temizle)
        self.musterifiltreButton.clicked.connect(self.musteri_filtre_penceresi)

        try:
            self.aracyeniaracButton.clicked.connect(self.yeni_arac_ekle_penceresi)
        except AttributeError:
            pass
        self.aracsilButton.clicked.connect(self.arac_sil)
        self.aracguncelleButton.clicked.connect(self.arac_guncelle_penceresi)
        self.aractemizleButton.clicked.connect(self.arac_filtre_temizle)
        try:
            self.aracfiltreButton.clicked.connect(self.arac_filtre_penceresi)
        except AttributeError:
            pass

        # --- SİNYALLER (Kiralama İşlemleri) ---
        self.kirala_pushbutton.clicked.connect(self.arac_kirala)
        self.teslimal_pushbutton.clicked.connect(self.arac_teslim_al)
        
        self.kiralama_arac_combobox.currentIndexChanged.connect(self.fiyat_hesapla)
        self.kiralama_baslangic_date.dateChanged.connect(self.fiyat_hesapla)
        self.kiralama_bitis_date.dateChanged.connect(self.fiyat_hesapla)
        
        self.teslimal_araclar_combobox.currentIndexChanged.connect(self.teslim_ekrani_guncelle)
        self.teslimal_teslimalmatarihi_date.dateChanged.connect(self.teslim_hesapla)

        self.kiralama_baslangic_date.setDate(QDate.currentDate())
        self.kiralama_bitis_date.setDate(QDate.currentDate())
        self.teslimal_teslimalmatarihi_date.setDate(QDate.currentDate())
        
        # Sekme değiştiğinde raporları yenile
        self.tabWidget.currentChanged.connect(self.sekme_degisti)


    def baglanti_kur(self):
        try:
            self.conn = sqlite3.connect("database.db")
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"Veritabanı hatası: {e}")

    def sekme_degisti(self, index):
        if index == 3: # Raporlar sekmesi
            self.raporlari_yukle()

    # ==========================================
    # --- RAPORLAR MODÜLÜ (GÜNCELLENDİ) ---
    # ==========================================
    def raporlari_yukle(self):
        self.rapor_ozetlerini_yukle()
        self.rapor_finansal_tablo_yukle()
        self.rapor_enler_tablolari_yukle()

    def rapor_ozetlerini_yukle(self):
        self.cursor.execute("SELECT COUNT(*) FROM Araclar")
        self.rapor_toplamarac_label.setText(str(self.cursor.fetchone()[0]))

        self.cursor.execute("SELECT COUNT(*) FROM Araclar WHERE Durum='Kirada'")
        self.rapor_kiradakiaraclar_label.setText(str(self.cursor.fetchone()[0]))

        self.cursor.execute("SELECT COUNT(*) FROM Araclar WHERE Durum='Bakımda'")
        self.rapor_bakimdakiaraclar_label.setText(str(self.cursor.fetchone()[0]))

        self.cursor.execute("SELECT COUNT(*) FROM Araclar WHERE Durum='Müsait'")
        self.rapor_musaitaraclar_label.setText(str(self.cursor.fetchone()[0]))

        self.cursor.execute("SELECT SUM(Miktar) FROM Odemeler")
        ciro = self.cursor.fetchone()[0]
        self.rapor_ciro_label.setText(f"{ciro:.2f} TL" if ciro else "0.00 TL")

    def rapor_finansal_tablo_yukle(self):
        sorgu = """
            SELECT O.OdemeTarihi, M.Ad || ' ' || M.Soyad, A.Plaka, O.OdemeTipi, O.Miktar
            FROM Odemeler O
            JOIN Kiralamalar K ON O.KiralamaID = K.KiralamaID
            JOIN Musteriler M ON K.MusteriID = M.MusteriID
            JOIN Araclar A ON K.AracID = A.AracID
            ORDER BY O.OdemeTarihi DESC
        """
        self.cursor.execute(sorgu)
        kayitlar = self.cursor.fetchall()
        
        self.rapor_finansalhareketler_table.setColumnCount(5)
        self.rapor_finansalhareketler_table.setHorizontalHeaderLabels(["Tarih", "Müşteri Adı", "Plaka", "Ödeme Tipi", "Tutar"])
        self.rapor_finansalhareketler_table.setRowCount(0)
        
        for satir, veri in enumerate(kayitlar):
            self.rapor_finansalhareketler_table.insertRow(satir)
            for sutun, deger in enumerate(veri):
                self.rapor_finansalhareketler_table.setItem(satir, sutun, QTableWidgetItem(str(deger)))

    def rapor_enler_tablolari_yukle(self):
        # NOT: Bu kodun çalışması için Designer'da tabloları 'QTableWidget' yapmış olmalısın.
        
        # 1. En Çok Kiralanan Araçlar
        sorgu_arac = """
            SELECT A.Plaka || ' - ' || A.Marka, COUNT(K.KiralamaID) as Sayi
            FROM Kiralamalar K
            JOIN Araclar A ON K.AracID = A.AracID
            GROUP BY K.AracID
            ORDER BY Sayi DESC
            LIMIT 5
        """
        self.cursor.execute(sorgu_arac)
        kayitlar = self.cursor.fetchall()
        
        self.rapor_enaraclar_table.setColumnCount(2)
        self.rapor_enaraclar_table.setHorizontalHeaderLabels(["Araç", "Kiralama Sayısı"])
        self.rapor_enaraclar_table.setRowCount(0)
        for s, v in enumerate(kayitlar):
            self.rapor_enaraclar_table.insertRow(s)
            self.rapor_enaraclar_table.setItem(s, 0, QTableWidgetItem(str(v[0])))
            self.rapor_enaraclar_table.setItem(s, 1, QTableWidgetItem(str(v[1])))

        # 2. En İyi Müşteriler (En Çok Para Harcayanlar)
        sorgu_musteri = """
            SELECT M.Ad || ' ' || M.Soyad, SUM(O.Miktar) as ToplamHarcama
            FROM Odemeler O
            JOIN Kiralamalar K ON O.KiralamaID = K.KiralamaID
            JOIN Musteriler M ON K.MusteriID = M.MusteriID
            GROUP BY M.MusteriID
            ORDER BY ToplamHarcama DESC
            LIMIT 5
        """
        self.cursor.execute(sorgu_musteri)
        musteriler = self.cursor.fetchall()
        
        self.rapor_enmusteriler_table.setColumnCount(2)
        self.rapor_enmusteriler_table.setHorizontalHeaderLabels(["Müşteri", "Toplam Harcama"])
        self.rapor_enmusteriler_table.setRowCount(0)
        for s, v in enumerate(musteriler):
            self.rapor_enmusteriler_table.insertRow(s)
            self.rapor_enmusteriler_table.setItem(s, 0, QTableWidgetItem(str(v[0])))
            self.rapor_enmusteriler_table.setItem(s, 1, QTableWidgetItem(f"{v[1]:.2f} TL"))

        # 3. En Çok Gelir Getiren Markalar
        sorgu_marka = """
            SELECT A.Marka, SUM(O.Miktar) as ToplamCiro
            FROM Odemeler O
            JOIN Kiralamalar K ON O.KiralamaID = K.KiralamaID
            JOIN Araclar A ON K.AracID = A.AracID
            GROUP BY A.Marka
            ORDER BY ToplamCiro DESC
            LIMIT 5
        """
        self.cursor.execute(sorgu_marka)
        markalar = self.cursor.fetchall()
        
        self.rapor_enmarkalar_table.setColumnCount(2)
        self.rapor_enmarkalar_table.setHorizontalHeaderLabels(["Marka", "Toplam Ciro"])
        self.rapor_enmarkalar_table.setRowCount(0)
        for s, v in enumerate(markalar):
            self.rapor_enmarkalar_table.insertRow(s)
            self.rapor_enmarkalar_table.setItem(s, 0, QTableWidgetItem(str(v[0])))
            self.rapor_enmarkalar_table.setItem(s, 1, QTableWidgetItem(f"{v[1]:.2f} TL"))


    # --- KİRALAMA EKRANI İÇİN VERİ YÜKLEME ---
    def kiralamalari_yukle(self):
        self.kiralama_musteri_combobox.clear()
        self.cursor.execute("SELECT MusteriID, Ad, Soyad FROM Musteriler")
        musteriler = self.cursor.fetchall()
        for m in musteriler:
            self.kiralama_musteri_combobox.addItem(f"{m[1]} {m[2]}", m[0])

        self.kiralama_arac_combobox.clear()
        self.cursor.execute("SELECT AracID, Plaka, Marka, Model, GunlukKiraBedeli, Kilometre FROM Araclar WHERE Durum = 'Müsait'")
        araclar = self.cursor.fetchall()
        for a in araclar:
            metin = f"{a[1]} - {a[2]} {a[3]}"
            self.kiralama_arac_combobox.addItem(metin, {"id": a[0], "fiyat": a[4], "km": a[5]})

        self.teslimal_araclar_combobox.clear()
        sorgu = """
            SELECT K.KiralamaID, A.AracID, A.Plaka, M.Ad, M.Soyad, K.KiraBitisTarihi, A.Kilometre, A.GunlukKiraBedeli, K.KiraBaslangicTarihi
            FROM Kiralamalar K
            JOIN Araclar A ON K.AracID = A.AracID
            JOIN Musteriler M ON K.MusteriID = M.MusteriID
            WHERE A.Durum = 'Kirada' AND K.GercekBitisTarihi IS NULL
        """
        self.cursor.execute(sorgu)
        kiradakiler = self.cursor.fetchall()
        for k in kiradakiler:
            metin = f"{k[2]} - {k[3]} {k[4]}"
            veri = {
                "kiralama_id": k[0],
                "arac_id": k[1],
                "bitis_tarihi": k[5],     
                "baslangic_km": k[6],
                "fiyat": k[7],
                "baslangic_tarihi": k[8]  
            }
            self.teslimal_araclar_combobox.addItem(metin, veri)

        self.aktif_kiralari_listele()

    # --- AKTİF KİRALAR LİSTESİ ---
    def aktif_kiralari_listele(self):
        sorgu = """
            SELECT K.KiralamaID, M.Ad || ' ' || M.Soyad, A.Plaka, A.Marka, K.KiraBaslangicTarihi, K.KiraBitisTarihi, A.Durum, K.BaslangicKm
            FROM Kiralamalar K
            JOIN Musteriler M ON K.MusteriID = M.MusteriID
            JOIN Araclar A ON K.AracID = A.AracID
            WHERE K.GercekBitisTarihi IS NULL
        """
        self.cursor.execute(sorgu)
        kayitlar = self.cursor.fetchall()
        
        self.aktifkiralar_table.setColumnCount(8)
        self.aktifkiralar_table.setHorizontalHeaderLabels(["ID", "Müşteri", "Plaka", "Marka", "Başlangıç", "Bitiş", "Durum", "Başlangıç KM"])
        self.aktifkiralar_table.setRowCount(0)
        
        for satir, veri in enumerate(kayitlar):
            self.aktifkiralar_table.insertRow(satir)
            for sutun, deger in enumerate(veri):
                self.aktifkiralar_table.setItem(satir, sutun, QTableWidgetItem(str(deger)))

    # --- FİYAT HESAPLAMA ---
    def fiyat_hesapla(self):
        secili_arac_data = self.kiralama_arac_combobox.currentData()
        if not secili_arac_data:
            self.kiralama_toplamfiyat_label.setText("0.00 TL")
            self.kiralama_baslangickm_label.setText("KM: -")
            return

        self.kiralama_baslangickm_label.setText(f"KM: {secili_arac_data['km']}")
        tarih1 = self.kiralama_baslangic_date.date()
        tarih2 = self.kiralama_bitis_date.date()
        gun_farki = tarih1.daysTo(tarih2)
        if gun_farki <= 0: gun_farki = 1 
        gunluk_fiyat = float(secili_arac_data['fiyat'])
        toplam = gun_farki * gunluk_fiyat
        self.kiralama_toplamfiyat_label.setText(f"{toplam:.2f} TL")

    # --- TESLİM EKRANI GÜNCELLEME ---
    def teslim_ekrani_guncelle(self):
        data = self.teslimal_araclar_combobox.currentData()
        if data:
            self.teslimal_bitiskm_spinbox.setMinimum(data['baslangic_km'])
            self.teslimal_bitiskm_spinbox.setValue(data['baslangic_km'])
            self.teslim_hesapla()
        else:
             self.teslimal_bitiskm_spinbox.setValue(0)
             self.teslimal_gecikme_label.setText("")
             self.teslimal_toplamtutar_label.setText("")

    # --- TESLİM FİYAT & GECİKME HESAPLAMA ---
    def teslim_hesapla(self):
        data = self.teslimal_araclar_combobox.currentData()
        if not data: return

        planlanan_bitis = QDate.fromString(data['bitis_tarihi'], "yyyy-MM-dd")
        gercek_baslangic = QDate.fromString(data['baslangic_tarihi'], "yyyy-MM-dd")
        gercek_bitis = self.teslimal_teslimalmatarihi_date.date()
        gunluk_fiyat = float(data['fiyat'])

        gecikme_gun = planlanan_bitis.daysTo(gercek_bitis)
        if gecikme_gun > 0:
            gecikme_bedeli = gecikme_gun * gunluk_fiyat
            self.teslimal_gecikme_label.setText(f"{gecikme_bedeli:.2f} TL ({gecikme_gun} Gün)")
        else:
            self.teslimal_gecikme_label.setText("Gecikme Yok")

        toplam_gun = gercek_baslangic.daysTo(gercek_bitis)
        if toplam_gun <= 0: toplam_gun = 1 
        
        toplam_tutar = toplam_gun * gunluk_fiyat
        self.teslimal_toplamtutar_label.setText(f"{toplam_tutar:.2f} TL")


    # --- ARAÇ KİRALA ---
    def arac_kirala(self):
        musteri_id = self.kiralama_musteri_combobox.currentData()
        arac_data = self.kiralama_arac_combobox.currentData()
        
        if not musteri_id or not arac_data:
            QMessageBox.warning(self, "Uyarı", "Lütfen müşteri ve araç seçiniz!")
            return

        baslangic_tarihi = self.kiralama_baslangic_date.date().toString("yyyy-MM-dd")
        bitis_tarihi = self.kiralama_bitis_date.date().toString("yyyy-MM-dd")
        
        t1 = self.kiralama_baslangic_date.date()
        t2 = self.kiralama_bitis_date.date()
        gun = t1.daysTo(t2)
        if gun <= 0: gun = 1
        toplam_ucret = gun * float(arac_data['fiyat'])

        try:
            sorgu_kira = """
                INSERT INTO Kiralamalar (MusteriID, AracID, KiraBaslangicTarihi, KiraBitisTarihi, BaslangicKm, ToplamUcret)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(sorgu_kira, (musteri_id, arac_data['id'], baslangic_tarihi, bitis_tarihi, arac_data['km'], toplam_ucret))
            
            self.cursor.execute("UPDATE Araclar SET Durum = 'Kirada' WHERE AracID = ?", (arac_data['id'],))

            self.conn.commit()
            QMessageBox.information(self, "Başarılı", "Kiralama işlemi başlatıldı.")
            self.kiralamalari_yukle() 
            self.araclari_listele()
            self.raporlari_yukle()

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Kiralama hatası: {e}")

    # --- ARAÇ TESLİM AL ---
    def arac_teslim_al(self):
        data = self.teslimal_araclar_combobox.currentData()
        if not data: return

        yeni_km = self.teslimal_bitiskm_spinbox.value()
        donus_tarihi_str = self.teslimal_teslimalmatarihi_date.date().toString("yyyy-MM-dd")
        odeme_tipi = self.teslimal_odeme_lineedit.text()
        if not odeme_tipi: odeme_tipi = "Nakit/Kredi Kartı"

        donus_tarihi_qdate = self.teslimal_teslimalmatarihi_date.date()
        baslangic_tarihi_qdate = QDate.fromString(data['baslangic_tarihi'], "yyyy-MM-dd")

        if yeni_km < data['baslangic_km']:
            QMessageBox.warning(self, "Hata", f"Dönüş kilometresi ({yeni_km}), başlangıç kilometresinden ({data['baslangic_km']}) düşük olamaz!")
            return

        toplam_gun = baslangic_tarihi_qdate.daysTo(donus_tarihi_qdate)
        if toplam_gun <= 0: toplam_gun = 1
        gunluk_fiyat = float(data['fiyat'])
        son_toplam_ucret = toplam_gun * gunluk_fiyat

        try:
            sorgu_bitir = "UPDATE Kiralamalar SET GercekBitisTarihi = ?, BitisKm = ?, ToplamUcret = ? WHERE KiralamaID = ?"
            self.cursor.execute(sorgu_bitir, (donus_tarihi_str, yeni_km, son_toplam_ucret, data['kiralama_id']))

            sorgu_arac = "UPDATE Araclar SET Durum = 'Müsait', Kilometre = ? WHERE AracID = ?"
            self.cursor.execute(sorgu_arac, (yeni_km, data['arac_id']))

            sorgu_odeme = "INSERT INTO Odemeler (KiralamaID, OdemeTarihi, Miktar, OdemeTipi) VALUES (?, ?, ?, ?)"
            bugun = datetime.now().strftime("%Y-%m-%d")
            self.cursor.execute(sorgu_odeme, (data['kiralama_id'], bugun, son_toplam_ucret, odeme_tipi))

            self.conn.commit()
            QMessageBox.information(self, "Başarılı", f"Araç teslim alındı.\n\nTutar: {son_toplam_ucret:.2f} TL\nÖdeme Tipi: {odeme_tipi}\nKaydedildi.")

            self.kiralamalari_yukle()
            self.araclari_listele()
            self.teslimal_odeme_lineedit.clear()
            self.raporlari_yukle() 

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Teslim alma hatası: {e}")


    # --- DİĞER FONKSİYONLAR ---
    def musteri_filtre_temizle(self):
        self.musteriaramaLineEdit.clear()
        self.musterileri_listele()
    def arac_filtre_temizle(self):
        self.aracaraLineEdit.clear()
        self.araclari_listele()
    def musteri_filtre_penceresi(self):
        dialog = MusteriFiltreDialog()
        if dialog.exec_() == QDialog.Accepted:
            baslangic_tarihi = dialog.date_filtre_baslangic.date().toString("yyyy-MM-dd")
            bitis_tarihi = dialog.date_filtre_bitis.date().toString("yyyy-MM-dd")
            adres_arama = dialog.lne_filtre_adres.text()
            sorgu = "SELECT * FROM Musteriler WHERE 1=1"
            parametreler = []
            sorgu += " AND DogumTarihi >= ? AND DogumTarihi <= ?"
            parametreler.append(baslangic_tarihi)
            parametreler.append(bitis_tarihi)
            if adres_arama:
                sorgu += " AND Adres LIKE ?"
                parametreler.append(f"%{adres_arama}%")
            try:
                self.cursor.execute(sorgu, parametreler)
                kayitlar = self.cursor.fetchall()
                self.musterilerTableWidget.setRowCount(0)
                for satir_indeks, satir_verisi in enumerate(kayitlar):
                    self.musterilerTableWidget.insertRow(satir_indeks)
                    for sutun_indeks, veri in enumerate(satir_verisi):
                        self.musterilerTableWidget.setItem(satir_indeks, sutun_indeks, QTableWidgetItem(str(veri)))
                if not kayitlar:
                    QMessageBox.information(self, "Sonuç", "Kriterlere uygun müşteri bulunamadı.")
            except Exception as e:
                print(f"Filtreleme hatası: {e}")
    def arac_filtre_penceresi(self):
        dialog = AracFiltreDialog()
        if dialog.exec_() == QDialog.Accepted:
            fiyat_min = dialog.spin_filtre_fiyat_min.value()
            fiyat_max = dialog.spin_filtre_fiyat_max.value()
            yil_min = dialog.spin_filtre_yil_min.value()
            yil_max = dialog.spin_filtre_yil_max.value()
            km_min = dialog.spin_filtre_kilometre_min.value() 
            km_max = dialog.spin_filtre_kilometre_max.value()
            durum = dialog.arac_filtre_durum.currentText()
            sorgu = "SELECT * FROM Araclar WHERE 1=1"
            parametreler = []
            sorgu += " AND GunlukKiraBedeli >= ? AND GunlukKiraBedeli <= ?"
            parametreler.append(fiyat_min)
            parametreler.append(fiyat_max)
            sorgu += " AND Yil >= ? AND Yil <= ?"
            parametreler.append(yil_min)
            parametreler.append(yil_max)
            sorgu += " AND Kilometre >= ? AND Kilometre <= ?"
            parametreler.append(km_min)
            parametreler.append(km_max)
            if durum != "Tümü":
                sorgu += " AND Durum = ?"
                parametreler.append(durum)
            try:
                self.cursor.execute(sorgu, parametreler)
                kayitlar = self.cursor.fetchall()
                self.araclarTableWidget.setRowCount(0)
                for satir_indeks, satir_verisi in enumerate(kayitlar):
                    self.araclarTableWidget.insertRow(satir_indeks)
                    for sutun_indeks, veri in enumerate(satir_verisi):
                        self.araclarTableWidget.setItem(satir_indeks, sutun_indeks, QTableWidgetItem(str(veri)))
                if not kayitlar:
                    QMessageBox.information(self, "Sonuç", "Kriterlere uygun araç bulunamadı.")
            except Exception as e:
                print(f"Araç Filtreleme hatası: {e}")
    def yeni_musteri_ekle_penceresi(self):
        dialog = YeniMusteriDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.musterileri_listele()
    def yeni_arac_ekle_penceresi(self):
        dialog = YeniAracDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.araclari_listele()
            self.kiralamalari_yukle()
    def musteri_guncelle_penceresi(self):
        secili_satir = self.musterilerTableWidget.currentRow()
        if secili_satir == -1: return 
        kayit_verisi = []
        for i in range(8):
            kayit_verisi.append(self.musterilerTableWidget.item(secili_satir, i).text())
        dialog = GuncelleMusteriDialog()
        dialog.bilgileri_doldur(kayit_verisi)
        if dialog.exec_() == QDialog.Accepted:
            self.musterileri_listele()
            self.kiralamalari_yukle()
    def arac_guncelle_penceresi(self):
        secili_satir = self.araclarTableWidget.currentRow()
        if secili_satir == -1: return 
        kayit_verisi = []
        sutun_sayisi = self.araclarTableWidget.columnCount()
        for i in range(sutun_sayisi):
            item = self.araclarTableWidget.item(secili_satir, i)
            text = item.text() if item else "" 
            kayit_verisi.append(text)
        dialog = GuncelleAracDialog()
        dialog.bilgileri_doldur(kayit_verisi)
        if dialog.exec_() == QDialog.Accepted:
            self.araclari_listele()
            self.kiralamalari_yukle()
    def musteri_sil(self):
        secili_satir = self.musterilerTableWidget.currentRow()
        if secili_satir == -1: return 
        id_item = self.musterilerTableWidget.item(secili_satir, 0)
        musteri_id = id_item.text()
        soru = QMessageBox.question(self, "Silme Onayı", "Müşteriyi silmek istediğinize emin misiniz?", QMessageBox.Yes | QMessageBox.No)
        if soru == QMessageBox.Yes:
            try:
                self.cursor.execute("DELETE FROM Musteriler WHERE MusteriID = ?", (musteri_id,))
                self.conn.commit()
                self.musterileri_listele()
                self.kiralamalari_yukle()
                QMessageBox.information(self, "Bilgi", "Müşteri silindi.")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Silme başarısız: {e}")
    def arac_sil(self):
        secili_satir = self.araclarTableWidget.currentRow()
        if secili_satir == -1: return 
        id_item = self.araclarTableWidget.item(secili_satir, 0)
        arac_id = id_item.text()
        soru = QMessageBox.question(self, "Silme Onayı", "Aracı silmek istediğinize emin misiniz?", QMessageBox.Yes | QMessageBox.No)
        if soru == QMessageBox.Yes:
            try:
                self.cursor.execute("DELETE FROM Araclar WHERE AracID = ?", (arac_id,))
                self.conn.commit()
                self.araclari_listele()
                self.kiralamalari_yukle()
                QMessageBox.information(self, "Bilgi", "Araç silindi.")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Silme başarısız: {e}")
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