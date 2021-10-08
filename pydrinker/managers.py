from cached_property import cached_property
from loafer.managers import LoaferManager

from .dispatchers import DrinkerDispatcher
from .exceptions import ConfigurationError
from .routes import DrinkerRoute
from .runners import DrinkerRunner


class DrinkerManager(LoaferManager):
    def __init__(self, routes, runner=None, _concurrency_limit=None, _max_threads=None):
        self._concurrency_limit = _concurrency_limit
        if runner is None:
            self.runner = DrinkerRunner(on_stop_callback=self.on_loop__stop, max_workers=_max_threads)
        else:
            self.runner = runner

        self.routes = routes

    @cached_property
    def dispatcher(self):
        if not (self.routes and all(isinstance(r, DrinkerRoute) for r in self.routes)):
            raise ConfigurationError(f"invalid routes to dispatch, routes={self.routes}")

        return DrinkerDispatcher(self.routes, max_jobs=self._concurrency_limit)
