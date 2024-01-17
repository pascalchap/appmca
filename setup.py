from distutils.core import setup

setup(
	name='appmca',
	version='0.1',
	description='application dedicated to MCA to manage the employee list, invoice and salary preparation',
	author='Pascal Chapier',
	autor_email='pascalchap@gmail.com',
	packages=['gui','functions',],
	install_requires=[
		'pandas',
		'numpy',
		'tkinter',
		'collections',
	],
	license='MIT',
	long_description=open('README.md').read(),
)
