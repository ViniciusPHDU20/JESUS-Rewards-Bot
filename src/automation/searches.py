import asyncio
import random
from src.core.engine import RewardsEngine
from src.utils.logger import logger

class SearchAutomation:
    """Módulo especializado em emulação de buscas Desktop e Mobile."""
    
    def __init__(self, engine: RewardsEngine):
        self.engine = engine

    async def run_desktop_searches(self, count: int = 30):
        """Executa buscas simulando um ambiente Desktop."""
        logger.info(f"Iniciando ciclo de {count} buscas DESKTOP...")
        # Lista de termos reais para evitar detecção
        terms = [
            "melhores configurações arch linux", "notícias tecnologia", 
            "clima agora", "cotação dólar", "receitas rápidas",
            "lançamentos steam 2026", "como otimizar xeon v2",
            "vulkan vs opengl linux", "hyprland config tutorial"
        ]
        # Gerar mais termos se necessário
        search_list = random.sample(terms * (count // len(terms) + 1), count)
        
        await self.engine.perform_search(search_list)
        logger.info("Buscas DESKTOP finalizadas.")

    async def run_mobile_searches(self, count: int = 20):
        """Executa buscas emulando o Moto G52 sem perder a sessão."""
        logger.info(f"Trocando para identidade MOBILE (Moto G52)... {count} buscas pendentes.")
        
        mobile_ua = "Mozilla/5.0 (Linux; Android 16; Moto G52) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
        
        # Reinicia o contexto com o novo User-Agent mantendo os cookies
        await self.engine.initialize(headless=False, user_agent=mobile_ua)
        
        terms = ["filmes em cartaz", "restaurantes próximos", "jogos android", "preço moto g52", "clima amanhã", "notícias do dia"]
        search_list = random.sample(terms * (count // len(terms) + 1), count)
        
        await self.engine.perform_search(search_list)
        logger.info("Buscas MOBILE finalizadas.")
