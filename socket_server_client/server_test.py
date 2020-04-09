from server import mock_db, pickle

def test_mock():
    obs = mock_db('1-1-A-T_HP:000001')
    pred = [3,10,1,10000]
    assert pred == obs

def test_byte():
    obs_q = pickle.dumps('1-1-A-T_HP:000001')
    obs = mock_db(pickle.loads(obs_q))
    pred = [3,10,1,10000]
    assert pred == obs
    obs_q = pickle.dumps('x')
    obs = mock_db(pickle.loads(obs_q))
    pred = False
    assert pred == obs