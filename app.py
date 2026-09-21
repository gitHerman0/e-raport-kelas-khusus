import os
import pandas as pd
import streamlit as st

# Konfigurasi Halaman
st.set_page_config(
    page_title="E-Raport Dashboard - SMK Karya Nasional",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Styling CSS untuk Tampilan Rapor Resmi 1 Lembar
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-weight: bold;
        color: #1f4e78;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        color: #595959;
        margin-bottom: 20px;
    }
    .section-header {
        background-color: #f2f4f8;
        padding: 6px 10px;
        border-left: 5px solid #1f4e78;
        font-weight: bold;
        color: #1f4e78;
        margin-top: 15px;
        margin-bottom: 10px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    "<h2 class='main-title'>E-RAPORT</h2>",
    unsafe_allow_html=True,
)
st.markdown(
    "<h4 class='sub-title'>JEPANG & DIGIPRENEUR</h4>", unsafe_allow_html=True
)

# Sumber Data Excel (Membaca otomatis dari file lokal atau upload sidebar)
default_excel = "Absensi_Siswa Update 3 september 2026.xlsx"
base_dir = (
    os.path.dirname(os.path.abspath(__file__))
    if "__file__" in locals()
    else os.getcwd()
)
excel_path = os.path.join(base_dir, default_excel)

st.sidebar.header("📁 Pengaturan Data & Siswa")
uploaded_file = st.sidebar.file_uploader(
    "Upload File Excel (.xlsx)", type=["xlsx", "xls"]
)

df = None
if uploaded_file is not None:
  try:
    df = pd.read_excel(uploaded_file, header=4)
  except Exception as e:
    st.sidebar.error(f"Gagal membaca file yang di-upload: {e}")
elif os.path.exists(excel_path):
  try:
    df = pd.read_excel(excel_path, header=4)
  except Exception as e:
    st.error(f"Gagal membaca file default: {e}")

if df is not None:
  # Bersihkan nama kolom dari spasi berlebih
  df.columns = [str(c).strip() for c in df.columns]

  if "Nama" in df.columns:
    # Buat Label unik untuk sidebar (Nomor. Nama - Kelas (Unggulan))
    df["Label_Siswa"] = (
        (df.index + 1).astype(str)
        + ". "
        + df["Nama"].astype(str)
        + " - "
        + df.get("Kelas", "").astype(str)
        + " ("
        + df.get("Kelas Unggulan", "").astype(str)
        + ")"
    )

    selected_label = st.sidebar.selectbox(
        "Pilih Siswa:", df["Label_Siswa"].unique()
    )
    siswa_data = df[df["Label_Siswa"] == selected_label].iloc[0]

    # ================= HEADER: LOGO, JUDUL, FOTO SISWA =================
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
      logo_path = os.path.join(base_dir, "logo_karnas.png")
      if os.path.exists(logo_path):
        st.image(logo_path, width=200)
      else:
        st.markdown("### **[ Logo Karnas ]**")

    with col2:
      st.markdown(
          "<div style='text-align: center; padding-top: 20px;'>",
          unsafe_allow_html=True,
      )
      st.markdown("</div>", unsafe_allow_html=True)

    with col3:
      foto_input = (
          str(siswa_data.get("Foto", ""))
          if pd.notna(siswa_data.get("Foto"))
          else ""
      )
      nama_cari = os.path.splitext(foto_input)[0].strip().lower()

      foto_path = ""
      if nama_cari:
        for f in os.listdir(base_dir):
          # Cek file di direktori utama, abaikan folder atau file lain
          if os.path.isfile(os.path.join(base_dir, f)):
            if os.path.splitext(f)[0].lower() == nama_cari:
              foto_path = os.path.join(base_dir, f)
              break

      if foto_path and os.path.exists(foto_path):
        st.image(foto_path, width=110)
      else:
        st.image(
            "https://via.placeholder.com/110x140?text=Foto+Siswa", width=110
        )

    st.markdown("---")

    # ================= IDENTITAS & ABSENSI =================
    c_id, c_abs = st.columns(2)

    with c_id:
      st.markdown(
          "<div class='section-header'>👤 IDENTITAS SISWA</div>",
          unsafe_allow_html=True,
      )
      st.write(f"**Nama Lengkap:** {siswa_data.get('Nama', '-')}")
      st.write(f"**Kelas:** {siswa_data.get('Kelas', '-')}")
      st.write(f"**Jurusan:** {siswa_data.get('Jurusan', '-')}")
      st.write(f"**Kelas Unggulan:** {siswa_data.get('Kelas Unggulan', '-')}")

    with c_abs:
      st.markdown(
          "<div class='section-header'>📅 KETIDAKHADIRAN (ABSENSI)</div>",
          unsafe_allow_html=True,
      )

      def safe_int(val):
        try:
          return int(val) if pd.notna(val) else 0
        except:
          return 0

      sakit_val = safe_int(siswa_data.get("Sakit", 0))
      izin_val = safe_int(siswa_data.get("Izin", 0))
      alpa_val = safe_int(siswa_data.get("Alpa", 0))
      bolos_val = safe_int(siswa_data.get("Bolos", 0))

      col_a1, col_a2 = st.columns(2)
      with col_a1:
        st.write(f"• Sakit: {sakit_val} hari")
        st.write(f"• Izin: {izin_val} hari")
      with col_a2:
        st.write(f"• Alpa: {alpa_val} hari")
        st.write(f"• Bolos: {bolos_val} hari")

    st.markdown("---")

    # ================= FISIK & PSIKOTES =================
    c_fis, c_psi = st.columns(2)

    with c_fis:
      st.markdown(
          "<div class='section-header'>🩺 PEMERIKSAAN FISIK</div>",
          unsafe_allow_html=True,
      )
      st.write(f"**Visus Mata:** {siswa_data.get('Visus Mata', '-')}")
      st.write(f"**Buta Warna:** {siswa_data.get('Buta Warna', '-')}")
      st.write(f"**Tinggi Badan:** {siswa_data.get('Tinggi Badan', '-')} cm")
      st.write(f"**Berat Badan:** {siswa_data.get('Berat Badan', '-')} kg")
      st.write(f"**Tindik:** {siswa_data.get('Tindik', '-')}")
      st.write(f"**Tato:** {siswa_data.get('Tato', '-')}")

      if "Visus Mata 2" in df.columns and pd.notna(
          siswa_data.get("Visus Mata 2")
      ):
        st.markdown("---")
        st.write(
            f"**Visus Mata (Periode 2):** {siswa_data.get('Visus Mata 2', '-')}"
        )
        st.write(
            f"**Buta Warna (Periode 2):** {siswa_data.get('Buta Warna 2', '-')}"
        )
        st.write(
            f"**Tinggi Badan (Periode 2):**"
            f" {siswa_data.get('Tinggi Badan 2', '-')} cm"
        )
        st.write(
            f"**Berat Badan (Periode 2):**"
            f" {siswa_data.get('Berat Badan 2', '-')} kg"
        )
        st.write(f"**Tindik (Periode 2):** {siswa_data.get('Tindik 2', '-')}")
        st.write(f"**Tato (Periode 2):** {siswa_data.get('Tato 2', '-')}")

    with c_psi:
      st.markdown(
          "<div class='section-header'>🧠 HASIL PSIKOTES</div>",
          unsafe_allow_html=True,
      )
      st.write(f"**Periode:** {siswa_data.get('Periode Psikotes', '-')}")
      st.write(
          f"**Tes Inteligensi Umum:**"
          f" {siswa_data.get('Tes Inteligensi Umum', '-')}"
      )
      st.write(f"**Army Alpha:** {siswa_data.get('Army Alpha', '-')}")
      st.write(
          f"**Matematika Dasar:** {siswa_data.get('Matematika Dasar', '-')}"
      )
      st.write(f"**Kraeplin:** {siswa_data.get('Kraeplin', '-')}")

      if "Periode Psikotes 2" in df.columns and pd.notna(
          siswa_data.get("Periode Psikotes 2")
      ):
        st.markdown("---")
        st.write(
            f"**Periode (Periode 2):**"
            f" {siswa_data.get('Periode Psikotes 2', '-')}"
        )
        st.write(
            f"**Tes Inteligensi Umum (Periode 2):**"
            f" {siswa_data.get('Tes Inteligensi Umum 2', '-')}"
        )
        st.write(
            f"**Army Alpha (Periode 2):** {siswa_data.get('Army Alpha 2', '-')}"
        )
        st.write(
            f"**Matematika Dasar (Periode 2):**"
            f" {siswa_data.get('Matematika Dasar 2', '-')}"
        )
        st.write(f"**Kraeplin (Periode 2):** {siswa_data.get('Kraeplin 2', '-')}")

    st.markdown("---")

    # ================= KOMPETENSI 1 SAMPAI 8 =================

    st.markdown(

        "<div class='section-header'>🏆 PENCAPAIAN KOMPETENSI (1 - 8)</div>",

        unsafe_allow_html=True,

    )



    kompetensi_list = []

    for i in range(1, 9):

      nama_komp = siswa_data.get(f"Kompetensi {i} Nama", f"Kompetensi {i}")

      target = siswa_data.get(f"Kompetensi {i} Target", 0)

      aktual = siswa_data.get(f"Kompetensi {i} Aktual", 0)

      grade = siswa_data.get(f"Kompetensi {i} Grade", "-")

      if pd.notna(nama_komp) and str(nama_komp).strip() != "":

        kompetensi_list.append({

            "No": i,

            "Nama Kompetensi": nama_komp,

            "Target": target,

            "Pencapaian Aktual": aktual,

            "Grade": grade,

        })

     df_komp = pd.DataFrame(kompetensi_list)
    
    # Menampilkan tabel dengan perataan tengah menggunakan column_config bawaan Streamlit
    df_komp = pd.DataFrame(kompetensi_list)

    st.dataframe(df_komp, use_container_width=True, hide_index=True)
    # ================= GRAFIK KOMPETENSI =================
    st.markdown(
        "<div class='section-header'>📈 GRAFIK TARGET VS PENCAPAIAN"
        " KOMPETENSI</div>",
        unsafe_allow_html=True,
    )
    try:
      chart_df = pd.DataFrame(
          {
              "Target": [row["Target"] for row in kompetensi_list],
              "Aktual": [row["Pencapaian Aktual"] for row in kompetensi_list],
          },
          index=[f"Komp {row['No']}" for row in kompetensi_list],
      )
      st.bar_chart(chart_df)
    except Exception:
      st.info(
          "Grafik belum dapat ditampilkan (pastikan data Target & Aktual berupa"
          " angka)."
      )

    st.markdown("---")

    # ================= RESUME =================
    st.markdown(
        "<div class='section-header'>📝 RESUME & KESIMPULAN</div>",
        unsafe_allow_html=True,
    )
    c_res1, c_res2 = st.columns(2)
    with c_res1:
      # Format Nilai Rata-rata agar menjadi 2 desimal
      raw_rata = siswa_data.get("Nilai Rata-rata", "-")
      if pd.notna(raw_rata):
        try:
          rata_str = f"{float(raw_rata):.2f}"
        except:
          rata_str = str(raw_rata)
      else:
        rata_str = "-"

      st.write(f"**Nilai Rata-rata:** {rata_str}")
      st.write(f"**Nilai Tertinggi:** {siswa_data.get('Nilai Tertinggi', '-')}")
      st.write(f"**Nilai Terendah:** {siswa_data.get('Nilai Terendah', '-')}")
    with c_res2:
      st.write(f"**Rekomendasi / Masukan:**")
      st.info(f"{siswa_data.get('Rekomendasi Masukan', '-')}")

    # ================= TANGGAL & TANDA TANGAN =================
    col_ttd1, col_ttd2 = st.columns([3, 1])
    with col_ttd2:
      raw_tgl = siswa_data.get("Tanggal", "...........................")
      
      # Bersihkan format tanggal agar tidak menampilkan jam (00:00:00) jika terbaca timestamp
      if pd.notna(raw_tgl):
        tgl_str = str(raw_tgl).split()[0] if " " in str(raw_tgl) else str(raw_tgl)
      else:
        tgl_str = "..........................."

      wali = siswa_data.get("Wali Kelas", "Nama Wali Kelas")
      st.write(f"Tanggal: {tgl_str}")
      st.write("\n\n")
      st.write(f"**({wali})**")
      st.write("Wali Kelas")

  else:
    st.error("File Excel harus memiliki kolom 'Nama'.")
else:
  st.info(
      "👈 Silakan upload file Excel atau pastikan file 'Absensi_Siswa Update 3"
      " september 2026.xlsx' berada di dalam folder project."
  )
