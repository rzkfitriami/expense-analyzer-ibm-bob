# Expense Analyzer - AI Agent dengan IBM Bob

AI Agent yang mengategorikan pengeluaran pribadi, mendeteksi outlier, menganalisis tren bulanan, dan memberi rekomendasi penghematan.

## Struktur
- `data/` - dataset 380 transaksi (CSV dan JSON, Apr-Sep 2026, IDR) dan skrip generator
- `prompts/` - `prompt_v1.txt` (iterasi 1, sederhana) dan `prompt_final.txt` (5 layer: Role, Context, Task, Output Format, Constraints)
- `screenshots/` - bukti hasil pengujian di IBM Bob

## Cara menjalankan
1. Buka IBM Bob dan upload `data/expenses_data.csv`
2. Paste isi `prompts/prompt_final.txt`
3. Bob menghasilkan tabel kategori, outlier, tren bulanan, dan rekomendasi

## Catatan
Dataset bersifat sintetis dan sengaja tanpa kolom kategori, sehingga kategorisasi sepenuhnya dikerjakan oleh AI Agent.
