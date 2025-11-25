# 📊 Benchmarking JSON vs TOON vs VSC

A comparative study of three data formats across multiple LLMs

## 🚀 Overview

This repository contains a comprehensive benchmarking suite that evaluates how different data serialization formats — **JSON**, **TOON** (Token-Oriented Object Notation), and **VSC** (Value-Separated by Commas) — perform when used as input to Large Language Models (LLMs).

The benchmark measures each format across:

1. **Token count efficiency**
2. **Latency**
3. **Response quality**
4. **Model cost**
5. **Context utilization**

This helps developers understand how these formats impact real-world LLM usage, especially in tasks that involve structured data.

---

## ⚙️ Setup Instructions

This benchmarking tool uses **uv** for fast Python dependency management and a **virtual environment (venv)** for isolated development.

---

### 1. Install `uv`

`uv` is a modern Python package/dependency manager and virtual-env tool.

#### macOS / Linux

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Windows (Powershell)

```sh
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### Verify Installation

```sh
uv --version
```

### 2. Create & Activate a Python Virtual Environment

```sh
uv venv
```

This creates a .venv directory in your project.

#### Activate venv

#### macOS / Linux

```sh
source .venv/bin/activate
```

#### Windows (PowerShell)

```sh
.\.venv\Scripts\Activate.ps1
```

#### Windows (cmd)

```sh
.\.venv\Scripts\activate.bat
```

### 3. Install Project Dependencies

With the venv activated:

```sh
uv sync
```

### 4. Adding New Dependencies

This project uses pyproject.toml as the source of truth.

#### Add a new dependency

```sh
uv add package_name
```

Example:

```sh
uv add requests
```

#### Remove a dependency

```sh
uv remove package_name
```

`pyproject.toml` and the `lockfile` update automatically.

## 🔑 API Keys Setup (OpenAI & Google Gemini)

The app requires environment variables for API access.

### 5. Generate API Keys

#### OpenAI API Key

1. Visit: https://platform.openai.com/api-keys

2. Create a new API key.

3. Copy it (starts with sk-...).

#### Gemini API Key (Google AI Studio)

1. Visit: https://aistudio.google.com/app/apikey

2. Generate a new API key.

3. Copy it.

### 6. Add API Keys to Environment Variables

#### macOS / Linux

```sh
export OPENAI_API_KEY="your key"
```

```sh
export GEMINI_API_KEY="your key"
```

#### Windows (Powershell)

```sh
setx OPENAI_API_KEY "your_openai_key_here"
setx GEMINI_API_KEY "your_gemini_key_here"
```

### ▶️ 7. Run the App

```sh
python main.py
```
