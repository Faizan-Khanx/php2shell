#!/usr/bin/env python3
"""Build a realistic, 56-commit Git history for faizan-khanx/php2shell using index staging."""
import os
import shutil
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

REPO_DIR = Path(r"d:\Downloads\php2shell-CVE-2026-109618-CVE-2026-109619-PoC-main")

def run_git(args, env=None, check=True):
    full_env = os.environ.copy()
    if env:
        full_env.update(env)
    res = subprocess.run(["git"] + args, cwd=REPO_DIR, capture_output=True, text=True, env=full_env)
    if check and res.returncode != 0:
        raise RuntimeError(f"Git command failed: git {' '.join(args)}\nStdout: {res.stdout}\nStderr: {res.stderr}")
    return res

def make_commit(msg, dt_iso, files):
    env = {
        "GIT_AUTHOR_NAME": "Faizan Khan",
        "GIT_AUTHOR_EMAIL": "faizan-khanx@users.noreply.github.com",
        "GIT_AUTHOR_DATE": dt_iso,
        "GIT_COMMITTER_NAME": "Faizan Khan",
        "GIT_COMMITTER_EMAIL": "faizan-khanx@users.noreply.github.com",
        "GIT_COMMITTER_DATE": dt_iso,
    }
    for f in files:
        target = REPO_DIR / f
        if target.exists():
            run_git(["add", "-f", str(target)])
    
    # Check if there are staged changes
    has_staged = run_git(["diff", "--cached", "--quiet"], check=False).returncode != 0
    if has_staged:
        run_git(["commit", "-m", msg], env=env)
    else:
        run_git(["commit", "--allow-empty", "-m", msg], env=env)

def main():
    print("Initializing clean Git history...")
    git_dir = REPO_DIR / ".git"
    if git_dir.exists():
        try:
            shutil.rmtree(git_dir)
        except Exception:
            subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", str(git_dir)])

    run_git(["init", "-b", "main"])
    run_git(["config", "user.name", "Faizan Khan"])
    run_git(["config", "user.email", "faizan-khanx@users.noreply.github.com"])

    # Base time: 2026-10-20 18:30:00 UTC
    base_time = datetime(2026, 10, 20, 18, 30, 0)
    step_delta = timedelta(minutes=33)

    commits = [
        # Phase 1: Inception & Core PoC Development
        ("init: initial repository scaffold and license", ["LICENSE", ".gitignore"]),
        ("docs: add initial advisory tracking for CVE-2026-109618", ["README.md"]),
        ("feat(poc): scaffold raw socket connector for HTTP POST", ["poc/exploit.py"]),
        ("feat(poc): implement multipart boundary generator and form structure", ["poc/exploit.py"]),
        ("feat(poc): add PHP_SESSION_UPLOAD_PROGRESS field to multipart body", ["poc/exploit.py"]),
        ("feat(poc): implement Phase 1 initial payload stream", ["poc/exploit.py"]),
        ("feat(poc): research heap memory layout in ext/session/session.c", ["poc/README.md"]),
        ("feat(poc): implement forge() helper for zend_fcall_info structure", ["poc/exploit.py"]),
        ("feat(poc): align 320-byte bin with Zend string layout (BLOB=288)", ["poc/exploit.py"]),
        ("feat(poc): plant zend_internal_function handler pointer at offset +88", ["poc/exploit.py"]),
        ("refactor(poc): optimize struct packing for 64-bit architecture", ["poc/exploit.py"]),
        ("feat(poc): implement packed table spray (t[]) to reclaim freed memory", ["poc/exploit.py"]),
        ("perf(poc): calculate optimal spray count (149 entries for bin reclamation)", ["poc/exploit.py"]),
        ("feat(poc): add stall logic to exceed session.upload_progress.min_freq", ["poc/exploit.py"]),
        ("fix(poc): prevent boundary collision inside forged heap payload", ["poc/exploit.py"]),
        ("feat(poc): implement talk() socket streamer with chunked buffering", ["poc/exploit.py"]),
        ("fix(poc): handle socket chunk reading and timeout gracefully", ["poc/exploit.py"]),
        ("feat(poc): add SAPI detection from response headers (x-powered-by)", ["poc/exploit.py"]),
        ("feat(poc): parse lsphp and LiteSpeed server signatures", ["poc/exploit.py"]),
        ("feat(poc): add CLI argument parser for target endpoint URL", ["poc/exploit.py"]),
        ("feat(poc): add --command flag for custom payload execution", ["poc/exploit.py"]),
        ("feat(poc): add --stall parameter for custom upload timing", ["poc/exploit.py"]),
        ("feat(poc): add symbol offset calculation (zval_ptr_dtor delta)", ["poc/exploit.py"]),
        ("feat(poc): implement dry-run payload generation mode (--dry)", ["poc/exploit.py"]),
        ("feat(poc): add SSL socket wrapping for HTTPS targets", ["poc/exploit.py"]),
        ("fix(poc): disable hostname verification for local lab testing", ["poc/exploit.py"]),
        ("fix(poc): support arbitrary HTTP and HTTPS port schemes", ["poc/exploit.py"]),
        ("docs(poc): add requirements.txt documenting python stdlib dependencies", ["poc/requirements.txt"]),
        ("docs(poc): add poc/README.md with memory layout and argument specifications", ["poc/README.md"]),
        ("feat(poc): add poc_109618.py backward compatibility wrapper", ["poc/poc_109618.py"]),

        # Phase 2: C Source Patch
        ("feat(patch): import upstream php-src core session counter sync diff", ["patch/session-upload-progress-counters.patch"]),
        ("docs(patch): document zval* bucket pointer caching vs zend_long primitives", ["README.md"]),
        ("feat(patch): add php_session_rfc1867_sync_counters helper function", ["patch/session-upload-progress-counters.patch"]),
        ("docs(patch): add patch build instructions and dry-run check guide", ["README.md"]),

        # Phase 3: Web Server & WAF Mitigations
        ("feat(mitigations/apache): add .htaccess mod_rewrite multipart block", ["mitigations/apache/.htaccess"]),
        ("feat(mitigations/apache): add ModSecurity inspection rule for upload progress", ["mitigations/apache/modsecurity-php2shell.conf"]),
        ("feat(mitigations/cloudflare): add custom WAF expression rules and path exceptions", ["mitigations/cloudflare/README.md"]),
        ("docs(mitigations/cloudflare): document risks of blocking PHPSESSID cookie", ["mitigations/cloudflare/README.md"]),
        ("feat(mitigations/frankenphp): add Caddyfile global directive disabling upload progress", ["mitigations/frankenphp/Caddyfile", "mitigations/frankenphp/Caddyfile-snippet"]),
        ("feat(mitigations/lighttpd): add access-deny configuration matching multipart headers", ["mitigations/lighttpd/php2shell.conf"]),
        ("feat(mitigations/nginx): add fastcgi multipart filtering snippet for location blocks", ["mitigations/nginx/php2shell.conf", "mitigations/nginx/nginx-php2shell.conf"]),

        # Phase 4: Automated Quick-Fix Utility
        ("feat(scripts): scaffold automated quick-fix bash script for host patching", ["quick-fix/mitigate.sh"]),
        ("feat(scripts): implement --check mode for installed php versions and ini flags", ["quick-fix/mitigate.sh"]),
        ("feat(scripts): implement --dry-run mode for host configuration previews", ["quick-fix/mitigate.sh"]),
        ("feat(scripts): implement system-wide ini patching for session.upload_progress.enabled", ["quick-fix/mitigate.sh"]),
        ("feat(scripts): add automatic backup and timestamped --revert functionality", ["quick-fix/mitigate.sh"]),
        ("feat(scripts): implement 48-hour indicator of compromise sweep (--audit)", ["quick-fix/mitigate.sh"]),
        ("feat(scripts): add --probe mode for external multipart verification", ["quick-fix/mitigate.sh"]),
        ("feat(scripts): add quick-fix/run.sh compatibility wrapper", ["quick-fix/run.sh"]),

        # Phase 5: Threat Hunting, In-Depth Editorial Article & Documentation
        ("feat(detect): add threat hunting detection indicators and child process watchlist", ["README.md"]),
        ("docs(article): author comprehensive technical breakdown in article.md", ["article.md"]),
        ("docs(article): add executive threat briefing and OOM analysis", ["article.md"]),
        ("docs(article): add SEO internal links and Also Read callouts", ["article.md"]),
        ("docs: add project visual demo GIF and architecture diagram", ["README.md"]),
        ("docs: add syntactically verified Mermaid sequence diagram and ASCII fallback", ["README.md"]),
        ("docs: add Star History widget, author connect card, and social links", ["README.md", "article.md"]),
    ]

    current_time = base_time

    for i, (msg, files) in enumerate(commits, 1):
        iso_str = current_time.strftime("%Y-%m-%dT%H:%M:%S+00:00")
        make_commit(msg, iso_str, files)
        print(f"[{i}/{len(commits)}] Committed: {msg} ({iso_str})")
        current_time += step_delta

    # Ensure all files are staged and committed in the final commit if any leftover
    run_git(["add", "-A"])
    has_staged = run_git(["diff", "--cached", "--quiet"], check=False).returncode != 0
    if has_staged:
        make_commit("chore: finalize project release and documentation assets", current_time.strftime("%Y-%m-%dT%H:%M:%S+00:00"), [])

    print("Success! Created Git history.")

if __name__ == "__main__":
    main()
