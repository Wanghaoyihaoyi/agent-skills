# Source Reading Methods

## Local helpers

`<skill-dir>` means the directory containing the installed Read `SKILL.md`, not the repository root or a former plugin dispatcher's directory. Its `scripts/` contains `fetch.sh`, `fetch_local.py`, `fetch_feishu.py` and `fetch_weixin.py`. Verify the helper and its runtime exist before use; a missing helper is not a reason to reinstall an unrelated tool bundle.

Prefer already available source readers and authenticated connectors when they fit the source. On a shell with Bash and Python 3, the local extraction adapter can be run with:

```bash
bash "<skill-dir>/scripts/fetch.sh" "<url>"
```

Read its structured stderr and inspect whether the article body was extracted. On systems without Bash, use a supported native reader or inspect the Python helper's current CLI; do not assume POSIX commands work everywhere.

The optional `--use-proxy` adapter sends URLs to third-party readers. Use it only with explicit opt-in for a public URL. Never send authenticated, internal or sensitive URLs to it. Failure to extract is not consent. If a tool returns JSON, extract the useful content instead of presenting a raw tool envelope.

## Repository URLs

Determine the host and requested revision from the URL; use its raw-file route, connector or authenticated API. Private content stays with an authorized integration. For GitHub, `gh` is one option when installed and authenticated, and the contents request must include the requested `ref`. Do not silently read the default branch when the URL names another revision. Branch names containing slashes must be resolved against actual repository references, not guessed by splitting the URL.

## PDFs

Use the available PDF skill or tool. For local text extraction, choose an already installed tool such as `pdftotext` or a Python PDF library. Download remote input from the source into a per-run temporary directory when necessary. For scanned pages use available OCR; for tables or visual layout inspect pages rather than trusting text order.

`marker_single` is an optional layout-oriented extractor when installed; it is not a universal dependency. Check available workspace dependencies before adding packages. Avoid prescribing Homebrew, global pip installs or a fixed temporary output directory for every user. Report encrypted, incomplete or unreadable input honestly. Third-party extraction retains the public-URL and opt-in boundary above.

## Feishu / Lark

Prefer an existing authorized connector. The bundled `fetch_feishu.py` uses `requests`, `FEISHU_APP_ID` and `FEISHU_APP_SECRET`; preserve those actual API names. Check that required credentials exist without displaying their values, then invoke the helper with the document URL using the existing Python environment.

The helper supports docx and wiki pages, with the corresponding read permissions. Legacy `/docs/` pages need another supported reader; do not modify or convert the original document without authorization. An already available user-login CLI or authenticated browser may be an alternative when app credentials are absent. Verify the installed CLI's current usage instead of assuming a global install and login are necessary. Return useful document content, not its JSON wrapper.

## WeChat and dynamic pages

Try a supported source reader or direct extraction, then inspect the failure. Use an available authenticated browser when the page needs browser rendering. The bundled `fetch_weixin.py` is an optional Playwright adapter if its Python packages and browser runtime already exist. Missing dependencies do not justify silently installing a large browser runtime; choose another supported reader or explain the concrete setup needed. Login and anti-bot pages are not article content.
