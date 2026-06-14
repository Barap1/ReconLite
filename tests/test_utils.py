import unittest

from reconlite_utils import (
    build_scanner_command,
    is_private_or_local_scope,
    parse_ports,
    parse_positive_int,
    validate_scan_scope,
)


class ReconLiteUtilsTests(unittest.TestCase):
    def test_parse_ports_accepts_comma_separated_ports(self):
        self.assertEqual(parse_ports("80,443"), [80, 443])

    def test_parse_ports_rejects_empty_string(self):
        with self.assertRaises(ValueError):
            parse_ports("")

    def test_parse_ports_rejects_non_numeric_input(self):
        with self.assertRaises(ValueError):
            parse_ports("80,https")

    def test_parse_ports_rejects_out_of_range_ports(self):
        for value in ("0", "65536"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    parse_ports(value)

    def test_parse_positive_int_accepts_valid_value(self):
        self.assertEqual(parse_positive_int("10", "masscan_rate"), 10)

    def test_parse_positive_int_rejects_invalid_values(self):
        invalid_values = ["", "abc", "0", "-1"]
        for value in invalid_values:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    parse_positive_int(value, "timeout")

    def test_is_private_or_local_scope_accepts_private_and_loopback(self):
        accepted = [
            "127.0.0.1",
            "localhost",
            "10.0.0.0/8",
            "192.168.1.0/24",
        ]
        for scope in accepted:
            with self.subTest(scope=scope):
                self.assertTrue(is_private_or_local_scope(scope))

    def test_is_private_or_local_scope_rejects_public_scopes(self):
        rejected = [
            "8.8.8.8",
            "1.1.1.1/32",
        ]
        for scope in rejected:
            with self.subTest(scope=scope):
                self.assertFalse(is_private_or_local_scope(scope))

    def test_validate_scan_scope_rejects_public_scope_by_default(self):
        with self.assertRaises(ValueError):
            validate_scan_scope("8.8.8.8")

    def test_validate_scan_scope_allows_public_scope_when_enabled(self):
        self.assertEqual(
            validate_scan_scope("8.8.8.8", allow_public_scan=True),
            "8.8.8.8",
        )

    def test_build_scanner_command_returns_list_without_shell_syntax(self):
        command = build_scanner_command("scanner.py", 1000, 3, 50, [80, 443])
        self.assertIsInstance(command, list)
        self.assertEqual(command, ["python3", "scanner.py", "1000", "3", "50", "80,443"])
        joined = " ".join(command)
        for shell_token in (";", "&&", "|", "`"):
            self.assertNotIn(shell_token, joined)


if __name__ == "__main__":
    unittest.main()
