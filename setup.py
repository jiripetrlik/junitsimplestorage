from setuptools import setup, find_packages
setup(
    name="JunitSimpleStorage",
    version="0.1",
    packages=find_packages(),
    author="Jiri Petrlik",
    author_email="jiripetrlik@gmail.com",
    install_requires=[
        "connexion>=2.4.0",
        "Flask>=1.1.1",
        "Flask-SQLAlchemy>=2.4.1",
        "junitparser>=1.4.0",
        "PyYAML>=5.1.2",
        "SQLAlchemy==1.3.10",
        "swagger-ui-bundle==0.0.6",
        "WTForms==2.2.1"
        ],
)
