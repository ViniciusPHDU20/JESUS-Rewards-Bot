import asyncio
import sys
import os
from src.core.engine import RewardsEngine
from src.automation.searches import SearchAutomation
from src.automation.stats import StatsAutomation
from src.utils.logger import logger

def clear_screen():
    os.system('clear')

def print_banner():
    print("\033[95m")
    print(" █████╗ ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗ ██████╗███████╗██████╗ ")
    print("██╔══██╗██╔══██╗██║   ██║██╔══██╗████╗  ██║██╔════╝██╔════╝██╔══██╗")
    print("███████║██║  ██║██║   ██║███████║██╔██╗ ██║██║     █████╗  ██║  ██║")
    print("██╔══██║██║  ██║╚██╗ ██╔╝██╔══██║██║╚██╗██║██║     ██╔══╝  ██║  ██║")
    print("██║  ██║██████╔╝ ╚████╔╝ ██║  ██║██║ ╚████║╚██████╗███████╗██████╔╝")
    print("╚═╝  ╚═╝╚═════╝   ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ")
    print("      ADVANCED REWARDS BOT | SOBERANO v3.2 | JESUS COMMAND")
    print("\033[0m")

async def interactive_menu():
    engine = RewardsEngine({})
    automation = SearchAutomation(engine)
    stats = StatsAutomation(engine)

    while True:
        clear_screen()
        print_banner()
        print("\033[94m[1]\033[0m Iniciar Farm Completo (Logado)")
        print("\033[94m[2]\033[0m Consultar Saldo e Gráfico")
        print("\033[93m[3] PRIMEIRO PASSO: Login Manual / Validar Conta\033[0m")
        print("\033[91m[0]\033[0m Sair")
        print("\n" + "═"*65)
        
        choice = input("\033[95mSelecione a operação soberana: \033[0m")

        try:
            if choice == "1":
                logger.info("Iniciando ciclo de farm automatizado...")
                await engine.initialize(headless=False)
                await automation.run_desktop_searches(35)
                await automation.run_mobile_searches(25)
                await stats.get_current_points()
                stats.generate_graph()
                input("\n\033[92m[OK] Farm concluído com sucesso. ENTER para voltar...\033[0m")
            
            elif choice == "2":
                await engine.initialize(headless=True)
                pts = await stats.get_current_points()
                stats.generate_graph()
                print(f"\n\033[92mSaldo Atual: {pts} pts\033[0m")
                input("\nENTER para voltar...")
            
            elif choice == "3":
                logger.info("Abrindo navegador para validação única de conta...")
                await engine.initialize(headless=False)
                print("\n\033[93m[!] Realize o login no Bing e marque 'Mantenha-me conectado'.\033[0m")
                print("\033[93m[!] Quando estiver logado e vendo seus pontos, feche o navegador.\033[0m")
                input("\n\033[92mPressione ENTER aqui APÓS fechar o navegador para validar a sessão.\033[0m")
            
            elif choice == "0":
                break
        
        except Exception as e:
            logger.error(f"Erro na operação: {e}")
            input("\nPressione ENTER para tentar novamente...")
        
        finally:
            if engine.playwright:
                await engine.shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(interactive_menu())
    except KeyboardInterrupt:
        sys.exit(0)
