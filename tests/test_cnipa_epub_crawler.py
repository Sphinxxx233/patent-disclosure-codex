# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from cnipa_epub_crawler import submit_index_search


class SubmitIndexSearchTests(unittest.TestCase):
    def test_uses_committed_navigation_and_result_title_instead_of_full_load(self) -> None:
        page = MagicMock()

        submit_index_search(page, "数据标注")

        page.expect_navigation.assert_called_once_with(timeout=120_000, wait_until="commit")
        page.wait_for_function.assert_called_once()
        title_condition = page.wait_for_function.call_args.args[0]
        self.assertIn("专利查询结果展示", title_condition)
        self.assertIn("无查询结果", title_condition)
        page.wait_for_load_state.assert_not_called()
        page.wait_for_timeout.assert_not_called()


if __name__ == "__main__":
    unittest.main()
