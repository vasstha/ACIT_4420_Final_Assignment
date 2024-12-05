from setuptools import setup, find_packages

setup(
    name="RouteOptimizer",  # Name of your project
    version="1.0.0",  # Project version
    author="Vaskar Shrestha",  # Replace with your name
    author_email="vashr0444@oslomet.no",  # Replace with your email
    description="A Fundamental Python Program for Route Calculation",
    long_description=open("README.md").read(),  # Pulls in your README file as a long description
    long_description_content_type="text/markdown",  # Ensures proper formatting for Markdown README
    url="https://github.com/vasstha/ACIT_4420_Final_Assignment.git",  # Replace with your project's GitHub link
    packages=find_packages(),  # Automatically find Python packages in your project
    include_package_data=True,
    install_requires=[
        'matplotlib>=3.0.0',
        'geopy>=2.0.0',
        'numpy>=1.18.0',
    ],
    entry_points={
        'gui_scripts': [
            'route-optimizer=main:main',  # Entry point for your GUI application
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",  # Specify the minimum Python version required
)