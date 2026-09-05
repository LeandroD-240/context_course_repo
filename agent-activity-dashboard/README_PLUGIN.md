# Text Processor Plugin

Plugin examples for text-analysis workflows built from the Unit 1 skills and Unit 2 MCP.

## Skills

- **Analyze Text** — Word counts, sentence stats, vocabulary diversity
- **Extract Keywords** — Find the most frequent meaningful terms
- **Check Reading Level** — Flesch-Kincaid grade level estimation
- **Reverse Text** — Reversed version of the text

## OpenCode

The OpenCode version is a local or npm-loaded JS/TS plugin module under `.opencode/plugins/` or the `plugin` and `mcp` array in `opencode.json`.

## Related MCP Server

If you also connect the `text-processor` MCP server, it provides:
- `analyze_text` — Compute text statistics
- `extract_keywords` — Extract frequent terms
- `check_reading_level` — Estimate reading difficulty
- `reverse_text` — Reverse a string

## Setup

The plugin can use your local server or the deployed Spaces version:

**Local:** Ensure `text-processor-mcp/server.py` is available and the MCP runtime is installed.

**Remote:** Update the `.mcp.json` or `opencode.json` URL to your deployed Space:
`https://YOUR-USERNAME-text-processor-mcp.hf.space/gradio_api/mcp/`