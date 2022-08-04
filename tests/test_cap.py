"""
..  codeauthor:: Charles Blais
"""
import pyravealert.cap as cap


def test_cap():
    capxml = cap.from_file('tests/examples/oasis-cap-example.xml')
    print(capxml)


def test_cap2():
    capxml = cap.from_file('tests/examples/oasis-cap-example2.xml')
    print(capxml)
