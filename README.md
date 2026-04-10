# Penalty Kick Simulator - Ronaldo vs Courtois

Simulasi 3D interaktif tendangan penalti antara Cristiano Ronaldo dan Thibaut Courtois.

## Fitur

- Simulasi 3D dengan animasi penendang dan kiper
- 10 skenario distribusi probabilitas
- Simulasi batch (100-5000 tendangan)
- Perbandingan hasil simulasi vs model probabilitas matematika
- Bar chart visual + output data ke console

## Cara Menjalankan

```bash
pip install -r requirements.txt
python main.py
```

## Kontrol

| Input        | Fungsi                           |
| ------------ | -------------------------------- |
| 1 / 2 / 3    | Tendang ke Kiri / Tengah / Kanan |
| Prev / Next  | Ganti skenario probabilitas      |
| Skenario Ini | Simulasi batch skenario aktif    |
| Semua        | Simulasi batch semua skenario    |
| ESC          | Tutup dashboard                  |
| Scroll       | Navigasi data dashboard          |

Output di `dist/PenaltySimulator/`.

## Tech Stack

Python 3, Ursina Engine, NumPy
