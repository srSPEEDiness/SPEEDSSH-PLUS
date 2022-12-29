clean:
	@echo 'Cleaning up...'
	rm -rf build dist *.egg-info
	rm -rf *.spec
	rm -rf ./virtualenv

build:
	$(MAKE) clean

	@echo 'Building...'
	python setup.py sdist bdist_wheel