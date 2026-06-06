import os
import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from ollama import Client
from dotenv import load_dotenv

# Importação dos módulos lógicos locais
from telemetria import TelemetriaSatélite
from alertas import AnalisadorAlertas

# Carrega as variáveis de ambiente antes de qualquer inicialização
load_dotenv()
console = Console()


class MissionControl:
    def __init__(self):
        # Configuração da lógica de hardware/alertas
        self.satelite = TelemetriaSatélite()
        self.analisador = AnalisadorAlertas()

        # Lógica de autenticação validada no seu script de teste
        self.api_key = os.getenv("OLLAMA_API_KEY")
        self.client = Client(
            host="https://ollama.com",
            headers={
                "Authorization": f"Bearer {self.api_key}"
            }
        )
        self.model_name = "gpt-oss:120b"
        self.prompt_path = os.path.join('docs', 'system_prompt.md')

    def _carregar_system_prompt(self):
        """Busca as diretrizes da ARIA no diretório docs."""
        if os.path.exists(self.prompt_path):
            with open(self.prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        return "Você é a ARIA, inteligência artificial do satélite Amazonia_Enviro_1."

    def consultar_aria(self, contexto):
        """Envia os dados para o modelo 120b na nuvem."""
        system_instructions = self._carregar_system_prompt()

        # Chamada direta ao modelo conforme validado
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

    def menu(self):
        """Interface Principal (TUI)."""
        # Limpa o console e exibe o banner do PyFiglet
        os.system('cls' if os.name == 'nt' else 'clear')
        banner = pyfiglet.figlet_format("MISSION CONTROL", font="slant")
        console.print(f"[bold cyan]{banner}[/bold cyan]")
        console.print("[dim]Sistema Amazonia_Enviro_1 v2.0 | Status: Online[/dim]\n")

        while True:
            try:
                # Uso do input padrão para evitar erros de console screen buffer
                console.print("\n(aria) > ", end="")
                cmd = input().strip().lower()

                if cmd in ['sair', 'exit']:
                    console.print("[bold yellow]Encerrando sistemas orbitais...[/bold yellow]")
                    break
                elif cmd == 'status':
                    self.executar_ciclo("normal")
                elif cmd == 'incendio':
                    self.executar_ciclo("critico_incendio")
                elif cmd == 'ajuda':
                    console.print("[yellow]Comandos: status, incendio, sair[/yellow]")
                else:
                    console.print("[red]Comando inválido. Digite 'ajuda'.[/red]")
            except KeyboardInterrupt:
                break


if __name__ == "__main__":
    # Inicializa o controle de missão
    app = MissionControl()
    app.menu()