"""
Faza 3d: Gemma 4 E4B IT (TEXT-ONLY przez mlx-vlm bez przekazywania obrazka).

Gemma 4 jest multimodalna (Gemma4ForConditionalGeneration), więc używamy mlx-vlm,
ale przekazujemy tylko tekst — dla fair compare z Bielikiem/PLLuM-em.
Wynik: results/gemma4_text_odpowiedzi.json
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path

from mlx_vlm import apply_chat_template, generate, load
from mlx_vlm.utils import load_config

ROOT = Path(__file__).resolve().parents[1]
MODEL_ID = "mlx-community/gemma-4-e4b-it-4bit"

ZADANIA = ROOT / "data" / "zadania.json"
SYS_ZAMK = (ROOT / "prompts" / "system_zamkniete.txt").read_text(encoding="utf-8")
SYS_OTW = (ROOT / "prompts" / "system_otwarte.txt").read_text(encoding="utf-8")
OUT = ROOT / "results" / "gemma4_text_odpowiedzi.json"


def format_opcje(opcje: dict[str, str]) -> str:
    if not opcje:
        return ""
    return "\n".join(f"  {k}. {v}" for k, v in opcje.items())


def build_user_prompt(zadanie: dict) -> str:
    parts = [zadanie["tresc"]]
    if zadanie.get("opis_obrazka"):
        parts.append(f"\nOpis rysunku do zadania:\n{zadanie['opis_obrazka']}")
    if zadanie["typ"] == "zamkniete" and zadanie.get("opcje"):
        parts.append("\nOpcje odpowiedzi:")
        parts.append(format_opcje(zadanie["opcje"]))
    return "\n".join(parts)


def extract_odpowiedz(text: str) -> str:
    m = re.search(r"<odpowiedz>\s*(.*?)\s*</odpowiedz>", text, re.S | re.I)
    return m.group(1).strip() if m else ""


def main() -> None:
    print(f"Ładuję {MODEL_ID} (mlx-vlm, tekst bez obrazków)...")
    model, processor = load(MODEL_ID)
    config = load_config(MODEL_ID)
    print("Model załadowany")

    zadania = json.loads(ZADANIA.read_text(encoding="utf-8"))
    wyniki = []

    for z in zadania:
        sys_prompt = SYS_ZAMK if z["typ"] == "zamkniete" else SYS_OTW
        user_prompt = build_user_prompt(z)

        messages = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        formatted = apply_chat_template(processor, config, messages, num_images=0)

        t0 = time.perf_counter()
        result = generate(
            model,
            processor,
            formatted,
            image=None,
            max_tokens=1500,
            temperature=0.0,
            verbose=False,
        )
        dt = time.perf_counter() - t0

        text = result.text if hasattr(result, "text") else str(result)
        odp = extract_odpowiedz(text)
        toks = getattr(result, "generation_tokens", None)
        tps = (toks / dt) if (toks and dt > 0) else None

        print(f"  z{z['id']:02d}: {dt:5.1f}s, {toks or '?'} tok, odp={odp[:40]!r}")

        wyniki.append({
            "id": z["id"],
            "typ": z["typ"],
            "punkty_max": z["punkty_max"],
            "ma_obrazek": bool(z.get("obrazek")),
            "czas_s": round(dt, 2),
            "tokens": toks,
            "tokens_per_s": round(tps, 1) if tps else None,
            "raw": text,
            "odpowiedz": odp,
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(wyniki, ensure_ascii=False, indent=2), encoding="utf-8")
    suma_t = sum(w["czas_s"] for w in wyniki)
    print(f"\nOK: {OUT}, łączny czas {suma_t:.0f}s ({suma_t/60:.1f} min)")


if __name__ == "__main__":
    main()
