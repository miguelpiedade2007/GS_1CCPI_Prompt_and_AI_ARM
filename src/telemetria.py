"""
FIAP - Ciência da Computação - Global Solution 2026.1
Trilha 2: EnviroSat (Amazonia_Enviro_1)
Módulo de Simulação de Telemetria Orbital
"""

import random
from datetime import datetime


class TelemetriaSatélite:
    def __init__(self):
        # Estado inicial estável dos parâmetros dentro do range normal
        self.estado_atual = {
            "temperatura_sensor_termo": 25.0,  # °C (Normal: 18-45)
            "bateria_disponivel": 90.0,  # %  (Normal: 40-100)
            "buffer_imagens": 15.0,  # %  (Normal: 0-60)
            "erro_geolocalizacao": 8.0,  # metros (Normal: 0-15)
            "funcional_optico_nir": 95.0  # %  (Normal: 85-100)
        }

    def coletar(self, modo_cenario: str = "normal") -> dict:
        """
        Simula a leitura dos sensores do Amazonia_Enviro_1 baseado no cenário desejado.
        Retorna um dicionário com os dados tipados e timestamp oficial.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if modo_cenario == "normal":
            self.estado_atual["temperatura_sensor_termo"] = round(random.uniform(20.0, 40.0), 2)
            self.estado_atual["bateria_disponivel"] = round(
                max(40.0, self.estado_atual["bateria_disponivel"] - random.uniform(0.1, 0.5)), 2)
            self.estado_atual["buffer_imagens"] = round(random.uniform(10.0, 50.0), 2)
            self.estado_atual["erro_geolocalizacao"] = round(random.uniform(4.0, 12.0), 1)
            self.estado_atual["funcional_optico_nir"] = round(random.uniform(90.0, 99.0), 1)

        elif modo_cenario == "critico_incendio":
            # Simula anomalia de superaquecimento do sensor térmico por uso excessivo
            self.estado_atual["temperatura_sensor_termo"] = round(random.uniform(61.0, 75.0), 2)
            self.estado_atual["bateria_disponivel"] = round(random.uniform(25.0, 35.0), 2)
            self.estado_atual["buffer_imagens"] = round(random.uniform(70.0, 84.0), 2)


        # Garante limites físicos dos sensores matematicamente
        self.estado_atual["bateria_disponivel"] = max(0.0, min(100.0, self.estado_atual["bateria_disponivel"]))
        self.estado_atual["buffer_imagens"] = max(0.0, min(100.0, self.estado_atual["buffer_imagens"]))

        return {
            "timestamp": timestamp,
            "telemetria": self.estado_atual.copy()
        }