#!/usr/bin/env python3
"""Generate the complete skill-icons README.md with updated documentation,
showcases, aliases, and the full catalog of 920+ icons in a balanced 10-column table.
"""

import os
import glob
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HEADER = """<p align="center">
  <a href="https://skill-icons-go.vercel.app">
    <img src="./.github/text-logo.svg#gh-dark-mode-only" width="300" alt="Skill Icons Logo (Dark)" />
    <img src="./.github/text-logo-light.svg#gh-light-mode-only" width="300" alt="Skill Icons Logo (Light)" />
  </a>
</p>
<h3 align="center">Showcase your skills and tech stack on GitHub profiles and resumés with ease!</h3>
<p align="center">
  Ultra-fast, zero-dependency SVG icon cloud service written in Go.
</p>

<p align="center">
  <a href="https://skill-icons-go.vercel.app/api/icons?i=docker,kubernetes,golang"><img src="https://img.shields.io/badge/API-skill--icons--go.vercel.app-10b981?style=for-the-badge&logo=vercel&logoColor=white" alt="Live API" /></a>
  <a href="#icons-list"><img src="https://img.shields.io/badge/Icons-920%2B-6366f1?style=for-the-badge&logo=shieldsdotio&logoColor=white" alt="Icons Count" /></a>
  <a href="https://github.com/UMMAN2005/skill-icons/actions/workflows/build.yml"><img src="https://img.shields.io/github/actions/workflow/status/UMMAN2005/skill-icons/build.yml?branch=main&style=for-the-badge&label=Build" alt="Build Status" /></a>
  <a href="https://github.com/UMMAN2005/skill-icons/actions/workflows/security.yml"><img src="https://img.shields.io/github/actions/workflow/status/UMMAN2005/skill-icons/security.yml?branch=main&style=for-the-badge&label=Security" alt="Security Status" /></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="License" /></a>
</p>

<hr>

## 📑 Table of Contents

- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [⚙️ Query Parameters & Options](#️-query-parameters--options)
  - [Specifying Icons (`?i=`)](#specifying-icons-i)
  - [Theme Modes (`&theme=auto|dark|light`)](#theme-modes-themeautodarklight)
  - [Icons Per Line (`&perline=`)](#icons-per-line-perline)
  - [Interactive Tooltips (`&titles=true`)](#interactive-tooltips-titlestrue)
  - [Native Alignment (`&align=center|left|right`)](#native-alignment-aligncenterleftright)
- [🎨 Stack Showcases & Presets](#-stack-showcases--presets)
  - [Modern DevOps & Orchestration](#modern-devops--orchestration)
  - [DevSecOps & Supply Chain Security](#devsecops--supply-chain-security)
  - [Developer Tooling & Shell Environment](#developer-tooling--shell-environment)
  - [Infrastructure as Code & Config Formats](#infrastructure-as-code--config-formats)
  - [AI & Agentic Engineering](#ai--agentic-engineering)
- [🔀 Smart Aliases Reference](#-smart-aliases-reference)
- [📦 Self-Hosting & Local Development](#-self-hosting--local-development)
- [📋 Icons List (920+ Icons)](#icons-list)
- [💖 Support & Community](#-support--community)

---

## ✨ Features

- ⚡ **Ultra-Fast & Lightweight**: High-performance Go service powered by [Gin](https://github.com/gin-gonic/gin) for sub-millisecond responses and minimal memory footprint.
- 🌓 **Dynamic Theme Switching (`theme=auto`)**: By default, SVGs dynamically adjust to the viewer's GitHub or system theme (`prefers-color-scheme`) with adaptive dark and light mode styling.
- 🛡️ **DevOps & DevSecOps Focused**: First-class support for Semaphore UI, Docker Compose, Starship, Lefthook, Semgrep, Gitleaks, TruffleHog, Cosign, Uptime Kuma, and modern cloud ecosystems.
- 🏷️ **Accessible SVG Tooltips (`titles=true`)**: Embedded SVG `<title>` elements enable native mouse hover tooltips displaying the exact tool name.
- 🎯 **Native SVG Centering (`align=center`)**: Dynamic `viewBox` calculations center icon rows natively without fragile HTML wrappers.
- 🔀 **Rich Alias Engine**: Flexible shorthands like `compose`, `docker-compose`, `vs`, `semaphoreui`, `git-leaks`, `truffle-hog`, `left-hook`, `uv`, `ts`, and `go`.
- 🧩 **Zero Runtime Dependencies**: All vector assets are pre-compiled directly into Go bytecode.

---

## 🚀 Quick Start

Add your skills strip to your GitHub profile `README.md` or portfolio website in a single line:

```markdown
![My Skills](https://skill-icons-go.vercel.app/api/icons?i=docker,dockercompose,kubernetes,starship,semgrep,gitleaks,trufflehog,visualstudio)
```

**Live Preview:**

![My Skills](https://skill-icons-go.vercel.app/api/icons?i=docker,dockercompose,kubernetes,starship,semgrep,gitleaks,trufflehog,visualstudio)

---

## ⚙️ Query Parameters & Options

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `i` | `string` | *(Required)* | Comma-separated list of icon identifiers or aliases (or `all`). |
| `theme` | `string` | `auto` | Badge background theme: `auto`, `dark`, or `light`. |
| `perline` | `integer` | `15` | Maximum number of icons rendered per row (`1` to `50`). |
| `titles` | `boolean` | `false` | When set to `true`, embeds `<title>` hover tooltips with icon names. |
| `align` | `string` | `left` | Canvas alignment: `left`, `center`, or `right`. |

### Specifying Icons (`?i=`)

Specify a comma-separated list of tool names or aliases. You can explore all available icons in the [Icons List](#icons-list).

```markdown
![My Skills](https://skill-icons-go.vercel.app/api/icons?i=golang,rust,python,typescript,bash)
```

![My Skills](https://skill-icons-go.vercel.app/api/icons?i=golang,rust,python,typescript,bash)

### Theme Modes (`&theme=auto|dark|light`)

- `auto` *(default)*: Adaptive mode. Icons automatically switch between light and dark backgrounds depending on the viewer's GitHub or system theme.
- `dark`: Forces dark badge background.
- `light`: Forces light badge background.

**Light Theme Example:**

```markdown
![Light Skills](https://skill-icons-go.vercel.app/api/icons?i=java,kotlin,nodejs,figma&theme=light)
```

![Light Skills](https://skill-icons-go.vercel.app/api/icons?i=java,kotlin,nodejs,figma&theme=light)

**Dark Theme Example:**

```markdown
![Dark Skills](https://skill-icons-go.vercel.app/api/icons?i=java,kotlin,nodejs,figma&theme=dark)
```

![Dark Skills](https://skill-icons-go.vercel.app/api/icons?i=java,kotlin,nodejs,figma&theme=dark)

### Icons Per Line (`&perline=`)

Control how many icons appear on each row before wrapping. Accepts any value between `1` and `50` (default is `15`).

```markdown
![Per Line Example](https://skill-icons-go.vercel.app/api/icons?i=aws,gcp,azure,terraform,opentofu,ansible&perline=3)
```

![Per Line Example](https://skill-icons-go.vercel.app/api/icons?i=aws,gcp,azure,terraform,opentofu,ansible&perline=3)

### Interactive Tooltips (`&titles=true`)

Add accessible SVG `<title>` tags to help viewers learn unfamiliar logos when hovering their cursor over icons:

```markdown
![With Tooltips](https://skill-icons-go.vercel.app/api/icons?i=semaphore,starship,semgrep,gitleaks,trufflehog,lefthook&titles=true)
```

![With Tooltips](https://skill-icons-go.vercel.app/api/icons?i=semaphore,starship,semgrep,gitleaks,trufflehog,lefthook&titles=true)

### Native Alignment (`&align=center|left|right`)

Center your icon strip natively without wrapping HTML tags:

```markdown
![Centered Skills](https://skill-icons-go.vercel.app/api/icons?i=git,kubernetes,docker,dockercompose,linux&align=center)
```

![Centered Skills](https://skill-icons-go.vercel.app/api/icons?i=git,kubernetes,docker,dockercompose,linux&align=center)

You can also use standard HTML container centering if preferred:

```html
<p align="center">
  <a href="https://skill-icons-go.vercel.app/">
    <img src="https://skill-icons-go.vercel.app/api/icons?i=git,kubernetes,docker,dockercompose,linux" />
  </a>
</p>
```

<p align="center">
  <a href="https://skill-icons-go.vercel.app/">
    <img src="https://skill-icons-go.vercel.app/api/icons?i=git,kubernetes,docker,dockercompose,linux" />
  </a>
</p>

---

## 🎨 Stack Showcases & Presets

Below are real-world stack configurations highlighting our recently added and updated icons:

### Modern DevOps & Orchestration

Featuring [Semaphore UI](https://github.com/semaphoreui/semaphore), [Docker Compose](https://github.com/docker/compose), Kubernetes, Helm, Argo CD, and [Uptime Kuma](https://github.com/louislam/uptime-kuma):

```markdown
![DevOps](https://skill-icons-go.vercel.app/api/icons?i=kubernetes,docker,dockercompose,helm,argocd,semaphore,uptimekuma,grafana,prometheus)
```

![DevOps](https://skill-icons-go.vercel.app/api/icons?i=kubernetes,docker,dockercompose,helm,argocd,semaphore,uptimekuma,grafana,prometheus)

### DevSecOps & Supply Chain Security

Featuring [Semgrep](https://github.com/semgrep/semgrep), [Gitleaks](https://github.com/gitleaks/gitleaks), [TruffleHog](https://github.com/trufflesecurity/trufflehog), [Sigstore Cosign](https://github.com/sigstore/cosign), Trivy, Snyk, and SonarQube:

```markdown
![Security](https://skill-icons-go.vercel.app/api/icons?i=semgrep,gitleaks,trufflehog,cosign,trivy,snyk,sonarqube,falco)
```

![Security](https://skill-icons-go.vercel.app/api/icons?i=semgrep,gitleaks,trufflehog,cosign,trivy,snyk,sonarqube,falco)

### Developer Tooling & Shell Environment

Featuring [Starship](https://github.com/starship/starship), [Lefthook](https://github.com/evilmartians/lefthook), [Microsoft Visual Studio](https://visualstudio.microsoft.com/), VS Code, Neovim, and K9s:

```markdown
![Dev Tools](https://skill-icons-go.vercel.app/api/icons?i=starship,lefthook,git,visualstudio,vscode,neovim,ghostty,k9s)
```

![Dev Tools](https://skill-icons-go.vercel.app/api/icons?i=starship,lefthook,git,visualstudio,vscode,neovim,ghostty,k9s)

### Infrastructure as Code & Config Formats

Featuring Terraform, OpenTofu, [HashiCorp Configuration Language (HCL)](https://github.com/hashicorp/hcl), Ansible, [TOML](https://github.com/toml-lang/toml), YAML, and JSON:

```markdown
![IaC & Config](https://skill-icons-go.vercel.app/api/icons?i=terraform,opentofu,hcl,ansible,yaml,toml,json)
```

![IaC & Config](https://skill-icons-go.vercel.app/api/icons?i=terraform,opentofu,hcl,ansible,yaml,toml,json)

### AI & Agentic Engineering

Featuring Google Antigravity, Anthropic Claude Code, OpenAI Codex, [Hermes Agent](https://hermes-agent.nousresearch.com/), [MemPalace](https://github.com/mempalace/mempalace), GitHub Copilot, and Ollama:

```markdown
![AI Engineering](https://skill-icons-go.vercel.app/api/icons?i=antigravity,claudecode,codex,hermes,mempalace,githubcopilot,ollama)
```

![AI Engineering](https://skill-icons-go.vercel.app/api/icons?i=antigravity,claudecode,codex,hermes,mempalace,githubcopilot,ollama)

---

## 🔀 Smart Aliases Reference

Our Go service features an extensive alias engine so you can use common abbreviations and command-line names interchangeably:

| Category | Tool / Technology | Canonical ID | Supported Aliases |
| :--- | :--- | :--- | :--- |
| **Containers** | Docker Compose | `dockercompose` | `compose`, `docker-compose`, `docker_compose` |
| **Automation** | Semaphore UI | `semaphore` | `semaphoreui`, `semaphore-ui`, `ansible-semaphore` |
| **Security** | Gitleaks | `gitleaks` | `git-leaks` |
| **Security** | TruffleHog | `trufflehog` | `truffle-hog` |
| **Security** | Sigstore Cosign | `cosign` | `sigstore-cosign`, `sigstorecosign` |
| **Security** | Semgrep | `semgrep` | `semgrep` |
| **Git Tooling** | Lefthook | `lefthook` | `left-hook` |
| **Monitoring** | Uptime Kuma | `uptimekuma` | `uptime-kuma` |
| **Observability** | Elastic Beats | `beats` | `elasticbeats`, `elastic-beats` |
| **Observability** | OpenTelemetry | `opentelemetry` | `otel`, `opentel` |
| **Security** | Apache Ranger | `ranger` | `apacheranger`, `apache-ranger` |
| **Security** | ARMO Platform | `armo` | `armoplatform`, `armo-platform` |
| **Security** | Google OSS-Fuzz | `ossfuzz` | `oss-fuzz` |
| **Policy & Secrets** | External Secrets Operator | `externalsecrets` | `eso`, `external-secrets` |
| **Policy & Secrets** | Open Policy Agent | `opa` | `open-policy-agent` |
| **IDEs & Editors** | Microsoft Visual Studio | `visualstudio` | `vs`, `visual-studio`, `visual_studio` |
| **AI Assistants** | Google Antigravity | `antigravity` | `antigravitycli`, `antigravity-cli` |
| **AI Assistants** | Claude Code | `claudecode` | `claude-code` |
| **AI Assistants** | Codex CLI | `codex` | `codexcli`, `codex-cli` |
| **AI Agents** | Hermes Agent | `hermes` | `hermesagent`, `hermes-agent`, `nous-hermes` |
| **AI Memory** | MemPalace | `mempalace` | `mem-palace` |
| **AI & ML** | Hugging Face | `huggingface` | `hf` |
| **AI & ML** | Google Colab | `googlecolab` | `colab`, `google-colab` |
| **AI & ML** | Jupyter Notebook | `jupyter` | `jupyternotebook`, `jupyter-notebook` |
| **Languages** | Go | `golang` | `go` |
| **Languages** | TypeScript | `typescript` | `ts` |
| **Languages** | Python | `python` | `py` |
| **Languages** | C++ | `cpp` | `c++`, `cplusplus` |
| **Languages** | C# | `cs` | `c#`, `csharp` |
| **Python Tools** | Astral uv | `uv` | `python-uv`, `astral-uv` |

---

## 📦 Self-Hosting & Local Development

### Prerequisites

- [Go](https://golang.org/) (1.20+)
- [Docker](https://www.docker.com/) (optional)

### Running Locally with Go

1. Clone the repository:
   ```bash
   git clone https://github.com/UMMAN2005/skill-icons.git
   cd skill-icons
   ```

2. Generate icon definitions and run tests:
   ```bash
   go run build.go
   go test -v ./...
   python3 scripts/audit_svgs.py
   ```

3. Launch the development server:
   ```bash
   go run api/index.go
   ```

### Running with Docker

You can build and launch a containerized instance locally:

```bash
docker build -t skill-icons .
docker run -d -p 8080:8080 --name skill-icons skill-icons
```

Visit `http://localhost:8080/api/icons?i=docker,kubernetes,golang` in your browser.

---

# Icons List

Here's a list of all 920+ icons currently supported. Feel free to open an issue or pull request to suggest new icons!

"""

FOOTER = """
# 💖 Support & Community

Thank you for using **Skill Icons**! If you find this project helpful, please consider starring the repository on [GitHub](https://github.com/UMMAN2005/skill-icons).

To suggest new icons, request features, or report issues, please [open an issue](https://github.com/UMMAN2005/skill-icons/issues) or submit a [pull request](https://github.com/UMMAN2005/skill-icons/pulls)!
"""


def build_icon_table():
    assets_dir = ROOT / "assets"
    files = sorted(assets_dir.glob("*.svg"))

    icon_list = []
    img_tags = []

    for file_path in files:
        name = file_path.name
        if name.endswith("-light.svg") or name.endswith("-dark.svg"):
            continue
        if name.endswith("-auto.svg") and (assets_dir / (name[:-9] + ".svg")).exists():
            continue
        icon_list.append(name)
        img_tags.append(f'<img src="./assets/{name}" width="48">')

    icons_counter = len(icon_list)
    columns = icons_counter // 100 + 1

    max_icon_id_length = max(len(os.path.splitext(f)[0].replace("-auto", "")) for f in icon_list)
    max_img_tag_length = max(len(t) for t in img_tags)

    most_negative_number = 0
    for row in range(100):
        if row < icons_counter:
            img_tag = f'<img src="./assets/{icon_list[row]}">'
            padding_img_tag = (max_img_tag_length - len(img_tag) + 1) // 2
            if padding_img_tag > most_negative_number:
                most_negative_number = padding_img_tag

    table_header_0 = ""
    table_header_1 = ""
    for _ in range(columns):
        table_header_0 += "| Icon ID | Icon "
        table_header_1 += "| :-----------------: | :--------------: "
    table_header_0 += "|"
    table_header_1 += "|"

    icon_table = ["" for _ in range(100)]
    count_id = 0

    for col in range(columns):
        for row in range(100):
            if count_id >= icons_counter:
                continue
            curr_file = icon_list[count_id]
            icon_id = os.path.splitext(curr_file)[0].replace("-auto", "")
            img_tag = f'<img src="./assets/{curr_file}" width="48">'

            pad_id = (max_icon_id_length - len(icon_id) + 1) // 2
            pad_img = (max_img_tag_length - len(img_tag) + 1) // 2 + most_negative_number

            padded_icon_id = " " * pad_id + f"`{icon_id}`" + " " * pad_id
            padded_img_tag = " " * pad_img + img_tag + " " * pad_img

            if len(icon_id) % 2 != 0:
                padded_icon_id += " "
            if len(img_tag) % 2 != 0:
                padded_img_tag += " "
            if len(padded_img_tag) == 54:
                padded_img_tag += "  "

            icon_table[row] += f"|{padded_icon_id}|{padded_img_tag}"
            count_id += 1

    table_lines = [table_header_0, table_header_1]
    for row in range(100):
        table_lines.append(f"{icon_table[row]}|")

    return "\n".join(table_lines)


def main():
    table_content = build_icon_table()
    full_readme = HEADER + table_content + "\n" + FOOTER.strip() + "\n"

    readme_path = ROOT / "README.md"
    readme_path.write_text(full_readme, encoding="utf-8")
    print(f"Successfully generated {readme_path} with {len(full_readme)} bytes.")


if __name__ == "__main__":
    main()
