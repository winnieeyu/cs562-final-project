from generator import main as generator
from _generated import query as _generated

from sql import query as sql


def test_generator():
    # Generate the file
    generator()

    # Compare output
    assert _generated() == sql()
