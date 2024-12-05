from setuptools import setup, find_packages

setup(
    name="route_optimizer",  # The package name
    version="1.0",
    packages=find_packages(),  # Automatically find all packages in your project
    include_package_data=True,  # Include non-Python files specified in MANIFEST.in (if any)
    description="A GUI-based application for optimizing travel routes using evolutionary algorithms.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your_email@example.com",
    url="",  # You can add a repository URL here
    install_requires=[
        "ttkbootstrap",
        "matplotlib",
        "geopy",
        "numpy",
        "pandas",
        "setuptools"
    ],
    entry_points={
        'console_scripts': [
            'route_optimizer = gui_main:RouteOptimizerApp'  # Points to the main GUI application
        ],
    },
    python_requires='>=3.7'
)
