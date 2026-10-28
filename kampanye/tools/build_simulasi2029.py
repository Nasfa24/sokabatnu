#!/usr/bin/env python3
"""Bangun data SOKABAT NU · SIMULASI PEMILU 2029.
Sumber tunggal: Pemilu 2024 (rekap kecamatan resmi + Peta Suara kelurahan).
Setiap kelurahan membawa tiga pesaing terberat dan penanda dasar hitung.
"""
import json, re, collections, pathlib

BASE = pathlib.Path('/home/buleng/.hermes/projects/sokabatnu/kampanye')
DATA = BASE / 'data'
SING = ["PKB","Gerindra","PDIP","Golkar","NasDem","Buruh","Gelora","PKS","PKN",
        "Hanura","Garuda","PAN","PBB","Demokrat","PSI","Perindo","PPP","Ummat"]

def kunci(s):
    return re.sub(r'[^A-Z0-9]', '', s.upper())

def sl(votes, seats):
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
    for k in sorted(mentah, key=lambda k: -(mentah[k] % 1))[:sisa]:
        dasar[k] += 1
    return dasar

def kategori(rank, gapr, share):
    if rank == 1 or (rank == 2 and gapr <= 0.20):
        return 'menang'
    if rank <= 3 or (share >= 12 and rank <= 4):
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
                'nama': k['nama'], 'sah': k['suara_sah'], 'dpt': k['dpt'],
                'partai': {p['singkat']: p['total'] for p in k['partai']},
            }
    kel, ragu = [], []
    for nama_kec, isi in dhasil.items():
        kc = kec[kunci(nama_kec)]
        # uji kelayakan angka partai tingkat kelurahan
        jum = collections.Counter()
        for suara in isi['kelurahan'].values():
            for i, n in suara.items():
                jum[SING[int(i)]] += n
        selisih = abs(sum(jum.values()) - kc['sah']) / kc['sah']
        beda_partai = sum(1 for p in SING
                          if abs(jum[p] - kc['partai'].get(p, 0)) > max(25, 0.02 * kc['partai'].get(p, 0)))
        layak = selisih <= 0.05
        if not layak:
            ragu.append((nama_kec, round(100 * selisih, 1), beda_partai))
        # statistik tingkat kecamatan sebagai cadangan
        urut_kec = sorted(kc['partai'].items(), key=lambda x: -x[1])
        pkb_kec = kc['partai'].get('PKB', 0)
        rank_kec = [i for i, (p, _) in enumerate(urut_kec, 1) if p == 'PKB'][0]
        gap_kec = urut_kec[0][1] - pkb_kec
        for nama_kel, suara in isi['kelurahan'].items():
            v = {SING[int(i)]: n for i, n in suara.items()}
            pkb = v.get('PKB', 0)
            if layak:
                total = sum(v.values())
                urut = sorted(v.items(), key=lambda x: -x[1])
                rank = [i for i, (p, _) in enumerate(urut, 1) if p == 'PKB'][0]
                top, top_v = urut[0]
                dasar = 'kelurahan'
                pesaing = [(p, n, round(100 * n / total, 1)) for p, n in urut if p != 'PKB'][:3]
                hitung = pkb
            else:
                total = kc['sah']
                rank, top, top_v = rank_kec, urut_kec[0][0], urut_kec[0][1]
                dasar = 'kecamatan'
                hitung = pkb_kec
                pesaing = [(p, n, round(100 * n / total, 1)) for p, n in urut_kec if p != 'PKB'][:3]
            gap = top_v - hitung
            share = round(100 * hitung / total, 2) if total else 0
            gapr = round(gap / hitung, 3) if hitung else 99
            kel.append(dict(kec=kunci(nama_kec), kec_nama=nama_kec, nama=nama_kel,
                            pkb=pkb, sah=total, share=share, rank=rank,
                            top=top, top_v=top_v, gap=gap, gapr=gapr,
                            dasar=dasar,
                            pesaing=[dict(p=p, v=n, sh=sh) for p, n, sh in pesaing],
                            tier=kategori(rank, gapr, share)))
    return kec, kel, ragu

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
            per[r['tier']].append(r)
        tier = {}
        for t in ('menang', 'bersaing', 'jangan'):
            isi = sorted(per[t], key=lambda r: -r['pkb'])
            tier[t] = dict(n=len(isi), pkb=sum(r['pkb'] for r in isi),
                           kel=[dict(nama=r['nama'], kec=r['kec_nama'], pkb=r['pkb'],
                                     share=r['share'], rank=r['rank'], top=r['top'],
                                     gap=r['gap'], dasar=r['dasar'],
                                     pesaing=r['pesaing']) for r in isi])
        hasil.append(dict(nomor=d, kecamatan=[kec[kunci(x)]['nama'] for x in ks],
                          kursi=kursi, sah=sah,
                          dpt=sum(kec[kunci(x)]['dpt'] for x in ks),
                          partisipasi=round(100 * sah / sum(kec[kunci(x)]['dpt'] for x in ks), 1),
                          kuota=round(sah / kursi), harga=harga,
                          pkb=pkb, pkb_persen=round(100 * pkb / sah, 2),
                          pkb_kursi=kursi_partai['PKB'], tambah=tambah,
                          rasio=round(tambah / pkb, 2),
                          tier=tier, kel_total=len(anggota)))
    return dict(nama=nama, kursi_total=total_kursi,
                pkb_kursi=sum(x['pkb_kursi'] for x in hasil),
                pkb=sum(x['pkb'] for x in hasil),
                sah=sum(x['sah'] for x in hasil),
                dapil=hasil)

def harga20(votes, kursi, harga=20000):
    """Dua cara membaca aturan satu kursi sama dengan 20.000 suara."""
    amb = {p: v for p, v in votes.items() if v >= harga}
    kursi_amb = sl(amb, kursi)[0] if amb else {}
    dasar = {p: v // harga for p, v in votes.items()}
    sisa = kursi - sum(dasar.values())
    if sisa > 0:
        for p in sorted(votes, key=lambda q: votes[q] % harga, reverse=True)[:sisa]:
            dasar[p] += 1
    elif sisa < 0:
        for p in sorted([q for q in votes if dasar[q] > 0],
                        key=lambda q: votes[q] % harga)[:-sisa]:
            dasar[p] -= 1
    return kursi_amb, dasar, len(amb)

def tempel_h20(sk, dapilmap, kec):
    pkb_amb = pkb_kuota = lolos = 0
    kurang = 0
    partai_amb = collections.Counter()
    partai_biasa = collections.Counter()
    for d in sk['dapil']:
        ks = dapilmap[d['nomor']]
        votes = {p: sum(kec[kunci(x)]['partai'].get(p, 0) for x in ks) for p in SING}
        amb, kuota, jml = harga20(votes, d['kursi'])
        biasa = sl(votes, d['kursi'])[0]
        d['h20'] = dict(ambang_pkb=amb.get('PKB', 0), kuota_pkb=kuota['PKB'],
                        lolos=jml, selisih=d['pkb'] - 20000)
        pkb_amb += amb.get('PKB', 0)
        pkb_kuota += kuota['PKB']
        lolos += jml
        kurang += max(0, 20000 - d['pkb'])
        partai_amb.update(amb)
        partai_biasa.update(biasa)
    sk['h20'] = dict(
        harga=20000,
        kursi_kota=round(sk['sah'] / 20000, 1),
        ambang_pkb=pkb_amb, kuota_pkb=pkb_kuota, lolos=lolos, kurang=kurang,
        dapil_lolos=sum(1 for d in sk['dapil'] if d['pkb'] >= 20000),
        partai=[dict(p=p, biasa=partai_biasa.get(p, 0), ambang=partai_amb.get(p, 0))
                for p in SING if partai_biasa.get(p, 0) or partai_amb.get(p, 0)])

def main():
    kec, kel, ragu = muat()
    total_sah = sum(k['sah'] for k in kec.values())
    total_pkb = sum(k['partai'].get('PKB', 0) for k in kec.values())
    A = bangun('A', DAPIL_A, kec, kel)
    B = bangun('B', DAPIL_B, kec, kel)
    tempel_h20(A, DAPIL_A, kec)
    tempel_h20(B, DAPIL_B, kec)
    keluaran = dict(
        meta=dict(sumber='KPU, Pemilu 2024 (rekap kecamatan resmi + Peta Suara kelurahan)',
                  total_sah=total_sah, total_pkb=total_pkb,
                  pkb_persen=round(100 * total_pkb / total_sah, 2),
                  kursi_2024=50, kursi_pkb_2024=5,
                  kelurahan=len(kel), kelurahan_kota=153,
                  kecamatan=len(kec),
                  ragu=[dict(kec=n, selisih=s, beda_partai=b) for n, s, b in ragu],
                  catatan='Tegalsari tanpa rincian kelurahan. Angka partai non-PKB di beberapa kecamatan belum final, kategori di sana memakai hitungan kecamatan.'),
        A=A, B=B)
    (DATA / 'simulasi-2029.json').write_text(json.dumps(keluaran, ensure_ascii=False, indent=1))
    print('A', A['pkb_kursi'], 'B', B['pkb_kursi'], 'sah', total_sah, 'pkb', total_pkb)
    print('ragu', ragu)
    for x in A['dapil'] + B['dapil']:
        print(x['nomor'], x['kursi'], x['harga'], x['pkb_kursi'], x['tambah'],
              {t: v['n'] for t, v in x['tier'].items()})

if __name__ == '__main__':
    main()
