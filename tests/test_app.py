import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

#Временная папка для тестов для баланса вселенной (для дизбаланса основных данных в data)
os.environ["DATA_DIR"] = tempfile.mkdtemp(prefix="attendance-test-")

import app


class TestAppState(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        app.DATA_DIR = self.tmp_dir.name
        app.STATE_FILE = os.path.join(app.DATA_DIR, "state.json")

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_default_state(self):
        state = app.load_state()
        self.assertEqual(state, {"requests": 0, "present": 0})

    def test_save_and_load_state(self):
        state = {
            "requests": 5,
            "present": 2,
        }
        app.save_state(state)
        loaded = app.load_state()
        self.assertEqual(loaded, state)

    def test_utc_now_ends_with_z(self):
        now = app.utc_now()
        self.assertTrue(now.endswith("Z"))


if __name__ == "__main__":
    unittest.main()