import asyncio
import os
import shutil
import random
import subprocess
from typing import Dict, Any, List, Optional
from playwright.async_api import async_playwright, BrowserContext, Page
from src.utils.logger import logger

class RewardsEngine:
    """
    Motor de Automação Enterprise v3.0.
    Implementa Clonagem de Perfil Estratégica e Evasão HID via Playwright.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.playwright = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        self.bot_profile = os.path.join(self.project_root, "config/bot_profile")

    def _clone_profile(self):
        """Realiza a clonagem dos dados de autenticação com limpeza de travas."""
        source_profile = os.path.expanduser("~/.config/microsoft-edge")
        essential_items = ["Default/Cookies", "Default/Login Data", "Local State"]
        
        os.makedirs(self.bot_profile, exist_ok=True)
        logger.info("Sincronizando credenciais do Edge...")

        for item in essential_items:
            src = os.path.join(source_profile, item)
            dst = os.path.join(self.bot_profile, item)
            if os.path.exists(src):
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                try:
                    shutil.copy2(src, dst)
                except Exception as e:
                    logger.debug(f"Aviso na cópia de {item} (provavelmente em uso): {e}")

        # Limpeza atômica de arquivos lock para evitar erro 'Target closed'
        for root, dirs, files in os.walk(self.bot_profile):
            for file in files:
                if "lock" in file.lower() or "singleton" in file.lower():
                    try:
                        os.remove(os.path.join(root, file))
                    except:
                        pass

    async def initialize(self, headless: bool = False, user_agent: str = None):
        """Inicializa o contexto isolado e logado."""
        self._clone_profile()
        
        if not self.playwright:
            self.playwright = await async_playwright().start()

        ua = user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
        
        logger.info("Lançando motor de navegação...")
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=self.bot_profile,
            channel="msedge",
            headless=headless,
            user_agent=ua,
            viewport={'width': 1920, 'height': 1080},
            args=["--no-first-run", "--no-default-browser-check"]
        )
        
        self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()
        # Aumentar timeout global para 60s para conexões Arch estáveis
        self.page.set_default_timeout(60000)
        
        await self.page.goto("https://www.bing.com", wait_until="domcontentloaded")
        logger.info("Motor em prontidão operacional.")

    async def perform_search(self, keywords: List[str]):
        """Executa buscas com jitter de telemetria para bypass de detecção."""
        if not self.page: raise RuntimeError("Engine não inicializada.")

        for term in keywords:
            try:
                # Simulação de comportamento humano na URL
                url = f"https://www.bing.com/search?q={term.replace(' ', '+')}&form=ML102W"
                await self.page.goto(url, wait_until="domcontentloaded")
                
                # Jitter de interação
                await asyncio.sleep(random.uniform(4, 8))
                if random.random() > 0.5:
                    await self.page.mouse.wheel(0, random.randint(200, 500))
                
                logger.info(f"Busca validada: {term}")
            except Exception as e:
                logger.error(f"Falha no processamento: {e}")

    async def shutdown(self):
        if self.context: await self.context.close()
        if self.playwright: await self.playwright.stop()
        logger.info("Recursos liberados com integridade.")
