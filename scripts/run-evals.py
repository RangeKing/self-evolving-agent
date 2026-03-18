#!/usr/bin/env python3
"""
Repeatable local compliance checks for the self-evolving-agent skill.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "install.md",
    "system/coordinator.md",
    "modules/learning-agenda.md",
    "modules/diagnose.md",
    "modules/capability-map.md",
    "modules/curriculum.md",
    "modules/evaluator.md",
    "modules/promotion.md",
    "modules/reflection.md",
    "assets/LEARNINGS.md",
    "assets/ERRORS.md",
    "assets/FEATURE_REQUESTS.md",
    "assets/CAPABILITIES.md",
    "assets/LEARNING_AGENDA.md",
    "assets/TRAINING_UNITS.md",
    "assets/EVALUATIONS.md",
    "demos/demo-1-diagnosis.md",
    "demos/demo-2-training-loop.md",
    "demos/demo-3-promotion-and-transfer.md",
    "demos/demo-4-agenda-review.md",
    "hooks/openclaw/HOOK.md",
    "hooks/openclaw/handler.ts",
    "scripts/bootstrap-workspace.sh",
    "evals/evals.json",
]


def run_quick_validate(skill_dir: Path) -> tuple[bool, str]:
    validator = Path.home() / ".codex/skills/.system/skill-creator/scripts/quick_validate.py"
    proc = subprocess.run(
        [sys.executable, str(validator), str(skill_dir)],
        capture_output=True,
        text=True,
        check=False,
    )
    output = (proc.stdout + proc.stderr).strip()
    return proc.returncode == 0, output


def check_file_exists(skill_dir: Path) -> tuple[bool, list[str]]:
    missing = [path for path in REQUIRED_FILES if not (skill_dir / path).exists()]
    return not missing, missing


def require_text(path: Path, needles: list[str]) -> tuple[bool, list[str]]:
    content = path.read_text()
    missing = [needle for needle in needles if needle not in content]
    return not missing, missing


def count_bootstrap_capabilities(path: Path) -> int:
    content = path.read_text()
    return content.count("## [CAP-BOOTSTRAP-")


def main() -> int:
    skill_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()

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
            "Control Loop",
            "learning agenda",
            "recorded",
            "promoted",
            "Generate a training unit if weakness or recurrence is detected.",
        ],
    )
    checks.append(
        (
            "skill orchestration contract",
            skill_ok,
            "complete" if skill_ok else f"missing text: {', '.join(skill_missing)}",
        )
    )

    coordinator_ok, coordinator_missing = require_text(
        skill_dir / "system/coordinator.md",
        [
            "Layer 0: Learning Agenda",
            "Control Loop",
            "active learning agenda items",
            "Agenda Decision",
        ],
    )
    checks.append(
        (
            "coordinator control loop",
            coordinator_ok,
            "complete" if coordinator_ok else f"missing text: {', '.join(coordinator_missing)}",
        )
    )

    capability_count = count_bootstrap_capabilities(skill_dir / "assets/CAPABILITIES.md")
    checks.append(
        (
            "seeded capability baseline",
            capability_count >= 10,
            f"{capability_count} bootstrap capability entries",
        )
    )

    agenda_ok, agenda_missing = require_text(
        skill_dir / "assets/LEARNING_AGENDA.md",
        ["### Active Focus", "verification", "execution discipline", "memory retrieval"],
    )
    checks.append(
        (
            "bootstrap learning agenda",
            agenda_ok,
            "complete" if agenda_ok else f"missing text: {', '.join(agenda_missing)}",
        )
    )

    evals = json.loads((skill_dir / "evals/evals.json").read_text())
    eval_count = len(evals.get("evals", []))
    checks.append(
        (
            "eval scenario coverage",
            eval_count >= 4,
            f"{eval_count} eval scenarios",
        )
    )

    demo_ok, demo_missing = require_text(
        skill_dir / "demos/demo-4-agenda-review.md",
        ["## Skill Output", "Learning Agenda", "Active Focus"],
    )
    checks.append(
        (
            "proactive agenda demo",
            demo_ok,
            "complete" if demo_ok else f"missing text: {', '.join(demo_missing)}",
        )
    )

    hook_ok, hook_missing = require_text(
        skill_dir / "hooks/openclaw/handler.ts",
        ["learning agenda", "refresh the learning agenda if priorities changed"],
    )
    checks.append(
        (
            "hook reminder coverage",
            hook_ok,
            "complete" if hook_ok else f"missing text: {', '.join(hook_missing)}",
        )
    )

    passed = sum(1 for _, ok, _ in checks if ok)
    total = len(checks)

    report_lines = [
        "# Evaluation Report",
        "",
        "Skill under test: `self-evolving-agent`",
        "",
        "Date: 2026-03-18",
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

    report_dir = skill_dir / "eval-results/iteration-2"
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "report.md").write_text("\n".join(report_lines) + "\n")

    print("\n".join(report_lines))
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
