# Dynamika sita Eratostenesa ponad granicą 2q — twierdzenia i dowody

*Wersja robocza 5 do weryfikacji. Najlepiej czytać w JupyterLab (podgląd Markdown), gdzie wzory się renderują.*

**Zmiany względem wersji 4 (po drugiej recenzji):** wprowadzone $`H(N) := \max \mathcal{D}(N)`$ dla dowolnego $`N`$, z $`h(k) := H(p_k\#)`$; wszędzie, gdzie argumentem jest moduł, $`h(qN)`$ zastąpione przez $`H(qN)`$; dodana Uwaga 3.4 z dowodem, że $`H(qN) \le N`$, więc Wnioski 3.1–3.3 mieszczą się w dziedzinie Twierdzenia 3. Wyniki i weryfikacja bez zmian.

**Zmiany wersji 4 względem wersji 3 (po pierwszej recenzji):** dopisany warunek $`0 < g < N`$ (Tw. 1, 3) i $`0 < |s| < N`$ (Tw. 4); jawna zależność $`B_g`$ i $`M_2`$ od $`q`$ oraz $`g < H(qN)`$ we Wniosku 3.2; zawężone zdanie o przedziale maksymalnym we Wniosku 3.3; „pierwsze pojawienie się" w Tw. 5 oparte na nowym Lemacie 6 i Wniosku 5.1; Tw. 6 nazwane warunkiem wystarczającym; poprawiony zapis zbioru $`T`$ w Tw. 7. Wyniki i weryfikacja bez zmian.

**Zmiany wersji 3 względem wersji 2:** dodana sekcja 10 — przeniesienie wyników na konstelacje, prawo narodzin konstelacji, warunek wystarczający ścisłości łańcucha Holta, postać w momentach dla konstelacji oraz dokładne modele luk do 104 („pakiet Holta"). Sekcje 0–9 bez zmian.

**Zmiany wersji 2 względem wersji 1:** doprecyzowana klasyfikacja brakujących różnic (opóźnienie/zabójstwo oraz dziura/cień, §5); nowa sekcja z pełną klasyfikacją tabeli Zillera do k = 30 (§6); poprawiony spis narodzin maksimów — wycofane twierdzenie, że od k = 47 maksima rodzą się wyłącznie z ratunku (§7); uzupełniona tabela weryfikacji o solver CP-SAT i tabelę Gerbicza–Bożka (§9). Części dowodowe (§1–§5) bez zmian merytorycznych.

---

## 0. Oznaczenia i założenia

Niech $`N`$ będzie iloczynem różnych liczb pierwszych, przy czym $`2 \mid N`$. Niech $`q`$ będzie nieparzystą liczbą pierwszą, $`q \nmid N`$. Główny przypadek: $`N = p_k\#`$, $`q = p_{k+1}`$.

Oznaczmy $`\Omega(N) = \{x \in \mathbb{Z} : \gcd(x,N) = 1\}`$ — zbiór okresowy modulo $`N`$.

**Człon.** Dla parzystego $`g`$ z $`2 \le g < N`$ i $`j \ge 1`$ mówimy, że $`x \in \Omega(N)`$ (rozważane modulo $`N`$) jest *członem rozpiętości $`g`$ i długości $`j`$* w $`\mathcal{G}(N)`$, jeśli $`x + g \in \Omega(N)`$ oraz w przedziale otwartym $`(x, x+g)`$ leży dokładnie $`j-1`$ elementów $`\Omega(N)`$.

Zbiór punktów członu: $`P(x) = \{ t \in [0,g] : x + t \in \Omega(N) \}`$. Zawiera $`0`$ i $`g`$, ma $`j+1`$ elementów, a kolejne różnice to $`j`$ kolejnych luk cyklu $`\mathcal{G}(N)`$ o sumie $`g`$.

Liczność: $`n_{g,j}(N) = \#\{x \bmod N : x \text{ jest członem rozpiętości } g \text{ i długości } j\}`$. Dla $`j = 1`$ jest to liczba wystąpień luki $`g`$ w cyklu. W języku Holta i Rudda $`n_{g,j}`$ to populacja członów napędzających (driving terms) długości $`j`$ dla luki $`g`$.

**Klasy.** Dla członu $`x`$ dzielimy $`P(x)`$ na klasy kongruencji modulo $`q`$: $`t \sim t' \iff t \equiv t' \pmod q`$. Zbiór klas oznaczamy $`\mathcal{C}(x)`$.

$`\mathcal{D}(N)`$ oznacza zbiór długości luk występujących w $`\mathcal{G}(N)`$, a $`H(N) := \max \mathcal{D}(N)`$ — największą lukę cyklu, czyli wartość funkcji Jacobsthala dla $`N`$. Dla primoriali piszemy, zgodnie z Zillerem, $`\mathcal{D}(k) := \mathcal{D}(p_k\#)`$ i $`h(k) := H(p_k\#)`$.

---

## 1. Lematy podstawowe

**Lemat 1 (parzystość).** Dla $`t, t' \in P(x)`$: $`\; t \equiv t' \pmod q \iff 2q \mid (t - t')`$.

*Dowód.* Ponieważ $`2 \mid N`$, każdy element $`\Omega(N)`$ jest nieparzysty, więc $`t - t' = (x+t) - (x+t')`$ jest parzyste. Dla parzystego $`d`$ i nieparzystej liczby pierwszej $`q`$ mamy $`q \mid d \iff 2q \mid d`$. $`\square`$

**Lemat 2 (podniesienia).** Dla $`x`$ modulo $`N`$ istnieje dokładnie $`q`$ reszt $`X`$ modulo $`qN`$ z $`X \equiv x \pmod N`$, mianowicie $`X_i = x + iN`$, $`i = 0, \dots, q-1`$, a ich reszty modulo $`q`$ przebiegają cały zbiór $`\mathbb{Z}/q`$.

*Dowód.* Ponieważ $`\gcd(N, q) = 1`$, odwzorowanie $`i \mapsto iN \bmod q`$ jest bijekcją $`\mathbb{Z}/q \to \mathbb{Z}/q`$. $`\square`$

**Lemat 3.** Jeśli $`X \equiv x \pmod N`$, to dla każdego $`t`$: $`\; X + t \in \Omega(qN) \iff \big(x + t \in \Omega(N) \text{ oraz } q \nmid X + t\big)`$.

*Dowód.* $`\gcd(X+t, qN) = 1 \iff \gcd(X+t, N) = 1 \wedge q \nmid X+t`$, a $`X + t \equiv x + t \pmod N`$. $`\square`$

---

## 2. Twierdzenie 1 — prawo przejścia (wersja ogólna)

**Twierdzenie 1.** Niech $`x`$ będzie członem rozpiętości $`g`$, $`2 \le g < N`$, i długości $`j`$ w $`\mathcal{G}(N)`$, z klasami $`\mathcal{C} = \mathcal{C}(x)`$. Spośród $`q`$ podniesień $`X`$ członu $`x`$ do modułu $`qN`$:

1. dla każdej klasy $`C \in \mathcal{C}`$ istnieje dokładnie jedno podniesienie $`X_C`$, w którym $`q \mid X_C + t`$ dla wszystkich $`t \in C`$ i dla żadnego $`t \in P \setminus C`$;
2. pozostałe $`q - |\mathcal{C}|`$ podniesień nie mają żadnego punktu podzielnego przez $`q`$.

W konsekwencji:

- podniesienia z punktu 2 są członami rozpiętości $`g`$ i długości $`j`$ w $`\mathcal{G}(qN)`$;
- podniesienie $`X_C`$ z $`C \cap \{0, g\} = \emptyset`$ jest członem rozpiętości $`g`$ i długości $`j - |C|`$;
- podniesienie $`X_C`$ z $`C \cap \{0, g\} \neq \emptyset`$ nie jest członem rozpiętości $`g`$.

Każdy człon rozpiętości $`g`$ w $`\mathcal{G}(qN)`$ powstaje w ten sposób z dokładnie jednego członu $`x`$ i dokładnie jednego podniesienia. Zatem

```math
n_{g,m}(qN) \;=\; \sum_{x} \Big( [\,j(x) = m\,]\cdot\big(q - |\mathcal{C}(x)|\big) \;+\; \#\{ C \in \mathcal{C}(x) : C \cap \{0,g\} = \emptyset,\; j(x) - |C| = m \} \Big),
```

gdzie suma przebiega po wszystkich członach rozpiętości $`g`$ w $`\mathcal{G}(N)`$.

*Dowód.* $`q \mid X + t \iff X \equiv -t \pmod q`$. Zbiór $`\{-t \bmod q : t \in P\}`$ ma dokładnie $`|\mathcal{C}|`$ elementów, po jednym na klasę. Z Lematu 2 każda reszta modulo $`q`$ jest przyjmowana przez dokładnie jedno podniesienie; podniesienie o reszcie $`-t`$ zabija dokładnie punkty klasy $`t`$ i żadne inne. Pozostałe $`q - |\mathcal{C}|`$ podniesień nie zabija niczego. To daje 1 i 2.

Z Lematu 3 punkty $`\Omega(qN)`$ w $`[X, X+g]`$ to $`P`$ bez punktów zabitych. Końce przeżywają wtedy i tylko wtedy, gdy zabita klasa nie zawiera $`0`$ ani $`g`$. Jeśli zabita jest klasa wewnętrzna $`C`$, zostaje $`j + 1 - |C|`$ punktów, czyli człon długości $`j - |C|`$.

Odwrotnie, jeśli $`X`$ jest członem rozpiętości $`g`$ w $`\mathcal{G}(qN)`$, to z Lematu 3 $`x = X \bmod N`$ spełnia $`x, x+g \in \Omega(N)`$, więc jest członem rozpiętości $`g`$ w $`\mathcal{G}(N)`$, a $`X`$ jest jednym z jego podniesień; $`x`$ jest wyznaczone przez $`X`$ jednoznacznie. $`\square`$

**Uwaga 1.1 (przypadek Holta).** Jeśli $`g < 2q`$, to z Lematu 1 żadne dwa punkty nie są przystające (różnice są dodatnie i mniejsze od $`2q`$), więc wszystkie klasy są jednoelementowe, $`|\mathcal{C}| = j+1`$, i wzór przyjmuje postać

```math
n_{g,m}(qN) = (q - m - 1)\, n_{g,m}(N) + m\, n_{g,m+1}(N),
```

czyli Twierdzenie 3.2 z pracy Holta i Rudda (2015). Twierdzenie 1 rozszerza je na dowolne $`g`$. Holt i Rudd piszą wprost (Wniosek 5.3 i rys. 5), że dla $`g \ge 2q`$ nie potrafią określić długości powstających członów; Twierdzenie 1 określa je dokładnie. Najnowsza praca Holta (sierpień 2026) nadal podaje modele dokładne tylko dla rozpiętości $`< 2p_1`$.

---

## 3. Wniosek — drabina progów

**Wniosek 1.** Klasa o $`s`$ punktach w członie rozpiętości $`g`$ wymaga, by odległość między jej skrajnymi punktami była wielokrotnością $`2q`$ nie mniejszą niż $`2q(s-1)`$; w szczególności $`g \ge 2q(s-1)`$.

Jeśli dodatkowo $`3 \mid N`$ i $`q \neq 3`$, to klasa trzypunktowa wymaga rozpiętości co najmniej $`6q`$.

*Dowód drugiej części.* Niech $`t_1 < t_2 < t_3`$ leżą w jednej klasie: $`t_2 = t_1 + 2qa`$, $`t_3 = t_2 + 2qb`$, $`a, b \ge 1`$. Gdyby $`a = b = 1`$, reszty modulo 3 wynosiłyby $`t_1,\; t_1 + 2q,\; t_1 + 4q \equiv t_1,\; t_1 - q,\; t_1 + q`$, a ponieważ $`3 \nmid q`$, są to wszystkie trzy reszty — jeden z punktów byłby podzielny przez 3, wbrew $`3 \mid N`$. Zatem $`a + b \ge 3`$ i $`t_3 - t_1 \ge 6q`$. $`\square`$

**Związek z Hagedornem.** Propozycja 3.3 z pracy Hagedorna (2009) daje ograniczenia $`m_1 = 3`$, $`m_2 = 4`$, $`m_3 = 6`$ (w skali połówkowej, przy $`3, 5 \mid N`$). W skali pełnej oznacza to progi: klasa 3-punktowa od $`6q`$, 4-punktowa od $`8q`$, 5-punktowa od $`12q`$. Progów dla $`s \ge 4`$ nie dowodzimy tu osobno — powołujemy się na Hagedorna. Obliczeniowo sprawdziliśmy, że progi $`2q, 6q, 8q, 12q`$ są **ostre**: pierwsze wystąpienie klasy danej wielkości leży dokładnie na progu (§9).

**Wniosek 1.1 (reżim par).** Przy $`3 \mid N`$ i $`g < 6q`$ wszystkie klasy mają co najwyżej dwa punkty, odległe o $`2q`$ lub $`4q`$ (to drugie tylko dla $`g \ge 4q`$).

---

## 4. Twierdzenie 2 — postać w momentach dwumianowych

Dla ustalonego $`g`$ definiujemy

```math
S_k(N) = \sum_{j \ge 1} \binom{j-1}{k}\, n_{g,j}(N), \qquad k = 0, 1, 2, \dots
```

oraz, dla skończonego zbioru $`A`$, $`\; W_N(A) = \#\{x \bmod N : x + a \in \Omega(N)\ \forall a \in A\}`$.

**Lemat 4.** $`\displaystyle S_k(N) = \sum_{\substack{T \subseteq \{1,\dots,g-1\}\\ |T| = k}} W_N(T \cup \{0, g\}).`$

*Dowód.* Para ($`x`$, $`T`$) z $`x + a \in \Omega(N)`$ dla $`a \in T \cup \{0,g\}`$ to dokładnie człon $`x`$ rozpiętości $`g`$ wraz z $`k`$-elementowym podzbiorem $`T`$ jego punktów wewnętrznych. Człon długości $`j`$ ma $`j - 1`$ punktów wewnętrznych, więc $`\binom{j-1}{k}`$ takich podzbiorów. $`\square`$

**Lemat 5 (CRT).** $`W_{qN}(A) = W_N(A)\cdot\big(q - \nu_q(A)\big)`$, gdzie $`\nu_q(A)`$ to liczba różnych reszt zbioru $`A`$ modulo $`q`$.

*Dowód.* $`x \bmod qN`$ odpowiada parze $`(x \bmod N,\; x \bmod q)`$. Warunek modulo $`q`$ to $`x \not\equiv -a`$ dla $`a \in A`$, co wyklucza dokładnie $`\nu_q(A)`$ reszt. $`\square`$

**Twierdzenie 2.** Dla każdego $`k \ge 0`$:

```math
S_k(qN) = (q - k - 2)\, S_k(N) + \Pi_k(N), \qquad
\Pi_k(N) = \sum_{|T| = k} \big( k + 2 - \nu_q(T \cup \{0,g\}) \big)\, W_N(T \cup \{0,g\}) \;\ge\; 0 .
```

*Dowód.* Z Lematów 4 i 5: $`S_k(qN) = \sum_T W_N(A_T)(q - \nu_q(A_T))`$, gdzie $`A_T = T \cup \{0,g\}`$ ma $`k+2`$ elementów. Wystarczy zapisać $`q - \nu_q = (q - k - 2) + (k + 2 - \nu_q)`$. Liczba $`k + 2 - \nu_q(A_T)`$ to liczba elementów $`A_T`$ minus liczba klas — nieujemna. $`\square`$

**Uwaga 2.1.** Współczynnik $`(q-k-2)`$ to wartość własna Holta; współrzędne $`S_k`$ to jego współrzędne własne (macierz $`L`$ Pascala). Twierdzenie 2 mówi, że **w tych współrzędnych nieliniowość jest wyłącznie nieujemnym źródłem**. Liczności samych luk odzyskuje się przez odwrócenie dwumianowe:

```math
n_{g,1}(N) = \sum_{k \ge 0} (-1)^k S_k(N),
```

bo $`\sum_k (-1)^k \binom{j-1}{k} = [\,j = 1\,]`$. Zmniejszenia populacji luk (zabójstwa) pojawiają się więc wyłącznie przez naprzemienność tej sumy.

---

## 5. Twierdzenie 3 — prawo narodzin

**Twierdzenie 3.** Dla każdego parzystego $`g`$ z $`2 \le g < N`$ (wielkości $`e_g`$ i $`B_g(N)`$ zależą od $`q`$; gdy trzeba to podkreślić, piszemy $`e^{(q)}_g`$ i $`B^{(q)}_g(N)`$):

```math
n_{g,1}(qN) = (q - 2 + e_g)\, n_{g,1}(N) + B_g(N),
\qquad e_g = [\,2q \mid g\,],
```

gdzie $`B_g(N)`$ to liczba członów $`x`$ długości $`j \ge 2`$, których **wszystkie punkty wewnętrzne leżą w jednej klasie modulo $`q`$, rozłącznej z klasami końców**.

Równoważnie, w języku konstelacji (ciągów $`j`$ kolejnych luk $`\mathcal{G}(N)`$):

```math
B_g(N) = \sum_{\substack{(a_1,\dots,a_j),\; j \ge 2,\; \sum a_i = g \\ 2q \,\nmid\, a_1,\;\; 2q \,\nmid\, a_j \\ 2q \,\mid\, a_i \text{ dla } 1 < i < j}} \mathcal{N}_N(a_1, \dots, a_j),
```

gdzie $`\mathcal{N}_N(\cdot)`$ to liczba wystąpień konstelacji w cyklu.

*Dowód.* Twierdzenie 1 dla $`m = 1`$. Człony długości 1 mają punkty $`\{0, g\}`$; są one przystające dokładnie wtedy, gdy $`2q \mid g`$ (Lemat 1), więc $`|\mathcal{C}| = 2 - e_g`$ i nietkniętych podniesień jest $`q - 2 + e_g`$. Człon długości $`j \ge 2`$ daje lukę wtedy i tylko wtedy, gdy ma klasę wewnętrzną o $`j - 1`$ punktach, czyli gdy wszystkie punkty wewnętrzne są w jednej klasie rozłącznej z końcami — i daje wtedy dokładnie jedną lukę.

Tłumaczenie na konstelacje: punkty wewnętrzne $`t_1 < \dots < t_{j-1}`$ leżą w jednej klasie $`\iff`$ wszystkie luki między nimi, $`a_2, \dots, a_{j-1}`$, są podzielne przez $`2q`$ (Lemat 1). Klasa jest rozłączna z klasą $`0`$ $`\iff 2q \nmid t_1 = a_1`$, a z klasą $`g`$ $`\iff 2q \nmid g - t_{j-1} = a_j`$. $`\square`$

**Szczególnie, przy $`3 \mid N`$ i $`g < 6q`$** (Wniosek 1.1) jedynymi składnikami są pary $`(a, b)`$ z $`2q \nmid a`$, $`2q \nmid b`$ oraz trójki $`(u, v, w)`$ z $`v \in \{2q, 4q\}`$, $`2q \nmid u`$, $`2q \nmid w`$. Para, w której jedna luka jest wielokrotnością $`2q`$, **nie** rodzi luki — to *zabójstwo*. Trójka z luką $`2q`$ (lub $`4q`$) w środku **rodzi** lukę o sumie trzech — to *ratunek*.

**Wniosek 3.1 (reżim spokojny).** Jeśli wszystkie luki $`\mathcal{G}(N)`$ są mniejsze niż $`2q`$, to $`B_g(N) = n_{g,2}(N)`$ dla każdego $`g`$, a więc

```math
n_{g,1}(qN) = (q - 2 + e_g)\, n_{g,1}(N) + n_{g,2}(N),
```

```math
\mathcal{D}(qN) = \mathcal{D}(N) \,\cup\, \{\, a + b : (a,b) \text{ sąsiednie luki w } \mathcal{G}(N) \,\},
```

a największa luka $`\mathcal{G}(qN)`$ jest największą sumą dwóch sąsiednich luk $`\mathcal{G}(N)`$.

*Dowód.* Każda luka jest dodatnia, parzysta i $`< 2q`$, więc nie jest wielokrotnością $`2q`$: każda para się kwalifikuje, a konstelacji z luką środkową podzielną przez $`2q`$ nie ma. Zawieranie $`\mathcal{D}(N) \subseteq \mathcal{D}(qN)`$ wynika z $`q - 2 + e_g \ge 1`$. $`\square`$

**Zastosowanie do primoriali.** Wszystkie luki $`\mathcal{G}(p_k\#)`$ są $`\le h(k)`$, a ze znanych wartości funkcji Jacobsthala $`h(k) < 2p_{k+1}`$ dla wszystkich $`k \le 18`$ ($`h(18) = 132 < 134 = 2p_{19}`$), natomiast $`h(19) = 152 \ge 142 = 2p_{20}`$. Zatem dla $`k \le 18`$:
$`\mathcal{D}(k+1) = \mathcal{D}(k) \cup \Sigma_2(k)`$ oraz $`h(k+1) = \max \Sigma_2(k)`$, gdzie $`\Sigma_2(k)`$ to zbiór sum dwóch sąsiednich luk w $`\mathcal{G}(p_k\#)`$. Etap $`k = 20`$ jest pierwszym, przy którego budowie możliwe są zabójstwa i ratunki.

**Wniosek 3.2 (brakujące różnice — dwie klasyfikacje).** Liczba parzysta $`g`$ z $`2 \le g < H(qN)`$ nie występuje jako luka w $`\mathcal{G}(qN)`$ wtedy i tylko wtedy, gdy $`n_{g,1}(N) = 0`$ i $`B^{(q)}_g(N) = 0`$. Cały ten zakres leży w dziedzinie Twierdzenia 3, bo $`H(qN) \le N`$ (Uwaga 3.4).

Niech $`M^{(q)}_2(N)`$ będzie największą sumą $`a+b`$ po parach sąsiednich luk $`\mathcal{G}(N)`$ kwalifikujących się przy $`q`$ ($`2q \nmid a`$, $`2q \nmid b`$) — *zasięgiem par*. Wielkość ta zależy od $`q`$, nie tylko od $`N`$. Brakującą różnicę $`g`$ klasyfikujemy na dwa niezależne sposoby.

*Według przyczyny:* **opóźnienie** — w $`\mathcal{G}(N)`$ nie ma żadnej pary sąsiednich luk o sumie $`g`$; **zabójstwo** — takie pary są, ale każda zawiera lukę podzielną przez $`2q`$.

*Według położenia:* **dziura** — $`g < M^{(q)}_2(N)`$, czyli pary sięgają ponad $`g`$, ale żadna nie sumuje się do $`g`$; **cień** — $`M^{(q)}_2(N) < g < H(qN)`$, czyli $`g`$ leży ponad zasięgiem par, pod maksimum, które wobec tego musiało urodzić się z konstelacji długości $`\ge 3`$ (z ratunku).

W reżimie spokojnym (Wniosek 3.1) $`H(qN) = M^{(q)}_2(N)`$, więc cienie są niemożliwe, a zabójstwa również: **każda brakująca różnica jest dziurą i opóźnieniem**.

**Wniosek 3.3 (maksimum).** Największa luka $`\mathcal{G}(qN)`$ to największa z liczb: największa luka $`\mathcal{G}(N)`$ oraz sumy konstelacji kwalifikujących się w $`B_g`$. Maksimum *z pary* — gdy osiąga je kwalifikująca się para; *z ratunku* — gdy osiągają je wyłącznie konstelacje długości $`\ge 3`$. Jeśli maksimum pochodzi z kwalifikującej się konstelacji długości $`j`$, to w przedziale maksymalnym $`\mathcal{G}(qN)`$ liczba $`q`$ zabija sama dokładnie $`j-1`$ punktów (pozostałe są pokryte przez czynniki $`N`$). W reżimie par ($`3 \mid N`$, $`H(qN) < 6q`$) daje to 1 punkt dla pary i 2 punkty dla trójki; tylko w tym reżimie „ratunek" oznacza trójkę z luką środkową $`2q`$ lub $`4q`$ — poza nim mogą to być dłuższe konstelacje.


**Uwaga 3.4 (dziedzina).** Twierdzenie 3 jest sformułowane dla $`g < N`$, a Wnioski 3.1–3.3 dotyczą wszystkich luk $`\mathcal{G}(qN)`$, czyli $`g \le H(qN)`$. Mieszczą się więc w dziedzinie twierdzenia, o ile $`H(qN) \le N`$. **Zachodzi to dla każdego parzystego bezkwadratowego $`N`$ z co najmniej jednym nieparzystym czynnikiem pierwszym i każdej nieparzystej liczby pierwszej $`q \nmid N`$.**

*Dowód.* Korzystamy z klasycznego oszacowania Jacobsthala $`H(M) \le 2^{\omega(M)}`$, gdzie $`\omega(M)`$ to liczba czynników pierwszych $`M`$. Mamy $`\omega(qN) = \omega(N) + 1`$. Jeśli $`\omega(N) \ge 3`$, to $`N \ge 2 \cdot 3 \cdot 5 = 30`$ i każdy kolejny czynnik jest $`\ge 7`$, więc $`2^{\omega(N)+1} \le N`$. Jeśli $`N = 2p`$ z $`p \ge 5`$, to $`H(qN) \le 8 \le 2p`$. Jeśli $`N = 6`$, to luki $`\mathcal{G}(6)`$ to naprzemiennie 4 i 2, a punkty usuwane przez $`q \ge 5`$ są od siebie odległe o co najmniej $`2q \ge 10`$, więc nie usuwają dwóch sąsiednich punktów i $`H(6q) = 6`$. $`\square`$

Wyjątkiem jest tylko $`N = 2`$, gdzie $`H(2q) = 4 > 2`$ — tego przypadku nie rozważamy. Dla primoriali $`N = p_k\#`$, $`k \ge 2`$, daje to $`H(qN) = h(k+1) \le p_k\#`$. Sprawdzono też obliczeniowo: oszacowanie Jacobsthala na 163 modułach i nierówność $`H(qN) \le N`$ na 504 parach $`(N, q)`$, bez wyjątku. Dowody Twierdzeń 1 i 3 same z warunku $`g < N`$ nie korzystają; jest on konwencją, dzięki której człon jest zawsze ciągiem kolejnych luk jednego okresu cyklu.
---

## 6. Zastosowanie: tabela Zillera do k = 30

Wszystkie brakujące różnice z tabeli Zillera dla $`k \le 30`$, z klasyfikacją według Wniosku 3.2. „Twierdzenie" oznacza, że klasyfikacja wynika z Wniosku 3.1 bez obliczeń. „Klasyfikator" — nasz program (wyczerpujące przeszukanie, bez przekroczeń budżetu). „SAT" — niezależne potwierdzenie solverem CP-SAT (dowód nieistnienia konstelacji $`(2q, g-2q)`$). „mod 3" — potrzebna konstelacja jest niedopuszczalna modulo 3, więc zabójstwo wykluczone arytmetycznie.

| k+1 | g | przyczyna | położenie | zasięg par $`M^{(q)}_2`$ | maksimum | podstawa |
|---|---|---|---|---|---|---|
| 6 | 20 | opóźnienie | dziura | 22 | 22 (para) | twierdzenie |
| 8 | 32 | opóźnienie | dziura | 34 | 34 (para) | twierdzenie |
| 14 | 86, 88 | opóźnienie | dziura | 90 | 90 (para) | twierdzenie |
| 15 | 98 | opóźnienie | dziura | 100 | 100 (para) | twierdzenie |
| 19 | 146 | opóźnienie | dziura | 152 | 152 (para) | twierdzenie |
| 20 | 166, 172 | opóźnienie | dziura | 174 | 174 (para) | klasyfikator + SAT |
| 20 | 170 | opóźnienie | dziura | 174 | 174 (para) | klasyfikator + SAT, mod 3 |
| 21 | 182 | opóźnienie | dziura | 184 | 190 (ratunek) | klasyfikator + SAT |
| 21 | 186, 188 | opóźnienie | **cień** | 184 | 190 (ratunek) | klasyfikator + SAT |
| 22 | 194 | opóźnienie | dziura | 200 | 200 (para i ratunek) | klasyfikator + SAT |
| 24 | 230 | opóźnienie | dziura | 232 | 234 (ratunek) | klasyfikator + SAT, mod 3 |
| 25 | 254 | opóźnienie | dziura | 258 | 258 (para) | klasyfikator (SAT nierozstrzygnięty w 1 h) |
| 25 | 256 | opóźnienie | dziura | 258 | 258 (para) | klasyfikator + SAT, mod 3 |
| 27 | 278 | opóźnienie | dziura | 280 | 282 (ratunek) | klasyfikator |
| 28 | 296 | opóźnienie | dziura | 300 | 300 (para) | klasyfikator + SAT, mod 3 |
| 28 | 298 | opóźnienie | dziura | 300 | 300 (para) | klasyfikator |
| 30 | 328 | opóźnienie | **cień** | 326 | 330 (ratunek) | klasyfikator |

Podsumowanie: **20 brakujących różnic, wszystkie opóźnienia, zero zabójstw; 17 dziur i 3 cienie.** Zasięg par $`M^{(q)}_2`$ ustalono z przebiegu domknięcia (k+1 = 20–27 oraz 326 przy k+1 = 30); dla k+1 = 28 i 30 typ maksimum pochodzi z konfiguracji maksymalnych Zillera (§7).

---

## 7. Spis narodzin maksimów (część empiryczna)

Źródła: konfiguracje maksymalne Zillera (wszystkie konfiguracje, $`n \le 54`$) oraz tabela Gerbicza–Bożka w OEIS A048670 (po jednym przedziale maksymalnym, $`n \le 64`$). Obie zgadzają się we wszystkich wspólnych przypadkach.

- $`n \le 19`$: wszystkie maksima z pary — zgodnie z Wnioskiem 3.1.
- $`n = 20`$: para (pierwszy etap, przy którym ratunek jest możliwy, ale nie wygrywa).
- $`n = 21 \dots 54`$ (Ziller, wszystkie konfiguracje): 22 razy wyłącznie ratunek, 6 razy wyłącznie para, 6 razy mieszane.
- $`n = 55 \dots 64`$ (Gerbicz–Bożek, jeden przedział): 6 razy ratunek, 4 razy para ($`n = 55, 57, 60, 63`$).
- W każdym ratunku oba punkty zabijane przez największą liczbę pierwszą są odległe dokładnie o $`2p_n`$ — bez wyjątku.
- Do $`n = 64`$ zachodzi $`h(n) < 4p_n`$, więc innych dróg narodzin maksimum być nie może.

**Wniosek empiryczny:** od progu obie drogi konkurują, z przewagą ratunku (mniej więcej dwie trzecie przypadków). Nie ma prostej reguły, która droga wygra: wcześniejsze przewidywanie, że od $`n = 47`$ maksima rodzą się wyłącznie z ratunku, **nie potwierdziło się** na danych dla $`n = 55`$–$`64`$. Nie potwierdziło się też sterowanie jednym parametrem (stosunkiem $`2p_n / h(n-1)`$): pary wygrywają nawet przy jego najniższych wartościach.

---

## 8. Czego te twierdzenia nie mówią

- Nic o prawdziwych lukach między liczbami pierwszymi — dotyczą wyłącznie cykli $`\mathcal{G}(N)`$.
- Progi klas dla $`s \ge 4`$ są wzięte od Hagedorna, nie dowiedzione tutaj.
- Zastosowanie do primoriali opiera się na opublikowanych wartościach $`h(k)`$ (Hagedorn 2009, Ziller–Morack 2016, Gerbicz i Bożek w OEIS A048670).
- Pojęcie opóźnienia jako ograniczenia na chwilę narodzin luki pochodzi od Holta i Rudda (2015, §5.3), podobnie jak spostrzeżenie o dziurach w sumach członów; nowe jest dokładne rozliczenie i klasyfikacja tabeli Zillera.
- Nie dowodzą Hipotezy 4.1 Zillera; dają jej równoważną postać w reżimie spokojnym: każda liczba parzysta poniżej $`h(k-1)`$ jest luką albo sumą dwóch sąsiednich luk w $`\mathcal{G}(p_{k-1}\#)`$.
- Spis maksimów (§7) jest empiryczny; nie mamy prawa rozstrzygającego, która droga wygra.

---

## 9. Stan weryfikacji obliczeniowej

| Co | Jak | Wynik |
|---|---|---|
| Tw. 1, wersja ogólna | siłowe wypisanie całych cykli, kod niezależny od silnika; 7#→11, 11#→13, 13#→17 oraz sita z pominiętą liczbą pierwszą (bez 7, bez 5, bez 11) | 1585 komórek, 0 błędów; 462 zabójstwa i 48 ratunków rozliczonych; klasy do 5 punktów |
| Drabina progów | te same testy | pierwsze klasy 2-, 3-, 4-, 5-punktowe dokładnie przy 2q, 6q, 8q, 12q |
| Tw. 1, reżim par | silnik zliczający; 23#→29#, 37#→41#, 41#→43#, 43#→47# | 805 komórek, 0 błędów |
| Tw. 2 | 37#→41#, 41#→43# | 609 komórek, 0 błędów, 493 z niezerowym źródłem |
| Dane silnika | przeciw danym Holta G(37#) i jego rekurencji | ponad 1300 komórek, 0 błędów |
| Wniosek 3.2 — przyczyna | klasyfikator, k+1 = 20–30 | 14 brakujących różnic: wszystkie opóźnienia |
| Wniosek 3.2 — niezależnie | solver CP-SAT na modelu spełnialności (model sprawdzony siłowo na 70 konstelacjach w G(19#)); 3 kontrole + 14 przypadków | kontrole zgodne; 10 z 14 potwierdzone (166, 170, 172, 182, 186, 188, 194, 230, 256, 296); 254 nierozstrzygnięte w 1 h; 278, 298, 328 nie liczone |
| Wniosek 3.2 — położenie | domknięcie k+1 = 20–27 (54 obecne różnice) oraz 326 przy k+1 = 30 | 50 z pary, 4 z ratunku (190, 216, 234, 282 — wszystkie maksima), 0 sprzeczności; 17 dziur, 3 cienie |
| Wniosek 3.3 | konfiguracje Zillera ($`n \le 54`$) i tabela Gerbicza–Bożka ($`n \le 64`$) | 51 przedziałów poprawnych; pełna zgodność źródeł; 28 ratunków, wszystkie z odległością dokładnie $`2p_n`$ |

**Otwarte przed publikacją:** przeczytanie i sprawdzenie dowodów (§1–§5).


---

## 10. Pakiet Holta — konstelacje, łańcuch Markowa, modele dokładne

Ta sekcja przenosi Twierdzenia 1–3 z luk na dowolne konstelacje i formułuje je w języku, którego używa Holt. Stan jego prac według ostatniego sprawdzenia: sformułowanie w języku łańcuchów Markowa dla konstelacji o $`|s| < 2p_1`$ pochodzi z pracy z 2025 roku (arXiv 2502.20470, rys. 5: przy $`|s| < 2p_1`$ fuzje zachodzą w osobnych obrazach konstelacji); praca z sierpnia 2026 (arXiv 2608.26384) utrzymuje to ograniczenie; w pracy z marca 2026 podaje zasięg modeli dokładnych: luki do 82 i konstelacje o rozpiętości do 62. W dodatku z 2023 roku (arXiv 2309.16833) pisze, że poza progiem $`2p_1`$ nie mógł być pewien liczności członów napędzających różnych długości — tę lukę zamykają Twierdzenia 4–6.

**Według pełnego tekstu pracy z 2026 roku (arXiv 2608.26384v3):** nasz Lemat 1 to jego Obserwacja 2.3 (minimalna odległość między fuzjami wynosi $`2p_{k+1}`$) — trzeba go przy nim cytować. Holt rozróżnia fuzje *brzegowe* (niszczą obraz jako człon napędzający; u nas: klasy zawierające punkty $`C`$) i *wewnętrzne* (skracają obraz; u nas: klasy rozłączne z $`C`$). Kilka fuzji brzegowych w jednym obrazie obsługuje dokładnie, dla każdej rozpiętości, przez $`\nu_s(p)`$ (jego Lemat 2.5) — stąd jego wzór na łączną liczbę wystąpień. **Kilku fuzji wewnętrznych w jednym obrazie nie obsługuje** — to one zmieniają rozkład długości i to rozlicza nasze Twierdzenie 4. Dla rozpiętości $`\ge 2p_1`$ podaje tylko policzone liczby (jego rys. 6 dla $`p \le 13`$), bez prawa. W zakończeniu wymienia jako bieżący cel modele dla luk $`84 \le g \le 90`$.

### 10.1. Oznaczenia

Konstelacja $`s = (s_1, \dots, s_m)`$ to ciąg $`m`$ luk o sumie $`|s|`$, z punktami $`C = \{c_0 = 0 < c_1 < \dots < c_m = |s|\}`$.

**Człon napędzający dla $`s`$** w $`\mathcal{G}(N)`$ (przy $`0 < |s| < N`$, analogicznie do §0) to $`x`$ z $`x + c \in \Omega(N)`$ dla wszystkich $`c \in C`$. Jego zbiór punktów $`P(x) = \{t \in [0, |s|] : x + t \in \Omega(N)\} \supseteq C`$, długość $`J = |P| - 1`$, punkty dodatkowe $`E = P \setminus C`$. Liczności: $`n_{s,J}(N)`$. Wystąpienia samej konstelacji to $`J = m`$, czyli $`P = C`$. Dla $`m = 1`$ wracamy do członów luki z §0.

### 10.2. Twierdzenie 4 — przejście dla konstelacji

Niech $`x`$ będzie członem napędzającym dla $`s`$ długości $`J`$, a $`\mathcal{C}(P)`$ podziałem $`P`$ na klasy modulo $`q`$. Spośród $`q`$ podniesień $`x`$ do modułu $`qN`$:

- $`q - |\mathcal{C}(P)|`$ podniesień jest członami dla $`s`$ długości $`J`$;
- dla każdej klasy $`K`$ z $`K \cap C = \emptyset`$ dokładnie jedno podniesienie jest członem dla $`s`$ długości $`J - |K|`$;
- podniesienia zabijające klasę $`K`$ z $`K \cap C \neq \emptyset`$ nie są członami dla $`s`$.

Każdy człon dla $`s`$ w $`\mathcal{G}(qN)`$ powstaje w ten sposób dokładnie raz.

*Dowód.* Identyczny jak dowód Twierdzenia 1 (Lematy 1–3), z warunkiem „punkty $`C`$ przeżywają" w miejsce „końce przeżywają". $`\square`$

*Uwaga.* Gdy żadne dwa punkty $`P`$ nie są przystające modulo $`q`$, wszystkie klasy są jednoelementowe i dostajemy $`n_{s,J}(qN) = (q - J - 1)\, n_{s,J}(N) + (J + 1 - m)\, n_{s,J+1}(N)`$ — Twierdzenie 2.1 Holta i Rudda (2014), dowiedzione tam przy założeniu $`|s| < 2q`$.

### 10.3. Twierdzenie 5 — prawo narodzin konstelacji

```math
n_{s,m}(qN) = \big(q - \nu_q(C)\big)\, n_{s,m}(N) + B_s(N),
```

gdzie $`\nu_q(C)`$ to liczba klas reszt zajętych przez $`C`$, a $`B_s(N)`$ to liczba członów napędzających dla $`s`$, których **punkty dodatkowe tworzą jedną klasę modulo $`q`$, rozłączną z klasami punktów $`C`$**. Zatem $`s`$ występuje w $`\mathcal{G}(qN)`$, a nie występuje w $`\mathcal{G}(N)`$, wtedy i tylko wtedy, gdy $`n_{s,m}(N) = 0`$ i $`B_s(N) > 0`$. O *pierwszym* pojawieniu się w ciągu etapów mówi dopiero Wniosek 5.1, oparty na Lemacie 6.

*Dowód.* Twierdzenie 4 dla docelowej długości $`m`$: z członów długości $`m`$ (czyli $`P = C`$) przeżywa $`q - \nu_q(C)`$ nietkniętych kopii; człon dłuższy daje wystąpienie $`s`$ dokładnie wtedy, gdy jego klasa zabita jest równa całemu $`E`$ i nie zawiera punktów $`C`$. $`\square`$

**Lemat 6 (trwałość).** Jeśli $`\nu_q(C) < q`$, to $`n_{s,m}(qN) \ge n_{s,m}(N)`$ — raz obecna konstelacja nie znika. Jeśli $`\nu_q(C) = q`$, to $`s`$ nie występuje w $`\mathcal{G}(qN)`$ ani w $`\mathcal{G}(M)`$ dla żadnego modułu $`M`$ podzielnego przez $`q`$.

*Dowód.* Z Twierdzenia 5: $`n_{s,m}(qN) \ge (q - \nu_q(C))\, n_{s,m}(N) \ge n_{s,m}(N)`$. Gdy $`\nu_q(C) = q`$, dla każdego $`x`$ któryś punkt $`x + c`$, $`c \in C`$, jest podzielny przez $`q`$, a więc nie należy do $`\Omega(M)`$ dla żadnego $`M`$ z $`q \mid M`$. $`\square`$

**Wniosek 5.1 (pierwsze pojawienie się).** Niech $`N_0 \mid N_1 \mid N_2 \mid \dots`$ będzie ciągiem etapów, w którym $`2 \mid N_0`$ i $`N_{i+1} = q_i N_i`$ dla nieparzystych liczb pierwszych $`q_i \nmid N_i`$. Konstelacja $`s`$ pojawia się w tym ciągu po raz pierwszy na etapie $`N_{i+1}`$ wtedy i tylko wtedy, gdy $`n_{s,m}(N_i) = 0`$ i $`B^{(q_i)}_s(N_i) > 0`$.

*Dowód.* „$`\Rightarrow`$": z Twierdzenia 5, bo $`s`$ występuje w $`\mathcal{G}(N_{i+1})`$, a nie w $`\mathcal{G}(N_i)`$. „$`\Leftarrow`$": $`s`$ występuje w $`\mathcal{G}(N_{i+1})`$, więc jest dopuszczalna modulo każdej liczby pierwszej dzielącej $`N_{i+1}`$. Gdyby występowała na wcześniejszym etapie $`N_r`$, $`r < i`$, to z Lematu 6 zastosowanego kolejno do $`q_r, \dots, q_{i-1}`$ występowałaby też w $`\mathcal{G}(N_i)`$, wbrew $`n_{s,m}(N_i) = 0`$. $`\square`$

**Drogi narodzin:** *zwykła* — jeden punkt dodatkowy; *wielopunktowa* — kilka punktów dodatkowych w jednej klasie, czyli odległych o wielokrotności $`2q`$. Druga wymaga $`|s| \ge 2q`$.

**Przykład.** Konstelacja $`(4, 12, 2, 12)`$, $`|s| = 30 > 22 = 2 \cdot 11`$, ma w $`\mathcal{G}(11\#)`$ dokładnie jedno wystąpienie. W $`\mathcal{G}(7\#)`$ jej jedyny człon napędzający ma punkty dodatkowe w odległościach 6 i 28 od początku — dokładnie 22 od siebie. Liczba 11 zabija oba w jednej kopii; innej drogi narodzin nie ma, a model liniowy tego zdarzenia nie obejmuje.

### 10.4. Twierdzenie 6 — łańcuch na kształtach i warunek wystarczający ścisłości łańcucha Holta

Niech $`m_P(N)`$ będzie liczbą $`x`$ z $`P(x) = P`$ (populacja kształtu). Z Twierdzenia 4:

```math
m_{P'}(qN) = \sum_P m_P(N)\, T_q(P, P'), \qquad
T_q(P, P) = q - |\mathcal{C}(P)|, \quad T_q(P, P \setminus K) = 1 \text{ dla } K \cap C = \emptyset,
```

a pozostałe przejścia są zerowe. Proces na kształtach jest więc **dokładnym układem liniowym dla każdej rozpiętości**, a współczynniki zależą tylko od kształtu i od $`q`$.

Łańcuch Holta śledzi tylko długość $`J = |P| - 1`$, czyli jest zlepieniem kształtów tej samej długości. **Jeśli żaden zasiedlony kształt nie ma dwóch punktów przystających modulo $`q`$, to $`T_q`$ zależy wyłącznie od $`J`$** — $`T(J \to J) = q - J - 1`$, $`T(J \to J-1) = J - m`$ — i rekurencja Holta jest dokładna. W szczególności zachodzi to zawsze, gdy $`|s| < 2q`$.

*Dowód.* Przy klasach jednoelementowych $`|\mathcal{C}(P)| = J + 1`$, a klas rozłącznych z $`C`$ jest $`|E| = J - m`$, każda o jednym punkcie. $`\square`$

*Uwaga (zakres twierdzenia).* Twierdzenie 6 podaje warunek **wystarczający**, nie konieczny. Kierunek odwrotny nie wynika z dowodu: poprawki pochodzące od różnych kształtów mają różne znaki i w zasadzie mogą się znieść. Obserwacja, że we wszystkich sprawdzonych przypadkach z punktami przystającymi rekurencja Holta była niedokładna (44 z 44), tego nie zmienia.

### 10.5. Twierdzenie 7 — momenty dla konstelacji

Dla $`k \ge 0`$ niech $`S_k(s, N) = \sum_J \binom{J - m}{k}\, n_{s,J}(N)`$ — liczba par (człon, $`k`$-elementowy podzbiór jego punktów dodatkowych). Wtedy

```math
S_k(s, N) = \sum_{\substack{T \subseteq \{1, \dots, |s|-1\} \setminus C\\ |T| = k}} W_N(C \cup T),
\qquad
S_k(s, qN) = (q - m - 1 - k)\, S_k(s, N) + \Pi_k(s, N),
```

```math
\Pi_k(s, N) = \sum_{|T| = k} \big( m + 1 + k - \nu_q(C \cup T) \big)\, W_N(C \cup T) \;\ge\; 0,
```

a wystąpienia samej konstelacji to $`n_{s,m}(N) = \sum_k (-1)^k S_k(s, N)`$.

*Dowód.* Jak dla Twierdzenia 2 (Lematy 4 i 5), z $`C`$ w miejsce $`\{0, g\}`$. $`\square`$

Dla $`k = 0`$: $`S_0(s, qN) = (q - \nu_q(C))\, S_0(s, N)`$, czyli liczba wszystkich dopuszczalnych wystąpień $`s`$ łącznie z członami napędzającymi jest iloczynem $`\prod (q - \nu_q(s))`$. **Ten przypadek jest u Holta**: dla luk to Wniosek 5.3 Holta i Rudda (2015), dla konstelacji — praca Holta z 2025 roku (arXiv 2502.20470, §5). **Nowe są momenty $`k \ge 1`$** oraz źródło $`\Pi_k`$.

### 10.6. Modele dokładne dla luk do 104

Dla $`g \le 104`$ każde przejście od $`47\#`$ w górę jest w reżimie liniowym, bo już przy $`q = 53`$ mamy $`2q = 106 > 104`$. Zatem nasza macierz $`n_{g,j}(47\#)`$ (wszystkie długości) jako warunki początkowe daje przez rekurencję Holta **dokładne populacje wszystkich luk do 104 na wszystkich dalszych etapach sita** — o 22 wartości dalej niż opublikowane modele dokładne Holta ($`g \le 82`$).

Obserwacja: luki 84–104 zbliżają się do swoich granic Hardy'ego-Littlewooda niezwykle wolno — przy $`p \approx 10^5`$ osiągają dopiero od 0,4% do 1,2% docelowej względnej populacji.

### 10.7. Weryfikacja sekcji 10

| Co | Jak | Wynik |
|---|---|---|
| Tw. 4 | siłowe wypisanie cykli; 40 konstelacji na każde przejście 7#→11, 11#→13, 13#→17 oraz sito bez 7 → 7; rozpiętości 2q–5q | 160 konstelacji, 425 komórek, 0 błędów; tysiące zlań wielopunktowych |
| Tw. 5 | wszystkie konstelacje (do 3–4 luk, rozpiętość ≤ 4q) rodzące się przy danym q, te same przejścia | 783 narodziny, 0 błędów; wyłącznie drogą wielopunktową: 5 (przy 11), 13 (przy 13), 1 (przy 17), 46 (sito bez 7) |
| Tw. 6 | rekurencja Holta dla konstelacji, 180 konstelacji | poniżej 2q: 128/128 dokładnych; ≥ 2q bez punktów przystających: 8/8; ≥ 2q z punktami przystającymi: 0/44 |
| Tw. 7 | momenty k = 0…3, 180 konstelacji (k = 0 jest u Holta) | 720/720 zgodnych |
| §10.6 | populacje w G(53#) z nG47 vs niezależny profil N₁₆ | 52/52 zgodnych |
| §10.6 | pierwszy współczynnik $`\ell_1`$ modelu Holta (jego równ. 1.2) z warunków w G(47#) vs stała Hardy'ego-Littlewooda (jego równ. 1.3), luki 84–104 | 11/11 równych dokładnie, jako ułamki |
| Tw. 4 | rys. 6 Holta: $`s = 2,10,2,10,2`$, przejścia 5→7, 7→11, 11→13 (poza jego modelem) | wszystkie trzy odtworzone dokładnie: (1,0,2), (6,4,8), (52,44,48) |
