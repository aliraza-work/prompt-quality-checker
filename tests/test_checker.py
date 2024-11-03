import unittest
from src.checker import check_prompt

class PromptCheckerTests(unittest.TestCase):
    def test_detects_missing_sections(self):
        issues = check_prompt("Just a short note")
        self.assertTrue(any(i.startswith("missing_section") for i in issues))

    def test_accepts_complete_prompt(self):
        text = "Task: Rank.\nConstraints: Be brief.\nOutput format: JSON object."
        self.assertEqual(check_prompt(text), [])

if __name__ == "__main__":
    unittest.main()
