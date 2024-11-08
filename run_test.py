# run_tests.py

import pytest
import os

if not os.path.exists("reports"):
    os.makedirs("reports")

pytest.main()
