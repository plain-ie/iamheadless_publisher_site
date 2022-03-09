from distutils.core import setup


setup(
    name="iamheadless_publisher_site",
    description="#",
    long_description=open("README.txt").read(),
    url="#",
    license="LICENSE",
    author="Maris Erts",
    author_email="maris@plain.ie",
    version="0.0.1",
    include_package_data=True,
    packages=["iamheadless_publisher_site"],
    install_requires=[
        "Django==4.0.3",
    ],
)
