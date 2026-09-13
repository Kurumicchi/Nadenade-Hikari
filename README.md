<p align="center">

  <img src="assets/img/Banner.png" alt="Nadenade Hikari Banner">

</p>

# Nadenade Hikari

Game berbasis webcam yang terinspirasi dari permainan whack-a-mole, dengan pemain harus menepuk Hikari yang muncul di berbagai posisi pada layar.

Pemain menggerakkan tangan kanan di depan webcam untuk mengendalikan cursor pada area permainan. Ketika cursor berada pada posisi Hikari, pemain dapat menekan tombol `Z` untuk melakukan nadenade dan mendapatkan skor.

Program menggunakan webcam dan color tracking berbasis HSV untuk mendeteksi posisi tangan pemain.

Proyek tugas mata kuliah Pengolahan Citra dan Video (PCV).

## Konten

* `main.py` — aplikasi utama: webcam, game loop, dan perpindahan game state.
* `states/game_state.py` — definisi state permainan.
* `states/menu_state.py` — tampilan dan logika menu utama.
* `calibration.json` — batas HSV hasil proses kalibrasi warna.
* `assets/img/` — gambar Hikari dan aset visual lainnya.
* `assets/audio/` — efek suara dan audio game.
* `demo/` — video demo project.

## Test

Aktifkan virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Jalankan program:

```powershell
python main.py
```

Aplikasi akan membuka webcam dan menjalankan game.

Pada menu utama, pemain dapat menggerakkan tangan kanan untuk mengendalikan cursor.

Tekan `z` untuk melakukan nadenade ketika cursor berada pada Hikari.

## Teknologi

| Nama         | Fungsi                                     |
| ------------ | ------------------------------------------ |
| Python 3.13  | Bahasa pemrograman                         |
| OpenCV       | Webcam dan pemrosesan gambar               |
| Pygame       | Game window, rendering, dan input keyboard |
| NumPy        | Pemrosesan data gambar                     |
| Git / GitHub | Version control                            |

## Struktur Game

Game menggunakan sistem state untuk memisahkan menu dan gameplay.

State yang tersedia saat ini:

```text
MENU
  ↓
PLAYING
```

`main.py` bertugas mengatur state aktif, sedangkan masing-masing state memiliki tanggung jawabnya sendiri.

Alur utama program:

```text
main.py
   │
   ├── MENU
   │     └── menu_state.py
   │
   └── PLAYING
         └── game_state.py
```

## Cara Kerja

Pipeline utama program:

```text
Webcam
   ↓
OpenCV
   ↓
Frame Calibration
   ↓
HSV Color Detection
   ↓
Color Mask
   ↓
Hand Position
   ↓
Cursor Position
   ↓
Game Interaction
   ↓
Nadenade
   ↓
Game Response
```

Webcam menampilkan video dalam warna normal pada bagian kanan layar.

Frame kamera juga diproses dalam ruang warna HSV untuk mendeteksi warna yang telah ditentukan pada proses kalibrasi.

Batas warna hasil kalibrasi disimpan dalam:

```text
calibration.json
```

Contoh data kalibrasi:

```json
{
    "lower_hsv": [0, 0, 0],
    "upper_hsv": [0, 0, 0]
}
```

Nilai tersebut digunakan oleh OpenCV untuk membuat mask berdasarkan warna yang terdeteksi.

```text
Camera Frame
      ↓
     HSV
      ↓
  HSV Range
      ↓
   Color Mask
      ↓
Detected Position
```

Posisi hasil deteksi kemudian digunakan untuk menentukan posisi cursor pada area permainan.

Cursor akan mengikuti pergerakan tangan kanan pemain.

## Gameplay

Gameplay terinspirasi dari konsep whack-a-mole.

Hikari akan muncul pada posisi tertentu di area permainan. Pemain harus menggerakkan tangan kanan untuk mengarahkan cursor menuju Hikari.

Ketika cursor berada pada posisi Hikari, pemain dapat menekan tombol:

```text
Z
```

untuk melakukan nadenade.

Alur permainan:

```text
Hikari muncul
     ↓
Gerakkan tangan kanan
     ↓
Cursor menuju Hikari
     ↓
Tekan Z
     ↓
Nadenade berhasil
     ↓
Score bertambah
     ↓
Hikari berpindah
```

### Kontrol

| Input        | Fungsi                |
| ------------ | --------------------- |
| Right Hand   | Menggerakkan cursor   |
| `Z`          | Nadenade / pat Hikari |
| Window Close | Keluar dari permainan |

## User Interface

Game menggunakan window berukuran:

```text
1280 × 720
```

Area permainan berada di sebelah kiri, sedangkan webcam ditampilkan pada panel di sebelah kanan.

```text
┌───────────────────────────────────────────────────────────────┐
│                                           |                   │
│  NADENADE HIKARI                          |                   │
│                                           |                   │
│  START                                    |                   │
│  QUIT                                     |                   │
│                                           |                   │
│                         Game Area         |   ┌────────────┐  │
│                                           |   │            │  │
│                                           |   │   CAMERA   │  │
│                                           |   │            │  │
│                                           |   └────────────┘  │
└───────────────────────────────────────────────────────────────┘
```

Camera preview menggunakan rasio 4:3 agar tampilan webcam tidak terdistorsi.

## Progress

### 2026-09-13

* **Inisisasi game** Dikarenakan kurangnya informasi mengenai apakah model MediaPipe diizinkan atau tidak, saya mengulang progres dua minggu dengan membuat project baru tanpa MediaPipe.
* **Project setup.** Membuat project Python, virtual environment, dan struktur folder awal.
* **Color calibration.** Menggunakan HSV color tracking untuk mendeteksi warna yang telah dikalibrasi melalui webcam.
* **Game window.** Membuat window game berukuran 1280×720 menggunakan Pygame.
* **Game state system.** Membuat sistem state untuk memisahkan menu dan gameplay.
* **Main menu.** Membuat menu utama dengan area permainan dan panel webcam.
* **Camera preview.** Menampilkan webcam dalam warna normal dengan rasio 4:3 pada bagian kanan layar.
* **Gameplay concept.** Menentukan konsep permainan berupa whack-a-mole dengan Hikari sebagai karakter yang harus dinadenade.
* Repo ini mengikuti project lama saya sendiri (https://github.com/Kurumicchi/Daitaku-Helios-Simulator) yang seharusnya dijadikan untuk mata kuliah PCV sebelum ada rumor MediaPipe tidak diizinkan