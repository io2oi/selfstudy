import pytest
from translator import HGVStoGNOMAD

@pytest.fixture(scope="function")
def testobj():
    '''
    create SetUp and Teardown for testing
    '''
    res = HGVStoGNOMAD()
    yield res
    del res


def test_get_grch37(testobj):
    obs1 = (
        "NM_000314.6(PTEN):c.737C>T", "NC_000010.11:g.87957955C>T",
        "NC_000010.10:g.89717712C>T", "NC_000010.9:g.89707692C>T"
    )
    pred = ("NM_000314.6(PTEN):c.737C>T", "NC_000010.10:g.89717712C>T")
    assert pred == testobj.get_grch37(obs1)
    obs2 = (
        'NM_206933.3(USH2A):c.12295-?_14133+?del',
    )
    pred = ('NM_206933.3(USH2A):c.12295-?_14133+?del',)
    assert pred == testobj.get_grch37(obs2)


def test_get_ref_sequence(testobj):
    obs = (10, 89717712, 89717712)
    pred = "C"
    assert pred == testobj.get_ref_sequence(*(obs))

def test_translate_to_gnomadid_snp(testobj):
    ''' SNP case '''
    obs = "NC_000010.10:g.89717712C>T"
    pred = "10-89717712-C-T"
    assert pred == testobj.translate_to_gnomadid_snp(obs)


def test_translate_to_gnomadid_del(testobj):
    ''' DEL case '''
    obs = "NC_000016.9:g.68853330_68853335del"
    pred = "16-68853329-GTAAGGG-G"
    assert pred == testobj.translate_to_gnomadid_del(obs)


def test_translate_to_gnomadid_ins(testobj):
    ''' INS case
    96 97 98 99 00
     g  c  A  G  g
     ->
    96 97 98 99 00 01
     g  c  A  C  G  g
    '''
    obs = "NC_000012.11:g.103288598_103288599insC"
    pred = "12-103288599-G-CG"
    assert pred == testobj.translate_to_gnomadid_ins(obs)


def test_translate_to_gnomadid_dup(testobj):
    ''' DUP case
    nomenclature:
     https://varnomen.hgvs.org/recommendations/DNA/variant/duplication/
    74 75 76 77
     t  g  G  G
    ->
    74 75 76 77 78 79
     t  g  G  G  G  G
    '''
    obs = "NC_000012.11:g.103288676_103288677dup"
    pred = "12-103288677-G-GGG"
    assert pred == testobj.translate_to_gnomadid_dup(obs)


def test_translate_to_gnomadid_insdel(testobj):
    ''' delins case
    74 75 76 77 78 79
     g  C  C  C  c  g
    ->
    74 75 76 77
     g  T  c  g

    '''
    obs = "NC_000016.9:g.68772275_68772277delinsT"
    pred = "16-68772275-CCC-T"
    assert pred == testobj.translate_to_gnomadid_delins(obs)

def test_translate_to_gnomadid_wrapper(testobj):
    obs = "NC_000010.10:g.89717712C>T"
    pred = "10-89717712-C-T"
    assert pred == testobj.id_converter(obs)
    obs = "NC_000016.9:g.68853330_68853335del"
    pred = "16-68853329-GTAAGGG-G"
    assert pred == testobj.id_converter(obs)
    obs = "NC_000016.9:g.68772275_68772277delinsT"
    pred = "16-68772275-CCC-T"
    assert pred == testobj.id_converter(obs)
    obs = "NC_000012.11:g.103288676_103288677dup"
    pred = "12-103288677-G-GGG"
    assert pred == testobj.id_converter(obs)
    obs = "NC_000016.9:g.68772275_68772277delinsT"
    pred = "16-68772275-CCC-T"
    assert pred == testobj.id_converter(obs)
