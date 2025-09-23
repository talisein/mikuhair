from setuptools import setup, find_packages

setup(
    name='color_triangle_generator',
    version='0.1.0',
    description='A Python program to generate a color gradient triangle.',
#    long_description=open('README.md').read(),
#    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/color_triangle_generator',
    packages=find_packages(),
    install_requires=[
        'Pillow',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
