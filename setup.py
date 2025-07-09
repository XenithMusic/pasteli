from setuptools import setup, find_packages

with open("README.md","r") as f:
    long_description = f.read()

setup(
    name="pasteli",
    version="0.1.0",
    description="A cross-platform library for handling the clipboard through python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="cookiiq",
    author_email="xenith.contact.mail@gmail.com",
    url="https://github.com/XenithMusic/pasteli"
)