# commix 🚀

> AI-Powered Smart Git Commit Assistant

[![PyPI version](https://badge.fury.io/py/commix.svg)](https://badge.fury.io/py/commix)
[![Python](https://img.shields.io/pypi/pyversions/commix.svg)](https://pypi.org/project/commix/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/DocJlm/commix.svg?style=social)](https://github.com/DocJlm/commix)

**commix** 是一个智能的Git提交信息生成工具，利用AI分析你的代码变更，自动生成符合规范的提交信息。告别 "fix bug"、"update" 这种模糊的提交信息！

## ✨ 特性

- 🤖 **AI驱动** - 智能分析代码变更，生成高质量提交信息
- 📝 **规范支持** - 自动遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范
- 🎨 **Gitmoji集成** - 可选的emoji支持，让提交历史更美观
- ⚡ **极快执行** - 本地缓存 + 异步处理，秒级生成
- 🔄 **多AI提供商** - 支持 OpenAI、Claude、Ollama、本地模型
- 💬 **交互式编辑** - 实时预览、选择、编辑提交信息
- 📦 **零配置** - 开箱即用，自动检测最佳AI提供商
- 🛠️ **高度可定制** - 自定义模板、规范、语言

## 🚀 快速开始

### 安装

```bash
# 使用 pip
pip install commix

# 使用 pipx（推荐）
pipx install commix

# 使用 Homebrew
brew install commix
```

### 基本用法

```bash
# 生成提交信息（分析暂存的变更）
commix

# 生成并自动提交
commix --commit

# 使用特定AI提供商
commix --provider openai

# 生成中文提交信息
commix --lang zh
```

## 📖 使用示例

### 1. 基础用法

```bash
# 暂存你的变更
git add .

# 运行 commix
commix
```

commix 会分析你的变更并生成符合规范的提交信息：

```
✨ feat(auth): add OAuth2 login support

- Implement OAuth2 authentication flow
- Add Google and GitHub providers
- Create login page with provider selection
- Add session management middleware
```

### 2. 交互式选择

```bash
commix --interactive
```

显示多个候选提交信息，让你选择或编辑：

```
? Choose a commit message:

  1. ✨ feat(auth): add OAuth2 login support
  2. 🔐 feat: implement OAuth2 authentication
  3. ➕ feat(auth): add Google and GitHub OAuth

> Edit custom message
```

### 3. Gitmoji 支持

```bash
# 启用 emoji
commix --emoji

# 或在配置中设置
commix config set emoji true
```

### 4. 批量提交

```bash
# 拆分大型变更为多个提交
commix --batch
```

## ⚙️ 配置

### 配置文件

配置文件位于 `~/.commix/config.yaml`：

```yaml
# AI 提供商配置
provider: openai  # openai, claude, ollama, local

# OpenAI 配置
openai:
  api_key: ${OPENAI_API_KEY}
  model: gpt-4o-mini

# Claude 配置
claude:
  api_key: ${ANTHROPIC_API_KEY}
  model: claude-3-haiku-20240307

# Ollama 配置（本地）
ollama:
  base_url: http://localhost:11434
  model: llama3.2

# 提交信息设置
commit:
  style: conventional  # conventional, gitmoji, custom
  language: en  # en, zh, ja, ko
  max_length: 72
  include_scope: true
  
# Gitmoji 设置
gitmoji:
  enabled: true
  auto_detect: true
```

### 环境变量

```bash
# OpenAI
export OPENAI_API_KEY="sk-..."

# Claude
export ANTHROPIC_API_KEY="sk-ant-..."

# 使用环境变量覆盖配置
export COMMIX_PROVIDER=ollama
export COMMIX_LANGUAGE=zh
```

## 🎯 命令参考

```bash
commix [OPTIONS] [COMMAND]

Commands:
  commit    Generate and create commit
  config    Manage configuration
  providers List available AI providers
  cache     Manage cache
  version   Show version

Options:
  --provider TEXT      AI provider to use
  --lang TEXT          Commit message language (en/zh/ja/ko)
  --emoji              Enable gitmoji support
  --interactive, -i    Interactive mode
  --batch              Batch commit mode
  --dry-run            Preview without committing
  --config FILE        Use custom config file
  --help               Show help message
```

## 🔧 高级用法

### 自定义模板

在项目根目录创建 `.commix/template.md`：

```markdown
{emoji} {type}({scope}): {description}

{body}

Co-authored-by: AI Assistant <ai@example.com>
```

### CI/CD 集成

```yaml
# GitHub Actions
- name: Generate Commit Message
  run: |
    pip install commix
    commix --commit --non-interactive
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

### Pre-commit Hook

```bash
# 安装 pre-commit hook
commix install-hook

# 或手动添加到 .git/hooks/pre-commit
#!/bin/bash
commix --commit --non-interactive
```

## 🏗️ 架构

```
commix/
├── __init__.py
├── cli.py           # CLI入口
├── analyzer.py      # 代码变更分析
├── generator.py     # AI生成器
├── providers/       # AI提供商实现
│   ├── base.py
│   ├── openai.py
│   ├── claude.py
│   └── ollama.py
├── git_utils.py     # Git操作工具
├── templates.py     # 模板系统
└── config.py        # 配置管理
```

## 🤝 贡献

我们欢迎所有形式的贡献！

### 开发设置

```bash
# 克隆仓库
git clone https://github.com/DocJlm/commix.git
cd commix

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 代码格式化
black commix tests
isort commix tests
```

### 贡献指南

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交变更 (`commix` 😄)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解更多详情。

## 📝 更新日志

查看 [CHANGELOG.md](CHANGELOG.md) 了解版本历史。

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [Conventional Commits](https://www.conventionalcommits.org/) - 提交规范
- [Gitmoji](https://gitmoji.dev/) - Emoji 指南
- [Typer](https://typer.tiangolo.com/) - CLI 框架
- [Rich](https://github.com/Textualize/rich) - 终端美化

## ⭐ Star History

如果这个项目对你有帮助，请给一个 ⭐️！

[![Star History Chart](https://api.star-history.com/svg?repos=DocJlm/commix&type=Date)](https://star-history.com/#DocJlm/commix&Date)

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/DocJlm">DocJlm</a>
</p>
