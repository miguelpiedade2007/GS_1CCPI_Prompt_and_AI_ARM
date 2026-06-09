import os
import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from ollama import Client
from dotenv import load_dotenv

# Importação dos módulos lógicos locais
from src.telemetria import TelemetriaSatélite
from src.alertas import AnalisadorAlertas

# Carrega as variáveis de ambiente antes de qualquer inicialização
load_dotenv()
console = Console()


class MissionControl:
    def __init__(self):
        # Configuração da lógica de hardware/alertas
        self.satelite = TelemetriaSatélite()
        self.analisador = AnalisadorAlertas()

        # Lógica de autenticação validada
        self.api_key = os.getenv("OLLAMA_API_KEY")
        self.client = Client(
            host="https://ollama.com",
            headers={
                "Authorization": f"Bearer {self.api_key}"
            }
        )
        self.model_name = "gpt-oss:120b"
        self.prompt_path = os.path.join('prompts', 'system_prompt.md')

        # Variável de estado: guarda os alertas da última leitura para validação do mitigador
        self.alertas_ativos = None

    def _carregar_system_prompt(self):
        """Busca as diretrizes da ARIA no diretório docs."""
        if os.path.exists(self.prompt_path):
            with open(self.prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        return "Você é a ARIA, inteligência artificial do satélite Amazonia_Enviro_1."

    def consultar_aria(self, contexto):
        """Envia os dados para o modelo 120b na nuvem."""
        system_instructions = self._carregar_system_prompt()

        response = self.client.chat(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": contexto}
            ],
            options={"temperature": 0.3}
        )
        return response['message']['content'].strip()

    def mostrar_tabela(self, pacote):
        """Renderiza a telemetria usando a biblioteca Rich."""
        table = Table(title="TELEMETRIA EM TEMPO REAL", title_style="bold cyan")
        table.add_column("SENSOR", style="white")
        table.add_column("VALOR", style="green")

        for sensor, valor in pacote['telemetria'].items():
            table.add_row(sensor.replace('_', ' ').upper(), str(valor))

        console.print(table)

    def executar_ciclo(self, cenario="normal"):
        """Executa o fluxo: Captura -> Análise -> IA."""
        pacote = self.satelite.coletar(modo_cenario=cenario)
        analise = self.analisador.avaliar(pacote)

        # Controle de Estado: Atualiza a memória baseada na severidade atual
        if analise['severidade'] == "RED" or analise['alertas']:
            self.alertas_ativos = analise['alertas']
        else:
            # Limpa a memória se o sistema estiver operando normalmente
            self.alertas_ativos = None

        self.mostrar_tabela(pacote)

        contexto_ia = (
            f"Dados: {pacote['telemetria']}\n"
            f"Alertas: {analise['alertas']}\n"
            f"Risco: {analise['severidade']}"
        )

        with console.status("[bold yellow]Processando via Ollama Cloud...", spinner="dots"):
            diagnostico = self.consultar_aria(contexto_ia)

            # Define cor do painel conforme severidade técnica
            cor_borda = "red" if analise['severidade'] == "RED" else "green"
            console.print(Panel(diagnostico, title="DIAGNÓSTICO ARIA", border_style=cor_borda))

    def executar_mitigacao(self):
        """Funcionalidade 3: Gera plano de ação com base na memória de estado crítico."""
        # Trava de Segurança: impede a execução se não houver alerta na memória
        # A verificação (is None ou strings que indiquem vazio, dependendo do retorno do seu Analisador)
        if not self.alertas_ativos or self.alertas_ativos == "Nenhum":
            console.print(
                "[yellow]Aviso: Operação abortada. Não há alertas críticos na memória do sistema. Execute 'status' ou 'incendio' para reavaliar a telemetria antes de solicitar mitigação.[/yellow]")
            return

        contexto_ia = (
            f"Alertas ativos detectados na memória de hardware: {self.alertas_ativos}\n"
            "Instrução: Com base nesses alertas críticos, gere um plano de mitigação emergencial. "
            "Forneça os procedimentos sequenciais de baixo nível que o operador terrestre deve usar para conter as anomalias."
        )

        with console.status("[bold red]Compilando plano de mitigação de emergência via Ollama...", spinner="dots"):
            plano = self.consultar_aria(contexto_ia)
            console.print(Panel(plano, title="PLANO DE MITIGAÇÃO ARIA (AÇÃO REQUERIDA)", border_style="red"))

    def menu(self):
        """Interface Principal (TUI)."""
        os.system('cls' if os.name == 'nt' else 'clear')
        banner = pyfiglet.figlet_format("MISSION CONTROL", font="slant")
        console.print(f"[bold cyan]{banner}[/bold cyan]")
        console.print("[dim]Sistema Amazonia_Enviro_1 v2.0 | Status: Online[/dim]\n")

        console.print(
            "[yellow]Opções disponíveis:[/yellow] [green]status[/green] | [green]incendio[/green] | [green]mitigar[/green] | [green]sair[/green]")

        while True:
            try:
                console.print("\n(aria) > ", end="")
                cmd = input().strip().lower()

                if cmd in ['sair', 'exit']:
                    console.print("[bold yellow]Encerrando sistemas orbitais...[/bold yellow]")
                    break
                elif cmd == 'status':
                    self.executar_ciclo("normal")
                elif cmd == 'incendio':
                    self.executar_ciclo("critico_incendio")
                elif cmd == 'mitigar':
                    self.executar_mitigacao()
                elif cmd == 'ajuda':
                    console.print("[yellow]Comandos aceitos: status, incendio, mitigar, sair[/yellow]")
                else:
                    console.print("[red]Comando inválido. Digite 'ajuda'.[/red]")
            except KeyboardInterrupt:
                break


if __name__ == "__main__":
    app = MissionControl()
    app.menu()