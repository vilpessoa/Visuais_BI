#!/usr/bin/env python3
"""
Build script for Power_IA_TESS.pbiviz
Creates the Power BI custom visual with TESS AI integration.
"""

import json
import zipfile
import os

GUID = "PowerIATESS1F2A3B4C5D6E7F8A"
DISPLAY_NAME = "Power IA TESS"
VISUAL_CLASS = "Visual"
API_VERSION = "5.3.0"
VERSION = "1.0.0.0"

# ─────────────────────────────────────────────────────────────
# CSS — original visual CSS with green → TESS orange theme
# ─────────────────────────────────────────────────────────────
CSS = """.aiChatVisual {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #ffffff;
  overflow: hidden;
  font-size: 12px;
}
.aiChatVisual .module-setup {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 0;
  background: #F9FAFB;
}
.aiChatVisual .module-setup::-webkit-scrollbar { width: 4px; }
.aiChatVisual .module-setup::-webkit-scrollbar-thumb { background: #D1D5DB; border-radius: 2px; }
.aiChatVisual .module-header { background: #E85D04; padding: 14px 16px; display: flex; align-items: flex-start; justify-content: space-between; gap: 10px; flex-shrink: 0; }
.aiChatVisual .module-header-left { display: flex; align-items: center; gap: 10px; }
.aiChatVisual .module-badge { width: 28px; height: 28px; border-radius: 50%; background: rgba(255,255,255,0.25); color: white; font-size: 14px; font-weight: 800; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.aiChatVisual .module-title { font-size: 13px; font-weight: 700; color: #ffffff; line-height: 1.3; }
.aiChatVisual .module-subtitle { font-size: 10px; color: rgba(255,255,255,0.75); margin-top: 2px; }
.aiChatVisual .lang-wrap { display: flex; flex-direction: column; align-items: flex-end; gap: 3px; flex-shrink: 0; }
.aiChatVisual .lang-label { font-size: 9px; color: rgba(255,255,255,0.7); }
.aiChatVisual .lang-select-setup { background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.3); color: white; border-radius: 5px; padding: 3px 6px; font-size: 11px; cursor: pointer; outline: none; }
.aiChatVisual .lang-select-setup option { background: #E85D04; color: white; }
.aiChatVisual .setup-step { background: #ffffff; margin: 10px 12px 0; border-radius: 10px; border: 1px solid #E5E7EB; padding: 14px; display: flex; flex-direction: column; gap: 8px; }
.aiChatVisual .step-header { display: flex; align-items: center; gap: 8px; }
.aiChatVisual .step-num { width: 22px; height: 22px; border-radius: 50%; background: #E85D04; color: white; font-size: 11px; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.aiChatVisual .step-title { font-size: 12px; font-weight: 700; color: #111827; }
.aiChatVisual .step-desc { font-size: 10px; color: #6B7280; line-height: 1.5; }
.aiChatVisual .cmd-box { background: #1F2937; color: #FF8C42; font-family: 'Courier New', monospace; font-size: 10px; padding: 8px 10px; border-radius: 6px; word-break: break-all; line-height: 1.5; }
.aiChatVisual .step-note { font-size: 10px; color: #B45309; background: #FFF7ED; border-left: 3px solid #F59E0B; padding: 5px 8px; border-radius: 0 4px 4px 0; }
.aiChatVisual .tess-note { font-size: 10px; color: #C44D03; background: #FFF3E0; border-left: 3px solid #E85D04; padding: 5px 8px; border-radius: 0 4px 4px 0; font-weight: 600; }
.aiChatVisual .field-label { font-size: 10px; font-weight: 600; color: #374151; }
.aiChatVisual .field-input { width: 100%; border: 1px solid #D1D5DB; border-radius: 6px; padding: 7px 10px; font-size: 11px; outline: none; box-sizing: border-box; font-family: inherit; }
.aiChatVisual .field-input:focus { border-color: #E85D04; background: #FFF3E0; }
.aiChatVisual .setup-error { margin: 6px 12px 0; font-size: 10px; color: #EF4444; background: #FEF2F2; border: 1px solid #FECACA; border-radius: 6px; padding: 6px 10px; }
.aiChatVisual .next-btn { margin: 12px 12px; background: #E85D04; color: white; border: none; border-radius: 8px; padding: 11px; font-size: 13px; font-weight: 700; cursor: pointer; width: calc(100% - 24px); letter-spacing: 0.3px; }
.aiChatVisual .next-btn:hover { background: #C44D03; }
.aiChatVisual .load-agents-btn { background: #E85D04; color: white; border: none; border-radius: 6px; padding: 7px 14px; font-size: 11px; font-weight: 700; cursor: pointer; }
.aiChatVisual .load-agents-btn:hover { background: #C44D03; }
.aiChatVisual .load-agents-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.aiChatVisual .agent-spinner { display: inline-block; font-size: 11px; color: #E85D04; }
.aiChatVisual .module-chat { flex: 1; display: flex; flex-direction: column; overflow: hidden; background: #ffffff; }
.aiChatVisual .chat-header { background: #E85D04; padding: 9px 12px; display: flex; align-items: center; justify-content: space-between; flex-shrink: 0; }
.aiChatVisual .chat-header-left { display: flex; align-items: center; gap: 7px; }
.aiChatVisual .header-dot { width: 7px; height: 7px; border-radius: 50%; background: #FF8C42; flex-shrink: 0; }
.aiChatVisual .chat-title { font-size: 12px; font-weight: 700; color: white; }
.aiChatVisual .chat-header-right { display: flex; align-items: center; gap: 5px; }
.aiChatVisual .lang-select-chat { background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.3); color: white; border-radius: 4px; padding: 2px 5px; font-size: 12px; cursor: pointer; outline: none; }
.aiChatVisual .lang-select-chat option { background: #E85D04; color: white; }
.aiChatVisual .hdr-btn { background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25); color: white; border-radius: 5px; padding: 3px 8px; font-size: 10px; cursor: pointer; white-space: nowrap; }
.aiChatVisual .hdr-btn:hover { background: rgba(255,255,255,0.25); }
.aiChatVisual .hdr-btn-outline { background: transparent; opacity: 0.8; }
.aiChatVisual .hdr-btn-outline:hover { opacity: 1; }
.aiChatVisual .chat-messages { flex: 1; overflow-y: auto; padding: 12px; display: flex; flex-direction: column; gap: 8px; background: #F9FAFB; }
.aiChatVisual .chat-messages::-webkit-scrollbar { width: 4px; }
.aiChatVisual .chat-messages::-webkit-scrollbar-thumb { background: #D1D5DB; border-radius: 2px; }
.aiChatVisual .chat-messages .message { max-width: 85%; padding: 8px 12px; border-radius: 10px; font-size: 12px; line-height: 1.5; word-break: break-word; }
.aiChatVisual .chat-messages .message.user { align-self: flex-end; background: #E85D04; color: white; border-bottom-right-radius: 3px; }
.aiChatVisual .chat-messages .message.assistant { align-self: flex-start; background: white; color: #1F2937; border: 1px solid #E5E7EB; border-bottom-left-radius: 3px; }
.aiChatVisual .chat-messages .message.error { align-self: flex-start; background: #FEF2F2; color: #991B1B; border: 1px solid #FECACA; }
.aiChatVisual .chat-messages .message.thinking { align-self: flex-start; background: #F3F4F6; color: #6B7280; border: 1px solid #E5E7EB; font-style: italic; }
.aiChatVisual .chat-messages .message.thinking .dots { animation: blink 1.2s infinite; display: inline-block; }
.aiChatVisual .ctx-bar { padding: 6px 12px; background: #FFF3E0; border-top: 1px solid #FFE0B2; font-size: 10px; display: flex; gap: 5px; align-items: flex-start; flex-shrink: 0; flex-wrap: wrap; }
.aiChatVisual .ctx-label { font-weight: 700; color: #BF360C; white-space: nowrap; }
.aiChatVisual .ctx-values { color: #E64A19; line-height: 1.5; }
.aiChatVisual .chat-input-area { display: flex; gap: 6px; padding: 9px 12px; border-top: 1px solid #E5E7EB; background: white; align-items: flex-end; flex-shrink: 0; }
.aiChatVisual .chat-textarea { flex: 1; border: 1px solid #D1D5DB; border-radius: 8px; padding: 7px 10px; font-size: 12px; font-family: inherit; resize: none; max-height: 80px; line-height: 1.4; color: #1F2937; background: #F9FAFB; outline: none; }
.aiChatVisual .chat-textarea:focus { border-color: #E85D04; background: white; }
.aiChatVisual .chat-textarea::placeholder { color: #9CA3AF; }
.aiChatVisual .send-btn { background: #E85D04; color: white; border: none; border-radius: 8px; width: 34px; height: 34px; display: flex; align-items: center; justify-content: center; font-size: 16px; cursor: pointer; flex-shrink: 0; }
.aiChatVisual .send-btn:hover { background: #C44D03; }
.aiChatVisual .send-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.aiChatVisual .provider-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(90px, 1fr)); gap: 6px; }
.aiChatVisual .provider-btn { display: flex; flex-direction: column; align-items: center; gap: 3px; padding: 8px 4px; border-radius: 8px; border: 2px solid #E5E7EB; background: #F9FAFB; cursor: pointer; transition: all 0.15s; }
.aiChatVisual .provider-btn:hover { border-color: #E85D04; background: #FFF3E0; }
.aiChatVisual .provider-btn.active { border-color: #E85D04; background: #FFF3E0; }
.aiChatVisual .provider-icon { font-size: 20px; }
.aiChatVisual .provider-label { font-size: 9px; font-weight: 600; color: #374151; text-align: center; }
.aiChatVisual .provider-pill { font-size: 10px; background: rgba(255,255,255,0.2); color: white; padding: 2px 7px; border-radius: 10px; font-weight: 600; }
.dynamic-area { display: flex; flex-direction: column; gap: 0; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }
"""

# ─────────────────────────────────────────────────────────────
# JavaScript visual code
# ─────────────────────────────────────────────────────────────
JS = r"""
var PowerIATESS1F2A3B4C5D6E7F8A;
(function() {
    "use strict";

    // ── Provider definitions ──────────────────────────────────
    var PROVIDERS = [
        {
            id: "tess",
            label: "TESS AI",
            icon: "🔶",
            urlLabel: "proxyLabel",
            urlPlaceholder: "http://localhost:3100",
            urlRequired: false,
            keyLabel: "keyLabel",
            keyPlaceholder: "seu-token-tess...",
            modelLabel: "Modelo:",
            modelDefault: "tess-5",
            modelOptions: ["tess-5", "tess-3", "gpt-4o", "claude-sonnet-4-6"],
            proxyNote: "tessProxyNote",
            hasDynamicAgents: true
        },
        {
            id: "anthropic",
            label: "Claude (Anthropic)",
            icon: "🟣",
            urlLabel: "proxyLabel",
            urlPlaceholder: "http://localhost:3100",
            urlRequired: false,
            keyLabel: "keyLabel",
            keyPlaceholder: "sk-ant-api03-...",
            modelLabel: "Modelo:",
            modelDefault: "claude-sonnet-4-6",
            modelOptions: ["claude-haiku-4-5-20251001", "claude-sonnet-4-6", "claude-opus-4-6"],
            proxyNote: "proxyNote",
            hasDynamicAgents: false
        },
        {
            id: "openai",
            label: "GPT (OpenAI)",
            icon: "🟢",
            urlLabel: "proxyLabel",
            urlPlaceholder: "http://localhost:3100",
            urlRequired: false,
            keyLabel: "keyLabel",
            keyPlaceholder: "sk-...",
            modelLabel: "Modelo:",
            modelDefault: "gpt-4o",
            modelOptions: ["gpt-4.1-nano", "gpt-4.1-mini", "gpt-4.1", "gpt-4o", "gpt-5"],
            proxyNote: "proxyNote",
            hasDynamicAgents: false
        },
        {
            id: "gemini",
            label: "Gemini (Google)",
            icon: "🔵",
            urlLabel: "proxyLabel",
            urlPlaceholder: "http://localhost:3100",
            urlRequired: false,
            keyLabel: "keyLabel",
            keyPlaceholder: "AIzaSy...",
            modelLabel: "Modelo:",
            modelDefault: "gemini-2.5-flash-lite",
            modelOptions: ["gemini-2.5-flash-lite", "gemini-2.5-flash", "gemini-2.5-pro"],
            proxyNote: "proxyNote",
            hasDynamicAgents: false
        },
        {
            id: "azure",
            label: "Azure OpenAI",
            icon: "🔷",
            urlLabel: "azureUrlLabel",
            urlPlaceholder: "https://TU-RECURSO.openai.azure.com",
            urlRequired: true,
            keyLabel: "keyLabel",
            keyPlaceholder: "tu-api-key-de-azure",
            modelLabel: "Deployment name:",
            modelDefault: "",
            modelOptions: [],
            proxyNote: "azureNote",
            hasDynamicAgents: false
        }
    ];

    // ── i18n ──────────────────────────────────────────────────
    var I18N = {
        es: {
            mod1Title: "Módulo 1 — Configuración",
            mod1Subtitle: "Configura el proveedor de IA y tu API Key",
            providerLabel: "Proveedor de IA:",
            step1Title: "Paso 1 · Proxy local (Desktop)",
            step1Desc: "Abre una terminal y ejecuta:",
            step1Cmd: "node proxy.js --provider PROVEEDOR --key TU_API_KEY --port 3100",
            step1Note: "Deja la terminal abierta mientras usas el chat.",
            proxyLabel: "URL del proxy (opcional en Service):",
            azureUrlLabel: "Azure Endpoint URL:",
            proxyNote: "En Power BI Desktop necesitas el proxy. En Service puedes dejar vacío.",
            azureNote: "El endpoint de Azure es obligatorio.",
            tessProxyNote: "No Desktop necesitas el proxy. En Service publicado, déjalo vacío.",
            step2Title: "Paso 2 · API Key",
            step2Desc: "Ingresa tu clave del proveedor seleccionado:",
            keyLabel: "API Key:",
            modelCustomLabel: "O ingresa un modelo personalizado:",
            modelCustomPlaceholder: "nombre-del-modelo...",
            step3Title: "Paso 3 · Agente TESS",
            agentLabel: "Agente TESS:",
            loadAgentsBtn: "Cargar Agentes",
            agentLoadError: "Error al cargar agentes. Verifique el proxy y la API Key.",
            agentSelectPlaceholder: "Seleccione un agente...",
            nextBtn: "Ir al Chat →",
            errUrl: "La URL debe empezar con http",
            errKey: "La API Key no puede estar vacía",
            errModel: "Debes indicar el deployment name para Azure",
            errAgent: "Debes seleccionar un agente TESS",
            langLabel: "Idioma:",
            mod2Title: "Power IA TESS",
            configBtn: "⚙ Config",
            clearBtn: "🗑 Limpiar",
            placeholder: "Pregunta sobre los datos...",
            thinkingMsg: "Analizando",
            welcomeMsg: "¡Listo! Soy Power IA TESS. Puedo analizar las medidas, países y fechas conectadas. ¿Qué quieres explorar?",
            clearedMsg: "Chat limpiado. ¿En qué te puedo ayudar?",
            contextLabel: "Contexto:",
            noContext: "Sin datos — arrastra campos al visual",
            systemPrompt: "Eres un asistente de análisis de datos para Power BI con TESS AI. Responde en español, de forma concisa y orientada a negocios. Sin markdown, solo texto plano.",
            ctxHeader: "CONTEXTO DEL REPORTE:",
            ctxBase: "Basa tus respuestas en estos valores.",
            noCtxMsg: "No hay datos conectados al visual.",
            providerTag: "Proveedor:"
        },
        en: {
            mod1Title: "Module 1 — Setup",
            mod1Subtitle: "Configure the AI provider and your API Key",
            providerLabel: "AI Provider:",
            step1Title: "Step 1 · Local Proxy (Desktop)",
            step1Desc: "Open a terminal and run:",
            step1Cmd: "node proxy.js --provider PROVIDER --key YOUR_API_KEY --port 3100",
            step1Note: "Keep the terminal open while using the chat.",
            proxyLabel: "Proxy URL (optional in Service):",
            azureUrlLabel: "Azure Endpoint URL:",
            proxyNote: "In Power BI Desktop you need the proxy. In Service you can leave it empty.",
            azureNote: "The Azure endpoint URL is required.",
            tessProxyNote: "On Desktop you need the proxy. In published Service, leave it empty.",
            step2Title: "Step 2 · API Key",
            step2Desc: "Enter your key for the selected provider:",
            keyLabel: "API Key:",
            modelCustomLabel: "Or enter a custom model:",
            modelCustomPlaceholder: "model-name...",
            step3Title: "Step 3 · TESS Agent",
            agentLabel: "TESS Agent:",
            loadAgentsBtn: "Load Agents",
            agentLoadError: "Error loading agents. Check proxy and API Key.",
            agentSelectPlaceholder: "Select an agent...",
            nextBtn: "Go to Chat →",
            errUrl: "URL must start with http",
            errKey: "API Key cannot be empty",
            errModel: "You must provide the deployment name for Azure",
            errAgent: "You must select a TESS agent",
            langLabel: "Language:",
            mod2Title: "Power IA TESS",
            configBtn: "⚙ Config",
            clearBtn: "🗑 Clear",
            placeholder: "Ask about the data...",
            thinkingMsg: "Analyzing",
            welcomeMsg: "Ready! I am Power IA TESS. I can analyze the connected measures, countries and dates. What would you like to explore?",
            clearedMsg: "Chat cleared. How can I help you?",
            contextLabel: "Context:",
            noContext: "No data — drag fields to the visual",
            systemPrompt: "You are a data analysis assistant for Power BI with TESS AI. Respond in English, concisely and business-oriented. No markdown, plain text only.",
            ctxHeader: "REPORT CONTEXT:",
            ctxBase: "Base your answers on these values.",
            noCtxMsg: "No data connected to the visual.",
            providerTag: "Provider:"
        },
        pt: {
            mod1Title: "Módulo 1 — Configuração",
            mod1Subtitle: "Configure o provedor de IA e sua API Key",
            providerLabel: "Provedor de IA:",
            step1Title: "Passo 1 · Proxy local (Desktop)",
            step1Desc: "Abra um terminal e execute:",
            step1Cmd: "node proxy.js --provider PROVEDOR --key SUA_API_KEY --port 3100",
            step1Note: "Mantenha o terminal aberto enquanto usa o chat.",
            proxyLabel: "URL do proxy (opcional no Service):",
            azureUrlLabel: "URL do Azure Endpoint:",
            proxyNote: "No Power BI Desktop você precisa do proxy. No Service pode deixar vazio.",
            azureNote: "O endpoint do Azure é obrigatório.",
            tessProxyNote: "No Desktop o proxy é necessário. No Service publicado, deixe vazio.",
            step2Title: "Passo 2 · API Key",
            step2Desc: "Insira sua chave do provedor selecionado:",
            keyLabel: "API Key:",
            modelCustomLabel: "Ou insira um modelo personalizado:",
            modelCustomPlaceholder: "nome-do-modelo...",
            step3Title: "Passo 3 · Agente TESS",
            agentLabel: "Agente TESS:",
            loadAgentsBtn: "Carregar Agentes",
            agentLoadError: "Erro ao carregar agentes. Verifique o proxy e a API Key.",
            agentSelectPlaceholder: "Selecione um agente...",
            nextBtn: "Ir ao Chat →",
            errUrl: "A URL deve começar com http",
            errKey: "A API Key não pode estar vazia",
            errModel: "Você deve indicar o deployment name para Azure",
            errAgent: "Você deve selecionar um agente TESS",
            langLabel: "Idioma:",
            mod2Title: "Power IA TESS",
            configBtn: "⚙ Config",
            clearBtn: "🗑 Limpar",
            placeholder: "Pergunte sobre os dados...",
            thinkingMsg: "Analisando",
            welcomeMsg: "Pronto! Sou o Power IA TESS. Posso analisar as medidas, países e datas conectadas. O que você quer explorar?",
            clearedMsg: "Chat limpo. Como posso ajudar?",
            contextLabel: "Contexto:",
            noContext: "Sem dados — arraste campos ao visual",
            systemPrompt: "Você é um assistente de análise de dados para Power BI com TESS AI. Responda em português, de forma concisa e orientada a negócios. Sem markdown, apenas texto simples.",
            ctxHeader: "CONTEXTO DO RELATÓRIO:",
            ctxBase: "Baseie suas respostas nestes valores.",
            noCtxMsg: "Nenhum dado conectado ao visual.",
            providerTag: "Provedor:"
        }
    };

    // ── Visual Class ──────────────────────────────────────────
    function Visual(options) {
        this.host = options.host;
        this.container = options.element;
        this.container.classList.add("aiChatVisual");
        this.messages = [];
        this.apiKey = "";
        this.proxyUrl = "";
        this.lang = "es";
        this.provider = "tess";
        this.model = "tess-5";
        this.agentId = "";
        this.page = "setup";
        this.context = { measures: [], categories: [], dates: [] };
        this.isLoading = false;
        this.messagesContainer = null;
        this.textarea = null;
        this.sendBtn = null;
        this.contextValuesEl = null;

        try {
            this.apiKey = localStorage.getItem("pbiviz_aiChat_apiKey") || "";
            this.proxyUrl = localStorage.getItem("pbiviz_aiChat_proxyUrl") || "";
            this.lang = localStorage.getItem("pbiviz_aiChat_lang") || "es";
            this.provider = localStorage.getItem("pbiviz_aiChat_provider") || "tess";
            this.model = localStorage.getItem("pbiviz_aiChat_model") || "tess-5";
            this.agentId = localStorage.getItem("pbiviz_tess_agentId") || "";
        } catch(e) {}

        var needsAgent = this.provider === "tess" && !this.agentId;
        this.page = (this.apiKey && !needsAgent) ? "chat" : "setup";
        this.render();
    }

    Visual.prototype.t = function(key) {
        var dict = I18N[this.lang] || I18N.es;
        return dict[key] || I18N.es[key] || key;
    };

    Visual.prototype.clearContainer = function() {
        while (this.container.firstChild) {
            this.container.removeChild(this.container.firstChild);
        }
    };

    Visual.prototype.render = function() {
        this.clearContainer();
        if (this.page === "setup") {
            this.renderSetup();
        } else {
            this.renderChat();
        }
    };

    Visual.prototype.getProviderConfig = function() {
        for (var i = 0; i < PROVIDERS.length; i++) {
            if (PROVIDERS[i].id === this.provider) return PROVIDERS[i];
        }
        return PROVIDERS[0];
    };

    Visual.prototype.renderSetup = function() {
        var self = this;
        var wrap = document.createElement("div");
        wrap.className = "module-setup";

        // ── Header ──
        var hdr = document.createElement("div");
        hdr.className = "module-header";

        var hdrLeft = document.createElement("div");
        hdrLeft.className = "module-header-left";

        var badge = document.createElement("span");
        badge.className = "module-badge";
        badge.textContent = "T";

        var hdrInfo = document.createElement("div");
        var titleEl = document.createElement("div");
        titleEl.className = "module-title";
        titleEl.textContent = this.t("mod1Title");
        var subtitleEl = document.createElement("div");
        subtitleEl.className = "module-subtitle";
        subtitleEl.textContent = this.t("mod1Subtitle");
        hdrInfo.appendChild(titleEl);
        hdrInfo.appendChild(subtitleEl);

        hdrLeft.appendChild(badge);
        hdrLeft.appendChild(hdrInfo);

        var langWrap = document.createElement("div");
        langWrap.className = "lang-wrap";
        var langLbl = document.createElement("label");
        langLbl.className = "lang-label";
        langLbl.textContent = this.t("langLabel");
        var langSel = document.createElement("select");
        langSel.className = "lang-select-setup";
        [["es", "🇪🇸 ES"], ["en", "🇺🇸 EN"], ["pt", "🇧🇷 PT"]].forEach(function(pair) {
            var opt = document.createElement("option");
            opt.value = pair[0];
            opt.textContent = pair[1];
            if (pair[0] === self.lang) opt.selected = true;
            langSel.appendChild(opt);
        });
        langSel.addEventListener("change", function() {
            self.lang = langSel.value;
            try { localStorage.setItem("pbiviz_aiChat_lang", self.lang); } catch(e) {}
            self.render();
        });
        langWrap.appendChild(langLbl);
        langWrap.appendChild(langSel);

        hdr.appendChild(hdrLeft);
        hdr.appendChild(langWrap);
        wrap.appendChild(hdr);

        // ── Provider picker ──
        var provStep = document.createElement("div");
        provStep.className = "setup-step";
        var provLbl = document.createElement("div");
        provLbl.className = "field-label";
        provLbl.textContent = this.t("providerLabel");
        var provGrid = document.createElement("div");
        provGrid.className = "provider-grid";

        var currentProviderId = this.provider;
        PROVIDERS.forEach(function(p) {
            var btn = document.createElement("div");
            btn.className = "provider-btn" + (p.id === currentProviderId ? " active" : "");
            btn.dataset.id = p.id;
            var ico = document.createElement("span");
            ico.className = "provider-icon";
            ico.textContent = p.icon;
            var lbl = document.createElement("span");
            lbl.className = "provider-label";
            lbl.textContent = p.label;
            btn.appendChild(ico);
            btn.appendChild(lbl);
            provGrid.appendChild(btn);
        });

        provStep.appendChild(provLbl);
        provStep.appendChild(provGrid);
        wrap.appendChild(provStep);

        // ── Dynamic area for steps ──
        var dynArea = document.createElement("div");
        dynArea.className = "dynamic-area";
        wrap.appendChild(dynArea);

        // ── Error div ──
        var errDiv = document.createElement("div");
        errDiv.className = "setup-error";
        errDiv.style.display = "none";
        wrap.appendChild(errDiv);

        // ── Next button ──
        var nextBtn = document.createElement("button");
        nextBtn.className = "next-btn";
        nextBtn.textContent = this.t("nextBtn");
        wrap.appendChild(nextBtn);

        this.container.appendChild(wrap);

        // State vars
        var stateProxy = this.proxyUrl;
        var stateKey = "";
        var stateModel = "";
        var stateAgentId = this.agentId;

        function renderDynamic() {
            while (dynArea.firstChild) dynArea.removeChild(dynArea.firstChild);

            var prov = null;
            for (var i = 0; i < PROVIDERS.length; i++) {
                if (PROVIDERS[i].id === currentProviderId) { prov = PROVIDERS[i]; break; }
            }
            if (!prov) return;

            // ── Step 1: Proxy ──
            var s1 = document.createElement("div");
            s1.className = "setup-step";

            var s1hdr = document.createElement("div");
            s1hdr.className = "step-header";
            var s1num = document.createElement("span");
            s1num.className = "step-num";
            s1num.textContent = "1";
            var s1ttl = document.createElement("span");
            s1ttl.className = "step-title";
            s1ttl.textContent = self.t("step1Title");
            s1hdr.appendChild(s1num);
            s1hdr.appendChild(s1ttl);

            var s1desc = document.createElement("div");
            s1desc.className = "step-desc";
            s1desc.textContent = self.t("step1Desc");

            var s1cmd = document.createElement("div");
            s1cmd.className = "cmd-box";
            var cmdText = self.t("step1Cmd")
                .replace("PROVEEDOR", prov.id)
                .replace("PROVIDER", prov.id)
                .replace("PROVEDOR", prov.id);
            s1cmd.textContent = cmdText;

            var noteEl;
            if (prov.id === "tess") {
                noteEl = document.createElement("div");
                noteEl.className = "tess-note";
                noteEl.textContent = self.t("tessProxyNote");
            } else {
                noteEl = document.createElement("div");
                noteEl.className = "step-note";
                noteEl.textContent = self.t(prov.proxyNote);
            }

            var urlLbl = document.createElement("label");
            urlLbl.className = "field-label";
            urlLbl.textContent = self.t(prov.urlLabel);
            var urlInp = document.createElement("input");
            urlInp.type = "text";
            urlInp.className = "field-input";
            urlInp.placeholder = prov.urlPlaceholder;
            urlInp.value = stateProxy;
            urlInp.addEventListener("input", function() { stateProxy = urlInp.value.trim(); });

            s1.appendChild(s1hdr);
            if (prov.id !== "azure") {
                s1.appendChild(s1desc);
                s1.appendChild(s1cmd);
            }
            s1.appendChild(noteEl);
            s1.appendChild(urlLbl);
            s1.appendChild(urlInp);
            dynArea.appendChild(s1);

            // ── Step 2: Key + Model ──
            var s2 = document.createElement("div");
            s2.className = "setup-step";

            var s2hdr = document.createElement("div");
            s2hdr.className = "step-header";
            var s2num = document.createElement("span");
            s2num.className = "step-num";
            s2num.textContent = "2";
            var s2ttl = document.createElement("span");
            s2ttl.className = "step-title";
            s2ttl.textContent = self.t("step2Title");
            s2hdr.appendChild(s2num);
            s2hdr.appendChild(s2ttl);

            var s2desc = document.createElement("div");
            s2desc.className = "step-desc";
            s2desc.textContent = self.t("step2Desc");

            var keyLbl = document.createElement("label");
            keyLbl.className = "field-label";
            keyLbl.textContent = self.t(prov.keyLabel);
            var keyInp = document.createElement("input");
            keyInp.type = "password";
            keyInp.className = "field-input";
            keyInp.placeholder = prov.keyPlaceholder;
            keyInp.addEventListener("input", function() { stateKey = keyInp.value.trim(); });

            var modelLbl = document.createElement("label");
            modelLbl.className = "field-label";
            modelLbl.textContent = prov.modelLabel;

            s2.appendChild(s2hdr);
            s2.appendChild(s2desc);
            s2.appendChild(keyLbl);
            s2.appendChild(keyInp);
            s2.appendChild(modelLbl);

            if (prov.modelOptions.length > 0) {
                var modelSel = document.createElement("select");
                modelSel.className = "field-input";
                prov.modelOptions.forEach(function(m) {
                    var opt = document.createElement("option");
                    opt.value = m;
                    opt.textContent = m;
                    if (m === prov.modelDefault) opt.selected = true;
                    modelSel.appendChild(opt);
                });
                var customOpt = document.createElement("option");
                customOpt.value = "__custom__";
                customOpt.textContent = "✏ Personalizado...";
                modelSel.appendChild(customOpt);

                var customWrap = document.createElement("div");
                customWrap.style.display = "none";
                var customLbl = document.createElement("label");
                customLbl.className = "field-label";
                customLbl.textContent = self.t("modelCustomLabel");
                var customInp = document.createElement("input");
                customInp.type = "text";
                customInp.className = "field-input";
                customInp.placeholder = self.t("modelCustomPlaceholder");
                customWrap.appendChild(customLbl);
                customWrap.appendChild(customInp);

                stateModel = prov.modelDefault;
                modelSel.addEventListener("change", function() {
                    if (modelSel.value === "__custom__") {
                        customWrap.style.display = "block";
                        stateModel = customInp.value.trim();
                    } else {
                        customWrap.style.display = "none";
                        stateModel = modelSel.value;
                    }
                });
                customInp.addEventListener("input", function() { stateModel = customInp.value.trim(); });

                s2.appendChild(modelSel);
                s2.appendChild(customWrap);
            } else {
                var depInp = document.createElement("input");
                depInp.type = "text";
                depInp.className = "field-input";
                depInp.placeholder = "my-gpt4-deployment";
                depInp.addEventListener("input", function() { stateModel = depInp.value.trim(); });
                stateModel = "";
                s2.appendChild(depInp);
            }

            dynArea.appendChild(s2);

            // ── Step 3: TESS Agent selector ──
            if (prov.hasDynamicAgents) {
                var s3 = document.createElement("div");
                s3.className = "setup-step";

                var s3hdr = document.createElement("div");
                s3hdr.className = "step-header";
                var s3num = document.createElement("span");
                s3num.className = "step-num";
                s3num.textContent = "3";
                var s3ttl = document.createElement("span");
                s3ttl.className = "step-title";
                s3ttl.textContent = self.t("step3Title");
                s3hdr.appendChild(s3num);
                s3hdr.appendChild(s3ttl);

                var agentLbl = document.createElement("label");
                agentLbl.className = "field-label";
                agentLbl.textContent = self.t("agentLabel");

                var agentRow = document.createElement("div");
                agentRow.style.display = "flex";
                agentRow.style.gap = "6px";
                agentRow.style.alignItems = "center";

                var loadBtn = document.createElement("button");
                loadBtn.className = "load-agents-btn";
                loadBtn.textContent = self.t("loadAgentsBtn");

                var spinnerEl = document.createElement("span");
                spinnerEl.className = "agent-spinner";
                spinnerEl.style.display = "none";
                spinnerEl.textContent = "⏳";

                agentRow.appendChild(loadBtn);
                agentRow.appendChild(spinnerEl);

                var agentSelWrap = document.createElement("div");
                agentSelWrap.style.display = "none";

                var agentSel = document.createElement("select");
                agentSel.className = "field-input";
                var placeholderOpt = document.createElement("option");
                placeholderOpt.value = "";
                placeholderOpt.textContent = self.t("agentSelectPlaceholder");
                agentSel.appendChild(placeholderOpt);
                stateAgentId = "";
                agentSel.addEventListener("change", function() {
                    stateAgentId = agentSel.value;
                });
                agentSelWrap.appendChild(agentSel);

                var agentErrEl = document.createElement("div");
                agentErrEl.className = "setup-error";
                agentErrEl.style.display = "none";

                loadBtn.addEventListener("click", function() {
                    var proxyBase = (stateProxy || "").replace(/\/$/, "");
                    if (proxyBase && !proxyBase.startsWith("http")) {
                        agentErrEl.textContent = self.t("errUrl");
                        agentErrEl.style.display = "block";
                        return;
                    }
                    agentErrEl.style.display = "none";
                    loadBtn.disabled = true;
                    spinnerEl.style.display = "inline";

                    var agentsUrl = proxyBase ? proxyBase + "/agents" : "https://api.tess.im/agents";
                    var agentsFetchOpts = proxyBase
                        ? {}
                        : { headers: { "Authorization": "Bearer " + stateKey } };

                    fetch(agentsUrl, agentsFetchOpts)
                        .then(function(r) {
                            if (!r.ok) throw new Error("HTTP " + r.status);
                            return r.json();
                        })
                        .then(function(data) {
                            spinnerEl.style.display = "none";
                            loadBtn.disabled = false;

                            // Clear existing options except placeholder
                            while (agentSel.options.length > 1) {
                                agentSel.remove(1);
                            }

                            var agents = Array.isArray(data) ? data : (data.data || data.agents || []);
                            agents.forEach(function(agent) {
                                var opt = document.createElement("option");
                                opt.value = agent.id;
                                opt.textContent = agent.name || ("Agent " + agent.id);
                                agentSel.appendChild(opt);
                            });

                            agentSelWrap.style.display = "block";
                        })
                        .catch(function(err) {
                            spinnerEl.style.display = "none";
                            loadBtn.disabled = false;
                            agentErrEl.textContent = self.t("agentLoadError") + " (" + err.message + ")";
                            agentErrEl.style.display = "block";
                        });
                });

                s3.appendChild(s3hdr);
                s3.appendChild(agentLbl);
                s3.appendChild(agentRow);
                s3.appendChild(agentSelWrap);
                s3.appendChild(agentErrEl);
                dynArea.appendChild(s3);
            }
        }

        renderDynamic();

        // Provider switch
        provGrid.addEventListener("click", function(evt) {
            var btn = evt.target.closest(".provider-btn");
            if (!btn) return;
            currentProviderId = btn.dataset.id;
            provGrid.querySelectorAll(".provider-btn").forEach(function(b) {
                b.classList.remove("active");
            });
            btn.classList.add("active");
            stateProxy = "";
            stateKey = "";
            stateModel = "";
            stateAgentId = "";
            renderDynamic();
        });

        // Next button validation + save
        nextBtn.addEventListener("click", function() {
            errDiv.style.display = "none";

            var prov = null;
            for (var i = 0; i < PROVIDERS.length; i++) {
                if (PROVIDERS[i].id === currentProviderId) { prov = PROVIDERS[i]; break; }
            }

            if (prov.urlRequired && (!stateProxy || !stateProxy.startsWith("http"))) {
                errDiv.textContent = self.t("errUrl");
                errDiv.style.display = "block";
                return;
            }
            if (stateProxy && !stateProxy.startsWith("http")) {
                errDiv.textContent = self.t("errUrl");
                errDiv.style.display = "block";
                return;
            }
            if (!stateKey) {
                errDiv.textContent = self.t("errKey");
                errDiv.style.display = "block";
                return;
            }
            if (currentProviderId === "azure" && !stateModel) {
                errDiv.textContent = self.t("errModel");
                errDiv.style.display = "block";
                return;
            }
            if (prov.hasDynamicAgents && !stateAgentId) {
                errDiv.textContent = self.t("errAgent");
                errDiv.style.display = "block";
                return;
            }

            self.provider = currentProviderId;
            self.apiKey = stateKey;
            self.proxyUrl = stateProxy;
            self.model = stateModel || prov.modelDefault;
            self.agentId = stateAgentId;

            try {
                localStorage.setItem("pbiviz_aiChat_apiKey", self.apiKey);
                localStorage.setItem("pbiviz_aiChat_proxyUrl", self.proxyUrl);
                localStorage.setItem("pbiviz_aiChat_lang", self.lang);
                localStorage.setItem("pbiviz_aiChat_provider", self.provider);
                localStorage.setItem("pbiviz_aiChat_model", self.model);
                if (self.agentId) localStorage.setItem("pbiviz_tess_agentId", self.agentId);
            } catch(e) {}

            self.messages = [{ role: "assistant", content: self.t("welcomeMsg") }];
            self.page = "chat";
            self.render();
        });
    };

    Visual.prototype.renderChat = function() {
        var self = this;
        var prov = this.getProviderConfig();

        var chatWrap = document.createElement("div");
        chatWrap.className = "module-chat";

        // ── Chat header ──
        var chatHdr = document.createElement("div");
        chatHdr.className = "chat-header";

        var hdrLeft = document.createElement("div");
        hdrLeft.className = "chat-header-left";
        var dot = document.createElement("div");
        dot.className = "header-dot";
        var chatTitle = document.createElement("span");
        chatTitle.className = "chat-title";
        chatTitle.textContent = this.t("mod2Title");
        var pill = document.createElement("span");
        pill.className = "provider-pill";
        pill.textContent = prov.icon + " " + prov.label.split(" ")[0];
        hdrLeft.appendChild(dot);
        hdrLeft.appendChild(chatTitle);
        hdrLeft.appendChild(pill);

        var hdrRight = document.createElement("div");
        hdrRight.className = "chat-header-right";

        var langSelChat = document.createElement("select");
        langSelChat.className = "lang-select-chat";
        [["es", "🇪🇸"], ["en", "🇺🇸"], ["pt", "🇧🇷"]].forEach(function(pair) {
            var opt = document.createElement("option");
            opt.value = pair[0];
            opt.textContent = pair[1];
            if (pair[0] === self.lang) opt.selected = true;
            langSelChat.appendChild(opt);
        });
        langSelChat.addEventListener("change", function() {
            self.lang = langSelChat.value;
            try { localStorage.setItem("pbiviz_aiChat_lang", self.lang); } catch(e) {}
            if (self.textarea) self.textarea.placeholder = self.t("placeholder");
            if (self.contextValuesEl) self.contextValuesEl.textContent = self.buildContextParts() || self.t("noContext");
        });

        var clearBtn = document.createElement("button");
        clearBtn.className = "hdr-btn";
        clearBtn.textContent = this.t("clearBtn");
        clearBtn.addEventListener("click", function() {
            self.messages = [{ role: "assistant", content: self.t("clearedMsg") }];
            self.renderMessages();
        });

        var cfgBtn = document.createElement("button");
        cfgBtn.className = "hdr-btn hdr-btn-outline";
        cfgBtn.textContent = this.t("configBtn");
        cfgBtn.addEventListener("click", function() {
            self.apiKey = "";
            self.proxyUrl = "";
            try {
                localStorage.removeItem("pbiviz_aiChat_apiKey");
                localStorage.removeItem("pbiviz_aiChat_proxyUrl");
            } catch(e) {}
            self.page = "setup";
            self.render();
        });

        hdrRight.appendChild(langSelChat);
        hdrRight.appendChild(clearBtn);
        hdrRight.appendChild(cfgBtn);

        chatHdr.appendChild(hdrLeft);
        chatHdr.appendChild(hdrRight);
        chatWrap.appendChild(chatHdr);

        // ── Messages area ──
        var msgArea = document.createElement("div");
        msgArea.className = "chat-messages";
        this.messagesContainer = msgArea;
        chatWrap.appendChild(msgArea);

        // ── Context bar ──
        var ctxBar = document.createElement("div");
        ctxBar.className = "ctx-bar";
        var ctxLbl = document.createElement("span");
        ctxLbl.className = "ctx-label";
        ctxLbl.textContent = this.t("contextLabel");
        var ctxVals = document.createElement("span");
        ctxVals.className = "ctx-values";
        ctxVals.textContent = this.buildContextParts() || this.t("noContext");
        this.contextValuesEl = ctxVals;
        ctxBar.appendChild(ctxLbl);
        ctxBar.appendChild(ctxVals);
        chatWrap.appendChild(ctxBar);

        // ── Input area ──
        var inputArea = document.createElement("div");
        inputArea.className = "chat-input-area";
        var ta = document.createElement("textarea");
        ta.rows = 1;
        ta.placeholder = this.t("placeholder");
        ta.className = "chat-textarea";
        this.textarea = ta;
        var sendBtn = document.createElement("button");
        sendBtn.className = "send-btn";
        sendBtn.textContent = "➤";
        this.sendBtn = sendBtn;

        ta.addEventListener("keydown", function(evt) {
            if (evt.key === "Enter" && !evt.shiftKey) {
                evt.preventDefault();
                self.sendMessage();
            }
        });
        ta.addEventListener("input", function() {
            ta.style.height = "auto";
            ta.style.height = Math.min(ta.scrollHeight, 80) + "px";
        });
        sendBtn.addEventListener("click", function() { self.sendMessage(); });

        inputArea.appendChild(ta);
        inputArea.appendChild(sendBtn);
        chatWrap.appendChild(inputArea);

        this.container.appendChild(chatWrap);
        this.renderMessages();
    };

    Visual.prototype.buildContextParts = function() {
        var parts = [];
        if (this.context.measures.length > 0) {
            parts.push("📊 " + this.context.measures.map(function(m) { return m.name + ": " + m.value; }).join(" · "));
        }
        for (var i = 0; i < this.context.categories.length; i++) {
            parts.push("🏷 " + this.context.categories[i].name + " (" + this.context.categories[i].values.length + ")");
        }
        for (var j = 0; j < this.context.dates.length; j++) {
            parts.push("📅 " + this.context.dates[j].name + " (" + this.context.dates[j].values.length + ")");
        }
        return parts.join("  ");
    };

    Visual.prototype.renderMessages = function() {
        if (!this.messagesContainer) return;
        while (this.messagesContainer.firstChild) {
            this.messagesContainer.removeChild(this.messagesContainer.firstChild);
        }
        var self = this;
        this.messages.forEach(function(msg) {
            var el = document.createElement("div");
            el.className = "message " + msg.role;
            if (msg.role === "thinking") {
                el.appendChild(document.createTextNode(self.t("thinkingMsg") + " "));
                var dots = document.createElement("span");
                dots.className = "dots";
                dots.textContent = "...";
                el.appendChild(dots);
            } else {
                el.textContent = msg.content;
            }
            self.messagesContainer.appendChild(el);
        });
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    };

    Visual.prototype.buildSystemPrompt = function() {
        var parts = [];
        if (this.context.measures.length > 0) {
            parts.push("📊 " + this.context.measures.map(function(m) { return m.name + ": " + m.value; }).join(" | "));
        }
        for (var i = 0; i < this.context.categories.length; i++) {
            parts.push("🏷 " + this.context.categories[i].name + ": " + this.context.categories[i].values.slice(0, 50).join(", "));
        }
        for (var j = 0; j < this.context.dates.length; j++) {
            parts.push("📅 " + this.context.dates[j].name + ": " + this.context.dates[j].values.slice(0, 50).join(", "));
        }
        var ctx = parts.join("\n");
        var base = this.t("systemPrompt");
        if (ctx) {
            return base + "\n\n" + this.t("ctxHeader") + "\n" + ctx + "\n\n" + this.t("ctxBase");
        }
        return base + "\n\n" + this.t("noCtxMsg");
    };

    // ── callAPI dispatcher ─────────────────────────────────────
    Visual.prototype.callAPI = function(messages) {
        var systemPrompt = this.buildSystemPrompt();
        if (this.provider === "tess")      return this.callTess(messages, systemPrompt);
        if (this.provider === "anthropic") return this.callAnthropic(messages, systemPrompt);
        if (this.provider === "openai")    return this.callOpenAI(messages, systemPrompt, false);
        if (this.provider === "gemini")    return this.callGemini(messages, systemPrompt);
        if (this.provider === "azure")     return this.callOpenAI(messages, systemPrompt, true);
        return Promise.reject(new Error("Unknown provider"));
    };

    // ── TESS ──────────────────────────────────────────────────
    Visual.prototype.callTess = function(messages, systemPrompt) {
        var self = this;
        var agentId = this.agentId || localStorage.getItem("pbiviz_tess_agentId");
        var proxyBase = (this.proxyUrl || "").replace(/\/$/, "");

        // Build messages: inject system prompt into first user message
        var builtMessages = messages.map(function(m, idx) {
            if (idx === 0 && m.role === "user") {
                return { role: "user", content: systemPrompt + "\n\n---\n" + m.content };
            }
            return { role: m.role, content: m.content };
        });

        var body = JSON.stringify({
            model: self.model || "tess-5",
            temperature: "1",
            messages: builtMessages,
            tools: "no-tools",
            wait_execution: true
        });

        var tessEndpoint = proxyBase
            ? proxyBase + "/agents/" + agentId + "/execute?wait_execution=true"
            : "https://api.tess.im/agents/" + agentId + "/execute?wait_execution=true";
        var tessHeaders = proxyBase
            ? { "Content-Type": "application/json" }
            : { "Content-Type": "application/json", "Authorization": "Bearer " + self.apiKey };

        return fetch(tessEndpoint, {
            method: "POST",
            headers: tessHeaders,
            body: body
        }).then(function(r) {
            if (!r.ok) {
                return r.json().catch(function() { return {}; }).then(function(err) {
                    throw new Error((err && err.error && err.error.message) || ("Erro " + r.status));
                });
            }
            return r.json();
        }).then(function(data) {
            var firstResponse = data && data.responses && data.responses[0];
            if (!firstResponse) throw new Error("Resposta inválida da TESS");
            if (firstResponse.status === "succeeded") return firstResponse.output || "";
            if (firstResponse.id) return self.pollTessResponse(proxyBase, firstResponse.id, 0, self.apiKey);
            throw new Error("Status inesperado: " + firstResponse.status);
        });
    };

    Visual.prototype.pollTessResponse = function(proxyBase, responseId, attempt, apiKey) {
        var self = this;
        var maxAttempts = 30;
        var intervalMs = 2000;
        var currentAttempt = attempt || 0;

        if (currentAttempt >= maxAttempts) {
            return Promise.reject(new Error("Timeout aguardando resposta da TESS"));
        }

        var pollUrl = proxyBase
            ? proxyBase + "/agent-responses/" + responseId
            : "https://api.tess.im/agent-responses/" + responseId;
        var pollHeaders = proxyBase
            ? { "Content-Type": "application/json" }
            : { "Content-Type": "application/json", "Authorization": "Bearer " + (apiKey || self.apiKey) };

        return new Promise(function(resolve) {
            setTimeout(resolve, intervalMs);
        }).then(function() {
            return fetch(pollUrl, { headers: pollHeaders });
        }).then(function(res) {
            if (!res.ok) throw new Error("Polling falhou: " + res.status);
            return res.json();
        }).then(function(data) {
            var r = (data && data.responses && data.responses[0]) || data;
            if (r.status === "succeeded") return r.output || "";
            if (r.status === "failed") throw new Error("TESS retornou erro no processamento");
            return self.pollTessResponse(proxyBase, responseId, currentAttempt + 1, apiKey);
        });
    };

    // ── Anthropic ─────────────────────────────────────────────
    Visual.prototype.callAnthropic = function(messages, systemPrompt) {
        var self = this;
        var endpoint = this.proxyUrl
            ? this.proxyUrl.replace(/\/$/, "") + "/v1/messages"
            : "https://api.anthropic.com/v1/messages";

        var headers = { "Content-Type": "application/json", "x-api-key": self.apiKey, "anthropic-version": "2023-06-01" };
        if (!self.proxyUrl) headers["anthropic-dangerous-direct-browser-access"] = "true";

        return fetch(endpoint, {
            method: "POST",
            headers: headers,
            body: JSON.stringify({ model: self.model, max_tokens: 1000, system: systemPrompt, messages: messages })
        }).then(function(r) {
            if (!r.ok) return r.json().catch(function() { return {}; }).then(function(e) { throw new Error((e && e.error && e.error.message) || ("Error " + r.status)); });
            return r.json();
        }).then(function(d) { return (d && d.content && d.content[0] && d.content[0].text) || ""; });
    };

    // ── OpenAI / Azure ────────────────────────────────────────
    Visual.prototype.callOpenAI = function(messages, systemPrompt, isAzure) {
        var self = this;
        var msgs = [{ role: "system", content: systemPrompt }].concat(messages);
        var headers = { "Content-Type": "application/json" };
        var endpoint;

        if (self.proxyUrl) {
            endpoint = self.proxyUrl.replace(/\/$/, "") + "/v1/chat/completions";
            headers["Authorization"] = "Bearer " + self.apiKey;
        } else if (isAzure) {
            endpoint = self.proxyUrl + "/openai/deployments/" + self.model + "/chat/completions?api-version=2024-02-01";
            headers["api-key"] = self.apiKey;
        } else {
            endpoint = "https://api.openai.com/v1/chat/completions";
            headers["Authorization"] = "Bearer " + self.apiKey;
        }

        var bodyObj = { messages: msgs, max_tokens: 1000 };
        if (!isAzure) bodyObj.model = self.model;

        return fetch(endpoint, {
            method: "POST",
            headers: headers,
            body: JSON.stringify(bodyObj)
        }).then(function(r) {
            if (!r.ok) return r.json().catch(function() { return {}; }).then(function(e) { throw new Error((e && e.error && e.error.message) || ("Error " + r.status)); });
            return r.json();
        }).then(function(d) { return (d && d.choices && d.choices[0] && d.choices[0].message && d.choices[0].message.content) || ""; });
    };

    // ── Gemini ────────────────────────────────────────────────
    Visual.prototype.callGemini = function(messages, systemPrompt) {
        var self = this;
        if (self.proxyUrl) return self.callOpenAI(messages, systemPrompt, false);

        var endpoint = "https://generativelanguage.googleapis.com/v1beta/models/" + self.model + ":generateContent?key=" + self.apiKey;
        var contents = messages.map(function(m) {
            return { role: m.role === "assistant" ? "model" : "user", parts: [{ text: m.content }] };
        });

        return fetch(endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                system_instruction: { parts: [{ text: systemPrompt }] },
                contents: contents,
                generationConfig: { maxOutputTokens: 1000 }
            })
        }).then(function(r) {
            if (!r.ok) return r.json().catch(function() { return {}; }).then(function(e) { throw new Error((e && e.error && e.error.message) || ("Error " + r.status)); });
            return r.json();
        }).then(function(d) { return (d && d.candidates && d.candidates[0] && d.candidates[0].content && d.candidates[0].content.parts && d.candidates[0].content.parts[0] && d.candidates[0].content.parts[0].text) || ""; });
    };

    // ── Send message ──────────────────────────────────────────
    Visual.prototype.sendMessage = function() {
        var self = this;
        if (!this.textarea || this.isLoading) return;
        var text = this.textarea.value.trim();
        if (!text) return;

        this.textarea.value = "";
        this.textarea.style.height = "auto";
        this.messages.push({ role: "user", content: text });
        this.messages.push({ role: "thinking", content: "" });
        this.renderMessages();
        this.isLoading = true;
        if (this.sendBtn) this.sendBtn.disabled = true;

        var apiMessages = this.messages
            .filter(function(m) { return m.role === "user" || m.role === "assistant"; })
            .map(function(m) { return { role: m.role, content: m.content }; });

        this.callAPI(apiMessages).then(function(reply) {
            self.messages = self.messages.filter(function(m) { return m.role !== "thinking"; });
            self.messages.push({ role: "assistant", content: reply });
        }).catch(function(err) {
            self.messages = self.messages.filter(function(m) { return m.role !== "thinking"; });
            self.messages.push({ role: "error", content: "Erro: " + (err && err.message ? err.message : "Não foi possível conectar") });
        }).then(function() {
            self.isLoading = false;
            if (self.sendBtn) self.sendBtn.disabled = false;
            self.renderMessages();
            if (self.textarea) self.textarea.focus();
        });
    };

    // ── Power BI data update ───────────────────────────────────
    Visual.prototype.update = function(options) {
        var dvs = options.dataViews;
        this.context = { measures: [], categories: [], dates: [] };
        if (dvs && dvs.length > 0) {
            var dv = dvs[0];
            if (dv.categorical) {
                var cat = dv.categorical;
                if (cat.categories) {
                    for (var i = 0; i < cat.categories.length; i++) {
                        var c = cat.categories[i];
                        var roles = c.source.roles || {};
                        var vals = Array.from(new Set(
                            (c.values || []).map(function(v) { return v != null ? String(v) : ""; }).filter(function(v) { return v !== ""; })
                        )).slice(0, 200);
                        if (roles.date) {
                            this.context.dates.push({ name: c.source.displayName, values: vals });
                        } else {
                            this.context.categories.push({ name: c.source.displayName, values: vals });
                        }
                    }
                }
                if (cat.values) {
                    for (var j = 0; j < cat.values.length; j++) {
                        var v = cat.values[j];
                        if (v.source.isMeasure) {
                            var nums = (v.values || []).filter(function(x) { return x != null; });
                            var avg = nums.length > 0
                                ? (nums.reduce(function(a, b) { return a + b; }, 0) / nums.length).toLocaleString("es-CO", { maximumFractionDigits: 2 })
                                : "N/A";
                            this.context.measures.push({ name: v.source.displayName, value: avg });
                        }
                    }
                }
            }
        }
        if (this.contextValuesEl) {
            this.contextValuesEl.textContent = this.buildContextParts() || this.t("noContext");
        }
    };

    Visual.prototype.destroy = function() {};

    // ── Plugin registration ───────────────────────────────────
    var _exports = {};
    (function() {
        var pbiviz = window.powerbi;
        var pluginDef = {
            name: "PowerIATESS1F2A3B4C5D6E7F8A",
            displayName: "Power IA TESS",
            class: "Visual",
            apiVersion: "5.3.0",
            create: function(options) { return new Visual(options); },
            custom: true
        };
        if (typeof pbiviz !== "undefined") {
            pbiviz.visuals = pbiviz.visuals || {};
            pbiviz.visuals.plugins = pbiviz.visuals.plugins || {};
            pbiviz.visuals.plugins["PowerIATESS1F2A3B4C5D6E7F8A"] = pluginDef;
        }
        _exports.default = pluginDef;
    })();

    PowerIATESS1F2A3B4C5D6E7F8A = _exports;
})();
"""

# ─────────────────────────────────────────────────────────────
# Capabilities
# ─────────────────────────────────────────────────────────────
CAPABILITIES = {
    "dataRoles": [
        {
            "name": "measure",
            "kind": "Measure",
            "displayName": "Medidas DAX",
            "description": "Agrega tus medidas calculadas (GoldRate, TotalGold, etc.)"
        },
        {
            "name": "category",
            "kind": "Grouping",
            "displayName": "Dimensiones (País, Categoría...)",
            "description": "Columnas de texto o categorías como Country, Medal Type"
        },
        {
            "name": "date",
            "kind": "Grouping",
            "displayName": "Fechas / Períodos",
            "description": "Columnas de fecha, año o década"
        }
    ],
    "dataViewMappings": [
        {
            "conditions": [
                {"measure": {"max": 20}, "category": {"max": 10}, "date": {"max": 5}}
            ],
            "categorical": {
                "categories": {
                    "select": [
                        {"bind": {"to": "category"}},
                        {"bind": {"to": "date"}}
                    ],
                    "dataReductionAlgorithm": {"top": {"count": 200}}
                },
                "values": {
                    "select": [
                        {"bind": {"to": "measure"}}
                    ]
                }
            }
        }
    ],
    "privileges": [
        {
            "name": "WebAccess",
            "essential": True,
            "parameters": [
                "http://localhost:3100",
                "https://api.tess.im",
                "https://api.anthropic.com",
                "https://api.openai.com",
                "https://generativelanguage.googleapis.com"
            ]
        }
    ],
    "supportsMultiVisualSelection": True
}

# ─────────────────────────────────────────────────────────────
# Icon (same as original — small placeholder PNG)
# ─────────────────────────────────────────────────────────────
ICON_BASE64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAA2RpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMC1jMDYwIDYxLjEzNDc3NywgMjAxMC8wMi8xMi0xNzozMjowMCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0UmVmPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VSZWYjIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDpBOEJGMzkxN0NBRDNFMDExQTcxQ0JFODI3ODBCQUE5RSIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDo3NEY1QjA1NUQ0OTAxMUUwQTgxREI2NjMxMkNEMUNEMyIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDo3NEY1QjA1NEQ0OTAxMUUwQTgxREI2NjMxMkNEMUNEMyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgQ1M1IFdpbmRvd3MiPiA8eG1wTU06RGVyaXZlZEZyb20gc3RSZWY6aW5zdGFuY2VJRD0ieG1wLmlpZDo5Mjk5RDU1ODBGRDRFMDExQTcxQ0JFODI3ODBCQUE5RSIgc3RSZWY6ZG9jdW1lbnRJRD0ieG1wLmRpZDpBOEJGMzkxN0NBRDNFMDExQTcxQ0JFODI3ODBCQUE5RSIvPiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0YT4gPD94cGFja2V0IGVuZD0iciI/PpDoNX0AAAI3SURBVHjarJRLSFVRFIY9t7SiRDGLoEEPCRJRaCSYkxCiFCXCF+LIMExQLkilgumgwkbdBuWDRC2EomhURCOjgagkXEgKLUKhidobM6H0+i34rxyPnuvEA5/rXPda/1l7739vJxKJxG3ls93+hEKhTILxJhgMftmsiPxdhHw4CfepeR8dCyjWwwB0kZy3iVgCoQ2ewnmXxhrBD7Cgr/ZQVA17fDRPw2UYhzK6G99IsBse6/0QNME+H8FT4EA/YiPqOgA1q4IMzBNuw6iKjkCpj+Av+AdnEEmD3bxfhzvuDk30HaEaLsEkXCO53rN+Bwg5qsvTuj/TjGYtx9nINhRmEx7AYWiFW7AXOuEcbPOUvIZ2mnrl+PkQUbNEh4QHNKUSDdsSBWEOlmxTEfvs26FL9Khe211if6Acgee+xo7xzMgBxfq9qPe3fgWBGN2lEnqtG9nExM7CV3jp3bDos2bKJB0nHFRxAxRpA/5CIXyHh5ABv6GZqd9dJ6iz2SjbxMMypGhJFtTlNzu3kK7xgDxpove8U66FK2A+s6nul5gVVMEL+Ak7lG/T+g9JcIOGar2CRUoogxMwpP/bLTJMB9bRhDbkk5bBUU0y3ES0xS04CBfN9RSHiY90vJK0BHaSzG9h2eejS3RJeVfdtrGzuGyd8CX7Yq6ExuCH63jaVMPkFOv6OibB6DKs2+VEQp+WYBoqERn2sVWWRNN0YurIfeL14U6YkpkLYCSG6e0yqdCxvKBLIm5FgAEAV0nKuwMYRUsAAAAASUVORK5CYII="

# ─────────────────────────────────────────────────────────────
# Build the pbiviz.json content
# ─────────────────────────────────────────────────────────────
def build_pbiviz_json():
    visual_meta = {
        "name": GUID,
        "displayName": DISPLAY_NAME,
        "guid": GUID,
        "visualClassName": VISUAL_CLASS,
        "version": VERSION,
        "description": "Chatbox con TESS AI para analizar medidas DAX en Power BI",
        "supportUrl": "https://tess.im",
        "gitHubUrl": ""
    }

    pbiviz = {
        "visual": visual_meta,
        "author": {"name": "Power IA TESS", "email": "admin@example.com"},
        "apiVersion": API_VERSION,
        "style": "style/visual.less",
        "stringResources": {},
        "capabilities": CAPABILITIES,
        "content": {
            "js": JS,
            "css": CSS,
            "iconBase64": ICON_BASE64
        },
        "visualEntryPoint": "",
        "externalJS": [],
        "assets": {"icon": "assets/icon.png"}
    }

    return json.dumps(pbiviz, ensure_ascii=False, separators=(',', ':'))


# ─────────────────────────────────────────────────────────────
# Build package.json
# ─────────────────────────────────────────────────────────────
def build_package_json():
    resource_file = f"resources/{GUID}.pbiviz.json"
    pkg = {
        "version": VERSION,
        "author": {"name": "Power IA TESS", "email": "admin@example.com"},
        "resources": [
            {
                "resourceId": "rId0",
                "sourceType": 5,
                "file": resource_file
            }
        ],
        "visual": {
            "name": GUID,
            "displayName": DISPLAY_NAME,
            "guid": GUID,
            "visualClassName": VISUAL_CLASS,
            "version": VERSION,
            "description": "Chatbox con TESS AI para analizar medidas DAX en Power BI",
            "supportUrl": "https://tess.im",
            "gitHubUrl": ""
        },
        "metadata": {
            "pbivizjson": {
                "resourceId": "rId0"
            }
        }
    }
    return json.dumps(pkg, indent="\t", ensure_ascii=False)


# ─────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────
def main():
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "Power_IA_TESS.pbiviz")

    pbiviz_json_content = build_pbiviz_json()
    package_json_content = build_package_json()

    resource_name = f"resources/{GUID}.pbiviz.json"

    print(f"Building {output_path}...")
    print(f"  JS length   : {len(JS):,} chars")
    print(f"  CSS length  : {len(CSS):,} chars")
    print(f"  pbiviz.json : {len(pbiviz_json_content):,} bytes")

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("package.json", package_json_content)
        zf.writestr(resource_name, pbiviz_json_content)

    size = os.path.getsize(output_path)
    print(f"  Output size : {size:,} bytes")
    print(f"\nDone! -> {output_path}")

    # Verify
    print("\nVerifying ZIP contents:")
    with zipfile.ZipFile(output_path, "r") as zf:
        for info in zf.infolist():
            print(f"  {info.filename}  ({info.file_size:,} bytes uncompressed)")


if __name__ == "__main__":
    main()
