from setuptools import setup

dependencies = [
    'GitPython==3.1.7',
    'Pygments==2.6.1',
    'click==7.1.2',
    'flake8==3.8.3',
    'termcolor==1.1.0',
]

setup(
    name='git-praise',
    version='1.4.0',
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
            'praise = praise.main:praise_command',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ]
)
