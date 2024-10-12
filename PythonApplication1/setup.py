
"""
Author: _svennnn

Project: Computer Laboratory Inventory System

Description:
The Computer Laboratory Inventory System is a comprehensive software solution designed and implemented by _svennnn. This system is meticulously crafted to manage and organize the inventory of a computer laboratory efficiently. With version 1.2.0, this project brings a range of features and functionalities to streamline the inventory management process.

Key Features:
- Intuitive User Interface: The system boasts a user-friendly interface, making it easy for administrators to navigate and utilize its features seamlessly.
- Version Control: The project is labeled as version 1.2.0, signifying continuous improvements and updates to meet evolving requirements.
- Executable Integration: The setup script includes an executable file, "PythonApplication1.py," ensuring convenient deployment and execution of the inventory system.
"""

from cx_Freeze import setup, Executable

setup(
    name="Computer Laboratory Inventory System",
    version="1.2.0",
    description="A comprehensive software solution for managing and organizing the inventory of computer laboratories.",
    executables=[Executable("PythonApplication1.py")],
)