#!/usr/bin/env python3
import argparse
import datetime
import json
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write("[FATAL] Missing dependency: pyyaml\nInstall with: python3 -m pip install pyyaml\n")
    sys.exit(1)

RUN_STATE_DIRNAME = ".space_tools"
LAST_PLAN_FILENAME = "last_plan.json"


def fatal(msg: str, code: int = 1) -> None:
    sys.stderr.write(f"[FATAL] {msg}\n")
    sys.exit(code)


def load_config():
    repo_root = Path(__file__).resolve().parent
    config_path = repo_root / "config" / "spaces.yaml"
    if not config_path.exists():
        fatal(f"Missing config file: {config_path}")
    with config_path.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return cfg, repo_root, config_path


def resolve_paths(space_id, cfg, repo_root):
    try:
        defaults = cfg["defaults"]
        space_cfg = cfg["spaces"][space_id]
    except KeyError as e:
        fatal(f"Missing config key: {e}")

    dropbox_root = Path(defaults["dropbox_root"]).expanduser()
    backup_root = Path(defaults["backup_root"]).expanduser()
    configured_repo_root = Path(defaults.get("repo_root", str(repo_root))).expanduser()
    state_dir = configured_repo_root / RUN_STATE_DIRNAME
    config_file = configured_repo_root / "config" / "spaces.yaml"
    space_folder = dropbox_root / space_cfg["folder"]

    return {
        "repo_root": configured_repo_root,
        "space_folder": space_folder,
        "backup_root": backup_root,
        "config_path": config_file,
        "state_dir": state_dir,
        "plan_file": state_dir / LAST_PLAN_FILENAME,
        "space_cfg": space_cfg,
        "dropbox_root": dropbox_root,
    }


def print_paths_summary(paths):
    print("Path assumptions:")
    print(f"  Repo root:    {paths['repo_root']}")
    print(f"  Config file:  {paths['config_path']}")
    print(f"  Space folder: {paths['space_folder']}")
    print(f"  Backup root:  {paths['backup_root']}")


def list_spaces(cfg):
    defaults = cfg.get("defaults", {})
    dropbox_root = Path(defaults.get("dropbox_root", "")).expanduser()
    print("Configured spaces:")
    for sid, scfg in cfg.get("spaces", {}).items():
        path = dropbox_root / scfg["folder"]
        print(f"- {sid}: {scfg.get('name', sid)} -> {path}")


def find_candidate_files(space_folder, space_cfg, glob_pattern=None):
    include_patterns = space_cfg.get("patterns", {}).get("include", ["**/*"])
    exclude_patterns = space_cfg.get("patterns", {}).get("exclude", [])

    included = set()
    for pat in include_patterns:
        for p in space_folder.glob(pat):
            if p.is_file():
                included.add(p.resolve())

    excluded = set()
    for pat in exclude_patterns:
        for p in space_folder.glob(pat):
            if p.is_file():
                excluded.add(p.resolve())

    candidates = sorted(p for p in included if p not in excluded)

    if glob_pattern:
        candidates = [p for p in candidates if p.match(glob_pattern)]

    return candidates


def run_subprocess(cmd):
    print(f"\n[EXEC] {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        fatal(f"Command failed with exit code {result.returncode}: {' '.join(cmd)}", result.returncode)


def save_plan(plan_file: Path, payload: dict):
    plan_file.parent.mkdir(parents=True, exist_ok=True)
    with plan_file.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def load_plan(plan_file: Path) -> dict:
    if not plan_file.exists():
        fatal(f"No saved plan found: {plan_file}. Run plan-update first.")
    with plan_file.open("r", encoding="utf-8") as f:
        return json.load(f)


def create_backup(paths, space_id, files):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    backup_root = paths["backup_root"] / space_id / timestamp
    print(f"\n[BACKUP] Creating backup: {backup_root}")
    for f in files:
        src = Path(f)
        rel = src.relative_to(paths["space_folder"])
        dest = backup_root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
    return backup_root, timestamp


def cmd_list_spaces(args):
    cfg, _, _ = load_config()
    list_spaces(cfg)


def cmd_plan_update(args):
    cfg, repo_root, _ = load_config()
    paths = resolve_paths(args.space, cfg, repo_root)
    print_paths_summary(paths)

    if not paths["space_folder"].exists():
        fatal(f"Space folder does not exist: {paths['space_folder']}")

    script_path = paths["repo_root"] / args.script
    if not script_path.exists():
        fatal(f"Script not found: {script_path}")

    candidates = find_candidate_files(paths["space_folder"], paths["space_cfg"], args.glob)
    print(f"\n[DRY-RUN] Candidate files: {len(candidates)}")
    for p in candidates:
        print(f"  {p}")

    if not candidates:
        print("\n[DRY-RUN] No files matched. Nothing to do.")
        return

    cmd = [sys.executable, str(script_path), "--dry-run"]
    for item in args.script_arg or []:
        cmd.append(item)
    cmd.extend(str(p) for p in candidates)
    run_subprocess(cmd)

    payload = {
        "space": args.space,
        "script": args.script,
        "glob": args.glob,
        "script_arg": args.script_arg or [],
        "files": [str(p) for p in candidates],
        "saved_at": datetime.datetime.now().isoformat(),
    }
    save_plan(paths["plan_file"], payload)
    print(f"\n[DRY-RUN] Saved plan: {paths['plan_file']}")
    print("[DRY-RUN] No files were modified.")


def cmd_run_update(args):
    if not args.confirm:
        fatal("--confirm is required for run-update")

    cfg, repo_root, _ = load_config()
    paths = resolve_paths(args.space, cfg, repo_root)
    print_paths_summary(paths)

    saved_plan = load_plan(paths["plan_file"])
    requested = {
        "space": args.space,
        "script": args.script,
        "glob": args.glob,
        "script_arg": args.script_arg or [],
    }
    previous = {
        "space": saved_plan.get("space"),
        "script": saved_plan.get("script"),
        "glob": saved_plan.get("glob"),
        "script_arg": saved_plan.get("script_arg", []),
    }
    if requested != previous:
        fatal("run-update arguments do not match the most recent saved dry-run plan")

    files = [Path(p) for p in saved_plan.get("files", [])]
    if not files:
        print("[RUN] Saved plan contains no files. Nothing to do.")
        return

    for f in files:
        if not f.exists():
            fatal(f"Planned file no longer exists: {f}")

    script_path = paths["repo_root"] / args.script
    if not script_path.exists():
        fatal(f"Script not found: {script_path}")

    print(f"\n[RUN] Files to process: {len(files)}")
    for p in files:
        print(f"  {p}")

    backup_root, timestamp = create_backup(paths, args.space, files)

    cmd = [sys.executable, str(script_path)]
    for item in args.script_arg or []:
        cmd.append(item)
    cmd.extend(str(p) for p in files)
    run_subprocess(cmd)

    print("\n[RUN] Completed.")
    print("Commands executed:")
    print(f"  {sys.executable} {script_path} {' '.join(args.script_arg or [])} {' '.join(str(p) for p in files)}")
    print("Files touched:")
    for p in files:
        print(f"  {p}")
    print(f"Backup path: {backup_root}")
    print("Rollback:")
    print(f"  {sys.executable} {paths['repo_root'] / 'space_tools.py'} show-rollback --space {args.space} --timestamp {timestamp}")
    print("Suggested git commit message:")
    print(f"  chore({args.space}): run {args.script} on {timestamp}")


def cmd_show_rollback(args):
    cfg, repo_root, _ = load_config()
    paths = resolve_paths(args.space, cfg, repo_root)
    print_paths_summary(paths)

    backup_root = paths["backup_root"] / args.space / args.timestamp
    if not backup_root.exists():
        fatal(f"Backup folder not found: {backup_root}")

    print("\nRollback commands:")
    print(f"  rsync -av --dry-run \"{backup_root}/\" \"{paths['space_folder']}/\"")
    print(f"  rsync -av \"{backup_root}/\" \"{paths['space_folder']}/\"")


def build_parser():
    parser = argparse.ArgumentParser(description="Perplexity Space automation tools")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list-spaces", help="List configured spaces")
    p_list.set_defaults(func=cmd_list_spaces)

    p_plan = sub.add_parser("plan-update", help="Run a dry-run plan against a space")
    p_plan.add_argument("--space", required=True)
    p_plan.add_argument("--script", required=True, help="Path relative to repo root")
    p_plan.add_argument("--glob", default=None)
    p_plan.add_argument("--script-arg", action="append", help="Extra arg passed to target script")
    p_plan.set_defaults(func=cmd_plan_update)

    p_run = sub.add_parser("run-update", help="Run live update after matching dry-run plan")
    p_run.add_argument("--space", required=True)
    p_run.add_argument("--script", required=True, help="Path relative to repo root")
    p_run.add_argument("--glob", default=None)
    p_run.add_argument("--script-arg", action="append", help="Extra arg passed to target script")
    p_run.add_argument("--confirm", action="store_true")
    p_run.set_defaults(func=cmd_run_update)

    p_rb = sub.add_parser("show-rollback", help="Show rollback commands for a backup timestamp")
    p_rb.add_argument("--space", required=True)
    p_rb.add_argument("--timestamp", required=True)
    p_rb.set_defaults(func=cmd_show_rollback)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except KeyboardInterrupt:
        sys.stderr.write("\n[ABORTED] Interrupted by user\n")
        sys.exit(130)


if __name__ == "__main__":
    main()
