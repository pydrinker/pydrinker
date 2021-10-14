from loafer.routes import Route as LoaferRoute
from loafer.routes import logger

from .message_translators import AbstractMessageTranslator
from .providers import AbstractProvider

logger.name = __name__


class DrinkerRoute(LoaferRoute):
    def __init__(
        self,
        provider,
        handler,
        name="default",
        message_translator=None,
        error_handler=None,
    ):
        self.name = name

        if not isinstance(provider, AbstractProvider):
            raise TypeError(f"invalid provider instance: {provider!r}")

        self.provider = provider

        if message_translator:
            if not isinstance(message_translator, AbstractMessageTranslator):
                raise TypeError(f"invalid message translator instance: {message_translator!r}")

        self.message_translator = message_translator

        if error_handler:
            if not callable(error_handler):
                raise TypeError(f"error_handler must be a callable object: {error_handler!r}")

        self._error_handler = error_handler

        if callable(handler):
            self.handler = handler
            self._handler_instance = None
        else:
            self.handler = getattr(handler, "handle", None)
            self._handler_instance = handler

        if not self.handler:
            raise ValueError(
                f"handler must be a callable object or implement `handle` method: {self.handler!r}"
            )
