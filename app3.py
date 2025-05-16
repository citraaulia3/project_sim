import streamlit as st
import pandas as pd
import locale
locale.setlocale(locale.LC_ALL, '')

st.set_page_config(page_title="Aplikasi CV Bee Alaska", layout="wide")
st.title("📘 CV Bee Alaska")

# sidebar
st.sidebar.title("Siklus Akuntansi")
menu = st.sidebar.radio("", ["Neraca Saldo", "Jurnal Umum", "Buku Besar", "Neraca Saldo Setelah Disesuaikan", "Laporan Laba Rugi", "Laporan Perubahan Ekuitas", "Laporan Posisi Keuangan"])

#Neraca Saldo
if menu == "Neraca Saldo":
    st.subheader("Neraca Saldo")
    df_akun = ["Kas","Piutang Usaha", "Perlengkapan", "Persediaan Pakan", "Persediaan Madu", "Peralatan usaha", "Kendaraan", "Akumulasi Penyusutan Kendaraan", "Utang Usaha", "Utang Gaji", "Utang Pajak", "Modal, Alwi", "Prive, Alwi", "Ikhtisar Laba Rugi", "Penjualan", "Harga Pokok Penjualan", "Beban Gaji Karyawan", "Beban Pakan Lebah", "Beban Perlengkapan", "Beban Perawatan Sarang", "Beban Penyusutan Kendaraan", "Beban lain-lain", "Beban Pajak"]
    
    if "saldo_awal" not in st.session_state:
        st.session_state["saldo_awal"] = []
    
    with st.expander("Neraca Saldo"):
        akun = st.selectbox("Nama Akun", df_akun)
        #keterangan = st.selectbox("Keterangan", ["Kas", "Prive", "Utang", "Modal", "Pendapatan", "Beban"])
        saldo_debit = st.number_input("Saldo Debit", min_value=0.0)
        saldo_kredit = st.number_input("Saldo Kredit", min_value=0.0)
        if st.button("Tambah Saldo Awal"):
            st.session_state["saldo_awal"].append({
                "Nama Akun": akun,
                #"Keterangan": keterangan,
                "Debit": saldo_debit,
                "Kredit": saldo_kredit
            })
            st.success("Saldo awal berhasil ditambahkan!")
            
    # Tampilkan Neraca Saldo Awal
    #st.subheader("📄 Neraca Saldo")
    df = pd.DataFrame(st.session_state["saldo_awal"])
    
    if not df.empty and "Debit" in df.columns and "Kredit" in df.columns:
        saldo_debit = df["Debit"].sum()
        saldo_kredit = df["Kredit"].sum()
        
        total_row = pd.DataFrame([{
            "Nama Akun": ""   "Total",
            #"Keterangan": keterangan,
            "Debit": saldo_debit,
            "Kredit": saldo_kredit
        }])
        df_total = pd.concat([df, total_row], ignore_index=True)
        
        def format_rupiah(x):
            if x == 0 or x == "":
                return ""
            return f"Rp {int(x):,}".replace(",", ".")
        
        df_total["Debit"] = df_total["Debit"].apply(format_rupiah)
        df_total["Kredit"] = df_total["Kredit"].apply(format_rupiah)
        
        st.dataframe(df_total, use_container_width=True)
    else:
        st.info("Belum ada data nerasa saldo. Silakan tambahkan dulu.")

#Jurnal Umum
if menu == "Jurnal Umum":
    st.subheader("Jurnal Umum")
    df_akun = ["Kas","Piutang Usaha", "Perlengkapan", "Persediaan Pakan", "Persediaan Madu", "Peralatan usaha", "Kendaraan", "Akumulasi Penyusutan Kendaraan", "Utang Usaha", "Utang Gaji", "Utang Pajak", "Modal, Alwi", "Prive, Alwi", "Ikhtisar laba rugi", "Penjualan", "Harga Pokok Penjualan", "Beban Gaji Karyawan", "Beban Pakan Lebah", "Beban Perlengkapan", "Beban Perawatan Sarang", "Beban Penyusutan Kendaraan", "Beban lain-lain", "Beban Pajak"]
    
    # Inisialisasi data
    if "jurnal" not in st.session_state:
        st.session_state["jurnal"] = []
        
    # Form input transaksi
    with st.expander("Tambah Transaksi"):
        tanggal = st.date_input("Tanggal")
        nama_akun = st.selectbox("Nama Akun",df_akun)
        keterangan = st.text_input("Keterangan")
        saldo_debit = st.number_input("Saldo Debit", min_value=0.0)
        saldo_kredit = st.number_input("Saldo Kredit", min_value=0.0)
        if st.button("Tambah Transaksi"):
            st.session_state["jurnal"].append({
                "Tanggal": str(tanggal),
                "Nama Akun": nama_akun,
                "Keterangan": keterangan,
                "Debit": saldo_debit,
                "Kredit": saldo_kredit
            })
            st.success("Transaksi berhasil ditambahkan!")
            
    # Tampilkan jurnal umum
    #st.subheader("📄 Jurnal Umum")
    df = pd.DataFrame(st.session_state["jurnal"])
    
    if not df.empty and "Debit" in df.columns and "Kredit" in df.columns:
        total_debit = df["Debit"].sum()
        total_kredit = df["Kredit"].sum()
        
        total_row = pd.DataFrame([{
            "Tanggal": "",
            "Nama Akun": "",
            "Keterangan": "" "Total",
            "Debit": total_debit,
            "Kredit": total_kredit
        }])
        df_total = pd.concat([df, total_row], ignore_index=True)
        
        def format_rupiah(x):
            if x == 0 or x == "":
                return ""
            return f"Rp {int(x):,}".replace(",", ".")
        
        df_total["Debit"] = df_total["Debit"].apply(format_rupiah)
        df_total["Kredit"] = df_total["Kredit"].apply(format_rupiah)
        
        st.dataframe(df_total, use_container_width=True)
    else:
        st.info("Belum ada data transaksi. Silakan tambahkan dulu.")
        
#Buku Besar
if menu == "Buku Besar":
    st.subheader("📒 Buku Besar")

    # Kelompok akun
    akun_debit_normal = ["Kas","Piutang Usaha", "Perlengkapan", "Persediaan Pakan", "Persediaan Madu", "Peralatan usaha", "Kendaraan", "Prive, Alwi", "Harga Pokok Penjualan", "Beban Gaji Karyawan", "Beban Pakan Lebah", "Beban Perlengkapan", "Beban Perawatan Sarang", "Beban Penyusutan Kendaraan", "Beban lain-lain", "Beban Pajak"]
    akun_kredit_normal = ["Akumulasi Penyusutan Kendaraan", "Utang Usaha", "Utang Gaji", "Utang Pajak", "Modal, Alwi", "Penjualan"]

    # Fungsi saldo awal
    def saldo_awal_akun(akun, debit, kredit):
        if akun in akun_debit_normal:
            return + debit - kredit
        elif akun in akun_kredit_normal:
            return + kredit - debit
        else:
            return + debit - kredit

    # Fungsi saldo berjalan
    def hitung_saldo_berjalan(akun, debit, kredit, saldo_sebelumnya):
        if akun in akun_debit_normal:
            return saldo_sebelumnya + debit - kredit
        elif akun in akun_kredit_normal:
            return saldo_sebelumnya + kredit - debit
        else:
            return saldo_sebelumnya + debit - kredit

    # Ambil data dari session_state
    saldo_awal = st.session_state.get("saldo_awal", [])
    jurnal = st.session_state.get("jurnal", [])

    # Buat dict saldo awal
    saldo_awal_dict = {}
    for item in saldo_awal:
        nama = item["Nama Akun"]
        saldo_awal_dict[nama] = saldo_awal_akun(nama, item["Debit"], item["Kredit"])

    # Persiapkan jurnal
    df_jurnal = pd.DataFrame(jurnal)
    if not df_jurnal.empty:
        df_jurnal["Tanggal"] = pd.to_datetime(df_jurnal["Tanggal"], errors='coerce')
        df_jurnal["Debit"] = pd.to_numeric(df_jurnal["Debit"], errors='coerce').fillna(0)
        df_jurnal["Kredit"] = pd.to_numeric(df_jurnal["Kredit"], errors='coerce').fillna(0)
        df_jurnal = df_jurnal.sort_values("Tanggal").reset_index(drop=True)
    else:
        df_jurnal = pd.DataFrame(columns=["Tanggal", "Nama Akun", "Keterangan", "Debit", "Kredit"])

    # Gabungkan semua akun
    akun_list = list(set(saldo_awal_dict.keys()).union(set(df_jurnal["Nama Akun"].unique())))

    # Fungsi bantu untuk pecah saldo ke debit/kredit
    def pecah_saldo_ke_kolom(akun, nilai):
        if akun in akun_debit_normal:
            return (nilai if nilai >= 0 else 0, abs(nilai) if nilai < 0 else 0)
        elif akun in akun_kredit_normal:
            return (abs(nilai) if nilai < 0 else 0, nilai if nilai >= 0 else 0)
        else:
            return (nilai if nilai >= 0 else 0, abs(nilai) if nilai < 0 else 0)

    # Hitung buku besar per akun
    buku_besar = {}
    for akun in akun_list:
        saldo = saldo_awal_dict.get(akun, 0)
        saldo_debit, saldo_kredit = pecah_saldo_ke_kolom(akun, saldo)

        rows = [{
            "Tanggal": "",
            "Keterangan": "Saldo Awal",
            "Debit": "",
            "Kredit": "",
            "Saldo Debit": saldo_debit,
            "Saldo Kredit": saldo_kredit
        }]

        df_akun = df_jurnal[df_jurnal["Nama Akun"] == akun]
        for _, row in df_akun.iterrows():
            saldo = hitung_saldo_berjalan(akun, row["Debit"], row["Kredit"], saldo)
            saldo_debit, saldo_kredit = pecah_saldo_ke_kolom(akun, saldo)

            rows.append({
                "Tanggal": row["Tanggal"].strftime("%Y-%m-%d") if pd.notnull(row["Tanggal"]) else "",
                "Keterangan": row.get("Keterangan", ""),
                "Debit": row["Debit"],
                "Kredit": row["Kredit"],
                "Saldo Debit": saldo_debit,
                "Saldo Kredit": saldo_kredit
            })

        buku_besar[akun] = pd.DataFrame(rows)

    # Format rupiah
    def format_rupiah(x):
        if x == "" or x == 0 or pd.isna(x):
            return ""
        else:
            return f"Rp {int(x):,}".replace(",", ".")

    # Tampilkan hasil
    for akun, df_bb in buku_besar.items():
        st.subheader(f"Nama Akun: {akun}")
        df_display = df_bb.copy()
        df_display["Debit"] = df_display["Debit"].apply(format_rupiah)
        df_display["Kredit"] = df_display["Kredit"].apply(format_rupiah)
        df_display["Saldo Debit"] = df_display["Saldo Debit"].apply(format_rupiah)
        df_display["Saldo Kredit"] = df_display["Saldo Kredit"].apply(format_rupiah)
        st.dataframe(df_display, use_container_width=True)
    
    # Simpan ke sesssion_state agar bisa digunakan di menu lain
    st.session_state["buku_besar"] = buku_besar

# Neraca Saldo Setelah Disesuaikan
if menu == "Neraca Saldo Setelah Disesuaikan":
    st.subheader("📊 Neraca Saldo Setelah Disesuaikan")
    
    # Gunakan kategori akun yang sudah ada di menu Buku Besar
    akun_debit_normal = ["Kas","Piutang Usaha", "Perlengkapan", "Persediaan Pakan", "Persediaan Madu", 
                         "Peralatan usaha", "Kendaraan", "Prive, Alwi", "Harga Pokok Penjualan", 
                         "Beban Gaji Karyawan", "Beban Pakan Lebah", "Beban Perlengkapan", 
                         "Beban Perawatan Sarang", "Beban Penyusutan Kendaraan", "Beban lain-lain", "Beban Pajak"]
    
    akun_kredit_normal = ["Akumulasi Penyusutan Kendaraan", "Utang Usaha", "Utang Gaji", "Utang Pajak", 
                          "Modal, Alwi", "Penjualan"]

    # Ambil data buku besar dari session_state
    buku_besar = st.session_state.get("buku_besar", {})
    
    # Siapkan data untuk neraca saldo
    rows = []
    total_debit = 0
    total_kredit = 0
    
    for akun, df_bb in buku_besar.items():
        if len(df_bb) > 0:
            # Ambil saldo akhir dari baris terakhir
            saldo_debit = df_bb.iloc[-1]["Saldo Debit"] if not pd.isna(df_bb.iloc[-1]["Saldo Debit"]) else 0
            saldo_kredit = df_bb.iloc[-1]["Saldo Kredit"] if not pd.isna(df_bb.iloc[-1]["Saldo Kredit"]) else 0
            
            # Penempatan nilai sesuai dengan saldo normal akun
            if akun in akun_debit_normal:
                debit_val = saldo_debit
                kredit_val = 0
                total_debit += debit_val
            elif akun in akun_kredit_normal:
                debit_val = 0
                kredit_val = saldo_kredit
                total_kredit += kredit_val
            
            # Tambahkan ke tabel jika salah satu nilai tidak nol
            if debit_val > 0 or kredit_val > 0:
                rows.append({
                    "Nama Akun": akun,
                    "Debit": debit_val if debit_val > 0 else "",
                    "Kredit": kredit_val if kredit_val > 0 else ""
                })
    
    # Tambahkan total
    rows.append({
        "Nama Akun": "TOTAL",
        "Debit": total_debit,
        "Kredit": total_kredit
    })
    
    # Format rupiah
    def format_rupiah(x):
        if x == "" or x == 0 or pd.isna(x):
            return ""
        else:
            return f"Rp {int(x):,}".replace(",", ".")
    
    # Tampilkan tabel
    df_display = pd.DataFrame(rows)
    df_display["Debit"] = df_display["Debit"].apply(format_rupiah)
    df_display["Kredit"] = df_display["Kredit"].apply(format_rupiah)
    st.dataframe(df_display, use_container_width=True)

if menu == "Laporan Laba Rugi":
    st.subheader("📈 Laporan Laba Rugi")

    # Daftar akun pendapatan dan beban sesuai neraca saldo disesuaikan
    akun_pendapatan = [
        "Penjualan"
    ]

    akun_beban = [
        "Harga Pokok Penjualan", "Beban Gaji Karyawan", "Beban Pakan Lebah", "Beban Perlengkapan",
        "Beban Perawatan Sarang", "Beban Penyusutan Kendaraan", "Beban lain-lain", "Beban Pajak"
    ]

    buku_besar = st.session_state.get("buku_besar", {})

    rows = []
    total_pendapatan = 0
    total_beban = 0

    # Ambil saldo akhir dari neraca saldo setelah disesuaikan
    for akun, df_bb in buku_besar.items():
        if not df_bb.empty:
            saldo_debit = df_bb.iloc[-1].get("Saldo Debit", 0)
            saldo_kredit = df_bb.iloc[-1].get("Saldo Kredit", 0)
            saldo_debit = saldo_debit if pd.notna(saldo_debit) else 0
            saldo_kredit = saldo_kredit if pd.notna(saldo_kredit) else 0

            if akun in akun_pendapatan:
                # Pendapatan normalnya kredit
                saldo = saldo_kredit - saldo_debit
                total_pendapatan += saldo
                rows.append({
                    "Nama Akun": akun,
                    "Jumlah": saldo
                })

            elif akun in akun_beban:
                # Beban normalnya debit
                saldo = saldo_debit - saldo_kredit
                total_beban += saldo
                rows.append({
                    "Nama Akun": akun,
                    "Jumlah": saldo
                })

    # Hitung laba rugi bersih
    laba_rugi = total_pendapatan - total_beban

    def format_rupiah(x):
        if x == 0 or pd.isna(x):
            return ""
        else:
            return f"Rp {int(x):,}".replace(",", ".")

    df_display = pd.DataFrame(rows)
    df_display["Jumlah"] = df_display["Jumlah"].apply(format_rupiah)

    st.markdown("### Pendapatan")
    df_pendapatan = df_display[df_display["Nama Akun"].isin(akun_pendapatan)]
    st.dataframe(df_pendapatan, use_container_width=True)

    st.markdown("### Beban")
    df_beban = df_display[df_display["Nama Akun"].isin(akun_beban)]
    st.dataframe(df_beban, use_container_width=True)

    st.markdown("---")
    st.markdown(f"## Laba / Rugi Bersih: {format_rupiah(laba_rugi)}")