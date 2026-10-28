#!/usr/bin/env python3
"""Render halaman SOKABAT NU · SIMULASI PEMILU 2029.
Tampilan mengikuti bahasa desain halaman kampanye: latar terang, kartu putih, hijau dan emas.
"""
import json, html, pathlib

BASE = pathlib.Path('/home/buleng/.hermes/projects/sokabatnu/kampanye')
D = json.loads((BASE / 'data' / 'simulasi-2029.json').read_text())
M, A, B = D['meta'], D['A'], D['B']

def n(x):
    return f"{int(x):,}".replace(',', '.')

def pct(x):
    return f"{x:.2f}".replace('.', ',') + '%'

def pct1(x):
    return f"{x:.1f}".replace('.', ',') + '%'

def e(s):
    return html.escape(str(s))

LABEL = {'menang': 'Menang', 'bersaing': 'Bisa bersaing', 'jangan': 'Jangan sentuh'}

def kelrow(k):
    chip = ''
    if k['dasar'] == 'kecamatan':
        chip = ' <span class="chip t-adjust">kecamatan</span>'
    pes = ' · '.join(f"{e(p['p'])} {pct1(p['sh'])}" for p in k['pesaing'])
    return (f'<div class="kelrow"><div class="kiri">'
            f'<div class="nm">{e(k["nama"].title())}{chip}</div>'
            f'<div class="meta">{e(k["kec"].title())} · PKB {n(k["pkb"])} suara</div>'
            f'<div class="pes">Pesaing: {pes}</div></div>'
            f'<div class="kanan"><b>{pct(k["share"])}</b><span>peringkat {k["rank"]}</span></div></div>')

def tier(d, t):
    isi = d['tier'][t]
    judul = LABEL[t]
    if not isi['n']:
        return f'<div class="sub2">{judul} · tidak ada kelurahan</div>'
    badan = ''.join(kelrow(k) for k in isi['kel'])
    if t == 'jangan':
        return (f'<details><summary class="sub2 ringkas">{judul} · {isi["n"]} kelurahan · '
                f'{n(isi["pkb"])} suara PKB</summary>{badan}</details>')
    return (f'<div class="sub2">{judul} · {isi["n"]} kelurahan · '
            f'{n(isi["pkb"])} suara PKB</div>{badan}')

def kartu(d, buka=False):
    return f'''<details class="dcard"{' open' if buka else ''}>
  <summary class="dhead"><div class="dn">Dapil {d['nomor']}
    <small>{e(', '.join(x.title() for x in d['kecamatan']))}</small></div>
    <div class="badge{' nol' if not d['pkb_kursi'] else ''}">{d['pkb_kursi']} dari {d['kursi']} kursi</div></summary>
  <div class="dbody">
    <div class="grid4">
      <div><span>Suara sah</span><b>{n(d['sah'])}</b></div>
      <div><span>Kuota kursi</span><b>{n(d['kuota'])}</b></div>
      <div><span>Kursi terakhir</span><b>{n(d['harga'])}</b></div>
      <div><span>Kursi berikutnya</span><b>{'+' + n(d['tambah']) if d['tambah'] else 'maksimal'}</b></div>
    </div>
    <div class="baris-isi"><span>Suara PKB</span><b>{n(d['pkb'])} · {pct(d['pkb_persen'])}</b></div>
    {tier(d, 'menang')}
    {tier(d, 'bersaing')}
    {tier(d, 'jangan')}
  </div>
</details>'''

def panel(sk, label):
    kartu_html = ''.join(kartu(d, buka=(d['nomor'] == 1)) for d in sk['dapil'])
    menang = sum(d['tier']['menang']['n'] for d in sk['dapil'])
    bersaing = sum(d['tier']['bersaing']['n'] for d in sk['dapil'])
    return f'''<section class="panel{' aktif' if label == 'A' else ''}" id="panel-{label}">
  <div class="kartu">
    <h2>Ringkasan skenario</h2>
    <p class="sub">Suara PKB 2024 dibagi ke konfigurasi dapil ini. Kursi dihitung Sainte-Lague, tanpa ambang parlemen.</p>
    <div class="stat">
      <div class="sel"><span>Suara PKB</span><b>{n(sk['pkb'])}</b><small>10,37% kota</small></div>
      <div class="sel emas"><span>Kursi PKB</span><b>{sk['pkb_kursi']}</b><small>dari {sk['kursi_total']} kursi</small></div>
      <div class="sel"><span>Kelurahan menang</span><b>{menang}</b><small>basis aman</small></div>
      <div class="sel"><span>Bisa bersaing</span><b>{bersaing}</b><small>peluang realistis</small></div>
    </div>
  </div>
  {kartu_html}
</section>'''

CSS = """
:root{
  --hijau:#0b6b45; --hijau-gelap:#04301f; --hijau-muda:#e8f5ee;
  --emas:#f6b93b; --emas-muda:#ffe6a6;
  --bg:#eef3f0; --kartu:#ffffff; --garis:#dbe5df;
  --teks:#0e1a15; --redup:#4e615a; --redup2:#7b8c85;
  --merah:#b3402f; --merah-muda:#fdeeea; --r:16px;
}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{margin:0;padding:0 0 36px;background:var(--bg);color:var(--teks);
     font-family:'Segoe UI',system-ui,-apple-system,sans-serif;display:flex;justify-content:center}
.bungkus{width:100%;max-width:620px;padding:14px 14px 0;display:flex;flex-direction:column;gap:13px}
.hero{position:relative;overflow:hidden;border-radius:20px;padding:22px 20px 18px;color:#fff;
      background:radial-gradient(120% 140% at 0% 0%,#0e7d51 0%,#04301f 62%);box-shadow:0 14px 30px rgba(4,48,31,.28)}
.hero::after{content:"";position:absolute;right:-52px;top:-46px;width:160px;height:160px;border-radius:50%;
             background:radial-gradient(circle,rgba(246,185,59,.34),transparent 70%)}
.hero .label{font-size:10.5px;letter-spacing:1.6px;font-weight:800;color:var(--emas-muda);text-transform:uppercase}
.hero h1{margin:7px 0 5px;font-size:25px;line-height:1.18;font-weight:900;letter-spacing:.2px;position:relative}
.hero h1 em{font-style:normal;color:var(--emas)}
.hero p{margin:0;font-size:12.5px;color:#cfe4d9;line-height:1.5;position:relative}
.hero-angka{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:16px;position:relative}
.hero-angka div{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.16);border-radius:12px;padding:9px 6px;text-align:center}
.hero-angka span{display:block;font-size:9px;letter-spacing:.7px;text-transform:uppercase;color:#bcd8ca;font-weight:800}
.hero-angka b{font-size:15px;font-weight:900}
.pilih{display:flex;gap:6px;position:sticky;top:0;z-index:30;padding:8px 0;
       background:linear-gradient(var(--bg) 74%,rgba(238,243,240,0))}
.pilih button{flex:1 1 0;padding:11px 10px;border:1px solid var(--garis);background:#fff;border-radius:12px;
              font-weight:800;font-size:11.5px;color:var(--redup);cursor:pointer;line-height:1.25;text-align:left}
.pilih button small{display:block;font-weight:700;font-size:9.5px;color:var(--redup2);margin-top:1px}
.pilih button.aktif{background:var(--hijau);border-color:var(--hijau);color:#fff;box-shadow:0 6px 14px rgba(11,107,69,.24)}
.pilih button.aktif small{color:#cfe9dc}
.kartu{background:var(--kartu);border-radius:var(--r);padding:16px;border:1px solid var(--garis);
       box-shadow:0 4px 12px rgba(14,26,21,.04)}
.kartu > h2{margin:0 0 4px;font-size:12px;letter-spacing:1px;text-transform:uppercase;color:var(--hijau);font-weight:900}
.kartu > .sub{margin:0 0 13px;font-size:11.5px;color:var(--redup2);line-height:1.45}
.stat{display:grid;grid-template-columns:1fr 1fr;gap:9px}
.stat .sel{background:#f7faf8;border:1px solid var(--garis);border-radius:12px;padding:11px;text-align:center}
.stat .sel span{display:block;font-size:9.5px;text-transform:uppercase;letter-spacing:.5px;font-weight:800;color:var(--redup2);margin-bottom:5px}
.stat .sel b{font-size:17px;font-weight:900;color:var(--hijau-gelap)}
.stat .sel small{display:block;font-size:9.5px;color:var(--redup2);font-weight:700;margin-top:3px}
.stat .sel.emas{background:#fffaf0;border-color:#f0dfb6}
.stat .sel.emas b{color:#8a6410}
.panel{display:none;flex-direction:column;gap:13px}
.panel.aktif{display:flex}
.dcard{border:1px solid var(--garis);border-radius:14px;overflow:hidden;background:#fff}
.dcard summary{list-style:none;cursor:pointer}
.dcard summary::-webkit-details-marker{display:none}
.dhead{display:flex;align-items:center;gap:10px;padding:12px 13px}
.dhead .dn{flex:1;font-size:13px;font-weight:900;line-height:1.3}
.dhead .dn small{display:block;font-size:10.5px;font-weight:700;color:var(--redup2);margin-top:2px}
.dhead .badge{background:var(--hijau-muda);color:#0a5236;border:1px solid #cfe6d9;border-radius:20px;
              padding:5px 9px;font-size:10.5px;font-weight:900;white-space:nowrap}
.dhead .badge.nol{background:#f4f6f5;color:#8b9a94;border-color:#e3eae6}
.dcard[open] .dhead{border-bottom:1px dashed var(--garis)}
.dbody{padding:0 13px 13px}
.grid4{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin:11px 0 8px}
.grid4 div{background:#f7faf8;border:1px solid var(--garis);border-radius:10px;padding:8px;text-align:center}
.grid4 span{display:block;font-size:9px;text-transform:uppercase;color:var(--redup2);font-weight:800;margin-bottom:3px}
.grid4 b{font-size:12.5px;font-weight:900}
.baris-isi{display:flex;justify-content:space-between;align-items:center;background:#fffdf4;border:1px solid #f3e3b8;
           border-radius:10px;padding:8px 10px;margin-bottom:4px}
.baris-isi span{font-size:9.5px;text-transform:uppercase;letter-spacing:.5px;font-weight:800;color:#8a6d1f}
.baris-isi b{font-size:12.5px;font-weight:900;color:#8a6410}
.sub2{font-size:10px;letter-spacing:.6px;text-transform:uppercase;color:var(--redup2);font-weight:900;margin:13px 0 4px}
summary.ringkas{cursor:pointer}
.kelrow{display:flex;gap:9px;padding:9px 0;border-bottom:1px dashed #e6ece8;align-items:flex-start}
.kelrow:last-child{border-bottom:none}
.kelrow .kiri{flex:1;min-width:0}
.kelrow .nm{font-size:12px;font-weight:900;line-height:1.3}
.kelrow .meta{font-size:10.5px;color:var(--redup2);font-weight:700;margin-top:2px}
.kelrow .pes{font-size:10.5px;color:var(--redup);margin-top:3px;line-height:1.4}
.kelrow .kanan{text-align:right;white-space:nowrap}
.kelrow .kanan b{font-size:12.5px;font-weight:900;display:block;color:var(--hijau-gelap)}
.kelrow .kanan span{font-size:9px;color:var(--redup2);font-weight:800}
.chip{display:inline-block;border-radius:20px;padding:2px 7px;font-size:8.5px;font-weight:900;
      letter-spacing:.3px;text-transform:uppercase;vertical-align:middle;margin-left:5px;border:1px solid}
.t-pertebal{background:#e8f5ee;color:#0a5236;border-color:#bfe3d0}
.t-rebut{background:#fff5dd;color:#8a6410;border-color:#f0dfb6}
.t-adjust{background:#e8f0fb;color:#1f4f8a;border-color:#cfdff2}
.t-hindari{background:#f4f6f5;color:#7b8c85;border-color:#e3eae6}
.tandai{background:linear-gradient(180deg,#fffdf5,#fff);border:1px solid #f3e3b8}
.tandai h2{color:#8a6d1f}
.langkah{display:flex;gap:10px;padding:10px 0;border-bottom:1px dashed #efe0b4}
.langkah:last-child{border-bottom:none}
.langkah .nom{width:26px;height:26px;border-radius:50%;background:var(--emas);color:#3a2a00;
              font-weight:900;font-size:12px;display:flex;align-items:center;justify-content:center;flex:0 0 26px}
.langkah .isi{flex:1;font-size:11.5px;line-height:1.5}
.langkah .isi b{display:block;font-size:12.5px;margin-bottom:2px}
.legend{display:grid;gap:8px;margin-top:6px}
.legend div{display:flex;gap:8px;align-items:flex-start;font-size:10.5px;color:var(--redup);line-height:1.45}
.legend .chip{margin:0;flex:0 0 auto}
.ket{font-size:11.5px;color:var(--redup);line-height:1.55;margin:8px 0 0}
.ket b{color:var(--hijau-gelap)}
.kaki{text-align:center;font-size:11.5px;font-weight:800;padding:4px 0 24px}
.kaki a{color:var(--hijau);text-decoration:none;display:inline-block;padding:8px 10px}
.kaki .utama{display:block;margin-top:6px;background:#04301f;color:#ffe6a6;font-weight:800;
             font-size:12.5px;padding:11px;border-radius:10px;border:1px solid rgba(246,185,59,.45)}
@media(min-width:560px){.hero h1{font-size:29px}}
"""

JS = """
const tb=[...document.querySelectorAll('.pilih button')];
function pilih(v){
  tb.forEach(b=>b.classList.toggle('aktif',b.dataset.v===v));
  document.querySelectorAll('.panel').forEach(p=>p.classList.toggle('aktif',p.id==='panel-'+v));
  history.replaceState(null,'','#'+v.toLowerCase());
}
tb.forEach(b=>b.addEventListener('click',()=>pilih(b.dataset.v)));
const awal=location.hash.replace('#','').toUpperCase();
pilih(awal==='B'?'B':'A');
"""

hero = f'''<div class="hero">
  <div class="label">SOKABAT NU · SIMULASI PEMILU 2029</div>
  <h1><em>5 Dapil</em> dan <em>8 Dapil</em><br>55 Kursi</h1>
  <p>Suara asli Pemilu 2024 dibagi ulang ke dua kemungkinan daerah pemilihan. Setiap kelurahan dinilai: menang, bisa bersaing, atau jangan disentuh. Pesaing tiga besar ikut ditampilkan.</p>
  <div class="hero-angka">
    <div><span>Suara sah</span><b>{n(M['total_sah'])}</b></div>
    <div><span>Kelurahan</span><b>{M['kelurahan']}</b></div>
    <div><span>Kursi PKB</span><b>{A['pkb_kursi']} → {B['pkb_kursi']}</b></div>
  </div>
</div>'''

tab = '''<div class="pilih">
  <button data-v="A" class="aktif">Skenario A · 5 Dapil<small>55 kursi · 11 12 11 10 11</small></button>
  <button data-v="B">Skenario B · 8 Dapil<small>55 kursi · 6 7 8 6 6 8 7 7</small></button>
</div>'''

rekomendasi = f'''<div class="kartu tandai">
  <h2>Rekomendasi</h2>
  <div class="langkah"><div class="nom">1</div><div class="isi"><b>Ambil opsi delapan dapil</b>
    Dengan suara yang sama seperti 2024, PKB naik dari 5 menjadi {B['pkb_kursi']} kursi. Di tujuh dari delapan dapil PKB dapat satu kursi, jadi setiap wilayah punya wakil.</div></div>
  <div class="langkah"><div class="nom">2</div><div class="isi"><b>Fokus ke tiga dapil termurah</b>
    Dapil 7 butuh tambahan {n(B['dapil'][6]['tambah'])} suara, Dapil 3 butuh {n(B['dapil'][2]['tambah'])} suara, Dapil 8 butuh {n(B['dapil'][7]['tambah'])} suara. Ini rute terpendek menuju dua kursi tambahan.</div></div>
  <div class="langkah"><div class="nom">3</div><div class="isi"><b>Bangun dari nol di Dapil 7</b>
    Dapil 7 murah karena PKB belum punya kursi di sana. Jangan dibaca sebagai basis kuat. Kader dan suara harus ditanam, bukan dikonsolidasikan.</div></div>
  <div class="langkah"><div class="nom">4</div><div class="isi"><b>Kunci basis di delapan kelurahan</b>
    Delapan kelurahan sudah menang. Tugasnya menjaga suara, bukan menambah. Sisa energi digeser ke 39 kelurahan yang masih bisa bersaing.</div></div>
</div>'''

legenda = '''<div class="kartu">
  <h2>Arti tiga warna</h2>
  <div class="legend">
    <div><span class="chip t-pertebal">Menang</span><span>PKB juara, atau kalah di bawah 20 persen dari juara. Basis aman.</span></div>
    <div><span class="chip t-rebut">Bisa bersaing</span><span>PKB di tiga besar, atau peringkat empat dengan suara di atas 12 persen.</span></div>
    <div><span class="chip t-hindari">Jangan sentuh</span><span>Selisih terlalu jauh untuk dikejar dalam satu siklus.</span></div>
    <div><span class="chip t-adjust">Kecamatan</span><span>Rincian partai di kelurahan ini belum sahih, jadi kategori memakai hitungan kecamatan.</span></div>
  </div>
</div>'''

catatan = f'''<div class="kartu">
  <h2>Catatan data</h2>
  <p class="ket">Angka kelurahan berasal dari rekapan D.Hasil KPU 2024. Lima kelurahan Tegalsari tidak punya rincian, suaranya tetap dihitung lewat rekap kecamatan. Di {len(M['ragu'])} kecamatan, rincian partai selain PKB belum sahih, yaitu Gubeng, Tandes, Bulak, Mulyorejo, Pakal, dan Wonocolo. Kategori dan pesaing di 31 kelurahan sana memakai hitungan kecamatan dan diberi tanda.</p>
  <p class="ket">Pembagian kursi per dapil adalah asumsi kerja karena PKPU 2029 belum ada. Suara PKB per kelurahan akurat, kategori dan harga kursi adalah simulasi. Rata-rata kota {n(M['total_sah'] / 55)} suara per kursi menyesatkan kalau dipakai jadi target, karena kursi diperebutkan per dapil.</p>
</div>'''

kaki = '''<div class="kaki">
  <a href="peta-2024.html">Peta Suara 2024</a>
  <a href="index.html">Dashboard</a>
  <a class="utama" href="caleg.html">&larr; Kembali ke Beranda Caleg</a>
</div>'''

halaman = f'''<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Simulasi Pemilu 2029 · 5 Dapil dan 8 Dapil · SOKABAT NU</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#04301f">
<meta name="description" content="Simulasi Pemilu 2029 Kota Surabaya: 5 dapil dan 8 dapil, 55 kursi, peta kelurahan dan pesaing tiga besar, berbasis data Pemilu 2024.">
<link rel="manifest" href="manifest.json">
<style>{CSS}</style>
</head>
<body>
<div class="bungkus">
{hero}
{tab}
{panel(A, 'A')}
{panel(B, 'B')}
{rekomendasi}
{legenda}
{catatan}
{kaki}
</div>
<script>{JS}</script>
</body></html>
'''

keluaran = BASE / 'simulasi-2029.html'
keluaran.write_text(halaman)
print('tulis', keluaran, len(halaman), 'char')
