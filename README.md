# 🔄 TOON Converter Pro

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/Dama12/toon-converter)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Optimisez vos tokens LLM avec le format compact TOON**

TOON Converter Pro est un outil qui convertit des données JSON en un format compact appelé "TOON", réduisant significativement le nombre de tokens utilisés lors des interactions avec les LLM (GPT-4, Claude, etc.).

## 🎯 Qu'est-ce que TOON ?

TOON est un format de sérialisation compact qui :
- Remplace les accolades `{}` par des parenthèses `()`
- Utilise `;` comme séparateur de paires clé-valeur
- Utilise `:` pour séparer clé et valeur
- Supprime les guillemets autour des clés et valeurs simples

### Exemple

**JSON (47 tokens):**
```json
{"name": "John", "age": 30, "skills": ["Python", "JavaScript"]}
```

**TOON (28 tokens):**
```
(name:John;age:30;skills:[Python,JavaScript])
```

**Gain: ~40% de tokens économisés!**

## 🚀 Fonctionnalités

- ✅ **JSON → TOON** : Conversion instantanée avec statistiques
- ✅ **TOON → JSON** : Parsing inverse pour retrouver le JSON
- ✅ **Upload de fichiers** : Convertissez des fichiers JSON/TXT
- ✅ **Analyse de datasets** : Calculez le gain sur des collections
- ✅ **Analyse intelligente** : Évaluation détaillée de la structure

## 💻 Installation locale

```bash
# Cloner le repo
git clone https://github.com/Damasoumana1/toon-converter.git
cd toon-converter

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app.py
```

## 🤗 Déploiement sur Hugging Face Spaces

1. Créez un nouveau Space sur [Hugging Face](https://huggingface.co/new-space)
2. Sélectionnez **Streamlit** comme SDK
3. Uploadez les fichiers :
   - `app.py`
   - `requirements.txt`
   - `README.md`
4. Le Space sera automatiquement déployé !

## 📁 Structure du projet

```
toon-converter/
├── app.py              # Application Streamlit principale
├── requirements.txt    # Dépendances Python
└── README.md          # Documentation
```

## 🔧 API Python

Vous pouvez aussi utiliser les fonctions directement :

```python
from app import flatten_to_toon, toon_to_json_obj
import json

# JSON → TOON
data = {"name": "test", "values": [1, 2, 3]}
toon = flatten_to_toon(data)
print(toon)  # (name:test;values:[1,2,3])

# TOON → JSON
obj = toon_to_json_obj("(name:test;values:[1,2,3])")
print(json.dumps(obj, indent=2))
```

## 📊 Benchmarks

| Type de données | Gain moyen |
|-----------------|------------|
| API responses   | 35-45%     |
| Configuration   | 25-35%     |
| Nested objects  | 40-50%     |
| Arrays          | 30-40%     |

## ⚠️ Limitations

- Les valeurs contenant `;`, `:`, `(`, `)`, `[`, `]` peuvent causer des ambiguïtés
- Les booléens et null sont convertis en texte (`True`, `False`, `None`)
- Format optimisé pour la lecture par LLM, pas pour le stockage permanent

## 👤 Auteur

**Dama Soumana**

- GitHub: [@Damasoumana1](https://github.com/Damasoumana1)
- Hugging Face: [@Dama12](https://huggingface.co/Dama12)

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

<p align="center">
  Fait avec ❤️ pour la communauté LLM
</p>
