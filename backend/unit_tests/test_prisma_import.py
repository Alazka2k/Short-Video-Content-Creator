# backend/unit_tests/test_prisma_import.py

import os
import sys

print(f"Current working directory: {os.getcwd()}")
print(f"PYTHONPATH: {os.environ.get('PYTHONPATH', 'Not set')}")
print(f"sys.path: {sys.path}")

# Fügen Sie das Hauptverzeichnis des Projekts zum Python-Pfad hinzu
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from backend.src.prisma_client import init_prisma

print("Attempting to initialize Prisma...")
try:
    prisma = init_prisma()
    print("Prisma initialized successfully")
except Exception as e:
    print(f"Error initializing Prisma: {e}")

print("Script completed")

def test_prisma_import():
    prisma = init_prisma()
    assert prisma is not None