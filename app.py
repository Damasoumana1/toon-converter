import json
import streamlit as st
import os
import re

# =============================
# Configuration de la page
# =============================
st.set_page_config(
    page_title="JSON ↔ TOON Converter Pro",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================
# CSS personnalisé
# =============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Outfit:wght@400;500;600;700&display=swap');

:root {
    --primary: #7c3aed;
    --primary-light: #a78bfa;
    --success: #10b981;
    --warning: #f59e0b;
    --bg-dark: #0c0a1d;
    --bg-card: #1a1730;
    --bg-input: #0f0d1f;
    --text: #f1f5f9;
    --text-dim: #94a3b8;
    --border: #2e2850;
    --glow: rgba(124, 58, 237, 0.4);
}

.stApp {
    background: linear-gradient(135deg, var(--bg-dark) 0%, #1a1035 50%, #0d1a2d 100%);
}

.main-header {
    background: linear-gradient(135deg, #7c3aed 0%, #a855f7 50%, #ec4899 100%);
    padding: 2.5rem 2rem;
    border-radius: 20px;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: 0 15px 50px rgba(124, 58, 237, 0.4);
    position: relative;
    overflow: hidden;
}

.main-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 50%);
    animation: shimmer 3s ease-in-out infinite;
}

@keyframes shimmer {
    0%, 100% { transform: rotate(0deg); }
    50% { transform: rotate(180deg); }
}

.main-header h1 {
    color: white !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    margin: 0 !important;
    text-shadow: 0 2px 20px rgba(0,0,0,0.3);
    position: relative;
}

.main-header p {
    color: rgba(255,255,255,0.9) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.1rem !important;
    margin-top: 0.5rem !important;
    position: relative;
}

.stTextArea textarea, .stTextInput input {
    background: var(--bg-input) !important;
    border: 2px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.9rem !important;
    padding: 1rem !important;
}

.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px var(--glow) !important;
}

.stButton > button {
    background: linear-gradient(135deg, var(--primary) 0%, #9333ea 100%) !important;
    border: none !important;
    color: white !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.75rem 2rem !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 20px var(--glow) !important;
    transition: all 0.2s ease !important;
    width: 100%;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px var(--glow) !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card) !important;
    border-radius: 15px !important;
    padding: 0.5rem !important;
    gap: 0.5rem !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-dim) !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 500 !important;
    border-radius: 10px !important;
    padding: 0.75rem 1.5rem !important;
}

.stTabs [aria-selected="true"] {
    background: var(--primary) !important;
    color: white !important;
}

.stat-box {
    background: linear-gradient(135deg, var(--bg-card) 0%, #1e1845 100%);
    border: 1px solid var(--border);
    border-radius: 15px;
    padding: 1.5rem;
    margin: 1rem 0;
}

.stat-box.success {
    border-color: var(--success);
    box-shadow: 0 0 20px rgba(16, 185, 129, 0.2);
}

.result-box {
    background: linear-gradient(180deg, var(--bg-input) 0%, #0a0815 100%);
    border: 2px solid var(--success);
    border-radius: 12px;
    padding: 1rem;
    font-family: 'JetBrains Mono', monospace;
    color: var(--success);
}

.footer {
    text-align: center;
    padding: 1.5rem;
    color: var(--text-dim);
    font-family: 'Outfit', sans-serif;
    font-size: 0.9rem;
    border-top: 1px solid var(--border);
    margin-top: 3rem;
}

h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {
    font-family: 'Outfit', sans-serif !important;
}

code, pre {
    font-family: 'JetBrains Mono', monospace !important;
}

/* File uploader */
.stFileUploader {
    background: var(--bg-card) !important;
    border: 2px dashed var(--border) !important;
    border-radius: 15px !important;
    padding: 1rem !important;
}

.stFileUploader:hover {
    border-color: var(--primary) !important;
}

/* Metrics */
.stMetric {
    background: var(--bg-card) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}
</style>
""", unsafe_allow_html=True)

# =============================
#   JSON → TOON
# =============================
def flatten_to_toon(obj):
    """Aplati l'objet en TOON"""
    if isinstance(obj, dict):
        inner = ";".join([f"{k}:{flatten_to_toon(v)}" for k, v in obj.items()])
        return f"({inner})"
    elif isinstance(obj, list):
        inner = ",".join([flatten_to_toon(x) for x in obj])
        return f"[{inner}]"
    else:
        return str(obj)


# =============================
#   TOON → JSON (parseur inverse)
# =============================
def _split_top_level(s: str, sep: str):
    """Split s by sep but ignore separators inside (...) or [...] blocks."""
    parts = []
    buf = []
    depth = 0
    for ch in s:
        if ch in "([":
            depth += 1
            buf.append(ch)
        elif ch in ")]":
            depth = max(0, depth - 1)
            buf.append(ch)
        elif ch == sep and depth == 0:
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    parts.append("".join(buf))
    return parts


def _parse_toon_value(s: str):
    s = s.strip()
    if not s:
        return None
    if s.startswith("(") and s.endswith(")"):
        inner = s[1:-1]
        obj = {}
        pairs = _split_top_level(inner, ";")
        for p in pairs:
            if not p or ":" not in p:
                continue
            k, v = p.split(":", 1)
            obj[k.strip()] = _parse_toon_value(v)
        return obj
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1]
        items = _split_top_level(inner, ",")
        return [_parse_toon_value(x) for x in items if x != ""]
    try:
        return json.loads(s)
    except:
        return s


def toon_to_json_obj(text: str):
    """Parse TOON string back to Python object."""
    text = text.strip()
    if (text.startswith("(") and text.endswith(")")) or (text.startswith("[") and text.endswith("]")):
        return _parse_toon_value(text)
    obj = {}
    pairs = _split_top_level(text, ";")
    for p in pairs:
        if not p or ":" not in p:
            continue
        k, v = p.split(":", 1)
        obj[k.strip()] = _parse_toon_value(v)
    return obj


# =============================
# Comptage de tokens
# =============================
try:
    import tiktoken
    enc = tiktoken.get_encoding("cl100k_base")
    TIKTOKEN = True
except:
    TIKTOKEN = False


def count_tokens(s: str):
    if TIKTOKEN:
        return len(enc.encode(s))
    return max(1, len(s) // 4)


# =============================
# Analyse structure JSON
# =============================
def analyze_json_structure(obj):
    """Analyse récursive de la structure JSON."""
    stats = {"objects": 0, "arrays": 0, "strings": 0, "numbers": 0, "booleans": 0, "nulls": 0, "max_depth": 0}
    
    def _analyze(o, depth=0):
        stats["max_depth"] = max(stats["max_depth"], depth)
        if isinstance(o, dict):
            stats["objects"] += 1
            for v in o.values():
                _analyze(v, depth + 1)
        elif isinstance(o, list):
            stats["arrays"] += 1
            for item in o:
                _analyze(item, depth + 1)
        elif isinstance(o, str):
            stats["strings"] += 1
        elif isinstance(o, bool):
            stats["booleans"] += 1
        elif isinstance(o, (int, float)):
            stats["numbers"] += 1
        elif o is None:
            stats["nulls"] += 1
    
    _analyze(obj)
    return stats


# =============================
# Header
# =============================
st.markdown("""
<div class="main-header">
    <h1>🔄 JSON ↔ TOON Converter Pro</h1>
    <p>Optimisez vos tokens LLM avec le format compact TOON</p>
</div>
""", unsafe_allow_html=True)

# =============================
# Tabs
# =============================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📝 JSON → TOON", 
    "🔄 TOON → JSON", 
    "📁 Fichiers",
    "📊 Analyse Dataset",
    "🧠 Analyse Smart"
])

# =============================
# Tab 1: JSON → TOON
# =============================
with tab1:
    st.markdown("### Convertissez votre JSON en format TOON compact")
    
    col1, col2 = st.columns(2)
    
    with col1:
        json_input = st.text_area(
            "📄 Entrée JSON",
            height=300,
            placeholder='{\n  "name": "exemple",\n  "data": [1, 2, 3]\n}'
        )
        convert_btn = st.button("🚀 Convertir en TOON", key="convert_json", use_container_width=True)
    
    with col2:
        if convert_btn and json_input:
            try:
                data = json.loads(json_input)
                toon_text = flatten_to_toon(data)
                
                json_tokens = count_tokens(json_input)
                toon_tokens = count_tokens(toon_text)
                gain = round((1 - toon_tokens / json_tokens) * 100, 2) if json_tokens > 0 else 0
                
                st.text_area("🎯 Résultat TOON", value=toon_text, height=200)
                
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                with col_stat1:
                    st.metric("JSON", f"{json_tokens:,} tokens")
                with col_stat2:
                    st.metric("TOON", f"{toon_tokens:,} tokens")
                with col_stat3:
                    st.metric("Gain", f"{gain}%", delta=f"-{json_tokens - toon_tokens} tokens")
                    
            except json.JSONDecodeError as e:
                st.error(f"❌ Erreur JSON: {e}")
        elif convert_btn:
            st.warning("⚠️ Veuillez entrer du JSON")

# =============================
# Tab 2: TOON → JSON
# =============================
with tab2:
    st.markdown("### Reconvertissez votre TOON en JSON")
    
    col1, col2 = st.columns(2)
    
    with col1:
        toon_input = st.text_area(
            "🎯 Entrée TOON",
            height=300,
            placeholder="(name:exemple;data:[1,2,3])"
        )
        parse_btn = st.button("🔍 Parser en JSON", key="parse_toon", use_container_width=True)
    
    with col2:
        if parse_btn and toon_input:
            try:
                obj = toon_to_json_obj(toon_input)
                json_result = json.dumps(obj, indent=2, ensure_ascii=False)
                st.text_area("📄 Résultat JSON", value=json_result, height=300)
            except Exception as e:
                st.error(f"❌ Erreur: {e}")
        elif parse_btn:
            st.warning("⚠️ Veuillez entrer du TOON")

# =============================
# Tab 3: Fichiers
# =============================
with tab3:
    st.markdown("### Convertissez des fichiers JSON/TXT en TOON")
    
    # Trois méthodes d'import
    method = st.radio(
        "📥 Méthode d'import",
        ["📂 Chemin du fichier (RECOMMANDÉ)", "📋 Coller le contenu JSON", "📎 Uploader un fichier"],
        horizontal=True
    )
    
    content = None
    file_name = "output"
    
    if method == "📂 Chemin du fichier (RECOMMANDÉ)":
        st.markdown("**Entrez le chemin complet du fichier sur votre PC :**")
        file_path = st.text_input(
            "Chemin du fichier",
            placeholder=r"C:\Users\USER\Desktop\toon_project\test3.txt",
            label_visibility="collapsed"
        )
        
        if file_path and file_path.strip():
            file_path = file_path.strip().strip('"').strip("'")
            
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8-sig') as f:
                        content = f.read()
                    content = content.strip()
                    file_name = os.path.basename(file_path)
                    st.success(f"✅ Fichier lu: {file_name} ({len(content):,} caractères)")
                    
                    with st.expander("👀 Aperçu", expanded=False):
                        st.code(content[:2000] + ("..." if len(content) > 2000 else ""), language="json")
                        
                except Exception as e:
                    st.error(f"❌ Erreur de lecture: {e}")
            else:
                st.error(f"❌ Fichier introuvable: {file_path}")
    
    elif method == "📋 Coller le contenu JSON":
        st.markdown("**Copiez-collez votre JSON ci-dessous :**")
        pasted_content = st.text_area(
            "Contenu JSON",
            height=300,
            placeholder='{\n  "exemple": "collez votre JSON ici",\n  "data": [1, 2, 3]\n}',
            label_visibility="collapsed"
        )
        if pasted_content and pasted_content.strip():
            content = pasted_content.strip()
            st.info(f"📄 {len(content):,} caractères chargés")
    
    elif method == "📎 Uploader un fichier":
        uploaded_file = st.file_uploader(
            "📎 Charger un fichier JSON ou TXT",
            type=["json", "txt"],
            help="Glissez-déposez ou cliquez pour charger"
        )
        
        if uploaded_file is not None:
            try:
                # Méthode 1: getvalue()
                raw_bytes = uploaded_file.getvalue()
                
                # Debug info
                st.info(f"📊 Debug: {len(raw_bytes)} bytes reçus, nom: {uploaded_file.name}, type: {uploaded_file.type}")
                
                if len(raw_bytes) == 0:
                    st.warning("⚠️ Le fichier semble vide. Essayez la méthode 'Coller le contenu JSON' ci-dessus.")
                else:
                    # Décoder
                    for encoding in ['utf-8-sig', 'utf-8', 'latin-1', 'cp1252']:
                        try:
                            content = raw_bytes.decode(encoding)
                            break
                        except:
                            continue
                    
                    if content is None:
                        content = raw_bytes.decode('utf-8', errors='replace')
                    
                    # Nettoyage
                    content = content.lstrip('\ufeff\ufffe').strip()
                    file_name = uploaded_file.name
                    
                    st.success(f"✅ Fichier chargé: {file_name} ({len(content):,} caractères)")
                    
                    with st.expander("👀 Aperçu", expanded=False):
                        st.code(content[:2000] + ("..." if len(content) > 2000 else ""), language="json")
                        
            except Exception as e:
                st.error(f"❌ Erreur: {e}")
    
    # Bouton de conversion
    st.markdown("---")
    
    if content and len(content) > 0:
        if st.button("🚀 Convertir en TOON", key="convert_file", use_container_width=True, type="primary"):
            # Parser JSON ou JSONL
            data = None
            error_msg = None
            
            try:
                data = json.loads(content)
            except json.JSONDecodeError as e:
                error_msg = str(e)
                # Essayer JSONL
                lines = [l for l in content.splitlines() if l.strip()]
                items = []
                for ln in lines:
                    try:
                        items.append(json.loads(ln))
                    except:
                        break
                if len(items) == len(lines) and items:
                    data = items
                    error_msg = None
            
            if data is None:
                st.error(f"❌ Format JSON invalide")
                if error_msg:
                    st.code(f"Erreur: {error_msg}", language="text")
                with st.expander("🔍 Debug - Contenu brut"):
                    st.code(repr(content[:500]), language="text")
            else:
                toon_text = flatten_to_toon(data)
                
                # Stats
                json_tokens = count_tokens(content)
                toon_tokens = count_tokens(toon_text)
                json_chars = len(content)
                toon_chars = len(toon_text)
                gain = round((1 - toon_tokens / json_tokens) * 100, 2) if json_tokens > 0 else 0
                char_gain = round((1 - toon_chars / json_chars) * 100, 2) if json_chars > 0 else 0
                
                # Résultats dans un container stylé
                st.markdown("---")
                st.markdown("## ✅ Conversion Réussie!")
                
                # Métriques en grand
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("📝 JSON", f"{json_tokens:,}", help="Tokens dans le JSON original")
                with col2:
                    st.metric("🎯 TOON", f"{toon_tokens:,}", help="Tokens dans le format TOON")
                with col3:
                    st.metric("💰 Gain Tokens", f"{gain}%", delta=f"-{json_tokens - toon_tokens:,}")
                with col4:
                    st.metric("📉 Gain Chars", f"{char_gain}%", delta=f"-{json_chars - toon_chars:,}")
                
                st.markdown("---")
                
                # Résultat TOON dans une zone bien visible
                st.markdown("### 🎯 Résultat TOON")
                st.code(toon_text[:5000] + ("..." if len(toon_text) > 5000 else ""), language="text")
                
                # Téléchargement bien visible
                st.markdown("### 💾 Téléchargement")
                base_name = os.path.splitext(file_name)[0]
                col_dl1, col_dl2 = st.columns([2, 1])
                with col_dl1:
                    st.download_button(
                        label="⬇️ Télécharger le fichier TOON",
                        data=toon_text,
                        file_name=f"{base_name}.toon.txt",
                        mime="text/plain",
                        use_container_width=True,
                        type="primary"
                    )
                with col_dl2:
                    st.info(f"📄 {base_name}.toon.txt")
    else:
        st.info("👆 Chargez ou collez du contenu JSON pour commencer")

# =============================
# Tab 4: Analyse Dataset
# =============================
with tab4:
    st.markdown("### Analysez le gain sur un dataset complet")
    
    col1, col2 = st.columns(2)
    
    with col1:
        dataset_input = st.text_area(
            "📋 Dataset (JSON/JSONL)",
            height=350,
            placeholder='{"item": 1}\n{"item": 2}\n{"item": 3}'
        )
        analyze_btn = st.button("📈 Analyser le dataset", key="analyze_dataset", use_container_width=True)
    
    with col2:
        if analyze_btn and dataset_input:
            data = None
            try:
                data = json.loads(dataset_input)
            except:
                lines = [l for l in dataset_input.splitlines() if l.strip()]
                items = []
                for ln in lines:
                    try:
                        items.append(json.loads(ln))
                    except:
                        pass
                if items:
                    data = items
            
            if not data:
                st.error("❌ Dataset invalide")
            else:
                if isinstance(data, dict):
                    data = [data]
                
                json_total = toon_total = 0
                for item in data:
                    j = json.dumps(item)
                    t = flatten_to_toon(item)
                    json_total += count_tokens(j)
                    toon_total += count_tokens(t)
                
                gain = round((1 - toon_total / json_total) * 100, 2) if json_total > 0 else 0
                
                st.markdown("### 📊 Résultats d'analyse")
                
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    st.metric("📦 Éléments", f"{len(data):,}")
                    st.metric("📝 Tokens JSON", f"{json_total:,}")
                with col_m2:
                    st.metric("🎯 Tokens TOON", f"{toon_total:,}")
                    st.metric("💰 Gain total", f"{gain}%", delta=f"-{json_total - toon_total:,} tokens")
        elif analyze_btn:
            st.warning("⚠️ Veuillez coller un dataset")

# =============================
# Tab 5: Analyse Smart
# =============================
with tab5:
    st.markdown("### 🧠 Analyse Smart - Comprendre votre conversion")
    
    st.info("""
    **Rôle de l'Analyse Smart :**
    - 📊 **Analyse la structure** de votre JSON (objets, tableaux, profondeur)
    - 💰 **Calcule les économies** en tokens et caractères
    - 🔍 **Identifie les optimisations** possibles
    - ⚠️ **Détecte les pertes potentielles** (caractères spéciaux, types convertis)
    
    Utile pour comprendre **pourquoi** le gain est bon ou faible sur votre JSON.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        smart_json = st.text_area(
            "📄 JSON à analyser",
            height=250,
            placeholder='{"example": "data", "nested": {"key": "value"}}'
        )
        smart_toon = st.text_area(
            "🎯 TOON (optionnel)",
            height=80,
            placeholder="Laissez vide pour auto-générer"
        )
        smart_btn = st.button("⚡ Analyser en détail", key="smart_analyze", use_container_width=True)
    
    with col2:
        if smart_btn and smart_json:
            try:
                data = json.loads(smart_json)
                
                if not smart_toon or not smart_toon.strip():
                    toon_text = flatten_to_toon(data)
                else:
                    toon_text = smart_toon
                
                # Statistiques
                json_len = len(smart_json)
                toon_len = len(toon_text)
                json_tokens = count_tokens(smart_json)
                toon_tokens = count_tokens(toon_text)
                
                # Analyse structure
                struct = analyze_json_structure(data)
                
                # Calculs
                char_gain = round((1 - toon_len / json_len) * 100, 2) if json_len > 0 else 0
                token_gain = round((1 - toon_tokens / json_tokens) * 100, 2) if json_tokens > 0 else 0
                
                # Comptage des caractères économisés
                json_braces = smart_json.count("{") + smart_json.count("}")
                json_brackets = smart_json.count("[") + smart_json.count("]")
                json_quotes = smart_json.count('"')
                json_commas = smart_json.count(",")
                
                st.markdown("---")
                st.markdown("## 🔍 Résultats de l'Analyse")
                
                # Métriques principales en 4 colonnes
                col_a, col_b, col_c, col_d = st.columns(4)
                with col_a:
                    st.metric("📊 Gain Caractères", f"{char_gain}%")
                with col_b:
                    st.metric("🎯 Gain Tokens", f"{token_gain}%")
                with col_c:
                    st.metric("📝 JSON", f"{json_tokens:,} tok")
                with col_d:
                    st.metric("✨ TOON", f"{toon_tokens:,} tok")
                
                st.markdown("---")
                
                # Structure dans un expander
                with st.expander("🏗️ Structure JSON détaillée", expanded=True):
                    col_s1, col_s2, col_s3 = st.columns(3)
                    with col_s1:
                        st.metric("📦 Objets", struct['objects'])
                        st.metric("📋 Tableaux", struct['arrays'])
                    with col_s2:
                        st.metric("📝 Strings", struct['strings'])
                        st.metric("🔢 Nombres", struct['numbers'])
                    with col_s3:
                        st.metric("✓ Booléens", struct['booleans'])
                        st.metric("📐 Profondeur", struct['max_depth'])
                
                # Économies et Évaluation côte à côte
                col_eco, col_eval = st.columns(2)
                
                with col_eco:
                    with st.expander("🗑️ Caractères économisés", expanded=True):
                        total_saved = json_braces + json_brackets + json_quotes + (json_commas // 2)
                        st.metric("Total économisé", f"~{total_saved} chars")
                        st.caption(f"Accolades: {json_braces} | Crochets: {json_brackets}")
                        st.caption(f"Guillemets: {json_quotes} | Virgules: ~{json_commas // 2}")
                
                with col_eval:
                    with st.expander("💡 Évaluation qualité", expanded=True):
                        if token_gain >= 30:
                            st.success("🌟 Excellent gain (>30%)")
                            st.progress(1.0)
                        elif token_gain >= 20:
                            st.success("✅ Bon gain (20-30%)")
                            st.progress(0.75)
                        elif token_gain >= 10:
                            st.info("📊 Gain modéré (10-20%)")
                            st.progress(0.5)
                        else:
                            st.warning("⚠️ Gain limité (<10%)")
                            st.progress(0.25)
                        
                        # Pertes potentielles
                        special_chars = re.findall(r'[;:\[\]\(\)]', json.dumps(data))
                        if special_chars:
                            st.warning(f"⚠️ {len(special_chars)} caractères spéciaux")
                
            except json.JSONDecodeError as e:
                st.error(f"❌ JSON invalide: {e}")
        elif smart_btn:
            st.warning("⚠️ Veuillez entrer du JSON")

# =============================
# Footer
# =============================
st.markdown("""
<div class="footer">
    TOON Converter Pro • Optimisez vos prompts LLM • Compatible Hugging Face Spaces 🤗
</div>
""", unsafe_allow_html=True)
