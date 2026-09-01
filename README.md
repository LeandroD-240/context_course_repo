# context_course_repo
Repository for practice the hugging face context course

Installing `opencode`:

```bash
curl -fsSL https://opencode.ai/install | bash
```

Installing a **mcp server** and **gradio** (first create a virtual environment)

```bash
pip install "mcp[cli]"
pip install gradio
```

List the tools you've created with a *Web UI*
```bash
mcp dev server.py
```