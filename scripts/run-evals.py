#!/usr/bin/env python3
"""
Repeatable local compliance checks for the self-evolving-agent runtime.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "README.zh-CN.md",
    "install.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "SECURITY.md",
    "agents/openai.yaml",
    "benchmarks/suite.json",
    "benchmarks/schemas/judge-output.schema.json",
    ".github/workflows/ci.yml",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/pull_request_template.md",
    "system/coordinator.md",
    "modules/learning-agenda.md",
    "modules/diagnose.md",
    "modules/capability-map.md",
    "modules/curriculum.md",
    "modules/evaluator.md",
    "modules/promotion.md",
    "modules/reflection.md",
    "assets/CAPABILITIES.md",
    "assets/ERRORS.md",
    "assets/EVALUATIONS.md",
    "assets/FEATURE_REQUESTS.md",
    "assets/LEARNINGS.md",
    "assets/LEARNING_AGENDA.md",
    "assets/TRAINING_UNITS.md",
    "assets/records/capabilities/cap-bootstrap-004-verification.md",
    "assets/records/agenda/agd-bootstrap-001-bootstrap-agenda.md",
    "hooks/openclaw/HOOK.md",
    "hooks/openclaw/handler.ts",
    "scripts/activator.sh",
    "scripts/bootstrap-workspace.sh",
    "scripts/error-detector.sh",
    "scripts/evolution_runtime.py",
    "scripts/migrate-self-improving.py",
    "scripts/run-benchmark.py",
    "scripts/run-evals.py",
    "evals/evals.json",
]

MAX_SKILL_NAME_LENGTH = 64


def parse_frontmatter_minimal(frontmatter_text: str) -> tuple[dict | None, str | None]:
    parsed: dict[str, object] = {}

    for raw_line in frontmatter_text.splitlines():
        if not raw_line.strip():
            continue
        if raw_line.startswith(" ") or raw_line.startswith("\t"):
            continue
        if ":" not in raw_line:
            return None, f"Unsupported frontmatter line: {raw_line}"

        key, value = raw_line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if not key:
            return None, f"Invalid frontmatter key in line: {raw_line}"

        if value.startswith('"') and value.endswith('"') and len(value) >= 2:
            parsed[key] = value[1:-1]
        elif value.startswith("'") and value.endswith("'") and len(value) >= 2:
            parsed[key] = value[1:-1]
        elif value == "":
            parsed[key] = None
        else:
            parsed[key] = value

    return parsed, None


def local_quick_validate(skill_dir: Path) -> tuple[bool, str]:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text()
    if not content.startswith("---"):
        return False, "No YAML frontmatter found"

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)
    frontmatter, parse_error = parse_frontmatter_minimal(frontmatter_text)
    if parse_error:
        return False, parse_error
    if not isinstance(frontmatter, dict):
        return False, "Frontmatter must be a YAML dictionary"

    allowed_properties = {"name", "description", "license", "allowed-tools", "metadata"}
    unexpected_keys = set(frontmatter.keys()) - allowed_properties
    if unexpected_keys:
        unexpected = ", ".join(sorted(unexpected_keys))
        allowed = ", ".join(sorted(allowed_properties))
        return (
            False,
            f"Unexpected key(s) in SKILL.md frontmatter: {unexpected}. Allowed properties are: {allowed}",
        )

    name = str(frontmatter.get("name", "")).strip()
    if not name:
        return False, "Missing 'name' in frontmatter"
    if not re.match(r"^[a-z0-9-]+$", name):
        return False, f"Name '{name}' should be hyphen-case"
    if name.startswith("-") or name.endswith("-") or "--" in name:
        return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
    if len(name) > MAX_SKILL_NAME_LENGTH:
        return False, f"Name is too long ({len(name)} characters). Maximum is {MAX_SKILL_NAME_LENGTH}."

    description = str(frontmatter.get("description", "")).strip()
    if not description:
        return False, "Missing 'description' in frontmatter"
    if "<" in description or ">" in description:
        return False, "Description cannot contain angle brackets (< or >)"
    if len(description) > 1024:
        return False, f"Description is too long ({len(description)} characters). Maximum is 1024."

    return True, "Local fallback validation passed."


def run_quick_validate(skill_dir: Path) -> tuple[bool, str]:
    validator = Path.home() / ".codex/skills/.system/skill-creator/scripts/quick_validate.py"
    if validator.exists():
        proc = subprocess.run(
            [sys.executable, str(validator), str(skill_dir)],
            capture_output=True,
            text=True,
            check=False,
        )
        output = (proc.stdout + proc.stderr).strip()
        return proc.returncode == 0, output

    return local_quick_validate(skill_dir)


def check_file_exists(skill_dir: Path) -> tuple[bool, list[str]]:
    missing = [path for path in REQUIRED_FILES if not (skill_dir / path).exists()]
    return not missing, missing


def require_text(path: Path, needles: list[str]) -> tuple[bool, list[str]]:
    content = path.read_text()
    missing = [needle for needle in needles if needle not in content]
    return not missing, missing


def run_command(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)


def run_json(cmd: list[str], cwd: Path) -> tuple[bool, dict | list | None, str]:
    proc = run_command(cmd, cwd)
    output = (proc.stdout or proc.stderr).strip()
    if proc.returncode != 0:
        return False, None, output
    try:
        return True, json.loads(proc.stdout), output
    except json.JSONDecodeError as exc:
        return False, None, f"{output}\nJSON decode error: {exc}"


def main() -> int:
    skill_dir = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    checks: list[tuple[str, bool, str]] = []

    valid, message = run_quick_validate(skill_dir)
    checks.append(("skill-creator quick validation", valid, message))

    exists_ok, missing = check_file_exists(skill_dir)
    checks.append(
        (
            "required file set",
            exists_ok,
            "all required files present" if exists_ok else f"missing: {', '.join(missing)}",
        )
    )

    skill_ok, skill_missing = require_text(
        skill_dir / "SKILL.md",
        [
            "task_light",
            "task_full",
            "agenda_review",
            "promotion_review",
            "scripts/evolution_runtime.py",
            "generated dashboards",
        ],
    )
    checks.append(
        (
            "phase-aware skill contract",
            skill_ok,
            "complete" if skill_ok else f"missing text: {', '.join(skill_missing)}",
        )
    )

    coordinator_ok, coordinator_missing = require_text(
        skill_dir / "system/coordinator.md",
        [
            "Mode Contract",
            "task_light",
            "task_full",
            "agenda_review",
            "promotion_review",
            "Canonical Workspace",
        ],
    )
    checks.append(
        (
            "coordinator mode gates",
            coordinator_ok,
            "complete" if coordinator_ok else f"missing text: {', '.join(coordinator_missing)}",
        )
    )

    readme_ok, readme_missing = require_text(
        skill_dir / "README.md",
        [
            "phase-aware",
            "evolution_runtime.py",
            "records/",
            "manifest.json",
        ],
    )
    checks.append(
        (
            "runtime README coverage",
            readme_ok,
            "complete" if readme_ok else f"missing text: {', '.join(readme_missing)}",
        )
    )

    install_ok, install_missing = require_text(
        skill_dir / "install.md",
        [
            "Canonical records",
            "manifest.json",
            "evolution_runtime.py rebuild-index",
        ],
    )
    checks.append(
        (
            "install guide coverage",
            install_ok,
            "complete" if install_ok else f"missing text: {', '.join(install_missing)}",
        )
    )

    with tempfile.TemporaryDirectory(prefix="self-evo-evals-") as tmpdir_raw:
        tmpdir = Path(tmpdir_raw)
        workspace = tmpdir / ".evolution"
        legacy = tmpdir / ".learnings"
        legacy.mkdir()
        (legacy / "LEARNINGS.md").write_text("# Legacy Learnings\n\n- verify contracts before guessing flags\n")

        bootstrap = run_command(
            [str(skill_dir / "scripts/bootstrap-workspace.sh"), str(workspace), "--migrate-from", str(legacy)],
            skill_dir,
        )
        bootstrap_ok = bootstrap.returncode == 0
        bootstrap_detail = bootstrap.stdout.strip() or bootstrap.stderr.strip()
        checks.append(("bootstrap workspace", bootstrap_ok, bootstrap_detail))

        manifest_path = workspace / "index/manifest.json"
        manifest_ok = manifest_path.exists()
        manifest = json.loads(manifest_path.read_text()) if manifest_ok else {}
        checks.append(
            (
                "manifest generation",
                manifest_ok and manifest.get("record_count", 0) >= 11,
                f"record_count={manifest.get('record_count', 0)}",
            )
        )

        dirs_ok = all(
            (workspace / rel).is_dir()
            for rel in [
                "records/learnings",
                "records/errors",
                "records/feature_requests",
                "records/capabilities",
                "records/training_units",
                "records/evaluations",
                "records/agenda",
            ]
        )
        checks.append(("canonical record layout", dirs_ok, "all record directories present" if dirs_ok else "missing record directory"))

        classify_light_ok, classify_light, classify_light_detail = run_json(
            [
                sys.executable,
                str(skill_dir / "scripts/evolution_runtime.py"),
                "classify-task",
                "--workspace",
                str(workspace),
                "--prompt",
                "Update a familiar README sentence and verify the wording before sending it.",
            ],
            skill_dir,
        )
        checks.append(
            (
                "task_light mode classification",
                classify_light_ok and isinstance(classify_light, dict) and classify_light.get("mode") == "task_light",
                classify_light_detail,
            )
        )

        classify_full_ok, classify_full, classify_full_detail = run_json(
            [
                sys.executable,
                str(skill_dir / "scripts/evolution_runtime.py"),
                "classify-task",
                "--workspace",
                str(workspace),
                "--prompt",
                "I need to modify a production deployment workflow I have never touched before.",
            ],
            skill_dir,
        )
        checks.append(
            (
                "task_full mode classification",
                classify_full_ok and isinstance(classify_full, dict) and classify_full.get("mode") == "task_full",
                classify_full_detail,
            )
        )

        classify_agenda_ok, classify_agenda, classify_agenda_detail = run_json(
            [
                sys.executable,
                str(skill_dir / "scripts/evolution_runtime.py"),
                "classify-task",
                "--workspace",
                str(workspace),
                "--prompt",
                "I have completed five meaningful task cycles and need a learning agenda review before the next unfamiliar project.",
            ],
            skill_dir,
        )
        checks.append(
            (
                "agenda review classification",
                classify_agenda_ok and isinstance(classify_agenda, dict) and classify_agenda.get("mode") == "agenda_review",
                classify_agenda_detail,
            )
        )

        classify_promo_ok, classify_promo, classify_promo_detail = run_json(
            [
                sys.executable,
                str(skill_dir / "scripts/evolution_runtime.py"),
                "classify-task",
                "--workspace",
                str(workspace),
                "--prompt",
                "A trained verification-first strategy transferred to a new release automation task. Evaluate whether it should be promoted.",
            ],
            skill_dir,
        )
        checks.append(
            (
                "promotion review classification",
                classify_promo_ok and isinstance(classify_promo, dict) and classify_promo.get("mode") == "promotion_review",
                classify_promo_detail,
            )
        )

        retrieve_ok, retrieve_data, retrieve_detail = run_json(
            [
                sys.executable,
                str(skill_dir / "scripts/evolution_runtime.py"),
                "retrieve-context",
                "--workspace",
                str(workspace),
                "--mode",
                "task_light",
                "--prompt",
                "verification and retrieval check for a familiar edit",
            ],
            skill_dir,
        )
        retrieve_pass = (
            retrieve_ok
            and isinstance(retrieve_data, dict)
            and retrieve_data.get("record_count", 99) <= 3
        )
        checks.append(("selective task_light retrieval", retrieve_pass, retrieve_detail))

        record_ok, record_data, record_detail = run_json(
            [
                sys.executable,
                str(skill_dir / "scripts/evolution_runtime.py"),
                "record-incident",
                "--workspace",
                str(workspace),
                "--source",
                "error",
                "--title",
                "guessed-release-flag",
                "--summary",
                "Guessed a release flag instead of validating the command contract.",
                "--capability",
                "verification",
                "--trigger-signature",
                "unknown CLI flag on release workflows",
                "--prompt-text",
                "Edited a release command by guessing a flag name and the user corrected it.",
                "--linked-record",
                "CAP-BOOTSTRAP-004",
            ],
            skill_dir,
        )
        record_pass = record_ok and isinstance(record_data, dict) and str(record_data.get("record_id", "")).startswith("ERR-")
        checks.append(("record incident writes canonical evidence", record_pass, record_detail))

        manifest_after = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
        checks.append(
            (
                "manifest refresh after write",
                manifest_after.get("record_count", 0) >= manifest.get("record_count", 0) + 1,
                f"record_count={manifest_after.get('record_count', 0)}",
            )
        )

        agenda_ok, agenda_data, agenda_detail = run_json(
            [
                sys.executable,
                str(skill_dir / "scripts/evolution_runtime.py"),
                "review-agenda",
                "--workspace",
                str(workspace),
            ],
            skill_dir,
        )
        agenda_focus = agenda_data.get("active_focus", []) if isinstance(agenda_data, dict) else []
        checks.append(
            (
                "agenda review output",
                agenda_ok and 1 <= len(agenda_focus) <= 3,
                agenda_detail,
            )
        )

        evaluate_ok, evaluate_data, evaluate_detail = run_json(
            [
                sys.executable,
                str(skill_dir / "scripts/evolution_runtime.py"),
                "evaluate",
                "--workspace",
                str(workspace),
                "--subject",
                "CAP-BOOTSTRAP-004",
            ],
            skill_dir,
        )
        checks.append(
            (
                "evaluation output",
                evaluate_ok and isinstance(evaluate_data, dict) and "promotion_ready" in evaluate_data,
                evaluate_detail,
            )
        )

        legacy_index = workspace / "legacy-self-improving/IMPORT_INDEX.md"
        checks.append(
            (
                "legacy migration compatibility",
                legacy_index.exists(),
                "legacy import index present" if legacy_index.exists() else "missing legacy import index",
            )
        )

    evals = json.loads((skill_dir / "evals/evals.json").read_text())
    eval_ids = {str(item["id"]) for item in evals.get("evals", [])}
    checks.append(
        (
            "eval scenario coverage",
            {"task-light-restraint", "missed-retrieval-recovery", "pre-task-risk-diagnosis"}.issubset(eval_ids),
            ", ".join(sorted(eval_ids)),
        )
    )

    suite = json.loads((skill_dir / "benchmarks/suite.json").read_text())
    scenario_ids = {item["id"] for item in suite.get("scenarios", [])}
    checks.append(
        (
            "benchmark scenario suite",
            {"task-light-restraint", "missed-retrieval-recovery", "agenda-review", "evaluation-and-promotion"}.issubset(scenario_ids),
            ", ".join(sorted(scenario_ids)),
        )
    )

    passed = sum(1 for _, ok, _ in checks if ok)
    total = len(checks)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    report_lines = [
        "# Evaluation Report",
        "",
        "Skill under test: `self-evolving-agent`",
        "",
        f"Date: {today}",
        "",
        "## Summary",
        "",
        f"- Passed {passed}/{total} checks",
    ]

    for name, ok, detail in checks:
        report_lines.extend(
            [
                "",
                f"## {name}",
                "",
                f"- Result: {'pass' if ok else 'fail'}",
                f"- Detail: {detail}",
            ]
        )

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    report_dir = skill_dir / "eval-results" / f"structural-{timestamp}"
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "report.md").write_text("\n".join(report_lines) + "\n")

    print("\n".join(report_lines))
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
