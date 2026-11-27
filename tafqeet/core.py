"""Convert numbers to Arabic words (tafqeet) and Egyptian pound amounts to text."""
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

_ONES = ["", "واحد", "اثنان", "ثلاثة", "أربعة", "خمسة", "ستة", "سبعة", "ثمانية", "تسعة"]
_TEENS = {
    10: "عشرة", 11: "أحد عشر", 12: "اثنا عشر", 13: "ثلاثة عشر", 14: "أربعة عشر",
    15: "خمسة عشر", 16: "ستة عشر", 17: "سبعة عشر", 18: "ثمانية عشر", 19: "تسعة عشر",
}
_TENS = {
    20: "عشرون", 30: "ثلاثون", 40: "أربعون", 50: "خمسون",
    60: "ستون", 70: "سبعون", 80: "ثمانون", 90: "تسعون",
}
_HUNDREDS = {
    1: "مائة", 2: "مائتان", 3: "ثلاثمائة", 4: "أربعمائة", 5: "خمسمائة",
    6: "ستمائة", 7: "سبعمائة", 8: "ثمانمائة", 9: "تسعمائة",
}
# (singular, dual, plural for 3..10)
_SCALES = [
    ("", "", ""),
    ("ألف", "ألفان", "آلاف"),
    ("مليون", "مليونان", "ملايين"),
    ("مليار", "ملياران", "مليارات"),
    ("تريليون", "تريليونان", "تريليونات"),
]
MAX_NUMBER = 10 ** 15 - 1

_WESTERN = "0123456789"
_ARABIC_INDIC = "٠١٢٣٤٥٦٧٨٩"


def _below_100(n):
    if n < 10:
        return _ONES[n]
    if n < 20:
        return _TEENS[n]
    unit = n % 10
    tens = n - unit
    if unit:
        return _ONES[unit] + " و" + _TENS[tens]
    return _TENS[tens]


def _below_1000(n):
    hundreds, rest = divmod(n, 100)
    parts = []
    if hundreds:
        parts.append(_HUNDREDS[hundreds])
    if rest:
        parts.append(_below_100(rest))
    return " و".join(parts)


def number_to_words(n):
    """Return the Arabic words for a non-negative integer (masculine, nominative)."""
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("number_to_words expects an int")
    if n < 0:
        return "سالب " + number_to_words(-n)
    if n > MAX_NUMBER:
        raise ValueError("number too large (max %d)" % MAX_NUMBER)
    if n == 0:
        return "صفر"
    groups = []
    scale = 0
    while n:
        n, group = divmod(n, 1000)
        if group:
            singular, dual, plural = _SCALES[scale]
            if scale == 0:
                groups.append(_below_1000(group))
            elif group == 1:
                groups.append(singular)
            elif group == 2:
                groups.append(dual)
            elif group <= 10:
                groups.append(_below_100(group) + " " + plural)
            else:
                groups.append(_below_1000(group) + " " + singular)
        scale += 1
    return " و".join(reversed(groups))


def _counted(n, singular, dual, plural):
    """Number followed by a counted noun, with basic agreement rules."""
    if n == 1:
        return singular + " واحد"
    if n == 2:
        return dual
    words = number_to_words(n)
    return words + " " + (plural if 3 <= n % 100 <= 10 else singular)


def egp_to_words(amount, check_style=False):
    """Write an Egyptian pound amount in Arabic words.

    amount may be an int, str or Decimal (floats are accepted but converted
    through str). Piasters are rounded half up to two decimals.
    Example: 1250.50 -> "ألف ومائتان وخمسون جنيها وخمسون قرشا"
    """
    try:
        value = Decimal(str(amount).strip())
    except InvalidOperation:
        raise ValueError("not a number: %r" % (amount,))
    if not value.is_finite():
        raise ValueError("not a finite number: %r" % (amount,))
    value = value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    negative = value < 0
    value = abs(value)
    pounds = int(value)
    piasters = int((value - pounds) * 100)
    parts = []
    if pounds or not piasters:
        parts.append(_counted(pounds, "جنيه", "جنيهان", "جنيهات") if pounds else "صفر جنيه")
    if piasters:
        parts.append(_counted(piasters, "قرش", "قرشان", "قروش"))
    text = " و".join(parts)
    if negative and (pounds or piasters):
        text = "سالب " + text
    if check_style:
        text = "فقط " + text + " لا غير"
    return text


def to_arabic_indic(text):
    """Replace western digits 0-9 with Arabic-Indic digits."""
    return str(text).translate(str.maketrans(_WESTERN, _ARABIC_INDIC))


def to_western(text):
    """Replace Arabic-Indic digits with western digits 0-9."""
    return str(text).translate(str.maketrans(_ARABIC_INDIC, _WESTERN))
