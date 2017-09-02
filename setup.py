from setuptools import find_packages, setup

dependencies = [
    'GitPython==2.1.5',
    'Pygments==2.2.0',
    'termcolor==1.1.0',
]

setup(
    name='git-praise',
    version='1.0.0',
    url='https://github.com/sigvef/git-praise',
    license='MIT',
    author='Sigve Sebastian Farstad',
    author_email='sigvefarstad@gmail.com',
    description='A nicer git blame.',
    packages=['praise'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'praise = praise.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ]
)