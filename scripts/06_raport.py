"""
Faza 5: raport.md z wynikami benchmarku.

MODELE: lista (klucz_w_json, etykieta_pełna, skrót, ścieżka_do_results).
Sortowanie w tabelach: malejąco po sumie punktów.
"""

from __future__ import annotations

import json
from pathlib import Path
from statistics import mean

from tabulate import tabulate

ROOT = Path(__file__).resolve().parents[1]
OCENA = ROOT / "results" / "ocena_szczegolowa.json"
RAPORT = ROOT / "results" / "raport.md"

MODELE = [
    ("bielik", "Bielik 4.5B v3 (8-bit, text-only)", "Bielik4.5", ROOT / "results" / "bielik_odpowiedzi.json"),
    ("bielik_minitron", "Bielik-Minitron 7B v3 (8-bit, text-only)", "BielikMin", ROOT / "results" / "bielik_minitron_odpowiedzi.json"),
    ("pllum", "Llama-PLLuM 8B Instruct (8-bit, text-only)", "PLLuM", ROOT / "results" / "pllum_odpowiedzi.json"),
    ("gemma_text", "Gemma 3 4B IT (4-bit, text-only)", "Gemma3T", ROOT / "results" / "gemma_text_odpowiedzi.json"),
    ("gemma4_text", "Gemma 4 E4B IT (4-bit, text-only)", "Gemma4T", ROOT / "results" / "gemma4_text_odpowiedzi.json"),
    ("gemma4_mm", "Gemma 4 E4B IT (4-bit, multimodal)", "Gemma4MM", ROOT / "results" / "gemma4_mm_odpowiedzi.json"),
    ("gemma", "Gemma 3 4B IT (4-bit, multimodal)", "Gemma3MM", ROOT / "results" / "gemma_odpowiedzi.json"),
]


def main() -> None:
    data = json.loads(OCENA.read_text(encoding="utf-8"))
    raw_per_model = {
        nazwa: {r["id"]: r for r in json.loads(p.read_text(encoding="utf-8"))}
        for nazwa, _, _, p in MODELE
    }

    # Sortuj malejąco po sumie punktów dla tabel
    sorted_models = sorted(MODELE, key=lambda m: -data[m[0]]["suma"])

    # ===== Tabela podsumowania =====
    podsum_rows = []
    for nazwa, etykieta, _, _ in sorted_models:
        s = data[nazwa]
        podsum_rows.append([
            etykieta,
            f"**{s['suma']} / 30**",
            f"**{s['procent']}%**",
            f"{s['zamk_correct']}/{s['zamk_total']}",
            f"{s['otw_pkt']}/{s['otw_max']} pkt",
        ])
    podsum = tabulate(
        podsum_rows,
        headers=["Model", "Wynik", "Procent", "Zamknięte", "Otwarte"],
        tablefmt="github",
    )

    # ===== Tabela szczegółowa =====
    rows = []
    for z in data["zadania"]:
        nid = z["id"]
        row = [
            f"z{nid:02d}",
            "zamk" if z["typ"] == "zamkniete" else "otw",
            f"{z['punkty_max']}",
            (z["klucz_odp"][:18] + ("…" if len(z["klucz_odp"]) > 18 else "")),
        ]
        for nazwa, _, _, _ in sorted_models:
            odp = (z[nazwa]["odp"] or "—")[:14]
            pkt = z[nazwa]["punkty"]
            row.append(f"{odp} ({pkt})")
        rows.append(row)

    headers = ["zad", "typ", "max", "klucz"] + [skrot for _, _, skrot, _ in sorted_models]
    tabela = tabulate(rows, headers=headers, tablefmt="github")

    # ===== Wydajność =====
    perf_rows = []
    for nazwa, etykieta, _, _ in sorted_models:
        times = [v["czas_s"] for v in raw_per_model[nazwa].values()]
        tps = [v["tokens_per_s"] for v in raw_per_model[nazwa].values() if v.get("tokens_per_s")]
        perf_rows.append([
            etykieta,
            f"{sum(times):.0f} s",
            f"{mean(times):.1f} s",
            f"{mean(tps):.0f} tok/s" if tps else "—",
        ])
    perf = tabulate(
        perf_rows,
        headers=["Model", "Łączny czas", "Średni / zadanie", "Throughput"],
        tablefmt="github",
    )

    # ===== Raport =====
    raport_md = f"""# Raport — Egzamin Ósmoklasisty z Matematyki, 12 maja 2026

Benchmark sześciu konfiguracji modeli ~4-8B parametrów uruchamianych lokalnie przez MLX na Apple Silicon.

## Wyniki

{podsum}

(Próg zdawalności egzaminu nie jest formalnie ustanowiony — wynik to liczba zdobytych punktów na 30 możliwych.)

## Tabela szczegółowa

Format komórek: `odpowiedź (zdobyte_pkt)`. Dla zadań otwartych pole odpowiedzi może być puste, jeśli model nie użył wymaganego tagu `<odpowiedz>`; w tych przypadkach Claude i tak oceniał pełne rozwiązanie z `raw`.

{tabela}

## Wydajność

{perf}

## Metodyka

- **Arkusz**: oficjalny PDF CKE z 12 maja 2026, 20 zadań (1–14 zamknięte ABCD/PF, 15–20 otwarte), max 30 pkt.
- **Klucz odpowiedzi**: wygenerowany przez Claude Opus 4.7 z PDF jako kontekst, następnie **ręcznie zweryfikowany** (Claude pomylił się w 5 zadaniach, głównie copy-paste między rozumowaniem a polem `odpowiedz`).
- **Runtime**: `mlx-lm` / `mlx-vlm` na Apple Silicon.
- **Wszystkie text-only**: identyczny pipeline — system prompt PL, treść zadania + tekstowy opis rysunku (jeśli dotyczy) + opcje, temperatura 0, max 1500 tokenów.
- **Gemma 3 multimodal**: ten sam model co Gemma 3 text-only, ale z przekazaniem obrazka PNG.
- **Ocena zadań otwartych**: Claude Opus 4.7 wg kryteriów CKE (pełna metoda + wynik, błąd rachunkowy, brak postępu).
- **Parser odpowiedzi**: preferuje `<odpowiedz>` → `\\boxed{{}}` → ostatnie „Odpowiedź: X" → fallback regex.

## Uruchamiane modele

- **Bielik 4.5B v3 Instruct** (SpeakLeash): polski LLM ogólnego zastosowania, 8-bit MLX.
- **Bielik-Minitron 7B v3 Instruct** (SpeakLeash, NVIDIA-derived): polski model na bazie Llama-3.1-Nemotron pruningowany techniką Minitron, 8-bit MLX po konwersji.
- **Llama-PLLuM 8B Instruct** (CYFRAGOVPL): polski instruction-tuning na Llama 3.1 8B, 8-bit MLX po konwersji.
- **Gemma 3 4B IT** (Google): 4-bit MLX, w dwóch wariantach — multimodalnym (`mlx-vlm`, z obrazkami) i text-only (`mlx-lm`, z opisami).
- **Gemma 4 E4B IT** (Google): nowsza edycja edge, 4-bit MLX, uruchomiona text-only przez `mlx-vlm` bez przekazywania obrazków.
"""
    RAPORT.parent.mkdir(parents=True, exist_ok=True)
    RAPORT.write_text(raport_md, encoding="utf-8")
    print(f"OK: {RAPORT}")


if __name__ == "__main__":
    main()
