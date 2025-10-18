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
VLM_REPO    ?= https://github.com/dcunhrya/VLMEvalKit.git
VLM_DIR     ?= external/VLMEvalKit
VLM_COMMIT  ?= 3ead64034525f09eab4e4ccbf2b5ec4dfa39eddb

LLAVA_REPO   ?= https://github.com/haotian-liu/LLaVA.git
LLAVA_DIR    ?= external/LLaVA
LLAVA_COMMIT ?= c121f0432da27facab705978f83c4ada465e46fd

.PHONY: all flamingo llava mbmu huatuo1 moe clean help git-deps git-vlmevalkit # git-llava

all: flamingo llava mbmu huatuo1 moe

# ---------- Git deps ----------
git-deps: git-vlmevalkit
	@echo "Git dependencies ready."

git-vlmevalkit:
	@mkdir -p external
	@if [ -d "$(VLM_DIR)/.git" ]; then \
	  echo "→ Updating $(VLM_DIR)"; \
	  git -C "$(VLM_DIR)" fetch --all --tags --prune; \
	else \
	  echo "→ Cloning $(VLM_REPO) into $(VLM_DIR)"; \
	  git clone "$(VLM_REPO)" "$(VLM_DIR)"; \
	fi
	@echo "→ Checking out $(VLM_COMMIT)"; \
	git -C "$(VLM_DIR)" checkout --quiet "$(VLM_COMMIT)"

git-llava:
	@mkdir -p external
	@if [ -d "$(LLAVA_DIR)/.git" ]; then \
	  echo "→ Updating $(LLAVA_DIR)"; \
	  git -C "$(LLAVA_DIR)" fetch --all --tags --prune; \
	else \
	  echo "→ Cloning $(LLAVA_REPO) into $(LLAVA_DIR)"; \
	  git clone "$(LLAVA_REPO)" "$(LLAVA_DIR)"; \
	fi
	@echo "→ Checking out $(LLAVA_COMMIT)"; \
	git -C "$(LLAVA_DIR)" checkout --quiet "$(LLAVA_COMMIT)"

# --------- Targets ------------
# flamingo:
# 	@echo "Setting up flamingo environment..."
# 	$(CONDA_CMD) env create -f $(ENV_DIR)/flamingo.yml || $(CONDA_CMD) env update -f $(ENV_DIR)/flamingo.yml
# 	source $$(conda info --base)/etc/profile.d/conda.sh && \
# 		conda activate flamingo && \
# 		pip install uv && \
# 		uv pip install --no-deps -r $(REQ_DIR)/flamingo.txt
# 	@echo "flamingo environment ready!"

flamingo:
	@echo "Setting up flamingo environment..."
	$(CONDA_CMD) env create -f $(ENV_DIR)/flamingo.yml || $(CONDA_CMD) env update -f $(ENV_DIR)/flamingo.yml
	@$(call ACTIVATE,flamingo,pip install -q uv && uv pip install --no-deps -r $(REQ_DIR)/flamingo.txt)
	@echo "flamingo environment ready!"

llava:
	@echo "Setting up llava environment..."
	$(CONDA_CMD) env create -f $(ENV_DIR)/llava.yml || $(CONDA_CMD) env update -f $(ENV_DIR)/llava.yml
	source $$(conda info --base)/etc/profile.d/conda.sh && \
		conda activate llava && \
		pip install uv && \
		uv pip install --no-deps -r $(REQ_DIR)/llava.txt
	@echo "llava environment ready!"

mbmu:
	@echo "Setting up mbmu environment..."
	$(CONDA_CMD) env create -f $(ENV_DIR)/mbmu.yml || $(CONDA_CMD) env update -f $(ENV_DIR)/mbmu.yml
	source $$(conda info --base)/etc/profile.d/conda.sh && \
		conda activate mbmu && \
		pip install uv && \
		uv pip install --no-deps -r $(REQ_DIR)/mbmu.txt
	@echo "mbmu environment ready!"

huatuo1:
	@echo "Setting up huatuo1 environment..."
	$(CONDA_CMD) env create -f $(ENV_DIR)/huatuo1.yml || $(CONDA_CMD) env update -f $(ENV_DIR)/huatuo1.yml
	source $$(conda info --base)/etc/profile.d/conda.sh && \
		conda activate huatuo1 && \
		pip install uv && \
		uv pip install --no-deps -r $(REQ_DIR)/huatuo1.txt
	@echo "huatuo1 environment ready!"

moe:
	@echo "Setting up moe environment..."
	$(CONDA_CMD) env create -f $(ENV_DIR)/moe.yml || $(CONDA_CMD) env update -f $(ENV_DIR)/moe.yml
	source $$(conda info --base)/etc/profile.d/conda.sh && \
		conda activate moe && \
		pip install uv && \
		uv pip install --no-deps -r $(REQ_DIR)/moe.txt
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