from setuptools import find_packages, setup

install_requires = ["django>=4", "wagtail>=6"]

test_require = [
    "black",
    "factory_boy",
    "flake8",
    "isort",
    "pytest",
    "pytest-django",
]

docs_require = []

setup(
    name="wagtail-seo-report",
    version="0.1.0",
    description="",
    author="R.Moorman <rob@moori.nl>",
    install_requires=install_requires,
    extras_require={"test": test_require},
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
    ],
)
