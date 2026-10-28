"""Bangun peta okupansi 2029: target 8 kursi (5 dapil) dan 10 kursi (8 dapil).

Sumber suara TPS: data KPU 2024 (dhasil_tps.json).
Sumber lokasi TPS: spreadsheet alamat TPS (tps_lokasi.csv) dan kolom prediksi_tps Supabase.
Sumber kontak: Supabase (master_pemilih, data_ktp) per kelurahan dan per TPS.
"""
import json, collections, csv, re

BASE = '/home/buleng/.hermes/projects/sokabatnu/kampanye/data/'
SING = ["PKB", "Gerindra", "PDIP", "Golkar", "NasDem", "Buruh", "Gelora", "PKS",
        "PKN", "Hanura", "Garuda", "PAN", "PBB", "Demokrat", "PSI", "Perindo",
        "PPP", "Ummat"]
TARGET = {'A': 8, 'B': 10}
CAPTURE = 0.12          # asumsi realistis: 12 persen suara non-PKB di satu TPS bisa diraih
ORD = {'menang': 0, 'bersaing': 1, 'jangan': 2}


def norm(x):
    return x.upper().replace(' ', '').replace('-', '')


def muat(nama):
    return json.load(open(BASE + nama))


def baca_lokasi():
    """Alamat TPS dari spreadsheet, plus alamat dan jumlah binaan dari Supabase."""
    sheet = {}
    for r in csv.DictReader(open(BASE + 'tps_lokasi.csv', encoding='utf-8-sig')):
        try:
            no = f"{int(r['NO. TPS']):03d}"
        except (TypeError, ValueError):
            continue
        sheet[(norm(r['KECAMATAN']), norm(r['KELURAHAN']), no)] = (r.get('ALAMAT') or '').strip()
    sup = {}
    for r in muat('sb_tps.json'):
        m = re.search(r'TPS\s*(\d+)', r.get('tps') or '')
        if not m:
            continue
        no = f"{int(m.group(1)):03d}"
        kunci = (norm(r['kec'] or ''), norm(r['kel'] or ''), no)
        al = re.search(r'\((.*)\)', r['tps'])
        sup[kunci] = ((al.group(1).replace('📍', '').strip() if al else ''), r['n'])
    return sheet, sup


def baca_tps():
    sheet, sup = baca_lokasi()
    T = {norm(k): v for k, v in muat('dhasil_tps.json').items()}
    baris = []
    for kec, isi in T.items():
        for kel, isitps in isi['tps'].items():
            for no, v in isitps.items():
                tot = sum(v.values())
                pkb = v.get('0', 0)
                urut = sorted(v.items(), key=lambda z: -z[1])
                order = [SING[int(p)] for p, _ in urut]
                rank = order.index('PKB') + 1 if pkb > 0 else 99
                gap = max(0, urut[0][1] - pkb)
                share = pkb / tot if tot else 0
                if pkb == 0:
                    tier = 'jangan'
                elif rank == 1 or (rank == 2 and gap <= 0.15 * tot):
                    tier = 'menang'
                elif rank <= 3 or (share >= 0.12 and rank <= 4):
                    tier = 'bersaing'
                else:
                    tier = 'jangan'
                alamat, binaan = sup.get((kec, norm(kel), no), ('', 0))
                baris.append(dict(kec=kec, kel=kel, tps=no, pkb=pkb, tot=tot,
                                  rank=rank, gap=gap, share=round(share * 100, 2),
                                  tier=tier, gain=round(CAPTURE * (tot - pkb)),
                                  alamat=alamat or sheet.get((kec, norm(kel), no), ''),
                                  binaan=binaan))
    return baris


def sl(v, kursi):
    d = {p: 1 for p in v}
    k = {p: 0 for p in v}
    for _ in range(kursi):
        p = max(v, key=lambda q: v[q] / d[q])
        k[p] += 1
        d[p] += 2
    return k


def urutan(v, kursi, tambahan=0):
    """Urutan kursi dibagikan. Posisi ke-1 berarti kursi pertama yang jatuh."""
    w = dict(v)
    w['PKB'] += tambahan
    d = {p: 1 for p in w}
    hasil = []
    for _ in range(kursi):
        p = max(w, key=lambda q: w[q] / d[q])
        hasil.append(p)
        d[p] += 2
    return hasil


def biaya(v, kursi):
    dasar = sl(v, kursi)['PKB']
    lo, hi = 0, 300000
    while lo < hi:
        mid = (lo + hi) // 2
        w = dict(v)
        w['PKB'] += mid
        if sl(w, kursi)['PKB'] > dasar:
            hi = mid
        else:
            lo = mid + 1
    return lo, dasar


def suara_dapil(sk, n, kec):
    asli = sk['dapil'][n - 1]['kecamatan']
    ks = [norm(x) for x in asli]
    v = {p: 0 for p in SING}
    for kc in ks:
        for p, x in kec[kc].items():
            v[p] = v.get(p, 0) + x
    return v, ks, asli


def kontak():
    def baca(f):
        d = muat(f)
        hasil = collections.Counter()
        for r in d:
            if r.get('kel'):
                hasil[(norm(r['kec'] or ''), r['kel'].upper())] += r['n']
        return hasil
    return baca('sb_master_pemilih.json'), baca('sb_data_ktp.json')


def main():
    sim = muat('simulasi-2029.json')
    pem = muat('pemilu-2024.json')
    kec = {}
    for k, d in pem['dapil'].items():
        for kd in d['kecamatan_detail']:
            kec[norm(kd['nama'])] = {p['singkat']: p['total'] for p in kd['partai']}
    baris = baca_tps()
    binaan, ktp = kontak()

    keluaran = dict(meta=dict(
        sumber_suara='KPU Pemilu 2024, rekap TPS (dhasil_tps.json)',
        sumber_kontak='Supabase master_pemilih dan data_ktp, agregat per kelurahan',
        asumsi_capture=f'{int(CAPTURE * 100)} persen suara non-PKB per TPS',
        catatan='Supabase tidak menyimpan suara per TPS. Suara TPS dari KPU, kontak dari Supabase.'))

    for sk in ('A', 'B'):
        dapil = []
        for d in sim[sk]['dapil']:
            v, ks, asli = suara_dapil(sim[sk], d['nomor'], kec)
            biaya1, sekarang = biaya(v, d['kursi'])
            posisi = [i + 1 for i, p in enumerate(urutan(v, d['kursi'])) if p == 'PKB']
            posisi_target = [i + 1 for i, p in enumerate(urutan(v, d['kursi'], biaya1)) if p == 'PKB']
            dapil.append(dict(nomor=d['nomor'], kursi=d['kursi'], pkb=v['PKB'],
                             sekarang=sekarang, biaya=biaya1, kecamatan=[x.title() for x in asli],
                             posisi=posisi, posisi_target=posisi_target,
                             kursi_baru=posisi_target[-1] if len(posisi_target) > len(posisi) else 0))
        # pilih dapil termurah sampai target kursi tercapai
        sisa = TARGET[sk] - sum(x['sekarang'] for x in dapil)
        urut = sorted(dapil, key=lambda x: x['biaya'])
        pilih = [x['nomor'] for x in urut[:sisa]]
        total_biaya = sum(x['biaya'] for x in urut[:sisa])

        rute = []
        for n in pilih:
            info = next(x for x in dapil if x['nomor'] == n)
            ks = set(norm(x) for x in info['kecamatan'])
            sub = [r for r in baris if r['kec'] in ks]
            inti = sorted([r for r in sub if r['tier'] != 'jangan'],
                          key=lambda r: (ORD[r['tier']], -r['gain']))
            acc, pakai = 0, []
            for r in inti:
                if acc >= info['biaya']:
                    break
                pakai.append(r)
                acc += r['gain']
            perluas = 0
            if acc < info['biaya']:
                for r in sorted([r for r in sub if r['tier'] == 'jangan'], key=lambda r: -r['gain']):
                    if acc >= info['biaya']:
                        break
                    pakai.append(r)
                    acc += r['gain']
                    perluas += 1

            # skenario garap intensif 25 persen
            acc2, pakai2, perluas2 = 0, 0, 0
            for r in inti:
                if acc2 >= info['biaya']:
                    break
                pakai2 += 1
                acc2 += round(0.25 * (r['tot'] - r['pkb']))
            if acc2 < info['biaya']:
                for r in sorted([r for r in sub if r['tier'] == 'jangan'], key=lambda r: -r['gain']):
                    if acc2 >= info['biaya']:
                        break
                    pakai2 += 1
                    perluas2 += 1
                    acc2 += round(0.25 * (r['tot'] - r['pkb']))

            kelompok = collections.defaultdict(lambda: dict(kel='', pkb=0, gain=0, tps=0,
                                                            menang=0, bersaing=0, jangan=0,
                                                            daftar=[]))
            for r in sub:
                g = kelompok[(r['kec'], r['kel'])]
                g['kel'] = r['kel'].title()
                g['kec'] = r['kec'].title()
                g['pkb'] += r['pkb']
                g['gain'] += r['gain']
                g['tps'] += 1
                g[r['tier']] += 1
                g['daftar'].append(r)
            daftar_kel = []
            for g in kelompok.values():
                prio = [r for r in g['daftar'] if r['tier'] != 'jangan']
                prio.sort(key=lambda r: -r['gain'])
                daftar_kel.append(dict(
                    kel=g['kel'], kec=g['kec'], pkb=g['pkb'], tps=g['tps'],
                    menang=g['menang'], bersaing=g['bersaing'], jangan=g['jangan'],
                    gain=g['gain'],
                    binaan=binaan.get((norm(g['kec']), g['kel'].upper()), 0),
                    ktp=ktp.get((norm(g['kec']), g['kel'].upper()), 0),
                    tier=('menang' if g['menang'] and g['menang'] >= g['tps'] / 2 else
                          'bersaing' if (g['menang'] + g['bersaing']) >= g['tps'] / 2 else 'jangan'),
                    tps_prio=[dict(tps=r['tps'], pkb=r['pkb'], tot=r['tot'], rank=r['rank'],
                                   gap=r['gap'], share=r['share'], tier=r['tier'], gain=r['gain'])
                              for r in prio[:3]]))
            daftar_kel.sort(key=lambda x: -x['gain'])
            inti_kel = [k for k in daftar_kel if k['tier'] != 'jangan']
            rute.append(dict(
                nomor=n, kecamatan=info['kecamatan'], kursi=info['kursi'],
                sekarang=info['sekarang'], pkb=info['pkb'], biaya=info['biaya'],
                posisi=info['posisi'], posisi_target=info['posisi_target'],
                kursi_baru=info['kursi_baru'],
                tps_total=len(sub),
                tps_inti=sum(1 for r in sub if r['tier'] != 'jangan'),
                tps_pakai=len(pakai),
                tps_perluas=perluas,
                tps_pakai25=pakai2,
                tps_perluas25=perluas2,
                gain_inti=sum(r['gain'] for r in sub if r['tier'] != 'jangan'),
                kelurahan=inti_kel[:8],
                kel_total=len(daftar_kel),
                kel_jangan=len(daftar_kel) - len(inti_kel),
                tps_prio=[dict(kel=r['kel'].title(), kec=r['kec'].title(), tps=r['tps'],
                               pkb=r['pkb'], tot=r['tot'], alamat=r['alamat'], binaan=r['binaan'],
                               rank=r['rank'], gap=r['gap'], share=r['share'],
                               tier=r['tier'], gain=r['gain'])
                          for r in sorted(pakai, key=lambda r: (ORD[r['tier']], -r['gain']))[:12]]))
        keluaran[sk] = dict(target=TARGET[sk], sekarang=sum(x['sekarang'] for x in dapil),
                            tambah=sisa, biaya=total_biaya, rute=rute,
                            semua=[dict(nomor=x['nomor'], kursi=x['kursi'], pkb=x['pkb'],
                                        sekarang=x['sekarang'], posisi=x['posisi'],
                                        posisi_target=x['posisi_target'],
                                        kursi_baru=x['kursi_baru']) for x in dapil],
                            tps_pakai=sum(x['tps_pakai'] for x in rute))
    json.dump(keluaran, open(BASE + 'okupansi-2029.json', 'w'), ensure_ascii=False, indent=1)
    for sk in ('A', 'B'):
        k = keluaran[sk]
        print(sk, 'target', k['target'], 'dari', k['sekarang'], 'biaya', f"{k['biaya']:,}",
              'tps', k['tps_pakai'], [(r['nomor'], r['biaya'], r['tps_pakai']) for r in k['rute']])


if __name__ == '__main__':
    main()
