#!/bin/bash
# Instala las dependencias de los scripts al iniciar una sesión en la nube.
set -euo pipefail
[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0
cd "$CLAUDE_PROJECT_DIR"
pip install -q -r requirements.txt
