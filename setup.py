import setuptools



with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name="tags",
    version="0.1.0",
    author="Ken Hisanaga",
    author_email="Xenn.1i82@gmail.com",
    description="Commands used by the TA for grading",
    long_description=long_description,
    url="https://github.com/Qip21n0/TAGS",
	install_requires=[
		'click',
		'tqdm',
		'pandas',
        'selenium',
        'chromedriver-binary',
        'webdriber_manager',
        'pyautogui',
	], 
    packages=setuptools.find_packages(),
    entry_points = {
        'console_scripts': ['tags = tags.main:main']
    },
    python_requires='>=3.8',
)