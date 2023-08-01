"""Setup module."""

from setuptools import find_packages, setup


def get_long_description() -> str:
    """Return readme with changelog."""
    with open('README.md', encoding='utf8') as readme:
        with open('CHANGELOG.md', encoding='utf8') as changelog:
            return '{readme}\n\n{changelog}'.format(readme=readme.read(), changelog=changelog.read())


setup(
    name='drf-api-key',
    version='2.3.0',
    description='API key permissions for the Django REST Framework',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    url='https://jitdev.github.io/drf-api-key/',
    project_urls={
        'Documentation': 'https://jitdev.github.io/drf-api-key/'
    },
    author='Roland Kainrath',
    author_email='justintimedev@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    python_requires='>=3.7',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Environment :: Web Environment',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.2',
    ],
)
