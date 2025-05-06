import unittest
from scanner import scan_code

class ScannerTests(unittest.TestCase):
    def test_hardcoded_password(self):
        code = 'password = "1234"'
        results, _ = scan_code(code)
        self.assertTrue(any("hardcoded password" in r.lower() for r in results))

if __name__ == '__main__':
    unittest.main()
