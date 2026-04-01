import asyncio
import os
import shutil
import random
from typing import Dict, Any, List, Optional
from playwright.async_api import async_playwright, BrowserContext, Page
from src.utils.logger import logger

class RewardsEngine:
    """
    Motor de Automação Enterprise v3.1.
    Focado em estabilidade extrema e bypass de travas de perfil.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.playwright = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.bot_profile = os.path.expanduser("~/WORKSPACE_CORE/Advanced-Rewards-Bot/config/bot_profile")

    async def initialize(self, headless: bool = False, user_agent: str = None):
        """Inicializa o navegador com perfil limpo e persistente."""
        # Limpeza de travas de segurança do Chromium/Edge
        lock_files = [".com.google.Chrome.6H66", "SingletonLock", "SingletonSocket", "SingletonCookie"]
        for lock in lock_files:
            lock_path = os.path.join(self.bot_profile, lock)
            if os.path.exists(lock_path):
                try: os.remove(lock_path)
                except: pass

        if not self.playwright:
            self.playwright = await async_playwright().start()

        ua = user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
        
        logger.info(f"Lançando Navegador Soberano...")
        try:
            # Usar o Chromium interno do Playwright para evitar conflitos com o Edge do sistema
            self.context = await self.playwright.chromium.launch_persistent_context(
                user_data_dir=self.bot_profile,
                headless=headless,
                user_agent=ua,
                viewport={'width': 1280, 'height': 720},
                args=[
                    "--no-first-run",
                    "--disable-blink-features=AutomationControlled",
                    "--disable-infobars",
                    "--no-sandbox"
                ]
            )
            
            self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()
            self.page.set_default_timeout(45000)
            
            logger.info("Acessando Bing para validar sessão...")
            await self.page.goto("https://www.bing.com", wait_until="domcontentloaded")
            
        except Exception as e:
            logger.error(f"Erro no lançamento: {e}")
            raise e

    async def perform_search(self, keywords: List[str]):
        """Ciclo de busca com proteção de cadência."""
        if not self.page: raise RuntimeError("Engine não inicializada.")

        for term in keywords:
            try:
                url = f"https://www.bing.com/search?q={term.replace(' ', '+')}"
                await self.page.goto(url, wait_until="domcontentloaded")
                await asyncio.sleep(random.uniform(5, 9))
                logger.info(f"Busca Concluída: {term}")
            except Exception as e:
                logger.error(f"Erro na busca: {e}")

    async def shutdown(self):
        try:
            if self.context: await self.context.close()
            if self.playwright: await self.playwright.stop()
        except: pass
        logger.info("Recursos liberados.")
