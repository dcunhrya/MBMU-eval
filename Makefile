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

CONDA_CMD := $(shell command -v mamba >/dev/null 2>&1 && echo mamba || echo conda)
CONDABASE ?= $(shell conda info --base 2>/dev/null)

define ACTIVATE
source "$(CONDABASE)/etc/profile.d/conda.sh" && conda activate $(1) && $(2)
endef

# --------- Git deps (editable installs) ----------
# VLMEvalKit pinned to a specific commit, installed editable

.PHONY: all flamingo llava mbmu huatuo1 moe clean help git-deps git-vlmevalkit # git-llava

all: flamingo llava mbmu huatuo1 moe

# ---------- Git deps ----------
submodules:
	git submodule update --init --recursive

# --------- Targets ------------
# flamingo:
# 	@echo "Setting up flamingo environment..."
# 	$(CONDA_CMD) env create -f $(ENV_DIR)/flamingo.yml || $(CONDA_CMD) env update -f $(ENV_DIR)/flamingo.yml
# 	source $$(conda info --base)/etc/profile.d/conda.sh && \
# 		conda activate flamingo && \
# 		pip install uv && \
# 		uv pip install --no-deps -r $(REQ_DIR)/flamingo.txt
# 	@echo "flamingo environment ready!"

flamingo: submodules
	@echo "Setting up flamingo environment..."
	$(CONDA_CMD) env create -f $(ENV_DIR)/flamingo.yml || $(CONDA_CMD) env update -f $(ENV_DIR)/flamingo.yml
	@$(call ACTIVATE,flamingo,pip install -q uv && uv pip install --no-deps -r $(REQ_DIR)/flamingo.txt)
	@$(call ACTIVATE,flamingo,pip install -e ./VLMEvalKit)
	@echo "flamingo environment ready!"

llava: submodules
	@echo "Setting up llava environment..."
	$(CONDA_CMD) env create -f $(ENV_DIR)/llava.yml || $(CONDA_CMD) env update -f $(ENV_DIR)/llava.yml
	$(CONDA_CMD) env create -f $(ENV_DIR)/llava.yml || $(CONDA_CMD) env update -f $(ENV_DIR)/llava.yml
	@$(call ACTIVATE,llava,pip install -e ./VLMEvalKit)
	@$(call ACTIVATE,llava,pip install -e ./LLaVA)
	@$(call ACTIVATE,llava,pip install -e ./LLavaMed)
	@echo "llava environment ready!"

mbmu: submodules
	@echo "Setting up mbmu environment..."
	$(CONDA_CMD) env create -f $(ENV_DIR)/mbmu.yml || $(CONDA_CMD) env update -f $(ENV_DIR)/mbmu.yml
	$(CONDA_CMD) env create -f $(ENV_DIR)/mbmu.yml || $(CONDA_CMD) env update -f $(ENV_DIR)/mbmu.yml
	@$(call ACTIVATE,mbmu,pip install -e ./VLMEvalKit)
	@echo "mbmu environment ready!"

# huatuo1:
# 	@echo "Setting up huatuo1 environment..."
# 	$(CONDA_CMD) env create -f $(ENV_DIR)/huatuo1.yml || $(CONDA_CMD) env update -f $(ENV_DIR)/huatuo1.yml
# 	source $$(conda info --base)/etc/profile.d/conda.sh && \
# 		conda activate huatuo1 && \
# 		pip install uv && \
# 		uv pip install --no-deps -r $(REQ_DIR)/huatuo1.txt
# 	@echo "huatuo1 environment ready!"

huatuo1: submodules
	@echo "Setting up huatuo1 environment..."
	$(CONDA_CMD) env create -f $(ENV_DIR)/huatuo1.yml || $(CONDA_CMD) env update -f $(ENV_DIR)/huatuo1.yml
	@$(call ACTIVATE,huatuo1,pip install -q uv && uv pip install --no-deps -r $(REQ_DIR)/huatuo1.txt)
	@$(call ACTIVATE,huatuo1,pip install -e ./VLMEvalKit)
	@echo "huatuo1 environment ready!"

moe: submodules
	@echo "Setting up moe environment..."
	$(CONDA_CMD) env create -f $(ENV_DIR)/moe.yml || $(CONDA_CMD) env update -f $(ENV_DIR)/moe.yml
	@$(call ACTIVATE,moe,pip install -q uv && uv pip install --no-deps -r $(REQ_DIR)/moe.txt)
	@$(call ACTIVATE,moe,pip install -e ./VLMEvalKit)
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