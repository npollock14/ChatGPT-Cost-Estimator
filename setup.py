from setuptools import setup, find_packages

# Read requirements from requirements.txt
with open("requirements.txt", encoding="utf-16") as f:
    requirements = f.read().splitlines()

setup(
    name="chatgpt-cost-estimator",
    version="0.1.3",
    packages=find_packages(),
    description="A cost estimation tool for your ChatGPT Plus conversation history.",
    url="https://github.com/npollock14/ChatGPT-Cost-Estimator",
    author="Nathan Pollock",
    author_email="ndpollock@wpi.edu",
    license="MIT",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "chatgpt-cost-estimator=chatgpt_cost_estimator.main:main",
        ],
    },
    python_requires=">=3.11",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
