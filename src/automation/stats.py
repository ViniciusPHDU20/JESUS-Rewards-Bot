import asyncio
import csv
import os
from datetime import datetime
from playwright.async_api import Page
from src.utils.logger import logger

class StatsAutomation:
    """Módulo de estatísticas com bypass de detecção e seletores resilientes."""
    
    def __init__(self, engine):
        self.engine = engine
        self.log_file = "/home/viniciusphdu/WORKSPACE_CORE/Advanced-Rewards-Bot/config/points_log.csv"

    async def get_current_points(self) -> int:
        """Extrai o saldo usando múltiplos métodos de captura."""
        logger.info("Iniciando consulta de saldo soberano...")
        
        if not self.engine.page:
            await self.engine.initialize(headless=True)
            
        page: Page = self.engine.page
        try:
            # Método 1: Dashboard Oficial
            await page.goto("https://rewards.bing.com/dashboard", wait_until="domcontentloaded")
            await asyncio.sleep(5) # Tempo para o script de pontos carregar
            
            # Tenta múltiplos seletores conhecidos
            selectors = [".pointsValue", "#id_rc", "#rh_pw_target", ".id_rc"]
            points = 0
            
            for selector in selectors:
                try:
                    element = await page.wait_for_selector(selector, timeout=5000)
                    text = await element.inner_text()
                    points = int(text.replace(".", "").replace(",", "").strip())
                    if points > 0: break
                except: continue

            if points == 0:
                logger.warning("Saldo não detectado no Dashboard. Tentando Home do Bing...")
                await page.goto("https://www.bing.com", wait_until="domcontentloaded")
                await asyncio.sleep(3)
                element = await page.wait_for_selector("#id_rc", timeout=5000)
                text = await element.inner_text()
                points = int(text.replace(".", "").replace(",", "").strip())

            logger.info(f"Saldo Soberano: {points} pts")
            self._save_to_log(points)
            return points
            
        except Exception as e:
            logger.error(f"Erro na extração de pontos: {e}")
            return 0

    def _save_to_log(self, points: int):
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        config_dir = os.path.dirname(self.log_file)
        os.makedirs(config_dir, exist_ok=True)
        
        file_exists = os.path.isfile(self.log_file)
        with open(self.log_file, "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Data", "Pontos"])
            writer.writerow([date_str, points])

    def generate_graph(self):
        """Dispara o gerador de gráficos usando o venv atual."""
        logger.info("Gerando gráfico industrial...")
        python_venv = "/home/viniciusphdu/WORKSPACE_CORE/Advanced-Rewards-Bot/venv/bin/python"
        graph_script = "/home/viniciusphdu/WORKSPACE_CORE/Advanced-Rewards-Bot/graph_points.py"
        
        if os.path.exists(graph_script):
            os.system(f"{python_venv} {graph_script}")
            logger.info("Visualização Atualizada.")
        else:
            logger.warning("Módulo gráfico ausente.")
