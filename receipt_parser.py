import re
from datetime import datetime

RAW_TEXT = open("raw.txt", encoding="utf-8").read()


def parse_price(s: str) -> float:
    return float(s.replace(" ", "").replace(",", "."))


def extract_store_info(text: str) -> dict:
    fields = {
        "store_name":        r"Филиал\s+(.+)",
        "bin":               r"БИН\s+(\d+)",
        "receipt_number":    r"Чек\s+№(\d+)",
        "sequential_number": r"Порядковый номер чека\s+№(\d+)",
        "cash_register":     r"Касса\s+([\w-]+)",
        "cashier":           r"Кассир\s+(.+)",
    }
    return {k: m.group(1).strip() for k, p in fields.items() if (m := re.search(p, text))}


def extract_datetime(text: str) -> dict:
    m = re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})", text)
    if not m:
        return {}
    dt = datetime.strptime(f"{m.group(1)} {m.group(2)}", "%d.%m.%Y %H:%M:%S")
    return {
        "raw_date":     m.group(1),
        "raw_time":     m.group(2),
        "raw_datetime": f"{m.group(1)} {m.group(2)}",
        "iso_datetime": dt.isoformat(),
        "formatted":    dt.strftime("%B %d, %Y at %H:%M:%S"),
    }


def extract_payment(text: str) -> dict:
    for method, label in [("Банковская карта", "Bank Card"), ("Наличные", "Cash")]:
        m = re.search(rf"{method}:\s*\n([\d\s]+,\d{{2}})", text)
        if m:
            return {"method": label, "method_ru": method, "amount": parse_price(m.group(1).strip())}
    return {}


def extract_totals(text: str) -> dict:
    totals = {}
    if m := re.search(r"ИТОГО:\s*\n([\d\s]+,\d{2})", text):
        totals["grand_total"] = parse_price(m.group(1).strip())
    if m := re.search(r"в т\.ч\. НДС 12%:\s*\n([\d\s]+,\d{2})", text):
        totals["vat_12_percent"] = parse_price(m.group(1).strip())
        totals["vat_rate"] = "12%"
    return totals


def extract_items(text: str) -> list:
    pattern = re.compile(
        r"^(\d+)\.\n"
        r"((?:(?!\d+,\d{3}\s+x\s).+\n)+?)"
        r"^(\d[\d ]*,\d{3})\s+x\s+([\d ]+,\d{2})\n"
        r"^([\d ]+,\d{2})\n"
        r"^Стоимость\n"
        r"^([\d ]+,\d{2})",
        re.MULTILINE,
    )
    items = []
    for m in pattern.finditer(text):
        name = re.sub(r"\s+", " ", m.group(2)).strip()
        is_rx = name.startswith("[RX]-")
        items.append({
            "number":          int(m.group(1)),
            "name":            name[5:] if is_rx else name,
            "is_prescription": is_rx,
            "quantity":        parse_price(m.group(3)),
            "unit_price":      parse_price(m.group(4)),
            "line_total":      parse_price(m.group(5)),
        })
    return items


def extract_fiscal_info(text: str) -> dict:
    fields = {
        "fiscal_sign": r"Фискальный признак:\s*\n(\d+)",
        "ink_ofd":     r"ИНК ОФД:\s*(\d+)",
        "rnm_code":    r"Код ККМ КГД \(РНМ\):\s*(\d+)",
        "znm":         r"ЗНМ:\s*(\S+)",
    }
    result = {k: m.group(1) for k, p in fields.items() if (m := re.search(p, text))}
    if m := re.search(r"г\.\s*(.+?)(?:\nОператор)", text, re.DOTALL):
        result["address"] = re.sub(r"\s+", " ", m.group(1)).strip()
    return result


def parse_receipt(text: str) -> dict:
    items = extract_items(text)
    return {
        "store_info": extract_store_info(text),
        "datetime":   extract_datetime(text),
        "items":      items,
        "item_count": len(items),
        "totals":     {**extract_totals(text), "calculated_from_items": round(sum(i["line_total"] for i in items), 2)},
        "payment":    extract_payment(text),
        "fiscal":     extract_fiscal_info(text),
    }


def print_summary(receipt: dict):
    sep = "=" * 60
    si, dt, t, p, f = receipt["store_info"], receipt["datetime"], receipt["totals"], receipt["payment"], receipt["fiscal"]
    print(sep)
    print("  PARSED RECEIPT SUMMARY")
    print(sep)
    print(f"\n Store  : {si.get('store_name')}")
    print(f"   BIN    : {si.get('bin')}")
    print(f"   Receipt: №{si.get('receipt_number')}  (seq №{si.get('sequential_number')})")
    print(f"   Cashier: {si.get('cashier')}")
    print(f"\n Date/Time: {dt.get('formatted')}")
    print(f"   ISO     : {dt.get('iso_datetime')}")
    print(f"\n Items ({receipt['item_count']} total):")
    print(f"  {'#':<3} {'Rx':<3} {'Product':<52} {'Qty':>5} {'Unit ₸':>10} {'Total ₸':>10}")
    print(f"  {'-'*3} {'-'*3} {'-'*52} {'-'*5} {'-'*10} {'-'*10}")
    for item in receipt["items"]:
        name = item["name"][:49] + "..." if len(item["name"]) > 52 else item["name"]
        print(f"  {item['number']:<3} {'RX' if item['is_prescription'] else '':<3} {name:<52} "
              f"{item['quantity']:>5.0f} {item['unit_price']:>10,.2f} {item['line_total']:>10,.2f}")
    print(f"\n Totals:")
    print(f"   Sum of line items : ₸ {t.get('calculated_from_items', 0):>10,.2f}")
    print(f"   Receipt ИТОГО     : ₸ {t.get('grand_total', 0):>10,.2f}")
    print(f"   VAT (12%)         : ₸ {t.get('vat_12_percent', 0):>10,.2f}")
    print(f"   Totals match      : {'OK' if t.get('calculated_from_items') == t.get('grand_total') else 'MISMATCH'}")
    print(f"\n Payment: {p.get('method')} — ₸ {p.get('amount', 0):,.2f}")
    print(f"\n Fiscal Info:")
    print(f"   Fiscal sign : {f.get('fiscal_sign')}")
    print(f"   RNM code    : {f.get('rnm_code')}")
    print(f"   ZNM         : {f.get('znm')}")
    print(f"   Address     : {f.get('address')}")
    print(f"\n{sep}")


def print_stats(receipt: dict):
    prices = [i["unit_price"] for i in receipt["items"]]
    rx = [i for i in receipt["items"] if i["is_prescription"]]
    print(f"\n Price Stats:")
    print(f"   Min unit price : ₸ {min(prices):,.2f}")
    print(f"   Max unit price : ₸ {max(prices):,.2f}")
    print(f"   Avg unit price : ₸ {sum(prices)/len(prices):,.2f}")
    print(f"   Prescription (RX) items: {len(rx)}")
    print(f"   OTC items              : {len(receipt['items']) - len(rx)}")


def main():
    receipt = parse_receipt(RAW_TEXT)
    print_summary(receipt)
    print_stats(receipt)


if __name__ == "__main__":
    main()
