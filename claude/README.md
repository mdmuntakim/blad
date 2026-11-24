# Claude GitHub Repository

This repository sets up a "claude" binary that can be used with `claude -c "ask anything"` to get AI responses.

## Binary: `claude`

The `claude` binary is located at `./claude/claude` and can be used as:

```bash
claude -c "your question here"
```

### How it works:

1. **Local mode**: Runs with deterministic demo responses
2. **API mode**: Connects to Anthropic Claude API or OpenAI GPT API if keys are provided
3. **Local model mode**: Can be configured to run a local model path

### Setup:

```bash
# Make the binary executable and available in PATH
chmod +x claude/claude
export PATH="$PATH:$(pwd)/claude"
claude -c "Hello, how are?"
```

### Configuration:

- `ANTHROPIC_API_KEY` - Environment variable for Anthropic Claude API
- `OPENAI_API_KEY` - Environment variable for OpenAI GPT API
- `AI_MODEL` - Model name (default: gpt-3.5-turbo)
- `AI_MAX_TOKENS` - Maximum tokens in response (default: 500)
- `CLAUDE_MODEL_PATH` - Path to a local model directory (for future local inference)

### GitHub Actions:

This repository includes a GitHub Actions workflow (`.github/workflows/run-claude.yml`) that:

- Can be triggered manually via the GitHub Actions UI
- Runs the claude binary for up to 6 hours
- Supports API key injection from GitHub Secrets
- Uploads the response as an artifact

**Note:** GitHub Actions free runners do **not** include GPU acceleration. For GPU-accelerated AI inference, you would need:
- A self-hosted runner with NVIDIA GPU
- GitHub Codespaces with GPU configuration
- Dedicated cloud deployment

### Downloading a Small AI Model (1-3GB):

While this repo doesn't include the proprietary Claude model, you can download small open-source models such as:

- **Phi-3-mini-4k-instruct** (~2GB) - Microsoft
- **Gemma-2b-it** (~1.8GB) - Google
- **DistilGPT2** (~500MB) - Hugging Face

To use a local model, set `CLAUDE_MODEL_PATH` to the model directory and implement inference in `claude/claude`.

## Binary Usage

```bash
# Basic usage
claude -c "What is the capital of France?"

# With API key
ANTHROPIC_API_KEY=your_key claude -c "Tell me a joke"
```