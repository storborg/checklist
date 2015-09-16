from setuptools import setup, find_packages


setup(name='checklist',
      version='0.0.1.dev',
      description='Follow the checklist, dummy.',
      long_description=open('README.rst').read(),
      classifiers=[
          'Environment :: Console',
          'Development Status :: 1 - Planning',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Software Development :: Quality Assurance',
          'Topic :: Utilities',
      ],
      keywords='checklist cad code review',
      url='http://github.com/storborg/checklist',
      author='Scott Torborg',
      author_email='storborg@gmail.com',
      install_requires=[
          'six>=1.9.0',
      ],
      license='MIT',
      packages=find_packages(),
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False,
      entry_points="""\
      [console_scripts]
      checklist = checklist.cmd:main
      """)
