import asyncio
import random
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

    async def initialize(self, headless: bool = True):
        """Inicializa o motor Playwright e configura o contexto de navegação com persistência de sessão."""
        logger.info("Inicializando Motor de Automação Core...")
        playwright = await async_playwright().start()
        
        # Caminho do estado da sessão (Protegido pelo .gitignore)
        state_path = "/home/viniciusphdu/WORKSPACE_CORE/Advanced-Rewards-Bot/config/session_state.json"
        
        user_agent = self.config.get("user_agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        self.browser = await playwright.chromium.launch(headless=headless)
        
        # Tenta carregar a sessão existente se o arquivo existir
        try:
            self.context = await self.browser.new_context(
                user_agent=user_agent,
                viewport={'width': 1920, 'height': 1080},
                storage_state=state_path if os.path.exists(state_path) else None
            )
            logger.info("Sessão carregada com sucesso.")
        except Exception as e:
            logger.warning(f"Não foi possível carregar a sessão anterior: {str(e)}")
            self.context = await self.browser.new_context(
                user_agent=user_agent,
                viewport={'width': 1920, 'height': 1080}
            )

        await self._emit("ENGINE_READY")
        logger.info("Motor inicializado com sucesso.")

    async def save_session(self):
        """Salva o estado atual da sessão (cookies/tokens) para uso futuro."""
        if self.context:
            state_path = "/home/viniciusphdu/WORKSPACE_CORE/Advanced-Rewards-Bot/config/session_state.json"
            await self.context.storage_state(path=state_path)
            logger.info("Estado da sessão persistido localmente.")

    async def perform_search(self, keywords: List[str]):
        """Executa buscas dinâmicas com comportamento pseudo-humano."""
        if not self.context:
            raise RuntimeError("Motor não inicializado. Chame initialize() primeiro.")

        page: Page = await self.context.new_page()
        logger.info(f"Iniciando ciclo de busca para {len(keywords)} termos.")

        for term in keywords:
            try:
                await self._emit("SEARCH_START", term)
                logger.debug(f"Processando termo: {term}")
                
                await page.goto(f"https://www.bing.com/search?q={term}")
                
                # Delay randômico para simular comportamento humano (Ghost Engine logic)
                delay = random.uniform(2.5, 5.0)
                await asyncio.sleep(delay)
                
                await self._emit("SEARCH_SUCCESS", term)
                
            except Exception as e:
                logger.error(f"Erro ao processar termo '{term}': {str(e)}")
                await self._emit("SEARCH_ERROR", {"term": term, "error": str(e)})

        await page.close()
        logger.info("Ciclo de busca concluído.")

    async def shutdown(self):
        """Finaliza as sessões e libera os recursos do sistema."""
        if self.browser:
            await self.browser.close()
        logger.info("Motor finalizado. Recursos liberados.")
        await self._emit("ENGINE_SHUTDOWN")
