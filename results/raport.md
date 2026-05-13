# Raport — Egzamin Ósmoklasisty z Matematyki, 12 maja 2026

Benchmark sześciu konfiguracji modeli ~4-8B parametrów uruchamianych lokalnie przez MLX na Apple Silicon.

## Wyniki

| Model                                      | Wynik       | Procent   | Zamknięte   | Otwarte   |
|--------------------------------------------|-------------|-----------|-------------|-----------|
| Bielik-Minitron 7B v3 (8-bit, text-only)   | **25 / 30** | **83.3%** | 11/14       | 14/16 pkt |
| Gemma 4 E4B IT (4-bit, text-only)          | **24 / 30** | **80.0%** | 10/14       | 14/16 pkt |
| Bielik 4.5B v3 (8-bit, text-only)          | **23 / 30** | **76.7%** | 12/14       | 11/16 pkt |
| Gemma 4 E4B IT (4-bit, multimodal)         | **23 / 30** | **76.7%** | 11/14       | 12/16 pkt |
| Gemma 3 4B IT (4-bit, text-only)           | **18 / 30** | **60.0%** | 9/14        | 9/16 pkt  |
| Gemma 3 4B IT (4-bit, multimodal)          | **14 / 30** | **46.7%** | 8/14        | 6/16 pkt  |
| Llama-PLLuM 8B Instruct (8-bit, text-only) | **3 / 30**  | **10.0%** | 1/14        | 2/16 pkt  |

(Próg zdawalności egzaminu nie jest formalnie ustanowiony — wynik to liczba zdobytych punktów na 30 możliwych.)

## Tabela szczegółowa

Format komórek: `odpowiedź (zdobyte_pkt)`. Dla zadań otwartych pole odpowiedzi może być puste, jeśli model nie użył wymaganego tagu `<odpowiedz>`; w tych przypadkach Claude i tak oceniał pełne rozwiązanie z `raw`.

| zad   | typ   |   max | klucz               | BielikMin          | Gemma4T            | Bielik4.5   | Gemma4MM           | Gemma3T            | Gemma3MM           | PLLuM              |
|-------|-------|-------|---------------------|--------------------|--------------------|-------------|--------------------|--------------------|--------------------|--------------------|
| z01   | zamk  |     1 | A                   | A (1)              | A (1)              | A (1)       | A (1)              | A (1)              | A (1)              | B (0)              |
| z02   | zamk  |     1 | B                   | B (1)              | B (1)              | B (1)       | B (1)              | D (0)              | A (0)              | — (0)              |
| z03   | zamk  |     1 | C                   | C (1)              | C (1)              | C (1)       | C (1)              | C (1)              | C (1)              | A (0)              |
| z04   | zamk  |     1 | A                   | A (1)              | A (1)              | A (1)       | A (1)              | A (1)              | A (1)              | C (0)              |
| z05   | zamk  |     1 | D                   | D (1)              | D (1)              | D (1)       | D (1)              | C (0)              | C (0)              | — (0)              |
| z06   | zamk  |     1 | AC                  | BD (0)             | A (0)              | BD (0)      | A (0)              | D (0)              | BD (0)             | B (0)              |
| z07   | zamk  |     1 | B                   | B (1)              | B (1)              | B (1)       | B (1)              | B (1)              | B (1)              | B (1)              |
| z08   | zamk  |     1 | BD                  | BD (1)             | AC (0)             | BD (1)      | AC (0)             | BD (1)             | BD (1)             | A (0)              |
| z09   | zamk  |     1 | D                   | D (1)              | D (1)              | D (1)       | D (1)              | D (1)              | C (0)              | B (0)              |
| z10   | zamk  |     1 | PP                  | P (0)              | P (0)              | PP (1)      | P (0)              | P1 (0)             | P1 (0)             | — (0)              |
| z11   | zamk  |     1 | C                   | C (1)              | C (1)              | C (1)       | C (1)              | C (1)              | C (1)              | — (0)              |
| z12   | zamk  |     1 | PP                  | P1P2 (0)           | PF (0)             | PP (1)      | PP (1)             | P1 (0)             | PF (0)             | — (0)              |
| z13   | zamk  |     1 | D                   | D (1)              | D (1)              | B (0)       | D (1)              | D (1)              | D (1)              | C (0)              |
| z14   | zamk  |     1 | A                   | A (1)              | A (1)              | A (1)       | A (1)              | A (1)              | A (1)              | — (0)              |
| z15   | otw   |     2 | Ela przygotowała 5… | Ela przygotowa (2) | Ela przygotowa (2) | — (2)       | Ela przygotowa (2) | Ela przygotowa (2) | Ela przygotowa (1) | Ela przygotowa (0) |
| z16   | otw   |     3 | Przejazd z Jodłowa… | Przejazd samoc (3) | Prędkość samoc (3) | — (3)       | Prędkość samoc (3) | — (2)              | — (3)              | Przejazd z Jod (1) |
| z17   | otw   |     3 | Liczba dzieci na t… | Liczba dzieci, (3) | Liczba dzieci, (3) | — (1)       | — (3)              | Procent liczby (1) | Liczba procent (0) | 61,8% (0)          |
| z18   | otw   |     2 | Objętość ostrosłup… | Objętość ostro (2) | — (2)              | — (2)       | — (1)              | Objętość ostro (0) | Objętość ostro (0) | Ostrosłup ACDS (0) |
| z19   | otw   |     3 | Pani Anna zapłaci … | Pani Anna musi (3) | Pani Anna musi (3) | — (3)       | Pani Anna musi (3) | Pani Anna musi (3) | Pani Anna musi (2) | — (1)              |
| z20   | otw   |     3 | Obwód równoległobo… | Obwód równoleg (1) | — (1)              | — (0)       | Obwód równoleg (0) | Obwód równoleg (1) | — (0)              | Obwód równoleg (0) |

## Wydajność

| Model                                      | Łączny czas   | Średni / zadanie   | Throughput   |
|--------------------------------------------|---------------|--------------------|--------------|
| Bielik-Minitron 7B v3 (8-bit, text-only)   | 190 s         | 9.5 s              | 59 tok/s     |
| Gemma 4 E4B IT (4-bit, text-only)          | 151 s         | 7.6 s              | 121 tok/s    |
| Bielik 4.5B v3 (8-bit, text-only)          | 113 s         | 5.7 s              | 81 tok/s     |
| Gemma 4 E4B IT (4-bit, multimodal)         | 159 s         | 8.0 s              | 120 tok/s    |
| Gemma 3 4B IT (4-bit, text-only)           | 65 s          | 3.3 s              | 157 tok/s    |
| Gemma 3 4B IT (4-bit, multimodal)          | 68 s          | 3.4 s              | 151 tok/s    |
| Llama-PLLuM 8B Instruct (8-bit, text-only) | 39 s          | 2.0 s              | 36 tok/s     |

## Metodyka

- **Arkusz**: oficjalny PDF CKE z 12 maja 2026, 20 zadań (1–14 zamknięte ABCD/PF, 15–20 otwarte), max 30 pkt.
- **Klucz odpowiedzi**: wygenerowany przez Claude Opus 4.7 z PDF jako kontekst, następnie **ręcznie zweryfikowany** (Claude pomylił się w 5 zadaniach, głównie copy-paste między rozumowaniem a polem `odpowiedz`).
- **Runtime**: `mlx-lm` / `mlx-vlm` na Apple Silicon.
- **Wszystkie text-only**: identyczny pipeline — system prompt PL, treść zadania + tekstowy opis rysunku (jeśli dotyczy) + opcje, temperatura 0, max 1500 tokenów.
- **Gemma 3 multimodal**: ten sam model co Gemma 3 text-only, ale z przekazaniem obrazka PNG.
- **Ocena zadań otwartych**: Claude Opus 4.7 wg kryteriów CKE (pełna metoda + wynik, błąd rachunkowy, brak postępu).
- **Parser odpowiedzi**: preferuje `<odpowiedz>` → `\boxed{}` → ostatnie „Odpowiedź: X" → fallback regex.

## Uruchamiane modele

- **Bielik 4.5B v3 Instruct** (SpeakLeash): polski LLM ogólnego zastosowania, 8-bit MLX.
- **Bielik-Minitron 7B v3 Instruct** (SpeakLeash, NVIDIA-derived): polski model na bazie Llama-3.1-Nemotron pruningowany techniką Minitron, 8-bit MLX po konwersji.
- **Llama-PLLuM 8B Instruct** (CYFRAGOVPL): polski instruction-tuning na Llama 3.1 8B, 8-bit MLX po konwersji.
- **Gemma 3 4B IT** (Google): 4-bit MLX, w dwóch wariantach — multimodalnym (`mlx-vlm`, z obrazkami) i text-only (`mlx-lm`, z opisami).
- **Gemma 4 E4B IT** (Google): nowsza edycja edge, 4-bit MLX, uruchomiona text-only przez `mlx-vlm` bez przekazywania obrazków.
