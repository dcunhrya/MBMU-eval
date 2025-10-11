# ================
#  Makefile for project environments
#  Usage:
#     make flamingo
#     make huatuo1
#     make mbmu
#     make moe
#     make llava
#     make all
# ================

# allow "conda activate" in non-interactive shell
SHELL := /bin/bash

# --------- Variables ----------
ENV_DIR := envs
REQ_DIR := requirements

# Default conda command (mamba is faster if available)
CONDA_CMD := $(shell command -v mamba >/dev/null 2>&1 && echo mamba || echo conda)

# --------- Targets ------------

.PHONY: all flamingo llava mbmu huatuo1 moe clean help

all: flamingo llava mbmu huatuo1 moe

flamingo:
	@echo "Setting up flamingo environment..."
	$(CONDA_CMD) env create -f $(ENV_DIR)/flamingo.yml || $(CONDA_CMD) env update -f $(ENV_DIR)/flamingo.yml
	source $$(conda info --base)/etc/profile.d/conda.sh && conda activate flamingo && uv pip install --system -r $(REQ_DIR)/flamingo.txt
	@echo "flamingo environment ready!"

llava:
	@echo "Setting up llava environment..."
	$(CONDA_CMD) env create -f $(ENV_DIR)/llava.yml || $(CONDA_CMD) env update -f $(ENV_DIR)/llava.yml
	source $$(conda info --base)/etc/profile.d/conda.sh && conda activate llava && uv pip install --system -r $(REQ_DIR)/llava.txt
	@echo "llava environment ready!"

mbmu:
	@echo "Setting up mbmu environment..."
	$(CONDA_CMD) env create -f $(ENV_DIR)/mbmu.yml || $(CONDA_CMD) env update -f $(ENV_DIR)/mbmu.yml
	source $$(conda info --base)/etc/profile.d/conda.sh && conda activate mbmu && uv pip install --system -r $(REQ_DIR)/mbmu.txt
	@echo "mbmu environment ready!"

huatuo1:
	@echo "Setting up huatuo1 environment..."
	$(CONDA_CMD) env create -f $(ENV_DIR)/huatuo1.yml || $(CONDA_CMD) env update -f $(ENV_DIR)/huatuo1.yml
	source $$(conda info --base)/etc/profile.d/conda.sh && conda activate huatuo1 && uv pip install --system -r $(REQ_DIR)/huatuo1.txt
	@echo "huatuo1 environment ready!"

moe:
	@echo "Setting up moe environment..."
	$(CONDA_CMD) env create -f $(ENV_DIR)/moe.yml || $(CONDA_CMD) env update -f $(ENV_DIR)/moe.yml
	source $$(conda info --base)/etc/profile.d/conda.sh && conda activate moe && uv pip install --system -r $(REQ_DIR)/moe.txt
	@echo "moe environment ready!"

# --------- Utilities -----------

clean:
	@echo "🧹 Removing all conda envs for this project..."
	-conda env remove -n huatuo1
	-conda env remove -n llava
	-conda env remove -n moe
	-conda env remove -n flamingo
	-conda env remove -n mbmu
	@echo "✅ All envs removed."

help:
	@echo "Makefile commands:"
	@echo "  make mbmu    # create/update the mbmu env"
	@echo "  make llava     # create/update the llava env"
	@echo "  make moe         # create/update the moe env"
	@echo "  make huatuo1         # create/update the huatuo1 env"
	@echo "  make flamingo         # create/update the flamingo env"
	@echo "  make all           # create/update all envs"
	@echo "  make clean         # remove all envs"