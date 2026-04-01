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
    print(f"      {CYAN}ADVANCED REWARDS BOT | SOBERANO v4.4 | JESUS COMMAND{RESET}")
    print(f"      {GREEN}Bypass: Stealth Ativo | Saldo: Monitorado{RESET}")
    print("═"*70)

async def interactive_menu():
    engine = RewardsEngine({})
    automation = SearchAutomation(engine)
    stats = StatsAutomation(engine)

    while True:
        clear_screen()
        print_banner()
        print("\033[94m[1]\033[0m Farm Completo (Silencioso)")
        print("\033[94m[2]\033[0m Apenas Desktop (Visível)")
        print("\033[94m[3]\033[0m Apenas Mobile (Silencioso)")
        print("\033[94m[4]\033[0m Consultar Saldo e Gráfico")
        print("\033[93m[5] Login Manual / Validar Conta\033[0m")
        print("\033[91m[0]\033[0m Sair")
        print("\n" + "═"*70)
        
        choice = input("\033[95mJESUS, selecione a operação: \033[0m")

        try:
            if choice == "1":
                # Farm Desktop visível para segurança, Mobile oculto
                await engine.initialize(headless=False)
                await automation.run_desktop_searches(35)
                await engine.shutdown() # Reinicia para trocar UA
                await engine.initialize(headless=True)
                await automation.run_mobile_searches(25)
                await stats.get_current_points()
                stats.generate_graph()
                input("\n\033[92m[OK] Farm Total Concluído. ENTER...\033[0m")
            
            elif choice == "2":
                await engine.initialize(headless=False)
                await automation.run_desktop_searches(35)
                input("\nDesktop Concluído. ENTER...")
            
            elif choice == "3":
                await engine.initialize(headless=True)
                await automation.run_mobile_searches(25)
                input("\nMobile Concluído. ENTER...")

            elif choice == "4":
                await engine.initialize(headless=True)
                pts = await stats.get_current_points()
                stats.generate_graph()
                input("\nSaldo Sincronizado. ENTER...")
            
            elif choice == "5":
                await engine.initialize(headless=False)
                print("\n\033[93m[!] Logue e feche o navegador.\033[0m")
                input("\n\033[92mENTER aqui após fechar para salvar sessão.\033[0m")
            
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
