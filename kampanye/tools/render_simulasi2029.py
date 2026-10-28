#!/usr/bin/env python3
"""Render halaman statis SOKABAT NU · SIMULASI PEMILU 2029 dari simulasi-2029.json."""
import json, pathlib, html

BASE = pathlib.Path('/home/buleng/.hermes/projects/sokabatnu/kampanye')
D = json.loads((BASE / 'data/simulasi-2029.json').read_text())
M, A, B = D['meta'], D['A'], D['B']

def n(x):
    return f'{x:,}'.replace(',', '.')

def pct(x):
    return f'{x:.2f}'.replace('.', ',')

def chips(daftar):
    out = []
    for k in daftar:
        out.append(f'<span class="kel" title="PKB {n(k["pkb"])} suara, peringkat {k["rank"]}, juara {k["top"]}">{html.escape(k["nama"].title())} <b>{pct(k["share"])}%</b></span>')
    return ''.join(out)

def dapil_card(d, skenario):
    t = d['tier']
    warna = {'menang': 'Menang', 'bersaing': 'Bisa bersaing', 'jangan': 'Jangan disentuh'}
    blok = []
    blok.append(f'''<div class="tier t-menang"><div class="tier-kepala"><span class="dot"></span><h4>Menang</h4><em>{t["menang"]["n"]} kelurahan · {n(t["menang"]["pkb"])} suara PKB</em></div>
<div class="chips">{chips(t["menang"]["kel"]) or '<span class="kosong">Belum ada kelurahan yang benar-benar dikuasai PKB.</span>'}</div></div>''')
    blok.append(f'''<div class="tier t-bersaing"><div class="tier-kepala"><span class="dot"></span><h4>Bisa bersaing</h4><em>{t["bersaing"]["n"]} kelurahan · kurang {n(t["bersaing"]["gap"])} suara untuk menyalip juara</em></div>
<div class="chips">{chips(t["bersaing"]["kel"]) or '<span class="kosong">Tidak ada kelurahan di zona ini.</span>'}</div></div>''')
    blok.append(f'''<details class="tier t-jangan"><summary><span class="dot"></span><h4>Jangan disentuh</h4><em>{t["jangan"]["n"]} kelurahan · selisih terlalu jauh</em></summary>
<div class="chips">{chips(t["jangan"]["kel"]) or '<span class="kosong">Tidak ada.</span>'}</div></details>''')
    kec = ', '.join(k.title() for k in d['kecamatan'])
    return f'''<article class="dapil">
  <div class="dapil-kepala"><h3>Dapil {d['nomor']}</h3><span class="pil">{d['kursi']} kursi</span></div>
  <p class="kec">{kec}</p>
  <div class="angka">
    <div><span>Suara sah 2024</span><b>{n(d['sah'])}</b></div>
    <div><span>Harga kursi terakhir</span><b>{n(d['harga'])}</b></div>
    <div><span>PKB 2024</span><b>{n(d['pkb'])}</b><i>{pct(d['pkb_persen'])}%</i></div>
    <div><span>Kursi PKB</span><b>{d['pkb_kursi']}</b></div>
    <div class="lebar"><span>Tambahan suara PKB untuk satu kursi lagi</span><b>+{n(d['tambah'])}</b><i>setara {int(round(d['rasio']*100))}% dari suara PKB sekarang</i></div>
  </div>
  {''.join(blok)}
</article>'''

def skenario(nama, s, judul, sub):
    kartu = ''.join(dapil_card(d, nama) for d in s['dapil'])
    return f'''<section class="bagian">
<div class="bagian-kepala"><span class="tag">Skenario {nama}</span><h2>{judul}</h2><p>{sub}</p></div>
<div class="rekap"><div><span>Kursi PKB</span><b>{s['pkb_kursi']}</b></div><div><span>Suara PKB</span><b>{n(s['pkb'])}</b></div><div><span>Kursi total</span><b>{s['kursi_total']}</b></div></div>
{kartu}
</section>'''

# daftar prioritas rebut: kelurahan bersaing dengan selisih terkecil (skenario B)
semua = []
for d in B['dapil']:
    for k in d['tier']['bersaing']['kel']:
        semua.append((k['gap'], k['nama'].title(), d['nomor'], k['share'], k['top']))
semua.sort()
prioritas = ''.join(f'<li><b>{nm}</b> (Dapil {dp}) selisih {n(g)} suara, PKB {pct(sh)}%, juara {tp}</li>'
                    for g, nm, dp, sh, tp in semua[:10])

basis = []
for d in B['dapil']:
    for k in d['tier']['menang']['kel']:
        basis.append((k['pkb'], k['nama'].title(), d['nomor'], k['share']))
basis.sort(reverse=True)
basis_li = ''.join(f'<li><b>{nm}</b> (Dapil {dp}) {n(v)} suara, {pct(sh)}%</li>' for v, nm, dp, sh in basis)

def hitung_termurah(s):
    urut = sorted(s['dapil'], key=lambda d: d['tambah'])
    return urut

termurahB = hitung_termurah(B)
termurahA = hitung_termurah(A)

HALAMAN = f'''<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Simulasi Pemilu 2029 · SOKABAT NU</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#04301f">
<link rel="manifest" href="manifest.json">
<style>
:root{{--hijau:#0b6b45;--hijau-gelap:#04301f;--hijau-muda:#e8f5ee;--emas:#f6b93b;--emas-muda:#ffe6a6;
--bg:#eef3f0;--kartu:#fff;--garis:#dbe5df;--teks:#0e1a15;--redup:#4e615a;--redup2:#7b8c85;
--merah:#b3402f;--merah-muda:#fdeeea}}
*{{box-sizing:border-box;-webkit-tap-highlight-color:transparent}}
body{{margin:0;padding:0 0 44px;background:var(--bg);color:var(--teks);
font-family:'Segoe UI',system-ui,-apple-system,sans-serif;display:flex;justify-content:center;line-height:1.55}}
.bungkus{{width:100%;max-width:700px;padding:14px 14px 0;display:flex;flex-direction:column;gap:14px}}
.hero{{position:relative;overflow:hidden;border-radius:20px;padding:22px 20px 18px;color:#fff;
background:radial-gradient(120% 140% at 0% 0%,#0e7d51 0%,#04301f 62%);box-shadow:0 14px 30px rgba(4,48,31,.28)}}
.hero::after{{content:"";position:absolute;right:-52px;top:-46px;width:160px;height:160px;border-radius:50%;
background:radial-gradient(circle,rgba(246,185,59,.34),transparent 70%)}}
.hero .label{{font-size:10.5px;letter-spacing:1.6px;font-weight:800;color:var(--emas-muda);text-transform:uppercase}}
.hero h1{{margin:7px 0 6px;font-size:25px;line-height:1.18;font-weight:900}}
.hero h1 em{{font-style:normal;color:var(--emas)}}
.hero p{{margin:0;font-size:13px;color:#cfe4d9}}
.hero-angka{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:16px}}
.hero-angka div{{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.16);border-radius:12px;padding:9px 6px;text-align:center}}
.hero-angka span{{display:block;font-size:9px;letter-spacing:.6px;text-transform:uppercase;color:#bcd8ca;font-weight:800}}
.hero-angka b{{font-size:15px;font-weight:900}}
.kartu{{background:var(--kartu);border:1px solid var(--garis);border-radius:16px;padding:16px;box-shadow:0 4px 12px rgba(14,26,21,.04)}}
.kartu h2{{margin:0 0 8px;font-size:12px;letter-spacing:1px;text-transform:uppercase;color:var(--hijau)}}
.kartu p{{margin:0 0 8px;font-size:13.5px;color:var(--redup)}}
.kartu p:last-child{{margin-bottom:0}}
.kunci{{display:grid;gap:7px;margin-top:6px}}
.kunci div{{display:flex;gap:8px;align-items:flex-start;font-size:13px}}
.kunci i{{font-style:normal;width:16px;height:16px;border-radius:50%;flex:0 0 16px;margin-top:3px}}
.k-menang i{{background:var(--hijau)}} .k-bersaing i{{background:var(--emas)}} .k-jangan i{{background:var(--redup2)}}
.bagian{{display:flex;flex-direction:column;gap:12px;margin-top:6px}}
.bagian-kepala .tag{{display:inline-block;background:var(--hijau-gelap);color:var(--emas-muda);font-size:10px;
letter-spacing:1.4px;font-weight:800;text-transform:uppercase;padding:4px 9px;border-radius:999px}}
.bagian-kepala h2{{margin:9px 0 3px;font-size:21px;font-weight:900;line-height:1.2}}
.bagian-kepala p{{margin:0;font-size:13px;color:var(--redup)}}
.rekap{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}}
.rekap div{{background:var(--hijau-muda);border:1px solid #cfe7da;border-radius:14px;padding:11px;text-align:center}}
.rekap span{{display:block;font-size:9.5px;text-transform:uppercase;letter-spacing:.5px;color:var(--redup);font-weight:800}}
.rekap b{{font-size:19px;font-weight:900;color:var(--hijau-gelap)}}
.dapil{{background:var(--kartu);border:1px solid var(--garis);border-radius:16px;padding:15px;box-shadow:0 4px 12px rgba(14,26,21,.04)}}
.dapil-kepala{{display:flex;align-items:center;justify-content:space-between;gap:8px}}
.dapil-kepala h3{{margin:0;font-size:17px;font-weight:900}}
.pil{{background:var(--hijau);color:#fff;font-size:11px;font-weight:800;padding:3px 10px;border-radius:999px}}
.kec{{margin:4px 0 12px;font-size:11.5px;color:var(--redup2);line-height:1.45}}
.angka{{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-bottom:12px}}
.angka div{{background:#f7faf8;border:1px solid var(--garis);border-radius:11px;padding:8px 10px}}
.angka span{{display:block;font-size:9px;text-transform:uppercase;letter-spacing:.5px;color:var(--redup2);font-weight:800}}
.angka b{{font-size:14.5px;font-weight:900}}
.angka i{{font-style:normal;font-size:10.5px;color:var(--redup);margin-left:4px}}
.angka .lebar{{grid-column:1 / -1;background:var(--emas-muda);border-color:#f0d79a}}
.angka .lebar b{{color:#7a5200}}
.tier{{border-radius:12px;padding:10px;margin-top:8px;border:1px solid var(--garis)}}
.t-menang{{background:#f0f9f4;border-color:#cfe7da}}
.t-bersaing{{background:#fff8e8;border-color:#f3e2b6}}
.t-jangan{{background:#f7f8f7}}
.tier-kepala,.t-jangan summary{{display:flex;align-items:center;gap:7px;flex-wrap:wrap;cursor:pointer}}
.tier h4{{margin:0;font-size:12px;font-weight:900;text-transform:uppercase;letter-spacing:.7px}}
.tier em{{font-style:normal;font-size:10.5px;color:var(--redup);margin-left:auto;text-align:right}}
.dot{{width:8px;height:8px;border-radius:50%}}
.t-menang .dot{{background:var(--hijau)}} .t-bersaing .dot{{background:var(--emas)}} .t-jangan .dot{{background:var(--redup2)}}
.t-jangan summary{{list-style:none}}
.t-jangan summary::-webkit-details-marker{{display:none}}
.chips{{display:flex;flex-wrap:wrap;gap:5px;margin-top:8px}}
.kel{{display:inline-flex;align-items:center;gap:4px;background:#fff;border:1px solid var(--garis);
border-radius:999px;padding:3px 9px;font-size:11px;color:var(--redup)}}
.kel b{{color:var(--hijau-gelap)}}
.kosong{{font-size:11px;color:var(--redup2);font-style:italic}}
ol.daftar{{margin:6px 0 0;padding-left:18px;font-size:13px;color:var(--redup)}}
ol.daftar li{{margin-bottom:6px}}
ol.daftar b{{color:var(--teks)}}
.kaki{{font-size:11px;color:var(--redup2);text-align:center;padding:6px 10px 0;line-height:1.5}}
@media(max-width:420px){{.hero h1{{font-size:22px}}.angka{{grid-template-columns:1fr 1fr}}}}
</style>
</head>
<body>
<div class="bungkus">

<div class="hero">
  <div class="label">Sokabat NU · Pemilu 2029</div>
  <h1>Simulasi <em>Dapil dan Kursi</em></h1>
  <p>Dua kemungkinan peta dapil. Satu pertanyaan: di mana PKB menang, di mana masih bisa bersaing, dan di mana energi jangan dibuang.</p>
  <div class="hero-angka">
    <div><span>Suara sah 2024</span><b>{n(M['total_sah'])}</b></div>
    <div><span>Suara PKB</span><b>{n(M['total_pkb'])}</b></div>
    <div><span>PKB 2024</span><b>{pct(M['pkb_persen'])}%</b></div>
  </div>
</div>

<div class="kartu">
  <h2>Dari mana angka ini</h2>
  <p>Semua angka di halaman ini berasal dari Pemilu 2024 saja. Tidak ada survei, tidak ada asumsi pertumbuhan suara, tidak ada data lain yang dicampur.</p>
  <p>Suara partai dihitung dari rekap resmi tingkat kecamatan. Peta kelurahan memakai rincian TPS yang sudah diuji: 148 kelurahan menghasilkan 153.622 suara PKB. Lima kelurahan Tegalsari tidak punya rincian, tetapi rekap kecamatannya 5.748 suara. Kalau dijumlahkan menjadi 159.370 suara, hanya 8 suara atau 0,005 persen di atas rekap resmi 159.362.</p>
  <p>Kursi dihitung dengan metode Sainte-Laguë, metode yang dipakai dalam penghitungan kursi DPRD. Pembagian kursi antar dapil memakai perbandingan suara sah, karena belum ada PKPU untuk 2029.</p>
</div>

<div class="kartu">
  <h2>Cara membaca tiga warna</h2>
  <div class="kunci">
    <div class="k-menang"><i></i><span><b>Menang.</b> PKB juara di kelurahan itu, atau kalah sangat tipis, selisih di bawah 20 persen dari suara PKB sendiri.</span></div>
    <div class="k-bersaing"><i></i><span><b>Bisa bersaing.</b> PKB ada di tiga besar, atau peringkat empat dengan suara di atas 12 persen. Tambahan suara masih masuk akal.</span></div>
    <div class="k-jangan"><i></i><span><b>Jangan disentuh.</b> PKB di luar tiga besar dan selisihnya terlalu jauh. Energi kader lebih baik dipindah ke kelurahan kuning.</span></div>
  </div>
</div>

<div class="kartu">
  <h2>Harga satu kursi</h2>
  <p>Kalau 1.536.843 suara sah dibagi rata ke 55 kursi, satu kursi setara {n(round(M['total_sah']/55))} suara. Angka itu hanya rata-rata kota dan menyesatkan, karena kursi diperebutkan per dapil, bukan sekota.</p>
  <p>Yang lebih berguna adalah harga kursi terakhir di tiap dapil. Di dua skenario ini harganya bergerak dari {n(min(x['harga'] for x in A['dapil'] + B['dapil']))} sampai {n(max(x['harga'] for x in A['dapil'] + B['dapil']))} suara. Artinya, partai yang mendapat sekitar 13 ribu sampai 19 ribu suara di sebuah dapil sudah bisa merebut kursi terakhir.</p>
  <p>Bagi PKB, ukuran yang paling praktis adalah tambahan suara untuk satu kursi lagi di dapil yang sudah ada. Angka itu tertulis di setiap kartu dapil pada bagian berikut.</p>
</div>

{skenario('A', A, '5 Dapil · 55 Kursi', 'Peta dapil seperti pemilu sebelumnya, tetapi kursi ditambah dari 50 menjadi 55. Pembagian kursi mengikuti suara sah: 11, 12, 11, 10, 11. Dengan angka 2024, tambahan 5 kursi kota tidak menambah kursi PKB. Tetap 5.')}

{skenario('B', B, '8 Dapil · 55 Kursi', 'Kota dipecah menjadi delapan dapil kecil. Dengan wilayah yang lebih sempit, harga satu kursi turun dan peluang kader lokal naik. Pembagian kursi mengikuti suara sah: 6, 7, 8, 6, 6, 8, 7, 7. Dengan angka 2024, PKB naik dari 5 menjadi 7 kursi.')}

<div class="kartu">
  <h2>Rekomendasi</h2>
  <p><b>Pilih skenario 8 dapil kalau targetnya menambah kursi.</b> Dengan angka 2024 yang sama, PKB mendapat 7 kursi di 8 dapil, sedangkan di 5 dapil hanya 5 kursi. Dua kursi tambahan itu datang dari dapil yang lebih kecil, bukan dari suara yang bertambah.</p>
  <p><b>Kursi termurah ada di Dapil 7 skenario 8 dapil.</b> Wilayahnya Karang Pilang, Wiyung, Lakarsantri, Dukuh Pakis, dan Sambikerep. PKB belum punya kursi di sana, dan cukup tambahan {n(termurahB[0]['tambah'])} suara untuk membuka kursi pertama. Di 5 dapil, kursi termurah ada di Dapil 2 dengan tambahan {n(termurahA[0]['tambah'])} suara.</p>
  <p><b>Urutan biaya kursi tambahan di skenario 8 dapil:</b> Dapil 7 perlu {n(termurahB[0]['tambah'])} suara, Dapil 3 perlu {n(termurahB[1]['tambah'])}, Dapil 8 perlu {n(termurahB[2]['tambah'])}. Tiga dapil ini menjadi rute terpendek menuju 10 kursi.</p>
  <p><b>Amankan dulu basis yang sudah ada.</b> Ada {A['dapil'][0]['tier']['menang']['n'] + A['dapil'][1]['tier']['menang']['n'] + A['dapil'][2]['tier']['menang']['n'] + A['dapil'][3]['tier']['menang']['n'] + A['dapil'][4]['tier']['menang']['n']} kelurahan yang sudah dikuasai PKB. Jangan sampai berpindah tangan saat fokus merebut wilayah baru.</p>
  <p><b>Serang yang selisihnya kecil, bukan yang paling ramai.</b> Sepuluh kelurahan dengan selisih terkecil di skenario 8 dapil:</p>
  <ol class="daftar">{prioritas}</ol>
  <p><b>Jangan sebar energi.</b> Dari {M['kelurahan']} kelurahan yang terbaca, {B['dapil'][0]['tier']['jangan']['n'] + B['dapil'][1]['tier']['jangan']['n'] + B['dapil'][2]['tier']['jangan']['n'] + B['dapil'][3]['tier']['jangan']['n'] + B['dapil'][4]['tier']['jangan']['n'] + B['dapil'][5]['tier']['jangan']['n'] + B['dapil'][6]['tier']['jangan']['n'] + B['dapil'][7]['tier']['jangan']['n']} kelurahan masuk kategori jangan disentuh. Kunjungan tetap boleh, tetapi janji dan anggaran program sebaiknya dipusatkan di kelurahan kuning dan hijau.</p>
  <p><b>Basis terkuat yang wajib dijaga:</b></p>
  <ol class="daftar">{basis_li}</ol>
</div>

<div class="kartu">
  <h2>Batas kejujuran data</h2>
  <p>Rincian kelurahan hanya tersedia untuk {M['kelurahan']} dari 153 kelurahan. Lima kelurahan Tegalsari tidak punya berkas, jadi tidak masuk peta warna, tetapi suaranya tetap masuk hitungan kursi lewat rekap kecamatan.</p>
  <p>Di 12 kecamatan, angka partai selain PKB belum final. Akibatnya selisih suara di kelurahan-kelurahan tersebut bisa sedikit lebih kecil dari yang tertulis. Kategori kuning di sana perlu dicek ulang sebelum dijadikan dasar janji program.</p>
  <p>Pembagian kursi 55 ke dalam 5 atau 8 dapil adalah asumsi kerja, bukan keputusan KPU. Kalau kelak PKPU menetapkan pembagian lain, angka harga kursi akan bergeser.</p>
</div>

<div class="kaki">SOKABAT NU · Simulasi Pemilu 2029 · disusun dari data Pemilu 2024</div>
</div>
</body>
</html>
'''
(BASE / 'simulasi-2029.html').write_text(HALAMAN)
print('tulis', BASE / 'simulasi-2029.html', len(HALAMAN), 'char')
