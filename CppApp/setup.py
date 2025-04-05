from setuptools import setup, Extension
import pybind11

pybind11_include = pybind11.get_include()

ext_modules = [
    Extension(
        'Lab_1_Module',
        ['TaskModule.cpp', 'TestTask.cpp', 'FirstTask.cpp', 'SecondTask.cpp'],
        include_dirs=[pybind11_include],
        language='c++',
    ),
]

setup(
    name='Lab_1_Module',
    version='0.1',
    ext_modules=ext_modules,
    zip_safe=False,
)
