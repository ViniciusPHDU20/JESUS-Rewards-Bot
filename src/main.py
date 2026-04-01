import asyncio
import sys
import os
from src.core.engine import RewardsEngine
from src.automation.searches import SearchAutomation
from src.automation.stats import StatsAutomation
from src.automation.daily import DailyAutomation
from src.utils.logger import logger

def clear_screen():
    os.system('clear')

def print_banner():
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    RESET = "\033[0m"
    print(f"{PURPLE}")
    print(" █████╗ ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗ ██████╗███████╗██████╗ ")
    print("██╔══██╗██╔══██╗██║   ██║██╔══██╗████╗  ██║██╔════╝██╔════╝██╔══██╗")
    print("███████║██║  ██║██║   ██║███████║██╔██╗ ██║██║     █████╗  ██║  ██║")
    print("██╔══██║██║  ██║╚██╗ ██╔╝██╔══██║██║╚██╗██║██║     ██╔══╝  ██║  ██║")
    print("██║  ██║██████╔╝ ╚████╔╝ ██║  ██║██║ ╚████║╚██████╗███████╗██████╔╝")
    print("╚═╝  ╚═╝╚═════╝   ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ")
    print(f"      {CYAN}ADVANCED REWARDS BOT | SOBERANO v5.1 | JESUS COMMAND{RESET}")
    print(f"      {GREEN}Bypass: HID Emulation | Mobile: True Headless | Stats: Active{RESET}")
    print("═"*70)

async def interactive_menu():
    engine = RewardsEngine({})
    automation = SearchAutomation(engine)
    stats = StatsAutomation(engine)
    daily = DailyAutomation(engine)

    while True:
        clear_screen()
        print_banner()
        print("\033[94m[1]\033[0m Iniciar Farm Completo (Auto-Sequencial)")
        print("\033[94m[2]\033[0m Consultar Saldo e Gráfico")
        print("\033[94m[3]\033[0m Apenas Desktop (Visível)")
        print("\033[94m[4]\033[0m Apenas Mobile (Silencioso)")
        print("\033[93m[5] Validar Conta / Login Manual\033[0m")
        print("\033[91m[0]\033[0m Sair")
        print("\n" + "═"*70)
        
        choice = input("\033[95mJESUS, selecione o comando: \033[0m")

        try:
            if choice == "1":
                logger.info("Iniciando Farm Sequencial de Elite...")
                # 1. Desktop + Daily (Visível para segurança e auditoria)
                await engine.initialize(headless=False, is_mobile=False)
                await daily.solve_daily_set()
                await automation.run_desktop_searches(35)
                # 2. Mobile (Headless Nativo)
                await automation.run_mobile_searches(25)
                # 3. Finalização
                pts = await stats.get_current_points()
                stats.generate_graph()
                input(f"\n\033[92m[OK] Operação Concluída: {pts} pts. ENTER para voltar...\033[0m")
            
            elif choice == "2":
                await engine.initialize(headless=True)
                pts = await stats.get_current_points()
                stats.generate_graph()
                print(f"\n\033[92mSaldo Sincronizado: {pts} pts\033[0m")
                input("\nENTER para voltar...")
            
            elif choice == "3":
                await engine.initialize(headless=False, is_mobile=False)
                await automation.run_desktop_searches(35)
                input("\nDesktop Finalizado. ENTER...")
            
            elif choice == "4":
                # Forçar inicialização headless para mobile direto do menu
                await engine.initialize(headless=True, is_mobile=True)
                await automation.run_mobile_searches(25)
                input("\nMobile Finalizado (Silencioso). ENTER...")

            elif choice == "5":
                await engine.initialize(headless=False)
                print("\n\033[93m[!] Logue e feche o navegador quando terminar.\033[0m")
                input("\n\033[92mENTER após fechar para salvar.\033[0m")
            
            elif choice == "0":
                break
        
        except Exception as e:
            logger.error(f"Erro na operação: {e}")
            input("\nPressione ENTER para restaurar...")
        
        finally:
            if engine:
                await engine.shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(interactive_menu())
    except KeyboardInterrupt:
        sys.exit(0)
