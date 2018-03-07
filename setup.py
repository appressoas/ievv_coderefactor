from setuptools import setup, find_packages


setup(
    name='ievv-coderefactor',
    description='General purpose code refactor solution.',
    version='1.0.0',
    author='Appresso AS',
    author_email='post@appresso.no',
    url='https://github.com/appressoas/ievv_coderefactor',
    packages=find_packages(),
    install_requires=[
        'termcolor',
        'fire',
    ],
    include_package_data=True,
    zip_safe=False,
    license='MIT',
    entry_points={
        "console_scripts": ['ievv-coderefactor = ievv_coderefactor.cli:main']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Code Generators',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2'
    ],
    test_suite='tests'
)
