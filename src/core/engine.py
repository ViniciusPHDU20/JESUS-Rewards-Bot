import asyncio
import os
import random
from typing import Dict, Any, List, Optional
from playwright.async_api import async_playwright, BrowserContext, Page
from src.utils.logger import logger

class RewardsEngine:
    """
    Motor de Automação Enterprise v3.2.
    Arquitetura de Contexto Persistente Nativo para estabilidade absoluta.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.playwright = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.bot_profile = os.path.expanduser("~/WORKSPACE_CORE/Advanced-Rewards-Bot/config/bot_profile")

    async def initialize(self, headless: bool = False, user_agent: str = None):
        """Inicializa o navegador com perfil nativo isolado."""
        if not self.playwright:
            self.playwright = await async_playwright().start()

        ua = user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        
        logger.info("Lançando Motor de Navegação Nativo...")
        try:
            # Contexto persistente limpo (evita erros de classe ELF e conflitos de lock)
            self.context = await self.playwright.chromium.launch_persistent_context(
                user_data_dir=self.bot_profile,
                headless=headless,
                user_agent=ua,
                viewport={'width': 1280, 'height': 720},
                args=[
                    "--no-first-run",
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox"
                ]
            )
            
            self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()
            self.page.set_default_timeout(60000)
            
            logger.info("Sistema em prontidão.")
            
        except Exception as e:
            logger.error(f"Erro crítico no lançamento: {e}")
            raise e

    async def perform_search(self, keywords: List[str]):
        """Executa buscas com emulação de comportamento humano."""
        if not self.page: raise RuntimeError("Engine não inicializada.")

        for term in keywords:
            try:
                url = f"https://www.bing.com/search?q={term.replace(' ', '+')}"
                await self.page.goto(url, wait_until="domcontentloaded")
                # Interação pseudo-humana
                await asyncio.sleep(random.uniform(4, 7))
                if random.random() > 0.6:
                    await self.page.mouse.wheel(0, random.randint(300, 600))
                
                logger.info(f"Busca validada: {term}")
            except Exception as e:
                logger.warning(f"Erro no termo {term}: {e}")

    async def shutdown(self):
        try:
            if self.context: await self.context.close()
            if self.playwright: await self.playwright.stop()
        except: pass
        logger.info("Recursos liberados com sucesso.")
