# tafqeet

Zero-dependency Python library and command line tool that writes numbers and Egyptian pound amounts in Arabic words (تفقيط), the way they appear on cheques, invoices and contracts.

```python
from tafqeet import number_to_words, egp_to_words, to_arabic_indic

number_to_words(1250)              # 'ألف ومائتان وخمسون'
egp_to_words("3.25")               # 'ثلاثة جنيهات وخمسة وعشرون قرش'
egp_to_words(1500, check_style=True)  # 'فقط ألف وخمسمائة جنيه لا غير'
to_arabic_indic("2026")            # '٢٠٢٦'
```

Command line:

```
python -m tafqeet 1250
python -m tafqeet 1250.50 --egp --check
python -m tafqeet ١٢٣٤
```

## Features

- Integers from 0 up to 999,999,999,999,999 (thousands to trillions), with dual and plural forms (ألفان، ثلاثة آلاف، مليونان، ملايين).
- Egyptian pounds (جنيه) and piasters (قرش), with number agreement for 1, 2, 3 to 10, and 11 or more.
- Amounts are handled with `Decimal` and rounded half up to two decimals, so there are no float surprises.
- Cheque style wrapper: `فقط ... لا غير`.
- Arabic-Indic and western digit conversion.
- Pure standard library, Python 3.8+.

## Scope and known simplifications

- Output is masculine and nominative, and written without diacritics.
- For 11 and above the counted noun is written in the singular without tanween (e.g. `أحد عشر جنيه`).
- Other currencies and feminine forms are not covered yet. Pull requests are welcome.

## Development

```
python -m unittest discover -s tests -v
```

## License

MIT
