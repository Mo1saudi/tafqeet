import unittest

from tafqeet import egp_to_words, number_to_words, to_arabic_indic, to_western


class NumberTests(unittest.TestCase):
    def test_basic(self):
        cases = {
            0: "صفر",
            1: "واحد",
            11: "أحد عشر",
            12: "اثنا عشر",
            21: "واحد وعشرون",
            99: "تسعة وتسعون",
            100: "مائة",
            101: "مائة وواحد",
            200: "مائتان",
            300: "ثلاثمائة",
            999: "تسعمائة وتسعة وتسعون",
            1000: "ألف",
            2000: "ألفان",
            3000: "ثلاثة آلاف",
            11000: "أحد عشر ألف",
            1250: "ألف ومائتان وخمسون",
            1000000: "مليون",
            2500000: "مليونان وخمسمائة ألف",
            1000000000: "مليار",
        }
        for n, expected in cases.items():
            self.assertEqual(number_to_words(n), expected, n)

    def test_negative(self):
        self.assertEqual(number_to_words(-5), "سالب خمسة")

    def test_errors(self):
        with self.assertRaises(TypeError):
            number_to_words(1.5)
        with self.assertRaises(ValueError):
            number_to_words(10 ** 15)


class CurrencyTests(unittest.TestCase):
    def test_pounds(self):
        self.assertEqual(egp_to_words(1), "جنيه واحد")
        self.assertEqual(egp_to_words(2), "جنيهان")
        self.assertEqual(egp_to_words(5), "خمسة جنيهات")
        self.assertEqual(egp_to_words(11), "أحد عشر جنيه")
        self.assertEqual(egp_to_words(100), "مائة جنيه")

    def test_piasters(self):
        self.assertEqual(egp_to_words("0.5"), "خمسون قرش")
        self.assertEqual(egp_to_words("3.25"), "ثلاثة جنيهات وخمسة وعشرون قرش")
        self.assertEqual(egp_to_words("0"), "صفر جنيه")

    def test_rounding(self):
        self.assertEqual(egp_to_words("1.005"), egp_to_words("1.01"))

    def test_check_style(self):
        self.assertEqual(egp_to_words(5, check_style=True), "فقط خمسة جنيهات لا غير")


class DigitTests(unittest.TestCase):
    def test_roundtrip(self):
        self.assertEqual(to_arabic_indic("2026-11-27"), "٢٠٢٦-١١-٢٧")
        self.assertEqual(to_western("٢٠٢٦"), "2026")


if __name__ == "__main__":
    unittest.main()
