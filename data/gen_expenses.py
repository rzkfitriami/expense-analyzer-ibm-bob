"""
Generator dataset Expense Analyzer (Capstone IBM Bob).
Data transaksi pengeluaran personal, konteks Indonesia, mata uang IDR.
Sengaja TIDAK ada kolom kategori -> kategorisasi adalah tugas AI Agent.
"""
import csv, json, random
from datetime import date, timedelta

random.seed(42)  # deterministik -> hasil selalu sama

# (merchant, deskripsi, rentang nominal, metode bayar yang masuk akal)
MERCHANTS = [
    ("Indomaret",            "Belanja kebutuhan harian",        18000,   95000,  ["Debit Card", "QRIS", "Cash"]),
    ("Alfamart",             "Belanja kebutuhan harian",        15000,   85000,  ["Debit Card", "QRIS", "Cash"]),
    ("Superindo",            "Belanja bulanan",                 185000,  620000, ["Debit Card", "Credit Card"]),
    ("Warung Nasi Padang",   "Makan siang",                     22000,   45000,  ["Cash", "QRIS"]),
    ("Kopi Kenangan",        "Kopi",                            18000,   38000,  ["QRIS", "E-Wallet"]),
    ("GoFood",               "Pesan makanan online",            35000,   125000, ["E-Wallet"]),
    ("Gojek",                "Transportasi ojek online",        12000,   48000,  ["E-Wallet"]),
    ("Grab",                 "Transportasi mobil online",       28000,   95000,  ["E-Wallet", "Credit Card"]),
    ("SPBU Pertamina",       "Isi bensin motor",                25000,   60000,  ["Cash", "Debit Card"]),
    ("KAI Commuter",         "Top up kartu commuter line",      50000,   100000, ["Debit Card", "E-Wallet"]),
    ("Tokopedia",            "Belanja online perlengkapan",     65000,   780000, ["Bank Transfer", "Credit Card"]),
    ("Shopee",               "Belanja online pakaian",          55000,   450000, ["E-Wallet", "Bank Transfer"]),
    ("Netflix",              "Langganan streaming bulanan",     65000,   186000, ["Credit Card"]),
    ("Spotify",              "Langganan musik bulanan",         54000,   54000,  ["Credit Card"]),
    ("Telkomsel",            "Pulsa dan paket data",            50000,   150000, ["E-Wallet", "Debit Card"]),
    ("PLN",                  "Token listrik",                   100000,  350000, ["Bank Transfer", "E-Wallet"]),
    ("PDAM",                 "Tagihan air bulanan",             85000,   165000, ["Bank Transfer"]),
    ("Kos Melati",           "Pembayaran sewa kos bulanan",     1500000, 1500000,["Bank Transfer"]),
    ("Apotek K24",           "Obat dan vitamin",                35000,   185000, ["Cash", "Debit Card"]),
    ("Klinik Sehat Bersama", "Konsultasi dokter",               150000,  320000, ["Debit Card", "Cash"]),
    ("Gold's Gym",           "Iuran gym bulanan",               250000,  250000, ["Credit Card"]),
    ("CGV Cinemas",          "Tiket bioskop",                   40000,   70000,  ["E-Wallet", "Debit Card"]),
    ("Gramedia",             "Buku",                            68000,   195000, ["Debit Card", "Credit Card"]),
    ("Udemy",                "Kursus online",                   149000,  399000, ["Credit Card"]),
    ("Laundry Bersih",       "Cuci setrika kiloan",             25000,   65000,  ["Cash", "QRIS"]),
    ("Barbershop Rapi",      "Potong rambut",                   35000,   60000,  ["Cash", "QRIS"]),
    ("Bank Mandiri",         "Biaya admin bulanan",             15000,   15000,  ["Bank Transfer"]),
    ("Traveloka",            "Tiket kereta perjalanan",         150000,  620000, ["Credit Card", "Bank Transfer"]),
]

# transaksi rutin bulanan (muncul sekali tiap bulan di tanggal tetap)
MONTHLY = {
    "Kos Melati": 2, "Netflix": 5, "Spotify": 7, "PLN": 10,
    "PDAM": 12, "Gold's Gym": 15, "Bank Mandiri": 28,
}

START = date(2026, 4, 1)
END = date(2026, 9, 30)


def round_rupiah(n):
    """Bulatkan ke ratusan rupiah supaya terlihat wajar."""
    return int(round(n / 500.0) * 500)


rows = []
by_merchant = {m[0]: m for m in MERCHANTS}

# 1. Transaksi rutin bulanan
day = START
seen_months = []
while day <= END:
    if (day.year, day.month) not in seen_months:
        seen_months.append((day.year, day.month))
    day += timedelta(days=1)

for (y, m) in seen_months:
    for name, dom in MONTHLY.items():
        merchant, desc, lo, hi, methods = by_merchant[name]
        rows.append({
            "date": date(y, m, dom),
            "merchant": merchant,
            "description": desc,
            "amount": round_rupiah(random.randint(lo, hi)),
            "payment_method": random.choice(methods),
        })

# 2. Transaksi harian acak
irregular = [m for m in MERCHANTS if m[0] not in MONTHLY]
total_days = (END - START).days + 1
for i in range(total_days):
    d = START + timedelta(days=i)
    # akhir pekan cenderung lebih banyak transaksi
    n = random.randint(1, 4) if d.weekday() >= 5 else random.randint(0, 3)
    for _ in range(n):
        merchant, desc, lo, hi, methods = random.choice(irregular)
        rows.append({
            "date": d,
            "merchant": merchant,
            "description": desc,
            "amount": round_rupiah(random.randint(lo, hi)),
            "payment_method": random.choice(methods),
        })

# 3. Urutkan dan beri ID berurutan
rows.sort(key=lambda r: r["date"])
clean = []
for i, r in enumerate(rows, start=1):
    clean.append({
        "transaction_id": f"TRX-{i:04d}",
        "date": r["date"].isoformat(),
        "merchant": r["merchant"],
        "description": r["description"],
        "amount": r["amount"],
        "currency": "IDR",
        "payment_method": r["payment_method"],
    })

# Tulis CSV
with open("expenses_data.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(clean[0].keys()))
    w.writeheader()
    w.writerows(clean)

# Tulis JSON
with open("expenses_data.json", "w", encoding="utf-8") as f:
    json.dump(clean, f, indent=2, ensure_ascii=False)

print(f"Total baris       : {len(clean)}")
print(f"Rentang tanggal   : {clean[0]['date']} s/d {clean[-1]['date']}")
print(f"Jumlah merchant   : {len(set(r['merchant'] for r in clean))}")
print(f"Metode pembayaran : {sorted(set(r['payment_method'] for r in clean))}")
print(f"Total nominal     : Rp {sum(r['amount'] for r in clean):,}")
