# Komorka P - profile W(y) z optymalnymi wyborami klas reszt (pazdziernik 2026)
# Wymaga wczesniejszego uruchomienia komorek A i B (W_y) w tym samym kernelu.
# Dla kazdego z zapisuje plik profil_z{z}.txt z liniami: "y W wybor".
# Kazda dlugosc jest zapisywana od razu; juz policzone sa pomijane,
# wiec po przerwaniu wystarczy uruchomic profile_nocne() ponownie.
import os, time

PLAN_PROFILI = [(53, 104), (59, 116), (61, 130)]   # (z, pierwsza dlugosc = h(r) - 2; h(16)=106, h(17)=118, h(18)=132)
Y_DO = 700


def _profil(z, y_od, y_do):
    plik = "profil_z%d.txt" % z
    zrobione = set()
    if os.path.exists(plik):
        for l in open(plik):
            if l.strip():
                zrobione.add(int(l.split()[0]))
    t0 = time.time(); n = 0
    with open(plik, "a") as f:
        for y in range(y_od, y_do + 1, 2):
            if y in zrobione:
                continue
            w, _, wyb = policz_Wy(y, z=z, gadatliwy=False)
            f.write("%d %d %s\n" % (y, w, ",".join(map(str, wyb)) if wyb is not None else "-"))
            f.flush(); n += 1
            if n % 25 == 0:
                print("  z=%d: y=%d, W=%d, %.0f s" % (z, y, w, time.time() - t0), flush=True)
    print("z=%d gotowe: dopisano %d dlugosci w %.0f s -> %s" % (z, n, time.time() - t0, plik), flush=True)


def profile_nocne():
    for z, y_od in PLAN_PROFILI:
        _profil(z, y_od, Y_DO)
    print("Wszystkie profile gotowe.")


print("Plan: profile dla z = %s, dlugosci do %d. Uruchom:  profile_nocne()"
      % (", ".join(str(z) for z, _ in PLAN_PROFILI), Y_DO))
