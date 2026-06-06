"""
FIAP - Ciência da Computação - Global Solution 2026.1
Trilha 2: EnviroSat (Amazonia_Enviro_1)
Subsistema de Triagem de Thresholds e Resposta Automatizada
"""

class AnalisadorAlertas:
    def __init__(self):
        # Limites operacionais estritos definidos no escopo do projeto
        self.thresholds = {
            "temp_max": 60.0,
            "temp_min": 5.0,
            "bateria_critica": 20.0,
            "buffer_max": 85.0,
            "erro_geo_max": 50.0,
            "nir_min": 70.0
        }

    def avaliar(self, pacote_telemetria: dict) -> dict:
        """
        Varre os dados brutos e gera flags de severidade.
        Aplica ações automáticas diretamente no barramento se houver violação de segurança.
        """
        dados = pacote_telemetria["telemetria"]
        alertas_disparados = []
        acoes_automaticas_hardware = []
        nivel_severidade = "GREEN"

        # 1. Avaliação de Temperatura do Sensor Térmico
        t_sensor = dados["temperatura_sensor_termo"]
        if t_sensor > self.thresholds["temp_max"] or t_sensor < self.thresholds["temp_min"]:
            alertas_disparados.append(f"VIOLAÇÃO TÉRMICA: Sensor operando a {t_sensor}°C.")
            nivel_severidade = "RED"

        # 2. Avaliação da Bateria + Resposta Automatizada (Modo de Segurança)
        bat = dados["bateria_disponivel"]
        if bat < self.thresholds["bateria_critica"]:
            alertas_disparados.append(f"SUBTENSÃO CRÍTICA: Bateria em {bat}%.")
            nivel_severidade = "RED"
            acoes_automaticas_hardware.append(
                "[AUTO-COMANDO] Ativando Modo de Sobrevivência (Safe Mode). "
                "Desligando payloads não essenciais e orientando painéis solares ao vetor solar."
            )

        # 3. Avaliação do Buffer de Imagens
        buf = dados["buffer_imagens"]
        if buf > self.thresholds["buffer_max"]:
            alertas_disparados.append(f"SURAQUECIMENTO DE DADOS: Buffer de armazenamento em {buf}% de capacidade.")
            if nivel_severidade != "RED":
                nivel_severidade = "YELLOW"

        # 4. Avaliação de Geolocalização
        geo = dados["erro_geolocalizacao"]
        if geo > self.thresholds["erro_geo_max"]:
            alertas_disparados.append(f"DESVIO DE EFEMÉRIDE: Erro de apontamento em {geo} metros.")
            if nivel_severidade != "RED":
                nivel_severidade = "YELLOW"

        # 5. Avaliação do Sensor Óptico NIR
        nir = dados["funcional_optico_nir"]
        if nir < self.thresholds["nir_min"]:
            alertas_disparados.append(f"DEGRADAÇÃO DE PAYLOAD: Eficiência do sensor NIR caiu para {nir}%.")
            nivel_severidade = "RED"

        return {
            "severidade": nivel_severidade,
            "alertas": alertas_disparados,
            "acoes_defensivas": acoes_automaticas_hardware
        }