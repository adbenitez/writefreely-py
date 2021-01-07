
import setuptools


if __name__ == "__main__":
    with open('README.md') as file:
        long_desc = file.read()
    with open('src/writefreely/__init__.py') as file:
        for line in file.readlines():
            if line.startswith('__version__'):
                version = line.split('=')[1].strip().strip('\'"')
                break
    with open('requirements.txt') as file:
        install_requires = [
            line.replace('==', '>=') for line in file.read().split('\n')
            if line and not line.startswith(('#', '-'))]


    setuptools.setup(
        name='writefreely-py',
        version=version,
        description='An API client library for writefreely.org instances',
        long_description=long_desc,
        author='adbenitez',
        author_email='adbenitez@nauta.cu',
        url='https://github.com/adbenitez/writefreely-py',
        setup_requires=['setuptools_scm'],
        use_scm_version=True,
        package_dir={'': 'src'},
        packages=setuptools.find_packages('src'),
        license='MIT',
        classifiers=['Development Status :: 4 - Beta',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: MIT',
                     'Programming Language :: Python :: 3'],
        python_requires='>=3.5',
        install_requires=install_requires,
    )
