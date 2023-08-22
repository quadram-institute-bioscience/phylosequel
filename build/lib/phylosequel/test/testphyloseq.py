import pytest
import amplikraken.kraken

def test_confidence():
    z = '3:83 52:11 0:11 3:81 |:| 3:3 0:3 52:6 3:81'
    assert amplikraken.kraken.str_to_confidence(z) ==  0.75

def test_taxonomy_splitter():
    z = 'Bacteria (taxid 3)'
    assert amplikraken.kraken.taxonomy_splitter(z) == (3, 'Bacteria')

def test_taxonomy_splitter_spaces():
    z = 'More bacteria (taxid 10000000)'
    assert amplikraken.kraken.taxonomy_splitter(z) == (10000000, 'More bacteria')

def test_taxonomy_fails_badformat1():
    z = 'Bacteria (taxid 3'
    with pytest.raises(Exception):
        amplikraken.kraken.taxonomy_splitter(z)


def test_taxonomy_fails_isint():
    z = '3'
    with pytest.raises(Exception):
        amplikraken.kraken.taxonomy_splitter(z)
