import pytest

@pytest.mark.bulk
def test_bulk():
	"""
	should not be tested because -m 'not bulk'' as in pytest.ini
	if you want to test this, use -m 'not bulk' option
	"""
	obs = True
	pred = True
	assert pred == obs

def test_nobulk():
	obs = True
	pred = True
	assert pred == obs

@pytest.mark.skip
def test_skip():
	obs = True
	pred = True
	assert pred == obs
