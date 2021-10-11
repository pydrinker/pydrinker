from loafer.dispatchers import LoaferDispatcher

from pydrinker.dispatchers import DrinkerDispatcher


def test_dispatcher_instance():
    dispatcher = DrinkerDispatcher(routes=[])
    assert isinstance(dispatcher, LoaferDispatcher)
    assert isinstance(dispatcher.routes, list)
