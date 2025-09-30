#!/bin/bash
echo "I have not tested this.."
#if uv not found install astral-uv
if ! command -v uv &> /dev/null
then
    echo "uv could not be found, installing astral-uv..."
    curl -fsSL https://raw.githubusercontent.com/astral-sh/astral-uv/main/install.sh | bash
else
    echo "uv is already installed."
fi

#uv init venv
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    uv venv .venv -p 3.12 --prompt "lol" 
else
    echo "Virtual environment already exists."
fi

#activate venv
source .venv/bin/activate
#install requirements
uv pip install -r requirements.txt
