#!/usr/bin/env python3
"""Render halaman SOKABAT NU · SIMULASI PEMILU 2029 dari data/simulasi-2029.json."""
import json, html, pathlib

BASE = pathlib.Path('/home/buleng/.hermes/projects/sokabatnu/kampanye')
D = json.loads((BASE / 'data' / 'simulasi-2029.json').read_text())
M, A, B = D['meta'], D['A'], D['B']

def n(x):
    return f"{int(x):,}".replace(',', '.')

def pct(x):
    return f"{x:.2f}".replace('.', ',') + '%'

def e(s):
    return html.escape(str(s))

TEMA = {'menang': ('Menang', 'Basis aman. PKB juara atau kalah tipis di bawah 20 persen.'),
        'bersaing': ('Bisa bersaing', 'PKB di tiga besar, atau peringkat empat dengan suara di atas 12 persen.'),
        'jangan': ('Jangan sentuh', 'Selisih terlalu jauh untuk dikejar dalam satu siklus.')}

def baris(k):
    cap = ''
    if k['dasar'] == 'kecamatan':
        cap = ' <span class="badge" title="Rincian partai tingkat kelurahan belum sahih, kategori memakai hitungan kecamatan">kecamatan</span>'
    pes = ' · '.join(f"{e(p['p'])} {pct(p['sh'])}" for p in k['pesaing'])
    return (f'<div class="kel">'
            f'<div class="kepala"><span class="knama">{e(k["nama"].title())}</span>{cap}'
            f'<span class="kangka">PKB {pct(k["share"])}</span></div>'
            f'<div class="kmeta">{e(k["kec"].title())} · peringkat {k["rank"]} · {n(k["pkb"])} suara</div>'
            f'<div class="kpes"><span>Pesaing</span> {pes}</div></div>')

def blok(d, t):
    isi = d['tier'][t]
    judul, ket = TEMA[t]
    if not isi['n']:
        return (f'<div class="tier t-{t}"><div class="thead"><b>{judul}</b>'
                f'<span>tidak ada kelurahan</span></div></div>')
    kepala = (f'<div class="thead"><b>{judul}</b><span>{isi["n"]} kelurahan · '
              f'{n(isi["pkb"])} suara PKB</span></div><p class="tket">{ket}</p>')
    badan = ''.join(baris(k) for k in isi['kel'])
    if t == 'jangan':
        return (f'<details class="tier t-{t}"><summary>{judul} · {isi["n"]} kelurahan</summary>'
                f'<p class="tket">{ket}</p>{badan}</details>')
    return f'<div class="tier t-{t}">{kepala}{badan}</div>'

def kartu(d):
    tier = ''.join(blok(d, t) for t in ('menang', 'bersaing', 'jangan'))
    return f'''<div class="dapil">
  <div class="dhead"><div><span class="dnomor">Dapil {d['nomor']}</span>
    <span class="dkursi">{d['kursi']} kursi</span></div>
    <div class="dwil">{e(', '.join(x.title() for x in d['kecamatan']))}</div></div>
  <div class="dstat">
    <div><span>Suara sah</span><b>{n(d['sah'])}</b></div>
    <div><span>Kuota kursi</span><b>{n(d['kuota'])}</b></div>
    <div><span>Kursi terakhir</span><b>{n(d['harga'])}</b></div>
    <div><span>PKB 2024</span><b>{n(d['pkb'])} · {pct(d['pkb_persen'])}</b></div>
    <div><span>Kursi PKB</span><b>{d['pkb_kursi']}</b></div>
    <div><span>Kursi berikutnya</span><b>{'+' + n(d['tambah']) if d['tambah'] else 'sudah maksimal'}</b></div>
  </div>
  {tier}
</div>'''

def panel(sk, ket):
    kartu_html = ''.join(kartu(d) for d in sk['dapil'])
    menang = sum(d['tier']['menang']['n'] for d in sk['dapil'])
    bersaing = sum(d['tier']['bersaing']['n'] for d in sk['dapil'])
    return f'''<section class="panel" id="panel-{sk['nama']}" role="tabpanel" aria-labelledby="tab-{sk['nama']}">
  <p class="ringkas">{ket}</p>
  <div class="rekap"><span>PKB {n(sk['pkb'])} suara</span><span>{sk['pkb_kursi']} kursi dari {sk['kursi_total']}</span><span>{menang} kelurahan menang</span><span>{bersaing} bisa bersaing</span></div>
  {kartu_html}
</section>'''

CSS = """
:root{--bg:#0f1411;--card:#17201a;--card2:#1d2820;--line:#2b3a2f;--txt:#e8f0e9;--muted:#9db0a2;--hijau:#39b46a;--kuning:#d8a52c;--merah:#c8553d;--radius:14px}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--txt);font:16px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
.wrap{max-width:900px;margin:0 auto;padding:18px 14px 60px}
h1{font-size:1.5rem;line-height:1.25;margin:6px 0 4px}
.sub{color:var(--muted);font-size:.92rem;margin:0 0 18px}
p{color:#cfdcd3}
.kartu{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:14px 16px;margin:0 0 16px}
.kartu h2{font-size:1rem;margin:0 0 6px}
.kartu p{margin:0 0 8px;font-size:.92rem;color:#c3d2c7}
.kartu p:last-child{margin-bottom:0}
.tabs{position:sticky;top:0;z-index:9;display:grid;grid-template-columns:1fr 1fr;gap:8px;background:var(--bg);padding:10px 0 12px}
.tabs button{appearance:none;border:1px solid var(--line);background:var(--card);color:var(--txt);padding:11px 10px;border-radius:12px;font-size:.92rem;font-weight:600;cursor:pointer;text-align:left}
.tabs button small{display:block;font-weight:400;color:var(--muted);font-size:.78rem}
.tabs button[aria-selected="true"]{background:#1f3a29;border-color:var(--hijau)}
.tabs button[aria-selected="true"] small{color:#b6e3c6}
.panel{display:none}
.panel.aktif{display:block}
.ringkas{font-size:.93rem;color:#c3d2c7;margin:2px 0 12px}
.rekap{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 14px}
.rekap span{background:#1c2a21;border:1px solid var(--line);border-radius:999px;padding:4px 10px;font-size:.8rem;color:#bdd0c3}
.dapil{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:14px;margin:0 0 16px}
.dhead{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;align-items:baseline;margin-bottom:10px}
.dnomor{font-size:1.1rem;font-weight:700}
.dkursi{font-size:.82rem;color:#b6e3c6;background:#1f3a29;border-radius:999px;padding:3px 8px;margin-left:6px}
.dwil{font-size:.8rem;color:var(--muted);flex:1 1 100%}
.dstat{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:14px}
.dstat div{background:var(--card2);border-radius:10px;padding:8px 10px}
.dstat span{display:block;font-size:.72rem;color:var(--muted)}
.dstat b{font-size:.95rem;font-weight:600}
.tier{border-left:3px solid var(--line);padding:10px 0 4px 12px;margin:0 0 12px}
.tier.t-menang{border-color:var(--hijau)}
.tier.t-bersaing{border-color:var(--kuning)}
.tier.t-jangan{border-color:var(--merah)}
.thead{display:flex;justify-content:space-between;gap:8px;font-size:.86rem;color:var(--txt)}
.thead span{color:var(--muted)}
.tket{font-size:.78rem;color:var(--muted);margin:2px 0 8px}
details.tier summary{cursor:pointer;font-size:.86rem;font-weight:600;color:#e0c9a6}
.kel{background:var(--card2);border-radius:10px;padding:8px 10px;margin-bottom:6px}
.kepala{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.knama{font-weight:600;font-size:.92rem}
.kangka{margin-left:auto;font-size:.84rem;color:#b6e3c6;font-variant-numeric:tabular-nums}
.badge{font-size:.66rem;text-transform:uppercase;letter-spacing:.04em;color:#e0c9a6;border:1px solid #4a3d28;border-radius:6px;padding:1px 5px}
.kmeta{font-size:.74rem;color:var(--muted);margin-top:1px}
.kpes{font-size:.76rem;color:#cfdcd3;margin-top:3px}
.kpes span{color:var(--muted)}
@media(max-width:560px){.dstat{grid-template-columns:repeat(2,1fr)}h1{font-size:1.3rem}.tabs button{font-size:.86rem;padding:10px 8px}}
"""

JS = """
const tombol=[...document.querySelectorAll('.tabs button')];
function pilih(id,simpan){
  tombol.forEach(b=>{const on=b.dataset.panel===id;b.setAttribute('aria-selected',on?'true':'false');});
  document.querySelectorAll('.panel').forEach(p=>p.classList.toggle('aktif',p.id==='panel-'+id));
  if(simpan!==false){history.replaceState(null,'','#'+id.toLowerCase());}
}
tombol.forEach(b=>{b.addEventListener('click',()=>pilih(b.dataset.panel));
 b.addEventListener('keydown',ev=>{if(ev.key==='ArrowRight'||ev.key==='ArrowLeft'){const i=tombol.indexOf(b);const j=(i+(ev.key==='ArrowRight'?1:tombol.length-1))%tombol.length;tombol[j].focus();pilih(tombol[j].dataset.panel);}});});
const awal=location.hash.replace('#','').toUpperCase();
pilih(awal==='B'?'B':'A',false);
"""

awal = f'''<div class="wrap">
<h1>SOKABAT NU · Simulasi Pemilu 2029</h1>
<p class="sub">Peta kekuatan PKB per kelurahan, memakai angka Pemilu 2024. Tanpa tambahan data lain.</p>
<div class="kartu"><h2>Cara membaca halaman ini</h2>
<p>Setiap kelurahan dinilai dari peringkat PKB dan jarak suara ke juara. Menang berarti PKB juara atau kalah di bawah 20 persen. Bisa bersaing berarti PKB di tiga besar, atau peringkat empat dengan suara di atas 12 persen. Jangan sentuh berarti selisihnya terlalu jauh. Di tiap kelurahan, tiga partai terkuat selain PKB ditampilkan sebagai pesaing.</p></div>
<div class="kartu"><h2>Harga satu kursi</h2>
<p>Rata-rata kota {n(M['total_sah'])} suara sah dibagi 55 kursi menjadi {n(M['total_sah'] / 55)} suara per kursi. Angka ini menyesatkan kalau dipakai jadi target, karena kursi diperebutkan per dapil. Yang lebih berguna adalah angka kursi terakhir di tiap dapil, yaitu suara partai paling lemah yang masih dapat kursi.</p></div>
<div class="tabs" role="tablist" aria-label="Pilih skenario">
<button role="tab" id="tab-A" data-panel="A" aria-selected="true" aria-controls="panel-A">Skenario A · 5 Dapil<small>55 kursi, pembagian 11 12 11 10 11</small></button>
<button role="tab" id="tab-B" data-panel="B" aria-selected="false" aria-controls="panel-B">Skenario B · 8 Dapil<small>55 kursi, pembagian 6 7 8 6 6 8 7 7</small></button>
</div>
'''

panelA = panel(A, 'Peta dapil seperti pemilu sebelumnya, kursi ditambah dari 50 menjadi 55. Dengan angka 2024, tambahan lima kursi kota tidak menambah kursi PKB. Tetap lima.')
panelB = panel(B, 'Kota dipecah menjadi delapan dapil kecil. Wilayah lebih sempit, harga kursi turun, peluang kader lokal naik. Dengan angka 2024, PKB naik dari lima menjadi tujuh kursi.')

akhir = f'''<div class="kartu"><h2>Rekomendasi</h2>
<p><b>Pilih opsi delapan dapil.</b> Dengan suara yang sama seperti 2024, PKB naik dua kursi. Di tujuh dari delapan dapil PKB mendapat satu kursi, jadi setiap dapil punya wakil yang bisa dihubungi.</p>
<p><b>Rute kursi termurah.</b> Dapil 7 skenario delapan dapil hanya butuh tambahan {n(B['dapil'][6]['tambah'])} suara, karena PKB belum punya kursi di sana. Dapil 3 butuh {n(B['dapil'][2]['tambah'])} suara, Dapil 8 butuh {n(B['dapil'][7]['tambah'])} suara. Tiga dapil ini rute terpendek menuju dua kursi tambahan.</p>
<p><b>Jangan salah baca.</b> Dapil 7 murah karena PKB lemah di sana, bukan karena basis kuat. Kemenangan harus dibangun dari nol, bukan dikonsolidasikan.</p></div>
<div class="kartu"><h2>Catatan data</h2>
<p>Angka kelurahan berasal dari rekapan D.Hasil KPU 2024. Lima kelurahan Tegalsari tidak punya rincian, suaranya tetap dihitung lewat rekap kecamatan. Di {len(M['ragu'])} kecamatan, rincian partai selain PKB belum sahih, sehingga kategori dan pesaing di kelurahan sana memakai hitungan tingkat kecamatan dan diberi tanda.</p>
<p>Pembagian kursi per dapil adalah asumsi kerja, karena PKPU untuk 2029 belum ada. Suara PKB per kelurahan akurat. Kategori dan harga kursi adalah simulasi.</p></div>
</div>
'''

halaman = f'''<!doctype html>
<html lang="id"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>SOKABAT NU · Simulasi Pemilu 2029</title>
<meta name="description" content="Simulasi Pemilu 2029 untuk Kota Surabaya, 5 dapil dan 8 dapil, 55 kursi, berbasis data Pemilu 2024.">
<style>{CSS}</style>
</head><body>
{awal}{panelA}{panelB}{akhir}
<script>{JS}</script></body></html>
'''

keluaran = BASE / 'simulasi-2029.html'
keluaran.write_text(halaman)
print('tulis', keluaran, len(halaman), 'char')
