import io

from setuptools import setup, find_packages

with io.open("README.md", 'rt', encoding='utf-8') as f:
    readme = f.read()
setup(
    name='redisbuffer',
    version='0.0.8',
    author='kamalyes',
    url="https://gitee.com/kamalyes/redisbuffer",
    author_email='mryu168@163.com',
    packages=find_packages(),
    install_requires=('redis>=3.0.1'),
    long_description=readme,
    long_description_content_type='text/markdown',
)
