@echo off
pip install dicergirl
del dist /F /Q
python setup.py sdist bdist_wheel
twine upload dist/*
del dist /F /Q
pip uninstall dicergirl -y