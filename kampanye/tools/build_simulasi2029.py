#!/usr/bin/env python3
"""Bangun data + halaman SOKABAT NU · SIMULASI PEMILU 2029.
Sumber tunggal: data Pemilu 2024 (kecamatan resmi + kelurahan hasil Peta Suara).
"""
import json, math, re, collections, pathlib

BASE = pathlib.Path('/home/buleng/.hermes/projects/sokabatnu/kampanye')
DATA = BASE / 'data'
SING = ["PKB","Gerindra","PDIP","Golkar","NasDem","Buruh","Gelora","PKS","PKN",
        "Hanura","Garuda","PAN","PBB","Demokrat","PSI","Perindo","PPP","Ummat"]

def kunci(s):
    return re.sub(r'[^A-Z0-9]', '', s.upper())

def sl(votes, seats):
    """Sainte-Lague. Kembalikan kursi per partai + harga kursi terakhir."""
    div = {k: 1 for k in votes}
    kursi = {k: 0 for k in votes}
    log = []
    for _ in range(seats):
        pemenang = max(votes, key=lambda k: votes[k] / div[k])
        log.append((pemenang, votes[pemenang] / div[pemenang]))
        kursi[pemenang] += 1
        div[pemenang] += 2
    return kursi, log

def alokasi(total, bobot):
    semua = sum(bobot.values())
    mentah = {k: total * v / semua for k, v in bobot.items()}
    dasar = {k: int(v) for k, v in mentah.items()}
    sisa = total - sum(dasar.values())
    for k in sorted(mentah, key=lambda k: -mentah[k] % 1)[:sisa]:
        dasar[k] += 1
    return dasar

def kategori(r):
    """Aturan tiga warna, hanya dari angka 2024."""
    if r['rank'] == 1 or (r['rank'] == 2 and r['gapr'] <= 0.20):
        return 'menang'
    if r['rank'] <= 3 or (r['share'] >= 12 and r['rank'] <= 4):
        return 'bersaing'
    return 'jangan'

DAPIL_A = {
 1: ['TEGALSARI','GENTENG','GUBENG','SIMOKERTO','BUBUTAN','KREMBANGAN'],
 2: ['TAMBAKSARI','PABEAN CANTIAN','SEMAMPIR','KENJERAN'],
 3: ['WONOCOLO','RUNGKUT','SUKOLILO','TENGGILIS MEJOYO','GUNUNG ANYAR','MULYOREJO','BULAK'],
 4: ['WONOKROMO','SAWAHAN','GAYUNGAN','JAMBANGAN','SUKOMANUNGGAL'],
 5: ['KARANG PILANG','TANDES','LAKARSANTRI','BENOWO','WIYUNG','DUKUH PAKIS','ASEM ROWO','PAKAL','SAMBIKEREP'],
}
DAPIL_B = {
 1: ['GENTENG','SIMOKERTO','BUBUTAN','TEGALSARI'],
 2: ['KREMBANGAN','SEMAMPIR','PABEAN CANTIAN'],
 3: ['TAMBAKSARI','BULAK','KENJERAN'],
 4: ['MULYOREJO','SUKOLILO','GUBENG'],
 5: ['TENGGILIS MEJOYO','GUNUNG ANYAR','RUNGKUT','WONOCOLO'],
 6: ['GAYUNGAN','WONOKROMO','JAMBANGAN','SAWAHAN'],
 7: ['KARANG PILANG','WIYUNG','LAKARSANTRI','DUKUH PAKIS','SAMBIKEREP'],
 8: ['TANDES','SUKOMANUNGGAL','ASEM ROWO','BENOWO','PAKAL'],
}

def muat():
    pem = json.loads((DATA / 'pemilu-2024.json').read_text())
    dhasil = json.loads((DATA / 'dhasil_tps.json').read_text())
    kec = {}
    for d in pem['dapil'].values():
        for k in d['kecamatan_detail']:
            kec[kunci(k['nama'])] = {
                'nama': k['nama'],
                'sah': k['suara_sah'],
                'dpt': k['dpt'],
                'partai': {p['singkat']: p['total'] for p in k['partai']},
            }
    kel = []
    for nama_kec, isi in dhasil.items():
        for nama_kel, suara in isi['kelurahan'].items():
            v = {SING[int(i)]: n for i, n in suara.items()}
            total = sum(v.values())
            urut = sorted(v.items(), key=lambda x: -x[1])
            pkb = v.get('PKB', 0)
            rank = [i for i, (p, _) in enumerate(urut, 1) if p == 'PKB'][0]
            gap = urut[0][1] - pkb
            kel.append(dict(kec=kunci(nama_kec), kec_nama=nama_kec, nama=nama_kel,
                            pkb=pkb, sah=total,
                            share=round(100 * pkb / total, 2) if total else 0,
                            rank=rank, top=urut[0][0], top_v=urut[0][1],
                            gap=gap, gapr=round(gap / pkb, 3) if pkb else 99,
                            valid=isi['status']))
    return kec, kel

def bangun(nama, dapilmap, kec, kel, total_kursi=55):
    sah_dapil = {d: sum(kec[kunci(x)]['sah'] for x in ks) for d, ks in dapilmap.items()}
    kursi_dapil = alokasi(total_kursi, sah_dapil)
    hasil = []
    for d, ks in dapilmap.items():
        votes = {p: sum(kec[kunci(x)]['partai'].get(p, 0) for x in ks) for p in SING}
        sah = sah_dapil[d]
        kursi = kursi_dapil[d]
        kursi_partai, log = sl(votes, kursi)
        harga = round(log[-1][1])
        pkb = votes['PKB']
        lo, hi = 0, 300000
        while lo < hi:
            mid = (lo + hi) // 2
            uji = dict(votes); uji['PKB'] = pkb + mid
            if sl(uji, kursi)[0]['PKB'] > kursi_partai['PKB']:
                hi = mid
            else:
                lo = mid + 1
        tambah = lo
        anggota = [r for r in kel if r['kec'] in {kunci(x) for x in ks}]
        per = collections.defaultdict(list)
        for r in anggota:
            per[kategori(r)].append(r)
        tier = {}
        for t in ('menang', 'bersaing', 'jangan'):
            isi = sorted(per[t], key=lambda r: -r['pkb'])
            tier[t] = dict(n=len(isi), pkb=sum(r['pkb'] for r in isi),
                           gap=sum(r['gap'] for r in isi),
                           kel=[dict(nama=r['nama'], kec=r['kec_nama'], pkb=r['pkb'],
                                     share=r['share'], rank=r['rank'], top=r['top'],
                                     gap=r['gap']) for r in isi])
        hasil.append(dict(nomor=d, kecamatan=[kec[kunci(x)]['nama'] for x in ks],
                          kursi=kursi, sah=sah,
                          dpt=sum(kec[kunci(x)]['dpt'] for x in ks),
                          partisipasi=round(100 * sah / sum(kec[kunci(x)]['dpt'] for x in ks), 1),
                          kuota=round(sah / kursi), harga=harga,
                          pkb=pkb, pkb_persen=round(100 * pkb / sah, 2),
                          pkb_kursi=kursi_partai['PKB'], tambah=tambah,
                          rasio=round(tambah / pkb, 2),
                          tier=tier,
                          kel_total=len(anggota)))
    return dict(nama=nama, kursi_total=total_kursi,
                pkb_kursi=sum(x['pkb_kursi'] for x in hasil),
                pkb=sum(x['pkb'] for x in hasil),
                sah=sum(x['sah'] for x in hasil),
                dapil=hasil)

def main():
    kec, kel = muat()
    total_sah = sum(k['sah'] for k in kec.values())
    total_pkb = sum(k['partai'].get('PKB', 0) for k in kec.values())
    A = bangun('A', DAPIL_A, kec, kel)
    B = bangun('B', DAPIL_B, kec, kel)
    keluaran = dict(
        meta=dict(sumber='KPU, Pemilu 2024 (rekap kecamatan resmi + Peta Suara kelurahan)',
                  total_sah=total_sah, total_pkb=total_pkb,
                  pkb_persen=round(100 * total_pkb / total_sah, 2),
                  kursi_2024=50, kursi_pkb_2024=5,
                  kelurahan=len(kel), kelurahan_kota=153,
                  kecamatan=len(kec),
                  catatan='Tegalsari tidak punya rincian kelurahan. Angka partai non-PKB di 12 kecamatan belum final.'),
        A=A, B=B)
    (DATA / 'simulasi-2029.json').write_text(json.dumps(keluaran, ensure_ascii=False, indent=1))
    print('A', A['pkb_kursi'], 'B', B['pkb_kursi'], 'sah', total_sah, 'pkb', total_pkb)
    for x in A['dapil'] + B['dapil']:
        print(x['nomor'], x['kursi'], x['harga'], x['pkb_kursi'], x['tambah'],
              {t: v['n'] for t, v in x['tier'].items()})

if __name__ == '__main__':
    main()
