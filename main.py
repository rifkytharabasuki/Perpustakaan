# Import modul yang dibutuhkan
import sys  # Untuk keluar dari program
import datetime  # Untuk mendapatkan waktu dan tanggal saat ini
import os  # Untuk operasi yang berhubungan dengan sistem file
import csv  # Untuk membaca dan menulis file CSV

# Tampilan pembuka
program = "-----PERPUSTAKAAN DIGITAL-----"
univ = "Telkom University Purwokerto"
print("=" * 70)
print(program.center(70))  # Tampilkan nama program di tengah
print(univ.center(70))  # Tampilkan nama universitas di tengah
print("=" * 70)
print("Selamat Datang!")

# Kelas Perpustakaan untuk mengelola buku dan transaksi
class Perpustakaan:
    def __init__(self):
        # Inisialisasi nama file
        self.nama_file = "daftar_buku.csv"
        self.file_peminjam = "data_peminjam.csv"
        self.file_pengembalian = "data_pengembalian.csv"
        self.buku_tersedia = self.muatan_buku()  # Load data buku
        self.siapkan_file_csv()  # Buat file CSV jika belum ada

    def muatan_buku(self):
        # Load data buku dari file CSV jika ada, jika tidak buat daftar default
        if os.path.exists(self.nama_file):
            buku_dict = {}
            with open(self.nama_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    kode = row["Kode"]
                    judul = row["Judul"]
                    stok = int(row["Stok"])
                    buku_dict[kode] = (judul, stok)
            return buku_dict
        else:
            # Daftar default jika file tidak ditemukan
            daftar = [
                ("B001", "Laskar Pelangi"), ("B002", "Harry Potter"), ("B003", "Bumi Manusia"),
                ("B004", "Pulang"), ("B005", "Dilan 1990"), ("B006", "Dilan 1991"), ("B007", "Pulang Pergi"),
                ("B008", "Sang Pemimpi"), ("B009", "5 cm"), ("B010", "Negeri 5 Menara"),
                ("B011", "Ayat-Ayat Cinta"), ("B012", "Bumi"), ("B013", "Programming"),
                ("B014", "Akuntansi Dasar"), ("B015", "Buku Sastra dan Bahasa")
            ]
            # Semua buku default diberi stok 5
            return {kode: (judul, 5) for kode, judul in daftar}

    def simpan_buku(self):
        # Menyimpan data buku ke file CSV
        with open(self.nama_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Kode", "Judul", "Stok"])
            for kode, (judul, stok) in self.buku_tersedia.items():
                writer.writerow([kode, judul, stok])

    def siapkan_file_csv(self):
        # Membuat file peminjam dan pengembalian jika belum ada
        if not os.path.exists(self.file_peminjam):
            with open(self.file_peminjam, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(["Nama", "NIM", "Kode Buku", "Judul Buku", "Waktu"])
        if not os.path.exists(self.file_pengembalian):
            with open(self.file_pengembalian, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(["Nama", "NIM", "Kode Buku", "Judul Buku", "Waktu"])

    def simpan_peminjaman(self, nama, nim, kode, judul):
        # Menyimpan data peminjaman buku
        waktu = datetime.datetime.now()
        with open(self.file_peminjam, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([nama, nim, kode, judul, waktu])

    def simpan_pengembalian(self, nama, nim, kode, judul):
        # Menyimpan data pengembalian buku
        waktu = datetime.datetime.now()
        with open(self.file_pengembalian, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([nama, nim, kode, judul, waktu])

    def tampilkan_buku(self):
        # Menampilkan daftar semua buku
        print("\n" + "=" * 50)
        print("<<<<<< DAFTAR BUKU PERPUSTAKAAN >>>>>>")
        print("=" * 50)
        for kode, (judul, stok) in self.buku_tersedia.items():
            print(f"Kode: {kode} | Judul: {judul} | Stok: {stok}")
            print("-" * 50)

    def pinjam_buku(self, kode, nama, nim):
        # Proses peminjaman buku
        if kode in self.buku_tersedia and self.buku_tersedia[kode][1] > 0:
            judul, stok = self.buku_tersedia[kode]
            print(">" * 50)
            print("Buku berhasil dipinjam!")
            print("Waktu peminjaman: ", datetime.datetime.now())
            print("+------------------------------------+")
            print("| TOLONG KEMBALIKAN BUKU TEPAT WAKTU |")
            print("+------------------------------------+")
            self.buku_tersedia[kode] = (judul, stok - 1)  # Kurangi stok
            self.simpan_buku()
            self.simpan_peminjaman(nama, nim, kode, judul)
        else:
            print("Maaf, buku tidak tersedia atau kode salah.")

    def kembalikan_buku(self, kode, nama, nim):
        # Proses pengembalian buku
        if kode in self.buku_tersedia:
            judul, stok = self.buku_tersedia[kode]
            self.buku_tersedia[kode] = (judul, stok + 1)  # Tambah stok
        else:
            # Jika kode tidak ditemukan, input manual judul
            judul = input("Masukkan Judul Buku (karena kode tidak ditemukan): ")
            self.buku_tersedia[kode] = (judul, 1)

        print(">" * 50)
        print("Terima kasih telah mengembalikan buku!")
        print("Waktu Pengembalian: ", datetime.datetime.now())
        print("+-----------------------------------+")
        print("|  TERIMA KASIH TELAH MEMINJAM!     |")
        print("+-----------------------------------+")
        self.simpan_buku()
        self.simpan_pengembalian(nama, nim, kode, self.buku_tersedia[kode][0])

    def cari_buku(self, kata_kunci):
        # Mencari buku berdasarkan judul
        hasil = []
        for kode, (judul, stok) in self.buku_tersedia.items():
            if kata_kunci.lower() in judul.lower():
                hasil.append((kode, judul, stok))
        if hasil:
            print("\nBuku yang cocok dengan pencarianmu:")
            print("=" * 50)
            for kode, judul, stok in hasil:
                print(f"Kode: {kode} | Judul: {judul} | Stok: {stok}")
                print("-" * 50)
        else:
            print("\nMaaf, tidak ada buku yang cocok.")

# Kelas Orang sebagai induk dari Mahasiswa
class Orang:
    def set_nama(self, nama):
        self.nama = nama

    def set_nim(self, nim):
        self.nim = nim

# Kelas Mahasiswa mewarisi dari Orang
class Mahasiswa(Orang):
    def pinjam_buku(self):
        return input("Masukkan Kode Buku yang ingin dipinjam: ")

    def kembalikan_buku(self):
        return input("Masukkan Kode Buku yang ingin dikembalikan: ")

# Fungsi untuk kembali ke menu utama
def kembali_ke_menu(mahasiswa, perpustakaan):
    kembali = input('\nKembali ke Menu Utama? (y/n)>> ')
    if kembali.lower() == 'y':
        menu_utama(mahasiswa, perpustakaan)
    else:
        sys.exit()

# Fungsi awal untuk input nama dan NIM mahasiswa
def mulai():
    mhs = Mahasiswa()
    mhs.set_nama(input("Masukkan Nama: "))
    mhs.set_nim(input("Masukkan NIM: "))
    print(f"\nSelamat datang {mhs.nama}!")
    return mhs

# Fungsi untuk menampilkan menu utama dan proses pilihan
def menu_utama(mahasiswa, perpustakaan):
    while True:
        print("""
+------------------------------+
|          MENU UTAMA          |
+------------------------------+
| [1] Tampilkan Daftar Buku    |
| [2] Pinjam Buku              |
| [3] Kembalikan Buku          |
| [4] Cari Buku                |
| [5] Keluar                   |
+------------------------------+
        """)
        try:
            pilihan = int(input("Pilih menu: "))
        except ValueError:
            print("Masukkan angka yang valid!")
            continue

        if pilihan == 1:
            perpustakaan.tampilkan_buku()
            kembali_ke_menu(mahasiswa, perpustakaan)
        elif pilihan == 2:
            kode = mahasiswa.pinjam_buku()
            perpustakaan.pinjam_buku(kode, mahasiswa.nama, mahasiswa.nim)
            kembali_ke_menu(mahasiswa, perpustakaan)
        elif pilihan == 3:
            kode = mahasiswa.kembalikan_buku()
            perpustakaan.kembalikan_buku(kode, mahasiswa.nama, mahasiswa.nim)
            kembali_ke_menu(mahasiswa, perpustakaan)
        elif pilihan == 4:
            kata_kunci = input("Masukkan kata kunci pencarian: ")
            perpustakaan.cari_buku(kata_kunci)
            kembali_ke_menu(mahasiswa, perpustakaan)
        elif pilihan == 5:
            sys.exit()
        else:
            print("Pilihan tidak valid.")

# Program utama dijalankan di sini
mahasiswa = mulai()
perpustakaan = Perpustakaan()
menu_utama(mahasiswa, perpustakaan)
