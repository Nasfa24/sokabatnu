/**
 * CORE ENGINE MAS UUTH MPA (V6.0)
 * Mencakup: Pop-up Poster PKB (pkb 1.webp), Form Pendaftaran Kader PKB,
 * Searchable Dropdown 154 Wilayah & 117 Pekerjaan, Kompresi KTP/KK, & Fix Nomor HP 08..
 */

const scriptURL = 'https://script.google.com/macros/s/AKfycbxOo_Z8IPxSXYgvuyxBna8ZEjGx0GLUJl2orrjaDtJZePRGmSMNYVatvXWbpLljQyzYNg/exec';
// Akun Lebah Bergerak: satu pendaftaran, dua keanggotaan
const SUPA_URL = 'https://hvbrskchlpemypawpqjn.supabase.co';
const SUPA_ANON = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh2YnJza2NobHBlbXlwYXdwcWpuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY5MzYzNzksImV4cCI6MjA5MjUxMjM3OX0.0NCroyTHROeQ3SNKOTNZS1H1hxrGy5wGTLGWm5YdOdo';

const swalConfig = {
    backdrop: 'rgba(20, 35, 26, 0.75)',
    borderRadius: '24px',
    confirmButtonColor: '#50C878',
    cancelButtonColor: '#333333',
    color: '#333333',
    background: '#FFFFFF',
    customClass: {
        title: 'fw-bold',
        popup: 'shadow-lg border-0 rounded-4'
    }
};

// ====================================================
// 1. NORMALISASI NOMOR HP (MEMASTIKAN AWALAN 08...)
// ====================================================
function formatNomorHPIndonesia(input) {
    if (!input) return '';
    let clean = input.toString().replace(/[^0-9]/g, '');
    if (clean.startsWith('62')) {
        clean = '0' + clean.slice(2);
    } else if (clean.startsWith('8')) {
        clean = '0' + clean;
    }
    return clean;
}

// ====================================================
// 2. DATA MASTER: 154 WILAYAH (KECAMATAN & KELURAHAN)
// ====================================================
const DATA_WILAYAH_SURABAYA = [
    "LUAR SURABAYA",
    "(Asemrowo) Asemrowo", "(Asemrowo) Genting Kalianak", "(Asemrowo) Tambak Sarioso",
    "(Benowo) Kandangan", "(Benowo) Romokalisari", "(Benowo) Sememi", "(Benowo) Tambak Oso Wilangon",
    "(Bubutan) Alon-Alon Contong", "(Bubutan) Bubutan", "(Bubutan) Gundih", "(Bubutan) Jepara", "(Bubutan) Tembok Dukuh",
    "(Bulak) Bulak", "(Bulak) Kedung Cowek", "(Bulak) Kenjeran", "(Bulak) Sukolilo Baru",
    "(Dukuh Pakis) Dukuh Kupang", "(Dukuh Pakis) Dukuh Pakis", "(Dukuh Pakis) Gunungsari", "(Dukuh Pakis) Pradahkali Kendal",
    "(Gayungan) Dukuh Menanggal", "(Gayungan) Gayungan", "(Gayungan) Ketintang", "(Gayungan) Menanggal",
    "(Genteng) Embong Kaliasin", "(Genteng) Genteng", "(Genteng) Kapasari", "(Genteng) Ketabang", "(Genteng) Peneleh",
    "(Gubeng) Airlangga", "(Gubeng) Baratajaya", "(Gubeng) Gubeng", "(Gubeng) Kertajaya", "(Gubeng) Mojo", "(Gubeng) Pucang Sewu",
    "(Gunung Anyar) Gunung Anyar", "(Gunung Anyar) Gunung Anyar Tambak", "(Gunung Anyar) Rungkut Menanggal", "(Gunung Anyar) Rungkut Tengah",
    "(Jambangan) Jambangan", "(Jambangan) Karah", "(Jambangan) Kebonsari", "(Jambangan) Pagesangan",
    "(Karang Pilang) Karang Pilang", "(Karang Pilang) Kebraon", "(Karang Pilang) Kedurus", "(Karang Pilang) Warugunung",
    "(Kenjeran) Bulak Banteng", "(Kenjeran) Sidotopo Wetan", "(Kenjeran) Tambak Wedi", "(Kenjeran) Tanah Kali Kedinding",
    "(Krembangan) Dupak", "(Krembangan) Kemayoran", "(Krembangan) Krembangan Selatan", "(Krembangan) Morokrembangan", "(Krembangan) Perak Barat",
    "(Lakarsantri) Bangkingan", "(Lakarsantri) Jeruk", "(Lakarsantri) Lakarsantri", "(Lakarsantri) Lidah Kulon", "(Lakarsantri) Lidah Wetan", "(Lakarsantri) Sumur Welut",
    "(Mulyorejo) Dukuh Sutorejo", "(Mulyorejo) Kalijudan", "(Mulyorejo) Kalisari", "(Mulyorejo) Kejawen Putih Tambak", "(Mulyorejo) Manyar Sabrangan", "(Mulyorejo) Mulyorejo",
    "(Pabean Cantian) Bongkaran", "(Pabean Cantian) Krembangan Utara", "(Pabean Cantian) Nyamplungan", "(Pabean Cantian) Perak Timur", "(Pabean Cantian) Perak Utara",
    "(Pakal) Babat Jerawat", "(Pakal) Benowo", "(Pakal) Pakal", "(Pakal) Sumberrejo",
    "(Rungkut) Kali Rungkut", "(Rungkut) Kedung Baruk", "(Rungkut) Medokan Ayu", "(Rungkut) Penjaringan Sari", "(Rungkut) Rungkut Kidul", "(Rungkut) Wonorejo Rungkut",
    "(Sambikerep) Bringin", "(Sambikerep) Lontar", "(Sambikerep) Made", "(Sambikerep) Sambikerep",
    "(Sawahan) Banyu Urip", "(Sawahan) Kupang Krajan", "(Sawahan) Pakis", "(Sawahan) Petemon", "(Sawahan) Putat Jaya", "(Sawahan) Sawahan",
    "(Semampir) Ampel", "(Semampir) Pegirian", "(Semampir) Sidotopo", "(Semampir) Ujung", "(Semampir) Wonokusumo",
    "(Simokerto) Kapasan", "(Simokerto) Sidodadi", "(Simokerto) Simokerto", "(Simokerto) Simolawang", "(Simokerto) Tambakrejo",
    "(Suko Manunggal) Putat Gede", "(Suko Manunggal) Simomulyo", "(Suko Manunggal) Simomulyo Baru", "(Suko Manunggal) Sono Kwijenan", "(Suko Manunggal) Suko Manunggal", "(Suko Manunggal) Tanjungsari",
    "(Sukolilo) Gebang Putih", "(Sukolilo) Keputih", "(Sukolilo) Klampis Ngasem", "(Sukolilo) Medokan Semampir", "(Sukolilo) Menur Pumpungan", "(Sukolilo) Ngiden Jangkungan", "(Sukolilo) Semolowaru",
    "(Tambaksari) Dukuh Setro", "(Tambaksari) Gading", "(Tambaksari) Kapasmadya Baru", "(Tambaksari) Pacar Keling", "(Tambaksari) Pacar Kembang", "(Tambaksari) Ploso", "(Tambaksari) Rangkah", "(Tambaksari) Tambaksari",
    "(Tandes) Balongsari", "(Tandes) Banjar Sugihan", "(Tandes) Karangpoh", "(Tandes) Manukan Kulon", "(Tandes) Manukan Wetan", "(Tandes) Tandes",
    "(Tegalsari) Dr. Sutomo", "(Tegalsari) Kedungdoro", "(Tegalsari) Keputran", "(Tegalsari) Tegalsari", "(Tegalsari) Wonorejo Tegalsari",
    "(Tenggilis Mejoyo) Kendangsari", "(Tenggilis Mejoyo) Kutisari", "(Tenggilis Mejoyo) Panjang Jiwo", "(Tenggilis Mejoyo) Tenggilis Mejoyo",
    "(Wiyung) Babatan", "(Wiyung) Balas Klumprik", "(Wiyung) Jajar Tunggal", "(Wiyung) Wiyung",
    "(Wonocolo) Bendul Merisi", "(Wonocolo) Jemur Wonosari", "(Wonocolo) Margorejo", "(Wonocolo) Sidosermo", "(Wonocolo) Siwalankerto",
    "(Wonokromo) Darmo", "(Wonokromo) Jagir", "(Wonokromo) Ngagel", "(Wonokromo) Ngagelrejo", "(Wonokromo) Sawunggaling", "(Wonokromo) Wonokromo"
];

// ====================================================
// 3. DATA MASTER: 117 DAFTAR PEKERJAAN
// ====================================================
const DATA_PEKERJAAN = [
    "ADMINISTRASI", "AGEN46", "AHLI GIZI", "APOTEKER", "ARSITEK", "ARTIS", "ATLET", "BIARAWATI", "BIDAN",
    "BURUH BONGKAR MUAT/BAGASI", "BURUH HARIAN LEPAS", "BURUH NELAYAN/PERIKANAN", "BURUH PETERNAKAN",
    "BURUH TANI/PERKEBUNAN", "DOKTER", "DOKTER GIGI", "DOSEN", "FISIKAWAN MEDIK", "GURU", "IMAM MESJID",
    "JURU MASAK", "JURU PARKIR", "KONSULTAN", "LOGISTIK", "MARBOT MESJID", "MEKANIK", "MITRA GOJEK",
    "MITRA GOJEK-GO LIFE", "MITRA GRAB", "MITRA SHOPEE", "MITRA TELEPORT AIRASIA", "MITRA UBER",
    "NARAPIDANA DALAM PROSES ASIMILASI", "NELAYAN/PERIKANAN", "NOTARIS", "PARAJI", "PARANORMAL", "PASTOR",
    "PEDAGANG", "PEKERJA BAKAT DAN MINAT", "PEKERJA MAGANG", "PELAUT", "PEMANDU LAGU", "PEMASAR IKAN",
    "PEMASAR PELABUHAN", "PEMBANTU RUMAH TANGGA", "PEMBUDIDAYA IKAN", "PEMULUNG", "PENATA BUSANA",
    "PENATA RAMBUT", "PENATA RIAS", "PENDAMPING DESA", "PENDETA", "PENELITI", "PENGACARA", "PENGOLAH IKAN",
    "PENTERJEMAH", "PENYIAR RADIO", "PERANCANG BUSANA", "PERAWAT", "PEREKAM MEDIK DAN INFOKES", "PERISAI",
    "PETAMBAK GARAM", "PETANI/PEKEBUN", "PETERNAK", "PETUGAS KEAMANAN", "PIALANG", "PROMOTOR ACARA",
    "PSIKIATER/PSIKOLOG", "PSIKOLOGI KLINIS", "RADIOGRAFER", "RELAWAN TAGANA/RELAWAN BENCANA", "SEKRETARIS",
    "SENIMAN", "SISWA KERJA PRAKTEK", "SOPIR", "TABIB", "TEKNISI LAB MEDIK",
    "TENAGA HONORER (SELAIN PENYELENGGARA NEGARA)", "TENAGA KESEHATAN LINGKUNGAN", "TENAGA TEKNIS KEFARMASIAN",
    "TRANSPORTASI", "TUKANG BATU", "TUKANG CUKUR", "TUKANG GIGI", "TUKANG JAHIT", "TUKANG KAYU",
    "TUKANG LAS/PANDAI BESI", "TUKANG LISTRIK", "TUKANG PIJAT", "TUKANG SAMPAH", "TUKANG SOL SEPATU",
    "USTADZ/MUBALIGH", "WARTAWAN", "WIRASWASTA", "MENGURUS RUMAH TANGGA", "MAHASISWA", "PELAJAR",
    "PENSIUNAN", "BELUM / TIDAK BEKERJA", "KARYAWAN SWASTA", "PRAMUNIAGA / KASIR / SPG",
    "TENAGA PEMASARAN / SALES", "KURIR / PENGANTAR PAKET", "AKUNTAN", "MANAJER / DIREKTUR PERUSAHAAN",
    "PENGUSAHA", "AGEN ASURANSI / AGEN PROPERTI", "PRAMUGARA / PRAMUGARI", "PEMANDU WISATA",
    "TERAPIS KESEHATAN / KECANTIKAN", "AKTIVIS / PEKERJA SOSIAL",
    "PEMBUAT KONTEN (Content Creator / Youtuber / Influencer)", "DESAINER GRAFIS / VISUAL",
    "PROGRAMMER / PENGEMBANG IT", "FOTOGRAFER / VIDEOGRAFER", "PENULIS / COPYWRITER"
];

// ====================================================
// 4. MANAJEMEN CACHE & REFRESH
// ====================================================
function refreshData() {
    Swal.fire({
        ...swalConfig,
        title: 'Memperbarui...',
        text: 'Menyinkronkan data terbaru.',
        icon: 'info',
        timer: 1000,
        showConfirmButton: false
    }).then(() => {
        window.location.reload(true);
    });
}

function clearCacheAndRefresh() {
    Swal.fire({
        ...swalConfig,
        title: 'Pembersihan Sistem',
        text: 'Aplikasi akan disegarkan ke versi paling mutakhir.',
        icon: 'success',
        timer: 1500,
        showConfirmButton: false,
        confirmButtonColor: '#FFB703'
    }).then(() => {
        localStorage.clear();
        sessionStorage.clear();
        window.location.reload(true);
    });
}

// ====================================================
// 5. KOMPRESOR GAMBAR CERDAS (KTP & KK CEPAT ANTI-GAGAL)
// ====================================================
function compressAndGetBase64(file, maxWidth = 1400, quality = 0.8) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = (event) => {
            const img = new Image();
            img.src = event.target.result;
            img.onload = () => {
                const canvas = document.createElement('canvas');
                let width = img.width;
                let height = img.height;
                if (width > maxWidth) {
                    height = Math.round((height * maxWidth) / width);
                    width = maxWidth;
                }
                canvas.width = width;
                canvas.height = height;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0, width, height);
                const dataUrl = canvas.toDataURL('image/jpeg', quality);
                resolve({
                    mime: 'image/jpeg',
                    base64: dataUrl.split(',')[1]
                });
            };
            img.onerror = (err) => reject(err);
        };
        reader.onerror = (err) => reject(err);
    });
}

// ====================================================
// 6. INJEKSI UI MODAL POP-UP PKB KE SELURUH HALAMAN
// ====================================================
function injectPKBModalSystem() {
    if (document.getElementById('pkb-modal-overlay')) return;

    const modalHTML = `
    <div id="pkb-modal-overlay" class="pkb-modal-backdrop">
        <div class="pkb-modal-box">
            <div class="pkb-modal-header">
                <div>
                    <span class="badge bg-warning text-dark fw-bold mb-1"><i class="bi bi-flag-fill me-1"></i> DPAC PKB KECAMATAN RUNGKUT</span>
                    <h4 class="m-0 fw-bold">Pendaftaran Kader PKB Surabaya</h4>
                </div>
                <button type="button" onclick="closePKBModal()" class="btn btn-light rounded-circle fw-bold" style="width:40px;height:40px;"><i class="bi bi-x-lg"></i></button>
            </div>

            <div class="pkb-modal-body">
                <!-- TAHAP 1: INFORMASI & POSTER pkb 1.webp -->
                <div id="pkb-step-info">
                    <div class="pkb-poster-wrapper">
                        <img src="assets/pkb 1.webp" alt="Pendaftaran Kader PKB Surabaya" class="pkb-poster-img" onclick="showPKBFormStep()" onerror="this.style.display='none'">
                    </div>

                    <div class="text-center mb-4">
                        <h4 class="fw-bold text-emerald mb-2">Layanan Pendaftaran Kader PKB Kecamatan Rungkut</h4>
                        <p class="text-muted mb-0">Mari bergabung dalam barisan perjuangan akar rumput bersama <strong>Mas Uuth</strong>. Berikut manfaat nyata yang akan Anda dapatkan:</p>
                    </div>

                    <div class="row g-2 mb-4">
                        <div class="col-md-6">
                            <div class="pkb-benefit-item h-100">
                                <strong class="text-dark d-block"><i class="bi bi-person-badge-fill text-emerald me-2"></i>1. KTA Partai Kebangkitan Bangsa</strong>
                                <small class="text-muted">Kartu Tanda Anggota resmi sebagai identitas kader penggerak.</small>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="pkb-benefit-item h-100">
                                <strong class="text-dark d-block"><i class="bi bi-building-check text-emerald me-2"></i>2. Aksesibilitas Stakeholder Surabaya</strong>
                                <small class="text-muted">Jalur komunikasi strategis dengan pemangku kebijakan Kota Surabaya.</small>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="pkb-benefit-item h-100">
                                <strong class="text-dark d-block"><i class="bi bi-people-fill text-emerald me-2"></i>3. Jaringan Pertemanan Berkualitas</strong>
                                <small class="text-muted">Relasi solid lintas profesi, tokoh masyarakat, pemuda, dan wirausaha.</small>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="pkb-benefit-item h-100">
                                <strong class="text-dark d-block"><i class="bi bi-award-fill text-emerald me-2"></i>4. Pelatihan Peningkatan Diri</strong>
                                <small class="text-muted">Beragam program pengembangan kapasitas kepemimpinan dan keahlian.</small>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="pkb-benefit-item h-100">
                                <strong class="text-dark d-block"><i class="bi bi-heart-pulse-fill text-danger me-2"></i>5. Layanan Ambulance</strong>
                                <small class="text-muted">Bantuan darurat transportasi kesehatan bagi warga yang membutuhkan dengan respons cepat ke fasilitas medis terdekat.</small>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="pkb-benefit-item h-100">
                                <strong class="text-dark d-block"><i class="bi bi-bus-front-fill text-warning me-2"></i>6. Layanan Hiace & Bus</strong>
                                <small class="text-muted">Fasilitas mobilitas komunal warga untuk menunjang kegiatan sosial, keagamaan, ziarah, maupun keperluan bersama lainnya.</small>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="pkb-benefit-item h-100">
                                <strong class="text-dark d-block"><i class="bi bi-mortarboard-fill text-primary me-2"></i>7. Advokasi Pendidikan</strong>
                                <small class="text-muted">Mengawal hak-hak pendidikan siswa SD-SMA agar tepat sasaran dan memastikan akses merata tanpa dipersulit birokrasi.</small>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="pkb-benefit-item h-100">
                                <strong class="text-dark d-block"><i class="bi bi-shop text-emerald me-2"></i>8. Penguatan UMKM</strong>
                                <small class="text-muted">Pemberdayaan ekonomi warga melalui mentoring bisnis terstruktur dan pemanfaatan digital marketing dari Mas Uuth.</small>
                            </div>
                        </div>
                        <div class="col-12">
                            <div class="pkb-benefit-item">
                                <strong class="text-dark d-block"><i class="bi bi-diagram-3-fill text-emerald me-2"></i>9. Sinergi Parlemen</strong>
                                <small class="text-muted">Menjembatani aspirasi akar rumput. Kolaborasi aktif dengan program DPRD Fraksi PKB dari tingkat Kota hingga Pusat untuk eksekusi kebijakan nyata.</small>
                            </div>
                        </div>
                    </div>

                    <div class="d-grid gap-2">
                        <button type="button" onclick="showPKBFormStep()" class="btn btn-primary-custom py-3 fs-5">
                            <i class="bi bi-pencil-square me-2"></i> Daftar Menjadi Kader PKB Sekarang
                        </button>
                        <button type="button" onclick="closePKBModal()" class="btn btn-light rounded-pill py-2 text-muted fw-semibold">
                            Nanti Saja / Tutup
                        </button>
                    </div>
                </div>

                <!-- TAHAP 2: FORMULIR PENDAFTARAN KADER PKB -->
                <div id="pkb-step-form" style="display:none;">
                    <div class="d-flex justify-content-between align-items-center mb-3 pb-2 border-bottom">
                        <button type="button" onclick="showPKBInfoStep()" class="btn btn-sm btn-outline-secondary rounded-pill px-3">
                            <i class="bi bi-arrow-left me-1"></i> Kembali ke Info Manfaat
                        </button>
                        <span class="badge bg-success-subtle text-success border border-success-subtle px-3 py-2 rounded-pill">
                            <i class="bi bi-shield-lock-fill me-1"></i> Data Dijamin Rahasia
                        </span>
                    </div>

                    <form id="formPendaftaranPKB" novalidate>
                        <div class="row g-3">
                            <div class="col-md-6">
                                <label class="form-label fw-bold text-emerald small mb-1">NIK (16 Digit Sesuai KTP) <span class="text-danger">*</span></label>
                                <input type="tel" inputmode="numeric" maxlength="16" id="pkb-nik" class="form-control" placeholder="Contoh: 357810xxxxxxxxxx" required>
                            </div>
                            <div class="col-md-6">
                                <label class="form-label fw-bold text-emerald small mb-1">Nama Lengkap <span class="text-danger">*</span></label>
                                <input type="text" id="pkb-nama" class="form-control" placeholder="Nama lengkap sesuai KTP" required>
                            </div>

                            <div class="col-md-6">
                                <label class="form-label fw-bold text-emerald small mb-1">Jenis Kelamin <span class="text-danger">*</span></label>
                                <select id="pkb-jk" class="form-select" required>
                                    <option value="">-- Pilih Jenis Kelamin --</option>
                                    <option value="Laki-laki">Laki-laki</option>
                                    <option value="Perempuan">Perempuan</option>
                                </select>
                            </div>
                            <div class="col-md-6">
                                <label class="form-label fw-bold text-emerald small mb-1">Nomor HP / WhatsApp Aktif <span class="text-danger">*</span></label>
                                <input type="tel" inputmode="numeric" id="pkb-hp" class="form-control" placeholder="Contoh: 081339760265" required>
                            </div>

                            <div class="col-md-8">
                                <label class="form-label fw-bold text-emerald small mb-1">Alamat Jalan <span class="text-danger">*</span></label>
                                <input type="text" id="pkb-alamat" class="form-control" placeholder="Contoh: Jl. Raya Rungkut Mapan Blok FA No. 12" required>
                            </div>
                            <div class="col-6 col-md-2">
                                <label class="form-label fw-bold text-emerald small mb-1">RT <span class="text-danger">*</span></label>
                                <input type="tel" inputmode="numeric" maxlength="4" id="pkb-rt" class="form-control" placeholder="001" required>
                            </div>
                            <div class="col-6 col-md-2">
                                <label class="form-label fw-bold text-emerald small mb-1">RW <span class="text-danger">*</span></label>
                                <input type="tel" inputmode="numeric" maxlength="4" id="pkb-rw" class="form-control" placeholder="002" required>
                            </div>

                            <!-- SEARCHABLE DROPDOWN WILAYAH -->
                            <div class="col-12">
                                <label class="form-label fw-bold text-emerald small mb-1">
                                    <i class="bi bi-search me-1"></i> Cari & Pilih Wilayah (Kecamatan & Kelurahan) <span class="text-danger">*</span>
                                </label>
                                <div class="searchable-select-wrapper">
                                    <input type="text" id="pkb-wilayah-search" class="form-control border-success" placeholder="Ketik nama Kelurahan atau Kecamatan (Contoh: Rungkut / Medokan Ayu)..." autocomplete="off" required>
                                    <div id="pkb-wilayah-list" class="searchable-dropdown-list"></div>
                                </div>
                                <small class="text-muted">Ketik untuk mencari, lalu klik wilayah Anda. Kolom Kelurahan & Kecamatan di bawah akan terisi otomatis.</small>
                            </div>

                            <div class="col-md-6">
                                <label class="form-label fw-bold text-secondary small mb-1">Kelurahan (Otomatis) <span class="text-danger">*</span></label>
                                <input type="text" id="pkb-kelurahan" class="form-control bg-light" placeholder="Terisi otomatis" readonly required>
                            </div>
                            <div class="col-md-6">
                                <label class="form-label fw-bold text-secondary small mb-1">Kecamatan (Otomatis) <span class="text-danger">*</span></label>
                                <input type="text" id="pkb-kecamatan" class="form-control bg-light" placeholder="Terisi otomatis" readonly required>
                            </div>

                            <!-- SEARCHABLE DROPDOWN PEKERJAAN -->
                            <div class="col-12">
                                <label class="form-label fw-bold text-emerald small mb-1">
                                    <i class="bi bi-briefcase-fill me-1"></i> Cari & Pilih Pekerjaan <span class="text-danger">*</span>
                                </label>
                                <div class="searchable-select-wrapper">
                                    <input type="text" id="pkb-pekerjaan" class="form-control border-success" placeholder="Ketik untuk mencari pekerjaan (Contoh: WIRASWASTA / GURU / MAHASISWA)..." autocomplete="off" required>
                                    <div id="pkb-pekerjaan-list" class="searchable-dropdown-list"></div>
                                </div>
                            </div>

                            <!-- AKUN LEBAH BERGERAK -->
                            <div class="col-12">
                                <div class="p-3 rounded-4" style="background: rgba(212, 160, 23, 0.08); border: 1px solid rgba(212, 160, 23, 0.35);">
                                    <div class="fw-bold text-dark mb-1" style="font-size: 0.98rem;">
                                        <i class="bi bi-hexagon-fill me-1" style="color: #d4a017;"></i> Akun Ekosistem Lebah Bergerak
                                    </div>
                                    <div class="text-muted small mb-2">
                                        Satu pendaftaran, dua manfaat. Password ini dipakai untuk masuk ke Lebah Bergerak. Rekening dipakai untuk pencairan poin.
                                    </div>
                                    <div class="row g-2">
                                        <div class="col-md-4">
                                            <label class="form-label fw-bold text-emerald small mb-1">Password Akun <span class="text-danger">*</span></label>
                                            <input type="password" id="pkb-password" class="form-control" minlength="6" placeholder="Minimal 6 karakter" autocomplete="new-password" required>
                                        </div>
                                        <div class="col-md-4">
                                            <label class="form-label fw-bold text-emerald small mb-1">Nama Bank <span class="text-danger">*</span></label>
                                            <input type="text" id="pkb-bank" class="form-control" placeholder="Contoh: BCA / BRI / MANDIRI" required>
                                        </div>
                                        <div class="col-md-4">
                                            <label class="form-label fw-bold text-emerald small mb-1">Nomor Rekening <span class="text-danger">*</span></label>
                                            <input type="tel" inputmode="numeric" id="pkb-rekening" class="form-control" placeholder="Contoh: 1234567890" required>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- UPLOAD KTP & KK -->
                            <div class="col-md-6">
                                <label class="form-label fw-bold text-emerald small mb-1"><i class="bi bi-person-vcard-fill me-1"></i> Upload Foto KTP <span class="text-danger">* (Wajib)</span></label>
                                <input type="file" id="pkb-file-ktp" accept="image/*" class="form-control" required>
                                <small class="text-muted">Format JPG/PNG/WebP. Tersimpan aman di Drive PKB.</small>
                            </div>
                            <div class="col-md-6">
                                <label class="form-label fw-bold text-emerald small mb-1"><i class="bi bi-file-earmark-medical-fill me-1"></i> Upload Foto KK <span class="text-muted">(Opsional / Tidak Wajib)</span></label>
                                <input type="file" id="pkb-file-kk" accept="image/*" class="form-control">
                                <small class="text-muted">Boleh dikosongkan jika belum tersedia.</small>
                            </div>

                            <!-- PERSETUJUAN GABUNG -->
                            <div class="col-12 mt-3">
                                <div class="p-3 rounded-4" style="background: rgba(80, 200, 120, 0.1); border: 1px solid rgba(80, 200, 120, 0.3);">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" id="pkb-setuju" value="Setuju" required style="transform: scale(1.25); margin-top: 5px;">
                                        <label class="form-check-label fw-semibold ms-2 text-dark" for="pkb-setuju" style="font-size: 0.92rem;">
                                            Saya menyatakan data di atas benar dan <strong>Setuju Bergabung</strong> menjadi Anggota / Kader Partai Kebangkitan Bangsa (PKB) Surabaya. Saya juga setuju terdaftar sebagai anggota ekosistem Lebah Bergerak dan data rekening saya dipakai untuk pencairan poin. <span class="text-danger">*</span>
                                        </label>
                                    </div>
                                </div>
                            </div>

                            <div class="col-12 mt-4">
                                <button type="submit" class="btn btn-primary-custom w-100 py-3 fs-5">
                                    <i class="bi bi-send-check-fill me-2"></i> Kirim Pendaftaran Kader PKB
                                </button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>`;

    document.body.insertAdjacentHTML('beforeend', modalHTML);

    // Pasang Event Searchable Dropdown Wilayah
    setupSearchableDropdown(
        'pkb-wilayah-search',
        'pkb-wilayah-list',
        DATA_WILAYAH_SURABAYA,
        (selectedVal) => {
            if (selectedVal === 'LUAR SURABAYA') {
                document.getElementById('pkb-kecamatan').value = 'LUAR SURABAYA';
                document.getElementById('pkb-kelurahan').value = 'LUAR SURABAYA';
            } else {
                const match = selectedVal.match(/^\(([^)]+)\)\s*(.+)$/);
                if (match) {
                    document.getElementById('pkb-kecamatan').value = match[1].trim();
                    document.getElementById('pkb-kelurahan').value = match[2].trim();
                } else {
                    document.getElementById('pkb-kecamatan').value = selectedVal;
                    document.getElementById('pkb-kelurahan').value = selectedVal;
                }
            }
        }
    );

    // Pasang Event Searchable Dropdown Pekerjaan
    setupSearchableDropdown(
        'pkb-pekerjaan',
        'pkb-pekerjaan-list',
        DATA_PEKERJAAN,
        (selectedJob) => {
            document.getElementById('pkb-pekerjaan').value = selectedJob;
        }
    );

    // Pasang Event Submit Form Pendaftaran PKB
    document.getElementById('formPendaftaranPKB').addEventListener('submit', handlePKBSubmit);
}

function setupSearchableDropdown(inputId, listId, dataArray, onSelectCallback) {
    const inputEl = document.getElementById(inputId);
    const listEl = document.getElementById(listId);

    function renderList(filterText = '') {
        listEl.innerHTML = '';
        const q = filterText.toLowerCase().trim();
        const filtered = dataArray.filter(item => item.toLowerCase().includes(q));

        if (filtered.length === 0) {
            listEl.innerHTML = `<div class="p-3 text-muted small text-center">Data tidak ditemukan.</div>`;
        } else {
            filtered.forEach(item => {
                const div = document.createElement('div');
                div.className = 'searchable-dropdown-item';
                div.textContent = item;
                div.addEventListener('mousedown', (e) => {
                    e.preventDefault();
                    inputEl.value = item;
                    listEl.style.display = 'none';
                    if (onSelectCallback) onSelectCallback(item);
                });
                div.addEventListener('click', () => {
                    inputEl.value = item;
                    listEl.style.display = 'none';
                    if (onSelectCallback) onSelectCallback(item);
                });
                listEl.appendChild(div);
            });
        }
        listEl.style.display = 'block';
    }

    inputEl.addEventListener('focus', () => renderList(inputEl.value));
    inputEl.addEventListener('input', () => renderList(inputEl.value));
    inputEl.addEventListener('blur', () => {
        setTimeout(() => { listEl.style.display = 'none'; }, 200);
    });
}

// Fungsi Navigasi Modal PKB
window.openPKBModal = function(directToForm = false) {
    const overlay = document.getElementById('pkb-modal-overlay');
    if (!overlay) return;
    overlay.style.display = 'flex';
    document.body.style.overflow = 'hidden';
    if (directToForm) {
        showPKBFormStep();
    } else {
        showPKBInfoStep();
    }
};

window.closePKBModal = function() {
    const overlay = document.getElementById('pkb-modal-overlay');
    if (overlay) overlay.style.display = 'none';
    document.body.style.overflow = 'auto';
};

window.showPKBFormStep = function() {
    document.getElementById('pkb-step-info').style.display = 'none';
    document.getElementById('pkb-step-form').style.display = 'block';
};

window.showPKBInfoStep = function() {
    document.getElementById('pkb-step-form').style.display = 'none';
    document.getElementById('pkb-step-info').style.display = 'block';
};

// ====================================================
// 7. PROSES SUBMIT FORMULIR KADER PKB
// ====================================================
async function handlePKBSubmit(e) {
    e.preventDefault();

    const nik = document.getElementById('pkb-nik').value.replace(/[^0-9]/g, '').trim();
    const nama = document.getElementById('pkb-nama').value.trim();
    const jk = document.getElementById('pkb-jk').value;
    const hpRaw = document.getElementById('pkb-hp').value.trim();
    const hp = formatNomorHPIndonesia(hpRaw);
    const alamat = document.getElementById('pkb-alamat').value.trim();
    const rt = document.getElementById('pkb-rt').value.replace(/[^0-9]/g, '').trim();
    const rw = document.getElementById('pkb-rw').value.replace(/[^0-9]/g, '').trim();
    const kelurahan = document.getElementById('pkb-kelurahan').value.trim();
    const kecamatan = document.getElementById('pkb-kecamatan').value.trim();
    const pekerjaan = document.getElementById('pkb-pekerjaan').value.trim();
    const password = document.getElementById('pkb-password').value;
    const bank = document.getElementById('pkb-bank').value.trim();
    const rekening = document.getElementById('pkb-rekening').value.replace(/[^0-9]/g, '').trim();
    const fileKTP = document.getElementById('pkb-file-ktp').files[0];
    const fileKK = document.getElementById('pkb-file-kk').files[0];
    const setuju = document.getElementById('pkb-setuju').checked;

    // Validasi Ketat Semua Kolom Wajib (KK Tidak Wajib)
    if (nik.length !== 16) {
        return Swal.fire({ ...swalConfig, icon: 'warning', title: 'NIK Belum Sesuai', text: 'Mohon masukkan 16 digit angka NIK sesuai KTP Anda.' });
    }
    if (!nama || !jk || !hp || !alamat || !rt || !rw) {
        return Swal.fire({ ...swalConfig, icon: 'warning', title: 'Data Belum Lengkap', text: 'Seluruh kolom identitas dan alamat (Jalan, RT, RW) wajib diisi.' });
    }
    if (!kelurahan || !kecamatan) {
        return Swal.fire({ ...swalConfig, icon: 'warning', title: 'Wilayah Belum Dipilih', text: 'Silakan cari dan klik pilihan Kelurahan & Kecamatan dari daftar.' });
    }
    if (!pekerjaan || !DATA_PEKERJAAN.includes(pekerjaan.toUpperCase())) {
        return Swal.fire({ ...swalConfig, icon: 'warning', title: 'Pilih Pekerjaan', text: 'Silakan klik salah satu pekerjaan yang tersedia di daftar pencarian.' });
    }
    if (!fileKTP) {
        return Swal.fire({ ...swalConfig, icon: 'warning', title: 'Foto KTP Wajib Diunggah', text: 'Mohon lampirkan foto KTP Anda untuk verifikasi keanggotaan.' });
    }
    if (password.length < 6) {
        return Swal.fire({ ...swalConfig, icon: 'warning', title: 'Password Terlalu Pendek', text: 'Buat password minimal 6 karakter untuk akun Lebah Bergerak Anda.' });
    }
    if (!bank || rekening.length < 8) {
        return Swal.fire({ ...swalConfig, icon: 'warning', title: 'Data Rekening Belum Lengkap', text: 'Isi nama bank dan nomor rekening agar poin Anda bisa dicairkan.' });
    }
    if (!setuju) {
        return Swal.fire({ ...swalConfig, icon: 'warning', title: 'Konfirmasi Persetujuan', text: 'Mohon centang pernyataan Setuju Bergabung terlebih dahulu.' });
    }

    Swal.fire({
        ...swalConfig,
        title: 'Mendaftarkan Kader...',
        html: 'Menyimpan data, mengunggah KTP, dan menyiapkan akun Lebah Bergerak.<br><b>Mohon tunggu sebentar...</b>',
        allowOutsideClick: false,
        didOpen: () => { Swal.showLoading(); }
    });

    const acak = () => Math.random().toString(36).slice(2, 8);

    const unggahBerkas = async (awalan, file) => {
        const ext = (file.name.split('.').pop() || 'jpg').toLowerCase().replace(/[^a-z0-9]/g, '') || 'jpg';
        const path = `pkb/${nik}-${awalan}-${Date.now()}-${acak()}.${ext}`;
        const res = await fetch(`${SUPA_URL}/storage/v1/object/berkas_kader/${path}`, {
            method: 'POST',
            headers: {
                apikey: SUPA_ANON,
                Authorization: `Bearer ${SUPA_ANON}`,
                'Content-Type': file.type || 'application/octet-stream'
            },
            body: file
        });
        if (!res.ok) {
            throw new Error('Unggah berkas gagal (' + res.status + '). Periksa ukuran foto lalu coba lagi.');
        }
        return path;
    };

    try {
        const ktpPath = await unggahBerkas('ktp', fileKTP);
        let kkPath = null;
        if (fileKK) {
            kkPath = await unggahBerkas('kk', fileKK);
        }

        const res = await fetch(`${SUPA_URL}/rest/v1/rpc/daftar_kader_pkb`, {
            method: 'POST',
            headers: {
                apikey: SUPA_ANON,
                Authorization: `Bearer ${SUPA_ANON}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                p_nik: nik,
                p_nama: nama,
                p_jk: jk,
                p_hp: hp,
                p_alamat: alamat,
                p_rt: rt,
                p_rw: rw,
                p_kelurahan: kelurahan,
                p_kecamatan: kecamatan,
                p_pekerjaan: pekerjaan.toUpperCase(),
                p_password: password,
                p_bank_name: bank,
                p_bank_number: rekening,
                p_ktp_path: ktpPath,
                p_kk_path: kkPath
            })
        });

        const hasil = await res.json().catch(() => ({ ok: false, pesan: 'Jawaban server tidak terbaca.' }));
        if (!res.ok || !hasil.ok) {
            throw new Error(hasil.pesan || 'Pendaftaran ditolak server.');
        }

        // Arsip ke Google Sheet PKB, jalan di latar dan tidak menentukan hasil
        compressAndGetBase64(fileKTP).then((ktpData) => {
            const payload = {
                tipe: 'Pendaftaran Kader PKB',
                nik: nik,
                nama_lengkap: nama,
                jenis_kelamin: jk,
                no_hp: hp,
                alamat_jalan: alamat,
                rt: rt,
                rw: rw,
                kelurahan: kelurahan,
                kecamatan: kecamatan,
                pekerjaan: pekerjaan.toUpperCase(),
                setuju_gabung: 'Setuju',
                id_kader_lebah: hasil.id_kader,
                bank: bank,
                nomor_rekening: rekening,
                ktpBase64: ktpData.base64,
                ktpMime: ktpData.mime
            };
            fetch(scriptURL, {
                method: 'POST',
                mode: 'no-cors',
                headers: { 'Content-Type': 'text/plain;charset=utf-8' },
                body: JSON.stringify(payload)
            }).catch(() => {});
        }).catch(() => {});

        closePKBModal();
        const form = document.getElementById('formPendaftaranPKB');
        if (form) form.reset();

        Swal.fire({
            ...swalConfig,
            icon: 'success',
            title: 'Pendaftaran Berhasil',
            html: `
                <div class="p-2">
                    <p class="mb-2" style="font-size: 1rem; line-height: 1.6;">
                        Selamat, <b>${hasil.nama}</b>. Anda terdaftar sebagai Kader PKB Surabaya dan otomatis menjadi anggota ekosistem Lebah Bergerak.
                    </p>
                    <div class="p-3 rounded-4 text-start" style="background: #f4f6f5; border: 1px solid #dfe6e1;">
                        <div class="small text-muted">ID Kader</div>
                        <div class="fw-bold" style="font-size: 1.15rem; letter-spacing: 0.5px;">${hasil.id_kader}</div>
                        <div class="small text-muted mt-2">Login memakai NIK dan password yang Anda buat tadi.</div>
                        <div class="small text-muted">Bonus awal ${hasil.konekta_points} poin sudah masuk.</div>
                    </div>
                    <p class="mt-3 mb-0 small text-muted">Simpan ID ini. Data Anda disimpan di database PKB Surabaya.</p>
                </div>
            `,
            confirmButtonText: 'Buka Lebah Bergerak',
            showCancelButton: true,
            cancelButtonText: 'Nanti saja'
        }).then((r) => {
            if (r.isConfirmed) {
                window.open('https://lebahbergerak.fun/', '_blank');
            }
        });

    } catch (error) {
        console.error('PKB Submit Error:', error);
        Swal.fire({
            ...swalConfig,
            icon: 'error',
            title: 'Pendaftaran Gagal',
            text: error.message || 'Terjadi kendala jaringan. Silakan coba lagi.'
        });
    }
}

// ====================================================
// 8. AUTO-INIT SAAT HALAMAN DIMUAT
// ====================================================
document.addEventListener("DOMContentLoaded", () => {
    injectPKBModalSystem();

    // Tampilkan Pop-up Informasi PKB otomatis (kecuali jika sedang membuka CMS di halaman berita)
    if (!sessionStorage.getItem('pkb_popup_shown')) {
        setTimeout(() => {
            openPKBModal(false);
            sessionStorage.setItem('pkb_popup_shown', 'true');
        }, 700);
    }
});