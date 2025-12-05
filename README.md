---
title: Toon Converter
emoji: 🔄
colorFrom: purple
colorTo: pink
sdk: streamlit
sdk_version: 1.28.0
app_file: app.py
pinned: false
---

# 🔄 TOON Converter Pro

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/Dama12/toon-converter)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Optimize your LLM tokens with the compact TOON format**

TOON Converter Pro is a tool that converts JSON data into a compact format called "TOON", significantly reducing the number of tokens used during interactions with LLMs (GPT-4, Claude, etc.).

## 🎯 What is TOON?

TOON is a compact serialization format that:
- Replaces curly braces `{}` with parentheses `()`
- Uses `;` as the key-value pair separator
- Uses `:` to separate key and value
- Removes quotes around keys and simple values

### Example

**JSON (47 tokens):**
```json
{"name": "John", "age": 30, "skills": ["Python", "JavaScript"]}
```

**TOON (28 tokens):**
```
(name:John;age:30;skills:[Python,JavaScript])
```

**Gain: ~40% tokens saved!**

## 🚀 Features

- ✅ **JSON → TOON**: Instant conversion with statistics
- ✅ **TOON → JSON**: Reverse parsing to retrieve JSON
- ✅ **File Upload**: Convert JSON/TXT files
- ✅ **Dataset Analysis**: Calculate gain on collections
- ✅ **Smart Analysis**: Detailed evaluation of the structure

## 💻 Local Installation

```bash
# Clone the repo
git clone https://github.com/Damasoumana1/toon-converter.git
cd toon-converter

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## 🤗 Deployment on Hugging Face Spaces

1. Create a new Space on [Hugging Face](https://huggingface.co/new-space)
2. Select **Streamlit** as SDK
3. Upload the files:
   - `app.py`
   - `requirements.txt`
   - `README.md`
4. The Space will be automatically deployed!

## 📁 Project Structure

```
toon-converter/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md          # Documentation
```

## 🔧 Python API

You can also use the functions directly:

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

| Data Type | Average Gain |
|-----------------|------------|
| API responses | 35-45% |
| Configuration | 25-35% |
| Nested objects | 40-50% |
| Arrays | 30-40% |

## ⚠️ Limitations

- Values containing `;`, `:`, `(`, `)`, `[`, `]` may cause ambiguities
- Booleans and null are converted to text (`True`, `False`, `None`)
- Format optimized for reading by LLMs, not for permanent storage

## 👤 Author

**Dama Soumana**

- GitHub: [@Damasoumana1](https://github.com/Damasoumana1)
- Hugging Face: [@Dama12](https://huggingface.co/Dama12)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for more details.

---

<p align="center">
  Made with ❤️ for the LLM community
</p>
