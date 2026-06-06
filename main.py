"""
Mission Control AI — Amazonia_Enviro_1
FIAP · Ciência da Computação · Global Solution 2026.1
Ponto de entrada do sistema.
"""

from src.engine import MissionControl

if __name__ == "__main__":
    app = MissionControl()
    app.menu()