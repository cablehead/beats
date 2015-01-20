import pytest

import beats.store


def test_store(tmpdir):
    store = beats.store.Store(tmpdir.strpath)

    with store.db('foo') as foo:
        pytest.raises(KeyError, lambda: foo['bar'])
        assert foo.get('bar') is None
        assert foo.get('bar', 'default') == 'default'
        assert ('bar' in foo) is False

    with store.db('foo', write=True) as foo:
        foo['bar'] = 30
        foo['none'] = None

    with store.db('foo') as foo:
        assert foo.get('bar') == 30
        assert foo.get('none') is None
        assert ('bar' in foo) is True
