from setuptools import setup
setup(
    name="ddos-tool",
    version="2.0",
    py_modules=["ddos"],
    install_requires=["PySocks>=1.7.1","requests>=2.28.0"],
    entry_points={"console_scripts":["ddos=ddos:main"]},
    python_requires=">=3.8",
)
