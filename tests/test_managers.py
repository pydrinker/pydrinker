import pytest
from loafer.managers import LoaferManager

from pydrinker.dispatchers import DrinkerDispatcher
from pydrinker.exceptions import ConfigurationError
from pydrinker.managers import DrinkerManager
from pydrinker.routes import DrinkerRoute
from pydrinker.runners import DrinkerRunner


@pytest.fixture
def fake_route():
    from pydrinker.providers import AbstractProvider

    class FakeProvider(AbstractProvider):
        async def fetch_messages(self):
            pass

        async def confirm_message(self, message):
            pass

    def fake_handler():
        pass

    return DrinkerRoute(provider=FakeProvider(), handler=fake_handler)


def test_manager_instance():
    manager = DrinkerManager(routes=[])
    assert isinstance(manager, LoaferManager)
    assert isinstance(manager.runner, DrinkerRunner)
    assert isinstance(manager.routes, list)


def test_manager_with_custom_runner():
    class CustomRunner:
        pass

    manager = DrinkerManager(routes=[], runner=CustomRunner())
    assert isinstance(manager.runner, CustomRunner)


def test_manager_dispatcher_without_routes():
    manager = DrinkerManager(routes=[])
    with pytest.raises(ConfigurationError) as exc:
        manager.dispatcher

    assert "invalid routes to dispatch" in str(exc)


def test_manager_dispatcher_with_wrong_type_of_instance():
    class CustomRoute:
        pass

    manager = DrinkerManager(routes=[CustomRoute()])
    with pytest.raises(ConfigurationError) as exc:
        manager.dispatcher

    assert "invalid routes to dispatch" in str(exc)


def test_manager_dispatcher_instance(fake_route):
    manager = DrinkerManager(routes=[fake_route])
    dispatcher = manager.dispatcher
    assert isinstance(dispatcher, DrinkerDispatcher)
