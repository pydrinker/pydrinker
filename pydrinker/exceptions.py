class ProviderError(Exception):
    pass


class ProviderRuntimeError(ProviderError):
    pass


class ConfigurationError(Exception):
    pass


class DrinkerException(Exception):
    pass


class DeleteMessage(DrinkerException):
    pass
