.PHONY: help
help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

config-repositories:
	@poetry config repositories.testpypi https://test.pypi.org/legacy/
	@poetry config repositories.pypi https://upload.pypi.org/legacy/

clean-build:
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg-info

clean-eggs:
	@find . -name '*.egg' -print0|xargs -0 rm -rf --
	@rm -rf .eggs/

clean: clean-eggs clean-build ## Clean all thrash files (cached, builds .. etc)
	@find . -iname '*.pyc' -delete
	@find . -iname '*.pyo' -delete
	@find . -iname '*~' -delete
	@find . -iname '*.swp' -delete
	@find . -iname '__pycache__' -delete
	@find . -iname '.pytest_cache' -exec rm -rf {} \+

build:
	@poetry build

test-release: clean build config-repositories ## Release package to Test PyPI
	@git tag `poetry version -s`
	@git push origin `poetry version -s`
	@poetry publish -r testpypi

