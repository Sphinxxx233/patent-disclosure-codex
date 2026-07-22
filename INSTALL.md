# Codex 安装说明

本仓库根目录即技能根目录，包含 `SKILL.md`、`agents/openai.yaml`、`prompts/` 与 `tools/`。

## 全局安装

全局安装后，Codex 可在所有项目中发现该技能。

### Windows PowerShell

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.codex\skills"
git clone <你的仓库 URL> "$env:USERPROFILE\.codex\skills\patent-disclosure-codex"
```

### macOS / Linux

```bash
mkdir -p ~/.codex/skills
git clone <你的仓库 URL> ~/.codex/skills/patent-disclosure-codex
```

重新启动 Codex，或开启一个新任务使技能目录重新加载。可用 `$patent-disclosure-codex` 显式调用，也可直接提出“扫描项目并挖掘专利点”“生成技术交底书”等请求触发。

## 更新

```bash
git -C ~/.codex/skills/patent-disclosure-codex pull --ff-only
```

Windows PowerShell：

```powershell
git -C "$env:USERPROFILE\.codex\skills\patent-disclosure-codex" pull --ff-only
```

## 基础依赖

仅使用 Markdown 流程时无需额外安装。处理 Word、PowerPoint 或生成 `.docx` 时，在技能根目录运行：

```bash
python -m pip install -r requirements.txt
```

交底书中的 Mermaid 图需要 Node.js；在 `tools/` 下运行：

```bash
npm install
```

若 Mermaid CLI 找不到浏览器：

```bash
npx puppeteer browsers install chrome-headless-shell
```

## 可选：国知局查新

```bash
python -m pip install -r tools/requirements-cnipa.txt
python -m playwright install chromium
```

未安装时，查新步骤会改用 Codex 的联网搜索能力。Windows 终端如出现中文乱码，可设置 `$env:PYTHONUTF8='1'`。

## 环境诊断

安装完成后运行：

```bash
python tools/doctor.py
```

诊断器会区分核心依赖和可选能力。需要检查全部可选项时使用 `python tools/doctor.py --strict`；自动化场景可使用 `--json`。
