import asyncio
import random
import os
from typing import Dict, Any, List, Optional
from playwright.async_api import async_playwright, BrowserContext, Page
from src.utils.logger import logger

class RewardsEngine:
    """
    Motor de automação baseado em Playwright para orquestração de sessões do Microsoft Rewards.
    Implementa o padrão de Factory para contextos de navegação e emulação mobile.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.browser = None
        self.context: Optional[BrowserContext] = None
        self.is_running = False
        self._hooks = []

    def add_hook(self, callback):
        """Adiciona um observador para eventos de automação (Bridge para GUI)."""
        self._hooks.append(callback)

    async def _emit(self, event: str, data: Any = None):
        """Emite eventos para os observadores (GUI/Hooks)."""
        for hook in self._hooks:
            if asyncio.iscoroutinefunction(hook):
                await hook(event, data)
            else:
                hook(event, data)

    async def initialize(self, headless: bool = True, user_agent: str = None):
        """Inicializa ou reinicializa o contexto de navegação preservando a sessão."""
        if not self.browser:
            logger.info("Iniciando instância do navegador Chromium...")
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(headless=headless)

        # Se já existe um contexto, salva a sessão antes de fechar para não perder o login
        if self.context:
            await self.save_session()
            await self.context.close()

        # Caminho da sessão
        config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../config"))
        os.makedirs(config_dir, exist_ok=True)
        state_path = os.path.join(config_dir, "session_state.json")
        
        # Define o User-Agent (prioriza o passado por parâmetro ou o da config)
        ua = user_agent or self.config.get("user_agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        logger.info(f"Configurando novo contexto | UA: {ua[:50]}...")
        
        # Cria novo contexto com o estado persistido
        self.context = await self.browser.new_context(
            user_agent=ua,
            viewport={'width': 1920, 'height': 1080},
            storage_state=state_path if os.path.exists(state_path) and os.path.getsize(state_path) > 0 else None
        )
        
        await self._emit("ENGINE_READY")

    async def perform_search(self, keywords: List[str]):
        """Executa buscas na mesma página para manter a integridade da sessão."""
        if not self.context:
            raise RuntimeError("Contexto não inicializado.")

        # Reutiliza a página aberta ou cria uma nova se não houver
        pages = self.context.pages
        page = pages[0] if pages else await self.context.new_page()
        
        logger.info(f"Validando login em Bing.com...")
        await page.goto("https://www.bing.com", wait_until="networkidle")
        
        # Pequena pausa para garantir que os cookies foram injetados
        await asyncio.sleep(2)

        for term in keywords:
            try:
                await self._emit("SEARCH_START", term)
                logger.debug(f"Pesquisando: {term}")
                
                # Busca direta via URL para velocidade e estabilidade
                await page.goto(f"https://www.bing.com/search?q={term}", wait_until="domcontentloaded")
                
                # Delay humano
                await asyncio.sleep(random.uniform(3, 6))
                await self._emit("SEARCH_SUCCESS", term)
                
            except Exception as e:
                logger.error(f"Erro no termo {term}: {str(e)}")

    async def shutdown(self):
        """Finaliza as sessões e libera os recursos do sistema."""
        if self.browser:
            await self.browser.close()
        logger.info("Motor finalizado. Recursos liberados.")
        await self._emit("ENGINE_SHUTDOWN")
