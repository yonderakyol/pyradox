import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyradox",
    version="0.0.1",
    author="Ritvik Rastogi",
    author_email="rastogiritvik99@gmail.com",
    description="A Deep Learning framework built on top of Keras containing implementations of Artificial Neural Network Architectures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ritvik19",
    packages=setuptools.find_packages(exclude=['ProjectFiles', '.git', '.idea', '.gitattributes', '.gitignore']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)