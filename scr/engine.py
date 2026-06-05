"""
FIAP - Ciência da Computação - Global Solution 2026.1
Trilha 2: EnviroSat (Amazonia_Enviro_1)
Script Principal de Orquestração da Missão
"""


import os
from telemetria import TelemetriaSatélite
from alertas import AnalisadorAlertas




# Simulação de interface com a IA (Substitua pela chamada da API do Ollama/OpenAI depois)
def chamar_aria_ai(system_prompt, contexto_missao):
   """
   Simula o processamento da IA ARIA.
   Na versão final, aqui você usará client.chat.completions.create
   """
   return f"[RESPOSTA DA ARIA BASEADA NO PROMPT E NOS DADOS DA MISSÃO]\n{contexto_missao}"




def executar_ciclo_missao(cenario="normal"):
   print(f"\n--- INICIANDO MONITORAMENTO: CENÁRIO {cenario.upper()} ---")


   # 1. Instanciar módulos
   satelite = TelemetriaSatélite()
   analisador = AnalisadorAlertas()


   # 2. Coletar dados brutos
   pacote = satelite.coletar(modo_cenario=cenario)
   print(f"[*] Telemetria recebida às {pacote['timestamp']}")


   # 3. Processamento de regras (Frente 4 - Julgamento Técnico)
   resultado_analise = analisador.avaliar(pacote)


   # 4. Carregar o System Prompt (Frente 3 - Engenharia de Prompt)
   try:
       with open("docs/system_prompt.md", "r", encoding="utf-8") as f:
           sys_prompt = f.read()
   except FileNotFoundError:
       sys_prompt = "Erro: Arquivo system_prompt.md não encontrado na pasta docs/."


   # 5. Montar o contexto dinâmico para a IA
   contexto_para_ai = f"""
   DADOS DE TELEMETRIA ATUAIS: {pacote['telemetria']}
   ALERTAS DETECTADOS: {resultado_analise['alertas']}
   AÇÕES AUTOMÁTICAS: {resultado_analise['acoes_defensivas']}
   SEVERIDADE DO SISTEMA: {resultado_analise['severidade']}
   """


   # 6. Chamar a IA
   print("[*] Enviando dados para ARIA analisar impacto ambiental...")
   diagnostico = chamar_aria_ai(sys_prompt, contexto_para_ai)


   print("\n--- DIAGNÓSTICO FINAL DA MISSÃO ---")
   print(diagnostico)




if __name__ == "__main__":
   # Testando os três cenários exigidos no seu simulador
   executar_ciclo_missao("normal")
   executar_ciclo_missao("critico_incendio")
