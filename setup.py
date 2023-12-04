from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in quantbit_foundry_erp/__init__.py
from quantbit_foundry_erp import __version__ as version

setup(
	name="quantbit_foundry_erp",
	version=version,
	description="Quantbit Foundry ERP system is a comprehensive enterprise resource planning solution designed to streamline and optimize manufacturing operations. It integrates key processes like production planning, inventory management, and quality control, empowering businesses with efficient resource utilization and data-driven decision-making.",
	author="Quantbit Technologies Pvt ltd",
	author_email="contact@erpdata.in",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
