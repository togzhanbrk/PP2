import re
import json
from pathlib import Path

RAW_PATH = Path("raw.txt")


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    return text


def parse_date_time(text: str) -> dict:
    patterns = [
        r"\b(?P<date>\d{2}/\d{2}/\d{4})\s+(?P<time>\d{2}:\d{2}(?::\d{2})?)\b",
        r"\b(?P<date>\d{4}-\d{2}-\d{2})\s+(?P<time>\d{2}:\d{2}(?::\d{2})?)\b",
        r"\b(?P<date>\d{2}\.\d{2}\.\d{4})\s+(?P<time>\d{2}:\d{2}(?::\d{2})?)\b",
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            return {"date": m.group("date"), "time": m.group("time")}
    return {"date": None, "time": None}


def parse_payment_method(text: str) -> str | None:
    method_patterns = [
        r"\b(Apple Pay|Google Pay)\b",
        r"\b(VISA|MASTERCARD|AMEX|MIR)\b",
        r"\b(CARD|CREDIT|DEBIT)\b",
        r"\b(CASH)\b",
        r"\b(KASPI|HALYK|JUSAN)\b",
        r"\b(QR)\b",
    ]
    for p in method_patterns:
        m = re.search(p, text, flags=re.IGNORECASE)
        if m:
            return m.group(1)
    return None


def parse_prices(text: str) -> list[float]:
    money_re = re.compile(
        r"""
        (?<!\w)
        (?P<amount>
            (?:\d{1,3}(?:[ ,]\d{3})+|\d+)
            (?:[.,]\d{2})?
        )
        \s*
        (?P<cur>₸|KZT|тг|тенге|₽|RUB|\$|USD|EUR|€)?
        (?!\w)
        """,
        re.VERBOSE | re.IGNORECASE,
    )

    prices = []
    for m in money_re.finditer(text):
        raw = m.group("amount")
        cleaned = raw.replace(" ", "")
        if "," in cleaned and "." not in cleaned:
            if re.search(r",\d{2}$", cleaned):
                cleaned = cleaned.replace(",", ".")
            else:
                cleaned = cleaned.replace(",", "")
        else:
            cleaned = cleaned.replace(",", "")

        try:
            prices.append(float(cleaned))
        except ValueError:
            pass

    return prices


def find_total(text: str) -> float | None:
    total_patterns = [
        r"(?im)^\s*(TOTAL|TOTAL AMOUNT|ИТОГО|СУММА|ИТОГ)\s*[:\-]?\s*(\d[\d ,]*[.,]?\d{0,2})",
        r"(?im)\b(TOTAL|ИТОГО|ИТОГ)\b.*?(\d[\d ,]*[.,]?\d{0,2})",
    ]
    for p in total_patterns:
        m = re.search(p, text)
        if m:
            raw = m.group(2).strip().replace(" ", "")
            if "," in raw and "." not in raw and re.search(r",\d{2}$", raw):
                raw = raw.replace(",", ".")
            else:
                raw = raw.replace(",", "")
            try:
                return float(raw)
            except ValueError:
                pass
    return None


def parse_items(text: str) -> list[dict]:
    items = []
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]

    line_price_re = re.compile(
        r"(?P<name>.*?)(?P<price>\d[\d ,]*[.,]?\d{0,2})\s*(₸|KZT|тг|тенге|\$|USD|€|EUR|₽|RUB)?\s*$",
        re.IGNORECASE
    )

    ignore_re = re.compile(
        r"(?i)^(TOTAL|TOTAL AMOUNT|ИТОГО|ИТОГ|СУММА|CHANGE|СДАЧА|CASH|CARD|VISA|MASTERCARD|THANK|СПАСИБО|DATE|TIME)\b"
    )

    for ln in lines:
        if ignore_re.search(ln):
            continue
        m = line_price_re.search(ln)
        if not m:
            continue

        name = m.group("name").strip(" .:-")
        raw_price = m.group("price")

        if not re.search(r"[A-Za-zА-Яа-я]", name):
            continue

        cleaned = raw_price.replace(" ", "")
        if "," in cleaned and "." not in cleaned and re.search(r",\d{2}$", cleaned):
            cleaned = cleaned.replace(",", ".")
        else:
            cleaned = cleaned.replace(",", "")

        try:
            price_val = float(cleaned)
        except ValueError:
            continue

        items.append({"name": name, "price": price_val})

    return items


def main():
    if not RAW_PATH.exists():
        print("raw.txt not found. Put raw.txt рядом с receipt_parser.py")
        return

    text = RAW_PATH.read_text(encoding="utf-8", errors="ignore")
    text = normalize_text(text)

    dt = parse_date_time(text)
    payment = parse_payment_method(text)
    items = parse_items(text)
    prices = parse_prices(text)

    total = find_total(text)
    if total is None:
        total = round(sum(i["price"] for i in items), 2) if items else (round(sum(prices), 2) if prices else 0.0)

    result = {
        "date": dt["date"],
        "time": dt["time"],
        "payment_method": payment,
        "items": items,
        "all_prices_found": prices,
        "total": total,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()