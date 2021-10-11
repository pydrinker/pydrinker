import pytest
from loafer.message_translators import AbstractMessageTranslator as LoaferAbstractMessageTranslator
from loafer.providers import AbstractProvider as LoaferAbstractProvider
from loafer.routes import Route as LoaferRoute

from pydrinker.message_translators import AbstractMessageTranslator
from pydrinker.providers import AbstractProvider
from pydrinker.routes import DrinkerRoute


class FakeMessageTranslator(AbstractMessageTranslator):
    def translate(self, message):
        pass


class FakeProvider(AbstractProvider):
    async def fetch_messages(self):
        pass

    async def confirm_message(self, message):
        pass


def fake_handler():
    pass


def fake_error_handler():
    pass


def test_route_instance():
    route = DrinkerRoute(
        provider=FakeProvider(),
        message_translator=FakeMessageTranslator(),
        handler=fake_handler,
        error_handler=fake_error_handler,
    )
    assert isinstance(route, DrinkerRoute)
    assert isinstance(route, LoaferRoute)

    assert isinstance(route.provider, FakeProvider)
    assert isinstance(route.provider, AbstractProvider)
    assert isinstance(route.provider, LoaferAbstractProvider)

    assert isinstance(route.message_translator, FakeMessageTranslator)
    assert isinstance(route.message_translator, AbstractMessageTranslator)
    assert isinstance(route.message_translator, LoaferAbstractMessageTranslator)

    assert callable(route.handler) is True
    assert callable(route.error_handler) is True


def test_route_with_invalid_provider_instance():
    class FakeProvider:
        async def fetch_messages(self):
            pass

        async def confirm_message(self, message):
            pass

    with pytest.raises(TypeError) as exc:
        DrinkerRoute(
            provider=FakeProvider(),
            message_translator=FakeMessageTranslator(),
            handler=fake_handler,
            error_handler=fake_error_handler,
        )

    assert "invalid provider instance" in str(exc)


def test_route_with_invalid_message_translator_instance():
    class FakeMessageTranslator:
        def translate(self, message):
            pass

    with pytest.raises(TypeError) as exc:
        DrinkerRoute(
            provider=FakeProvider(),
            message_translator=FakeMessageTranslator(),
            handler=fake_handler,
            error_handler=fake_error_handler,
        )

    assert "invalid message translator instance" in str(exc)


def test_route_with_invalid_error_handler():
    with pytest.raises(TypeError) as exc:
        DrinkerRoute(
            provider=FakeProvider(),
            message_translator=FakeMessageTranslator(),
            handler=fake_handler,
            error_handler="error_handler",
        )

    assert "error_handler must be a callable object" in str(exc)


def test_route_with_invalid_handler():
    with pytest.raises(ValueError) as exc:
        DrinkerRoute(
            provider=FakeProvider(),
            message_translator=FakeMessageTranslator(),
            handler="handler",
            error_handler=fake_error_handler,
        )

    assert "handler must be a callable object or implement `handle` method" in str(exc)
