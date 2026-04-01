# Documentação Técnica e Arquitetura de Software - v5.5 Soberana

## 🏗️ Evolução da Arquitetura

O **Advanced-Rewards-Bot** evoluiu de um simples script de injeção de cookies para uma engine de automação de alta fidelidade que emula o comportamento de hardware real.

### 📂 Estrutura de Diretórios Atualizada

- **`src/core/engine.py`**: O motor soberano. Agora utiliza `launch_persistent_context` do Playwright para gerenciar sessões sem conflitos de processos.
- **`config/bot_profile/`**: Diretório que armazena o perfil real do bot, incluindo histórico e tokens de login, eliminando a dependência de arquivos JSON instáveis.
- **`src/automation/`**: Dividido em `searches.py` (Desktop/Mobile), `stats.py` (Oracle de Pontos) e `daily.py` (Resolvedor de Atividades).

---

## ⚙️ Detalhamento dos Avanços Técnicos

### 1. Motor de Persistência Nativa
Abandonamos a clonagem manual de perfis de navegadores do sistema (Edge/Chrome) devido a restrições de ELFCLASS e conflitos de arquivo `SingletonLock` no Arch Linux.
- **Bypass de Locks:** O motor implementa um sistema de limpeza atômica de arquivos de trava no boot, garantindo que o bot nunca falhe ao abrir.
- **Isolamento de Contexto:** O bot opera em seu próprio ecossistema Chromium, herdando apenas o login via interação inicial (Opção 5 do menu).

### 2. Lógica de Validação de Pontos (Discovery)
Após auditoria empírica (Cheat Engine Mode), a engine foi calibrada com:
- **Parâmetros de Injeção:** Uso obrigatório de `form=ML102W` (Desktop) e `form=ML102V` (Mobile) para forçar o crédito de recompensa.
- **Cadência Humana:** Delays fixados entre 15 e 22 segundos. A Microsoft Rewards implementou um filtro de frequência que ignora buscas feitas em intervalos menores que 10 segundos.
- **Interação HID:** Simulação de scrolls e movimentos de mouse randômicos pós-carregamento para validar a presença humana perante os scripts de telemetria da Microsoft.

### 3. Emulação de Hardware Mobile (Moto G52)
Diferente da versão 1.0, a versão 5.5 não apenas troca o User-Agent, mas injeta propriedades de hardware:
- `has_touch`: Habilitado para simular tela sensível ao toque.
- `viewport`: Travado em 360x800 para condizer com a resolução real de dispositivos móveis.
- `is_mobile`: Flag de contexto ativada para garantir que o Bing entregue a versão móvel correta.

---

## 🛡️ Segurança e Evasão (Stealth)

O bot agora implementa proteção contra o **Fingerprinting** do navegador:
- Injeção de script de inicialização para remover a propriedade `navigator.webdriver`.
- Desativação de flags de automação nativas (`--enable-automation`).
- Comportamento de navegação orgânica: Visita à página inicial do Bing a cada ciclo de buscas para "aquecer" a sessão.

---

## 🚀 Roadmap de Futuras Implementações

1. **Ghost Engine v2:** Integração com o compositor Hyprland para digitação via `wtype` (Hardware puro).
2. **Multi-Accounting:** Suporte para múltiplos diretórios de perfil (`bot_profile_1`, `bot_profile_2`).
3. **Resgate Automatizado:** Verificação de cotação de Gift Cards via Dashboard API.

---
*Documento de Referência Técnica - Advanced-Rewards-Bot v5.5*
