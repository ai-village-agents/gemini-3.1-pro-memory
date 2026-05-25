#!/usr/bin/env python3
"""Clone/pull peer repos, scan for constraint/ratio signals, and summarize results."""

from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

# Fallback list used only when peer_repos/ has no existing git checkouts.
FALLBACK_REPOS = [
    "https://github.com/ai-village-agents/memory-improvement.git",
    "https://github.com/ai-village-agents/deepseek-v3.2-memory-system.git",
    "https://github.com/ai-village-agents/gpt-5-4-memory-kit.git",
    "https://github.com/ai-village-agents/claude-opus-memory.git",
]

NEEDLE = "Consolidation Ratio Test Result"
FILENAME_KEYWORDS = ("constraint", "ratio")
MAX_REPORT_ITEMS = 8


@dataclass
class RepoScanResult:
    repo: str
    local_path: Path
    sync_action: str
    sync_ok: bool
    sync_error: str | None
    filename_hits: list[Path]
    content_hits: list[tuple[Path, int, str]]


@dataclass
class PeerRepo:
    repo: str
    local_path: Path
    clone_url: str | None


def run_git(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
    )


def normalize_repo_name(url_or_repo: str) -> str:
    value = url_or_repo.rstrip("/")
    base = value.rsplit("/", maxsplit=1)[-1]
    return base.removesuffix(".git")


def canonical_repo_id(url_or_repo: str) -> str:
    value = url_or_repo.strip().rstrip("/")
    if value.endswith(".git"):
        value = value[:-4]
    return value.lower()


def discover_peer_repos(target_dir: Path) -> list[PeerRepo]:
    repos: list[PeerRepo] = []
    seen_ids: set[str] = set()
    for entry in sorted(target_dir.iterdir()):
        if not entry.is_dir() or not (entry / ".git").exists():
            continue
        remote = run_git(["remote", "get-url", "origin"], cwd=entry)
        clone_url = remote.stdout.strip() if remote.returncode == 0 else None
        display = clone_url or entry.name
        repo_id = canonical_repo_id(clone_url or entry.name)
        if repo_id in seen_ids:
            continue
        seen_ids.add(repo_id)
        repos.append(PeerRepo(repo=display, local_path=entry, clone_url=clone_url))

    if repos:
        return repos

    for clone_url in FALLBACK_REPOS:
        repo_name = normalize_repo_name(clone_url)
        repos.append(
            PeerRepo(
                repo=clone_url,
                local_path=target_dir / repo_name,
                clone_url=clone_url,
            )
        )
    return repos


def sync_peer_repo(peer: PeerRepo) -> tuple[str, bool, str | None]:
    if (peer.local_path / ".git").exists():
        pull = run_git(["pull", "--ff-only"], cwd=peer.local_path)
        if pull.returncode == 0:
            return "pulled", True, None
        err = pull.stderr.strip() or pull.stdout.strip() or "git pull failed"
        return "pull-failed", False, err

    if peer.local_path.exists() and not (peer.local_path / ".git").exists():
        return "skipped", False, f"target exists but is not a git repo: {peer.local_path}"

    if not peer.clone_url:
        return "skipped", False, "missing clone URL"

    clone = run_git(["clone", "--depth", "1", peer.clone_url, str(peer.local_path)])
    if clone.returncode == 0:
        return "cloned", True, None
    err = clone.stderr.strip() or clone.stdout.strip() or "git clone failed"
    return "clone-failed", False, err


def is_probably_binary(path: Path) -> bool:
    try:
        with path.open("rb") as f:
            chunk = f.read(2048)
        return b"\x00" in chunk
    except OSError:
        return True


def scan_repo(path: Path) -> tuple[list[Path], list[tuple[Path, int, str]]]:
    filename_hits: list[Path] = []
    content_hits: list[tuple[Path, int, str]] = []

    for root, dirs, files in os.walk(path):
        if ".git" in dirs:
            dirs.remove(".git")
        root_path = Path(root)

        for file_name in files:
            file_path = root_path / file_name
            lowered = file_name.lower()

            if any(keyword in lowered for keyword in FILENAME_KEYWORDS):
                filename_hits.append(file_path)

            if is_probably_binary(file_path):
                continue

            try:
                with file_path.open("r", encoding="utf-8", errors="ignore") as f:
                    for line_no, line in enumerate(f, start=1):
                        if NEEDLE in line:
                            content_hits.append((file_path, line_no, line.strip()))
            except OSError:
                continue

    return filename_hits, content_hits


def format_path(path: Path, base: Path) -> str:
    try:
        return str(path.relative_to(base))
    except ValueError:
        return str(path)


def print_repo_summary(result: RepoScanResult) -> None:
    print(f"\n=== {result.repo} ===")
    print(f"Local: {result.local_path}")
    print(f"Sync: {result.sync_action}")
    if not result.sync_ok:
        print(f"Error: {result.sync_error}")
        return

    print(f"Filename hits (*constraint*/*ratio*): {len(result.filename_hits)}")
    for hit in result.filename_hits[:MAX_REPORT_ITEMS]:
        print(f"  - {format_path(hit, result.local_path)}")
    if len(result.filename_hits) > MAX_REPORT_ITEMS:
        print(f"  ... and {len(result.filename_hits) - MAX_REPORT_ITEMS} more")

    print(f"Content hits ('{NEEDLE}'): {len(result.content_hits)}")
    for file_path, line_no, line in result.content_hits[:MAX_REPORT_ITEMS]:
        preview = line[:140]
        print(f"  - {format_path(file_path, result.local_path)}:{line_no}: {preview}")
    if len(result.content_hits) > MAX_REPORT_ITEMS:
        print(f"  ... and {len(result.content_hits) - MAX_REPORT_ITEMS} more")


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    target_dir = script_dir / "peer_repos"
    target_dir.mkdir(parents=True, exist_ok=True)
    peers = discover_peer_repos(target_dir)

    print(f"Syncing peer repos into: {target_dir}")
    print(f"Peer repos to process: {len(peers)}")
    print(f"Scanning for content string: {NEEDLE}")
    print(f"Scanning for filename keywords: {', '.join(FILENAME_KEYWORDS)}")

    results: list[RepoScanResult] = []
    for peer in peers:
        action, ok, err = sync_peer_repo(peer)
        filename_hits: list[Path] = []
        content_hits: list[tuple[Path, int, str]] = []
        if ok:
            filename_hits, content_hits = scan_repo(peer.local_path)

        results.append(
            RepoScanResult(
                repo=peer.repo,
                local_path=peer.local_path,
                sync_action=action,
                sync_ok=ok,
                sync_error=err,
                filename_hits=filename_hits,
                content_hits=content_hits,
            )
        )
        print_repo_summary(results[-1])

    synced = [r for r in results if r.sync_ok]
    failed = [r for r in results if not r.sync_ok]
    total_filename_hits = sum(len(r.filename_hits) for r in synced)
    total_content_hits = sum(len(r.content_hits) for r in synced)

    print("\n=== Overall Summary ===")
    print(f"Repos requested: {len(results)}")
    print(f"Synced successfully: {len(synced)}")
    print(f"Sync failures/skips: {len(failed)}")
    print(f"Total filename hits: {total_filename_hits}")
    print(f"Total content hits: {total_content_hits}")

    if failed:
        print("\nSync issues:")
        for r in failed:
            print(f"  - {r.repo}: {r.sync_action} ({r.sync_error})")

    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
