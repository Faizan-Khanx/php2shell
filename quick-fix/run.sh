#!/usr/bin/env bash
# Compatibility wrapper for quick-fix/mitigate.sh
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$DIR/mitigate.sh" "$@"
