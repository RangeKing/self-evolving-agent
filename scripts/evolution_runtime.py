#!/usr/bin/env python3
"""
Phase-aware control plane for the self-evolving-agent workspace.

The runtime keeps canonical records under `.evolution/records/` and generates:
- `.evolution/index/manifest.json`
- human-readable summary ledgers at the workspace root
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


UTC = timezone.utc

GENERIC_FRONTMATTER_ORDER = [
    "id",
    "type",
    "title",
    "created_at",
    "updated_at",
    "tags",
    "linked_records",
    "trigger_signature",
]

RECORD_TYPES: dict[str, dict[str, Any]] = {
    "learning": {
        "dir": "learnings",
        "prefix": "LRN",
        "ledger": "LEARNINGS.md",
        "header": "# Learnings Ledger",
        "description": "Generated view of canonical learning records.",
        "sort": ("updated_at", "id"),
        "render_fields": [
            ("created_at", "Logged"),
            ("priority", "Priority"),
            ("state", "State"),
            ("capability", "Area"),
        ],
        "empty": "No learning records yet.",
    },
    "error": {
        "dir": "errors",
        "prefix": "ERR",
        "ledger": "ERRORS.md",
        "header": "# Error Ledger",
        "description": "Generated view of canonical failure and diagnostic records.",
        "sort": ("updated_at", "id"),
        "render_fields": [
            ("created_at", "Logged"),
            ("priority", "Priority"),
            ("status", "Status"),
            ("capability", "Primary Capability"),
        ],
        "empty": "No error records yet.",
    },
    "feature_request": {
        "dir": "feature_requests",
        "prefix": "FEAT",
        "ledger": "FEATURE_REQUESTS.md",
        "header": "# Feature Requests Ledger",
        "description": "Generated view of canonical feature-request records.",
        "sort": ("updated_at", "id"),
        "render_fields": [
            ("created_at", "Logged"),
            ("priority", "Priority"),
            ("status", "Status"),
            ("capability", "Related Capability"),
        ],
        "empty": "No feature-request records yet.",
    },
    "capability": {
        "dir": "capabilities",
        "prefix": "CAP",
        "ledger": "CAPABILITIES.md",
        "header": "# Capability Map",
        "description": "Generated view of canonical capability records.",
        "sort": ("id",),
        "render_fields": [
            ("level", "Level"),
            ("assessment_status", "Assessment Status"),
            ("confidence", "Confidence"),
            ("last_reviewed", "Last Reviewed"),
        ],
        "empty": "No capability records yet.",
    },
    "training_unit": {
        "dir": "training_units",
        "prefix": "TRN",
        "ledger": "TRAINING_UNITS.md",
        "header": "# Training Units",
        "description": "Generated view of canonical deliberate-practice records.",
        "sort": ("updated_at", "id"),
        "render_fields": [
            ("capability", "Capability"),
            ("status", "Status"),
            ("priority", "Priority"),
            ("created_at", "Created"),
            ("trigger_signature", "Trigger Signature"),
        ],
        "empty": "No training units yet.",
    },
    "evaluation": {
        "dir": "evaluations",
        "prefix": "EVL",
        "ledger": "EVALUATIONS.md",
        "header": "# Evaluations Ledger",
        "description": "Generated view of canonical evaluation records.",
        "sort": ("updated_at", "id"),
        "render_fields": [
            ("capability", "Capability"),
            ("state", "State"),
            ("reviewed_at", "Reviewed"),
            ("reviewer_judgment", "Reviewer Judgment"),
        ],
        "empty": "No evaluation records yet.",
    },
    "agenda": {
        "dir": "agenda",
        "prefix": "AGD",
        "ledger": "LEARNING_AGENDA.md",
        "header": "# Learning Agenda",
        "description": "Generated view of canonical agenda records.",
        "sort": ("updated_at", "id"),
        "render_fields": [
            ("reviewed_at", "Reviewed"),
            ("review_trigger", "Review Trigger"),
            ("status", "Status"),
            ("next_review_trigger", "Next Review Trigger"),
        ],
        "empty": "No agenda reviews yet.",
    },
}

MODE_RETRIEVAL_TYPES = {
    "task_light": {"learning", "error", "capability"},
    "task_full": {"learning", "error", "capability", "training_unit", "evaluation", "agenda"},
    "agenda_review": {"agenda", "capability", "training_unit", "evaluation", "error"},
    "promotion_review": {"evaluation", "learning", "training_unit", "capability", "agenda"},
}

MODE_LIMITS = {
    "task_light": 3,
    "task_full": 8,
    "agenda_review": 6,
    "promotion_review": 6,
}

LADDER = ["recorded", "understood", "practiced", "passed", "generalized", "promoted"]

REQUIRED_GENERIC_KEYS = {
    "id",
    "type",
    "title",
    "created_at",
    "updated_at",
    "tags",
    "linked_records",
    "trigger_signature",
}


@dataclass
class Record:
    path: Path
    relpath: str
    meta: dict[str, Any]
    body: str

    @property
    def id(self) -> str:
        return str(self.meta["id"])

    @property
    def type(self) -> str:
        return str(self.meta["type"])

    @property
    def title(self) -> str:
        return str(self.meta["title"])

    @property
    def linked_records(self) -> list[str]:
        linked = self.meta.get("linked_records", [])
        return linked if isinstance(linked, list) else []

    @property
    def tags(self) -> list[str]:
        tags = self.meta.get("tags", [])
        return tags if isinstance(tags, list) else []

    @property
    def updated_at(self) -> str:
        return str(self.meta.get("updated_at", ""))

    def summary(self) -> str:
        for raw in self.body.splitlines():
            line = raw.strip()
            if not line:
                continue
            if line.startswith("#") or line.startswith("- ") or line.startswith("```"):
                continue
            return collapse_ws(line)
        return self.title


def collapse_ws(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def tokenize(text: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9][a-z0-9_-]{1,}", text.lower())}


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "record"


def parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def days_since(value: str | None) -> float | None:
    parsed = parse_datetime(value)
    if parsed is None:
        return None
    delta = datetime.now(UTC) - parsed.astimezone(UTC)
    return max(delta.total_seconds(), 0) / 86400.0


def frontmatter_parse_value(raw: str) -> Any:
    raw = raw.strip()
    if raw == "":
        return ""
    if raw[0] in '[{"' or raw in {"true", "false", "null"} or re.fullmatch(r"-?\d+(\.\d+)?", raw):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            pass
    if raw.startswith("'") and raw.endswith("'") and len(raw) >= 2:
        return raw[1:-1]
    return raw


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        raise ValueError("record missing frontmatter delimiter")
    try:
        _, frontmatter_text, body = text.split("---\n", 2)
    except ValueError as exc:
        raise ValueError("record frontmatter is malformed") from exc

    meta: dict[str, Any] = {}
    for line in frontmatter_text.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"unsupported frontmatter line: {line}")
        key, raw = line.split(":", 1)
        meta[key.strip()] = frontmatter_parse_value(raw)
    return meta, body.lstrip("\n")


def dump_frontmatter(meta: dict[str, Any]) -> str:
    keys = []
    seen = set()
    for key in GENERIC_FRONTMATTER_ORDER:
        if key in meta:
            keys.append(key)
            seen.add(key)
    for key in sorted(meta):
        if key not in seen:
            keys.append(key)
    lines = ["---"]
    for key in keys:
        lines.append(f"{key}: {json.dumps(meta[key], ensure_ascii=False)}")
    lines.append("---")
    return "\n".join(lines)


def write_text_if_changed(path: Path, content: str) -> None:
    if path.exists() and path.read_text() == content:
        return
    path.write_text(content)


def ensure_workspace(workspace: Path) -> None:
    records_root = workspace / "records"
    for config in RECORD_TYPES.values():
        (records_root / config["dir"]).mkdir(parents=True, exist_ok=True)
    (workspace / "index").mkdir(parents=True, exist_ok=True)


def resolve_workspace(raw: str | None) -> Path:
    if raw:
        return Path(raw).expanduser().resolve()
    cwd = Path.cwd().resolve()
    if (cwd / "records").is_dir():
        return cwd
    if (cwd / ".evolution" / "records").is_dir():
        return (cwd / ".evolution").resolve()
    return (cwd / ".evolution").resolve()


def validate_record(record: Record) -> None:
    missing = sorted(REQUIRED_GENERIC_KEYS - set(record.meta))
    if missing:
        raise ValueError(f"{record.path}: missing required frontmatter keys: {', '.join(missing)}")
    if record.type not in RECORD_TYPES:
        raise ValueError(f"{record.path}: unsupported record type '{record.type}'")
    if not isinstance(record.meta.get("tags"), list):
        raise ValueError(f"{record.path}: tags must be a list")
    if not isinstance(record.meta.get("linked_records"), list):
        raise ValueError(f"{record.path}: linked_records must be a list")


def load_record(path: Path, workspace: Path) -> Record:
    meta, body = split_frontmatter(path.read_text())
    relpath = str(path.relative_to(workspace))
    record = Record(path=path, relpath=relpath, meta=meta, body=body.rstrip() + "\n")
    validate_record(record)
    return record


def load_records(workspace: Path) -> list[Record]:
    ensure_workspace(workspace)
    records: list[Record] = []
    for config in RECORD_TYPES.values():
        record_dir = workspace / "records" / config["dir"]
        for path in sorted(record_dir.glob("*.md")):
            records.append(load_record(path, workspace))
    return records


def extract_active_agenda(records: list[Record]) -> tuple[list[str], list[str]]:
    agenda_ids: list[str] = []
    focus: list[str] = []
    for record in records:
        if record.type != "agenda":
            continue
        if str(record.meta.get("status", "")).lower() != "active":
            continue
        agenda_ids.append(record.id)
        active_focus = record.meta.get("active_focus", [])
        if isinstance(active_focus, list):
            for item in active_focus:
                if isinstance(item, str):
                    focus.append(item)
    return agenda_ids, focus


def build_manifest(records: list[Record]) -> dict[str, Any]:
    active_agenda_ids, active_focus = extract_active_agenda(records)
    manifest_records: list[dict[str, Any]] = []
    for record in records:
        summary = record.summary()
        manifest_records.append(
            {
                "id": record.id,
                "type": record.type,
                "title": record.title,
                "path": record.relpath,
                "updated_at": record.meta.get("updated_at"),
                "created_at": record.meta.get("created_at"),
                "tags": record.tags,
                "linked_records": record.linked_records,
                "trigger_signature": record.meta.get("trigger_signature", ""),
                "status": record.meta.get("status") or record.meta.get("state") or "",
                "state": record.meta.get("state", ""),
                "capability": record.meta.get("capability", ""),
                "level": record.meta.get("level", ""),
                "confidence": record.meta.get("confidence", ""),
                "summary": summary,
            }
        )
    return {
        "generated_at": utc_now(),
        "workspace_layout_version": 2,
        "record_count": len(manifest_records),
        "active_agenda_ids": active_agenda_ids,
        "active_focus": sorted(dict.fromkeys(active_focus)),
        "records": manifest_records,
    }


def score_learning_state(state: str) -> int:
    try:
        return LADDER.index(state)
    except ValueError:
        return -1


def parse_level(level: str) -> int:
    match = re.search(r"L(\d+)", level)
    return int(match.group(1)) if match else 0


def recency_bonus(updated_at: str | None) -> float:
    age_days = days_since(updated_at)
    if age_days is None:
        return 0.0
    return max(0.0, 3.0 - min(age_days, 30.0) / 10.0)


def classify_task(prompt: str, manifest: dict[str, Any]) -> dict[str, Any]:
    lower = prompt.lower()
    tokens = tokenize(prompt)
    unfamiliar_markers = {
        "never",
        "unfamiliar",
        "first",
        "unknown",
        "new",
        "novel",
        "untouched",
    }
    mixed_markers = {
        "refactor",
        "follow-up",
        "existing",
        "unclear",
        "diagnose",
    }
    high_consequence_markers = {
        "production",
        "deploy",
        "deployment",
        "release",
        "security",
        "payment",
        "auth",
        "migration",
        "customer",
        "incident",
    }
    medium_consequence_markers = {
        "workflow",
        "ci",
        "config",
        "multi-file",
        "integration",
        "automation",
    }
    long_horizon_markers = {
        "long-horizon",
        "roadmap",
        "multi-step",
        "across",
        "sessions",
        "migration",
        "program",
    }
    medium_horizon_markers = {
        "feature",
        "project",
        "refactor",
        "review",
        "workflow",
        "integration",
    }
    recurrence_markers = {
        "again",
        "recurring",
        "repeat",
        "repeated",
        "similar",
        "user corrected",
        "rescue",
    }
    promotion_markers = {"promote", "promotion", "generalize", "generalized", "transfer", "promoted"}
    agenda_markers = {"agenda", "five", "5", "cycles", "structural", "review"}

    if promotion_markers & tokens or "promotion decision" in lower:
        mode = "promotion_review"
    else:
        mode = "task_light"

    if unfamiliar_markers & tokens or "never touched" in lower:
        novelty = "unfamiliar"
    elif mixed_markers & tokens:
        novelty = "mixed"
    else:
        novelty = "familiar"

    if high_consequence_markers & tokens:
        consequence = "high"
    elif medium_consequence_markers & tokens:
        consequence = "medium"
    else:
        consequence = "low"

    if long_horizon_markers & tokens:
        horizon = "long"
    elif medium_horizon_markers & tokens:
        horizon = "medium"
    else:
        horizon = "short"

    recurring = bool(recurrence_markers & tokens) or "user corrected" in lower
    agenda_due = bool(agenda_markers & tokens) or "after_5_cycles" in json.dumps(manifest.get("active_focus", []))

    if mode != "promotion_review":
        if agenda_due and ("agenda" in lower or "next unfamiliar project" in lower or "five meaningful task cycles" in lower):
            mode = "agenda_review"
        elif novelty != "familiar" or consequence != "low" or horizon != "short" or recurring:
            mode = "task_full"
        else:
            mode = "task_light"

    rationale = []
    rationale.append(f"novelty={novelty}")
    rationale.append(f"consequence={consequence}")
    rationale.append(f"horizon={horizon}")
    if recurring:
        rationale.append("recurrence detected")
    if agenda_due:
        rationale.append("agenda review trigger present")
    if mode == "promotion_review":
        rationale.append("promotion or transfer language detected")

    return {
        "mode": mode,
        "novelty": novelty,
        "consequence": consequence,
        "horizon": horizon,
        "agenda_due": agenda_due,
        "rationale": rationale,
    }


def score_record(
    record: dict[str, Any],
    query_tokens: set[str],
    mode: str,
    active_agenda_ids: set[str],
    active_focus: set[str],
) -> tuple[float, list[str]]:
    score = 0.0
    reasons: list[str] = []

    trigger_tokens = tokenize(str(record.get("trigger_signature", "")))
    trigger_overlap = len(query_tokens & trigger_tokens)
    if trigger_overlap:
        score += trigger_overlap * 5
        reasons.append("trigger signature overlap")

    title_tokens = tokenize(f"{record.get('title', '')} {record.get('summary', '')}")
    title_overlap = len(query_tokens & title_tokens)
    if title_overlap:
        score += title_overlap * 3
        reasons.append("title or summary match")

    tag_overlap = len(query_tokens & set(record.get("tags", [])))
    if tag_overlap:
        score += tag_overlap * 2
        reasons.append("tag match")

    capability = str(record.get("capability", "")).lower()
    if capability and (capability in active_focus or capability in " ".join(query_tokens)):
        score += 4
        reasons.append("capability match")

    status = str(record.get("status") or record.get("state") or "").lower()
    if status in {"active", "open", "recorded", "practiced", "passed", "generalized", "provisional"}:
        score += 2
        reasons.append("active or open state")

    linked = set(record.get("linked_records", []))
    if linked & active_agenda_ids:
        score += 3
        reasons.append("linked to active agenda")

    score += recency_bonus(record.get("updated_at"))
    if recency_bonus(record.get("updated_at")) > 0:
        reasons.append("recent evidence")

    if mode == "promotion_review" and record.get("type") == "evaluation":
        score += 3
        reasons.append("promotion review prioritizes evaluations")
    if mode == "agenda_review" and record.get("type") in {"capability", "agenda"}:
        score += 2
        reasons.append("agenda review prioritizes capabilities")

    return score, reasons


def retrieve_context(prompt: str, mode: str, manifest: dict[str, Any]) -> dict[str, Any]:
    allowed_types = MODE_RETRIEVAL_TYPES[mode]
    query_tokens = tokenize(prompt)
    active_agenda_ids = set(manifest.get("active_agenda_ids", []))
    active_focus = set(manifest.get("active_focus", []))
    scored: list[tuple[float, dict[str, Any], list[str]]] = []

    for record in manifest.get("records", []):
        if record["type"] not in allowed_types:
            continue
        score, reasons = score_record(record, query_tokens, mode, active_agenda_ids, active_focus)
        if score <= 0:
            continue
        scored.append((score, record, reasons))

    scored.sort(key=lambda item: (-item[0], item[1]["id"]))
    selected = scored[: MODE_LIMITS[mode]]

    if not selected:
        fallback = []
        for record in manifest.get("records", []):
            if record["type"] not in allowed_types:
                continue
            if record["id"] in active_agenda_ids or record.get("capability") in active_focus:
                fallback.append((1.0, record, ["active agenda fallback"]))
        selected = fallback[: MODE_LIMITS[mode]]

    return {
        "mode": mode,
        "record_count": len(selected),
        "records": [
            {
                "id": record["id"],
                "type": record["type"],
                "title": record["title"],
                "path": record["path"],
                "reason": "; ".join(dict.fromkeys(reasons)) or "relevant context",
            }
            for _, record, reasons in selected
        ],
    }


def next_record_id(record_type: str, workspace: Path) -> str:
    config = RECORD_TYPES[record_type]
    record_dir = workspace / "records" / config["dir"]
    today = datetime.now(UTC).strftime("%Y%m%d")
    prefix = f"{config['prefix']}-{today}-"
    highest = 0
    for path in record_dir.glob("*.md"):
        match = re.search(rf"{re.escape(prefix)}(\d+)", path.name)
        if match:
            highest = max(highest, int(match.group(1)))
    return f"{config['prefix']}-{today}-{highest + 1:03d}"


def build_record_body(source: str, meta: dict[str, Any], args: argparse.Namespace) -> str:
    linked_lines = [f"- {item}" for item in meta["linked_records"]] or ["- none yet"]
    if source == "error":
        return "\n".join(
            [
                "### Summary",
                meta["summary"],
                "",
                "### Error",
                "```text",
                args.error_text or meta["summary"],
                "```",
                "",
                "### Context",
                f"- Task: {args.prompt_text or 'not provided'}",
                f"- Source: {args.source}",
                f"- Environment: {args.environment or 'not provided'}",
                "",
                "### Diagnostic Hypothesis",
                args.diagnostic_hypothesis or "Verification or execution discipline weakness should be investigated.",
                "",
                "### Recurrence Signal",
                args.recurrence_signal or "first_time",
                "",
                "### Suggested Next Step",
                args.next_step or "diagnose",
                "",
                "### Linked Records",
                *linked_lines,
                "",
            ]
        ).strip() + "\n"

    return "\n".join(
        [
            "### Summary",
            meta["summary"],
            "",
            "### What Happened",
            args.prompt_text or meta["summary"],
            "",
            "### Correct Understanding",
            args.correct_understanding or "Capture the updated understanding explicitly before promoting it.",
            "",
            "### Why It Matters",
            args.why_it_matters or "This lesson should change future execution, not only today's log.",
            "",
            "### Counterexample",
            args.counterexample or "Do not apply this lesson blindly outside its trigger signature.",
            "",
            "### Linked Records",
            *linked_lines,
            "",
        ]
    ).strip() + "\n"


def write_record(workspace: Path, record_type: str, meta: dict[str, Any], body: str) -> Path:
    ensure_workspace(workspace)
    config = RECORD_TYPES[record_type]
    record_dir = workspace / "records" / config["dir"]
    filename = f"{meta['id'].lower()}-{slugify(meta['title'])}.md"
    path = record_dir / filename
    content = dump_frontmatter(meta) + "\n\n" + body.rstrip() + "\n"
    write_text_if_changed(path, content)
    return path


def render_record(record: Record) -> list[str]:
    config = RECORD_TYPES[record.type]
    lines = [f"## [{record.id}] {record.title}", ""]
    for key, label in config["render_fields"]:
        value = record.meta.get(key)
        if value in (None, "", []):
            continue
        if isinstance(value, list):
            value = ", ".join(str(item) for item in value)
        lines.append(f"**{label}**: {value}")
    if lines[-1] != "":
        lines.append("")
    if record.body.strip():
        lines.extend(record.body.rstrip().splitlines())
        lines.append("")
    lines.append("---")
    lines.append("")
    return lines


def rebuild_index(workspace: Path) -> dict[str, Any]:
    ensure_workspace(workspace)
    records = load_records(workspace)
    manifest = build_manifest(records)
    manifest_path = workspace / "index" / "manifest.json"
    write_text_if_changed(manifest_path, json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")

    grouped: dict[str, list[Record]] = defaultdict(list)
    for record in records:
        grouped[record.type].append(record)

    for record_type, config in RECORD_TYPES.items():
        sort_keys = config["sort"]

        def sort_key(record: Record) -> tuple[Any, ...]:
            values: list[Any] = []
            for key in sort_keys:
                value = record.meta.get(key, "")
                values.append(value)
            return tuple(values)

        ordered = sorted(grouped.get(record_type, []), key=sort_key, reverse=("updated_at" in sort_keys))
        lines = [
            config["header"],
            "",
            config["description"],
            "",
            f"Generated from canonical records on {manifest['generated_at']}.",
            "",
        ]
        if ordered:
            for record in ordered:
                lines.extend(render_record(record))
        else:
            lines.extend([config["empty"], ""])
        write_text_if_changed(workspace / config["ledger"], "\n".join(lines).rstrip() + "\n")

    return manifest


def load_manifest(workspace: Path) -> dict[str, Any]:
    manifest_path = workspace / "index" / "manifest.json"
    if manifest_path.exists():
        return json.loads(manifest_path.read_text())
    return rebuild_index(workspace)


def review_agenda(workspace: Path) -> dict[str, Any]:
    records = load_records(workspace)
    manifest = build_manifest(records)
    active_focus = set(manifest.get("active_focus", []))

    training_counts = Counter()
    error_counts = Counter()
    for record in records:
        capability = str(record.meta.get("capability", ""))
        if not capability:
            continue
        if record.type == "training_unit" and str(record.meta.get("status", "")).lower() in {"open", "active"}:
            training_counts[capability] += 1
        if record.type == "error" and str(record.meta.get("status", "")).lower() in {"open", "investigated"}:
            error_counts[capability] += 1

    ranked: list[tuple[float, Record]] = []
    for record in records:
        if record.type != "capability":
            continue
        level = parse_level(str(record.meta.get("level", "")))
        confidence = str(record.meta.get("confidence", "")).lower()
        score = 0.0
        score += max(0, 5 - level) * 2
        score += {"low": 2, "medium": 1}.get(confidence, 0)
        score += training_counts[record.title] * 2
        score += error_counts[record.title] * 3
        if record.title in active_focus:
            score += 2
        ranked.append((score, record))

    ranked.sort(key=lambda item: (-item[0], item[1].id))
    selected = ranked[:3]
    focus = []
    for score, record in selected:
        focus.append(
            {
                "capability": record.title,
                "score": round(score, 2),
                "why_now": first_section_text(record.body, "### Current Limits")
                or first_section_text(record.body, "### Next Training Focus")
                or record.summary(),
                "exit_criteria": first_section_text(record.body, "### Upgrade Condition")
                or "Advance when repeated transfer evidence appears.",
            }
        )
    return {
        "generated_at": utc_now(),
        "active_focus": focus,
        "active_agenda_ids": manifest.get("active_agenda_ids", []),
    }


def first_section_text(body: str, header: str) -> str:
    lines = body.splitlines()
    capture = False
    collected: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("### "):
            if stripped == header:
                capture = True
                continue
            if capture:
                break
        if capture and stripped:
            collected.append(collapse_ws(stripped.lstrip("- ")))
    return " ".join(collected[:2]).strip()


def evaluate_subject(workspace: Path, subject_id: str) -> dict[str, Any]:
    records = load_records(workspace)
    by_id = {record.id: record for record in records}
    if subject_id not in by_id:
        raise SystemExit(f"Unknown record id: {subject_id}")

    subject = by_id[subject_id]
    related_evaluations = [
        record
        for record in records
        if record.type == "evaluation"
        and (
            record.meta.get("subject_id") == subject_id
            or subject_id in record.linked_records
            or record.title == subject.title
        )
    ]
    related_trainings = [
        record
        for record in records
        if record.type == "training_unit" and (subject_id in record.linked_records or record.meta.get("capability") == subject.title)
    ]
    related_learnings = [
        record
        for record in records
        if record.type == "learning" and subject_id in record.linked_records
    ]

    if related_evaluations:
        latest = max(related_evaluations, key=lambda record: record.meta.get("updated_at", ""))
        state = str(latest.meta.get("state", "recorded"))
        reviewer_judgment = str(latest.meta.get("reviewer_judgment", "insufficient"))
        promotion_ready = score_learning_state(state) >= score_learning_state("generalized") and reviewer_judgment == "sufficient"
        reason = "latest evaluation record"
        evidence_ids = [record.id for record in related_evaluations]
    else:
        state = "recorded"
        if related_trainings:
            state = "practiced"
        if any(str(record.meta.get("status", "")).lower() == "passed" for record in related_trainings):
            state = "passed"
        if related_learnings and related_trainings:
            state = "understood" if state == "recorded" else state
        promotion_ready = False
        reviewer_judgment = "partial" if related_trainings or related_learnings else "insufficient"
        reason = "inferred from linked records"
        evidence_ids = [record.id for record in related_trainings + related_learnings]

    next_decision = "advance state" if reviewer_judgment in {"partial", "sufficient"} else "create training unit"
    if promotion_ready:
        next_decision = "consider promotion"

    return {
        "subject_id": subject_id,
        "subject_title": subject.title,
        "state": state,
        "reviewer_judgment": reviewer_judgment,
        "promotion_ready": promotion_ready,
        "reason": reason,
        "evidence_ids": evidence_ids,
        "next_decision": next_decision,
    }


def handle_classify_task(args: argparse.Namespace) -> None:
    workspace = resolve_workspace(args.workspace)
    manifest = load_manifest(workspace)
    result = classify_task(args.prompt, manifest)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def handle_retrieve_context(args: argparse.Namespace) -> None:
    workspace = resolve_workspace(args.workspace)
    manifest = load_manifest(workspace)
    result = retrieve_context(args.prompt, args.mode, manifest)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def handle_record_incident(args: argparse.Namespace) -> None:
    workspace = resolve_workspace(args.workspace)
    record_type = "error" if args.source == "error" else "learning"
    record_id = next_record_id(record_type, workspace)
    timestamp = utc_now()
    linked_records = sorted(dict.fromkeys(args.linked_record or []))
    tags = sorted(dict.fromkeys(args.tag or []))

    meta = {
        "id": record_id,
        "type": record_type,
        "title": args.title,
        "created_at": timestamp,
        "updated_at": timestamp,
        "tags": tags,
        "linked_records": linked_records,
        "trigger_signature": args.trigger_signature or args.title,
        "summary": args.summary,
        "priority": args.priority,
        "capability": args.capability,
    }

    if record_type == "error":
        meta["status"] = args.status or "open"
    else:
        meta["state"] = args.state or "recorded"

    body = build_record_body(args.source, meta, args)
    path = write_record(workspace, record_type, meta, body)
    rebuild_index(workspace)
    print(
        json.dumps(
            {
                "record_id": record_id,
                "record_type": record_type,
                "path": str(path),
            },
            indent=2,
            ensure_ascii=False,
        )
    )


def handle_review_agenda(args: argparse.Namespace) -> None:
    workspace = resolve_workspace(args.workspace)
    rebuild_index(workspace)
    print(json.dumps(review_agenda(workspace), indent=2, ensure_ascii=False))


def handle_evaluate(args: argparse.Namespace) -> None:
    workspace = resolve_workspace(args.workspace)
    rebuild_index(workspace)
    print(json.dumps(evaluate_subject(workspace, args.subject), indent=2, ensure_ascii=False))


def handle_rebuild_index(args: argparse.Namespace) -> None:
    workspace = resolve_workspace(args.workspace)
    manifest = rebuild_index(workspace)
    print(json.dumps({"workspace": str(workspace), "record_count": manifest["record_count"]}, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Phase-aware runtime for the self-evolving-agent workspace.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    classify_parser = subparsers.add_parser("classify-task", help="Classify a task into an evolution mode.")
    classify_parser.add_argument("--workspace", help="Path to the .evolution workspace.")
    classify_parser.add_argument("--prompt", required=True, help="Task description to classify.")
    classify_parser.set_defaults(func=handle_classify_task)

    retrieve_parser = subparsers.add_parser("retrieve-context", help="Return top relevant records for the selected mode.")
    retrieve_parser.add_argument("--workspace", help="Path to the .evolution workspace.")
    retrieve_parser.add_argument("--prompt", required=True, help="Task description to retrieve against.")
    retrieve_parser.add_argument(
        "--mode",
        required=True,
        choices=sorted(MODE_RETRIEVAL_TYPES),
        help="Evolution mode.",
    )
    retrieve_parser.set_defaults(func=handle_retrieve_context)

    record_parser = subparsers.add_parser("record-incident", help="Write a canonical evidence record.")
    record_parser.add_argument("--workspace", help="Path to the .evolution workspace.")
    record_parser.add_argument("--source", required=True, choices=["error", "reflection"], help="Evidence source.")
    record_parser.add_argument("--title", required=True, help="Record title.")
    record_parser.add_argument("--summary", required=True, help="One-line summary of the incident.")
    record_parser.add_argument("--capability", default="verification", help="Primary capability involved.")
    record_parser.add_argument("--priority", default="medium", help="Priority for the record.")
    record_parser.add_argument("--status", help="Status for error records.")
    record_parser.add_argument("--state", help="State for reflection-derived learning records.")
    record_parser.add_argument("--trigger-signature", help="Retrieval cue for this record.")
    record_parser.add_argument("--prompt-text", help="Original task or reflection context.")
    record_parser.add_argument("--error-text", help="Error output or failure description.")
    record_parser.add_argument("--environment", help="Environment or execution context.")
    record_parser.add_argument("--diagnostic-hypothesis", help="Initial root-cause hypothesis.")
    record_parser.add_argument("--recurrence-signal", help="Recurrence classification.")
    record_parser.add_argument("--next-step", help="Suggested next step.")
    record_parser.add_argument("--correct-understanding", help="Corrected understanding for reflection records.")
    record_parser.add_argument("--why-it-matters", help="Why the learning matters.")
    record_parser.add_argument("--counterexample", help="When not to apply the learning.")
    record_parser.add_argument("--linked-record", action="append", default=[], help="Linked record id. May be repeated.")
    record_parser.add_argument("--tag", action="append", default=[], help="Tag for the record. May be repeated.")
    record_parser.set_defaults(func=handle_record_incident)

    agenda_parser = subparsers.add_parser("review-agenda", help="Return the next 1-3 capability focuses.")
    agenda_parser.add_argument("--workspace", help="Path to the .evolution workspace.")
    agenda_parser.set_defaults(func=handle_review_agenda)

    evaluate_parser = subparsers.add_parser("evaluate", help="Return evaluation state and promotion readiness.")
    evaluate_parser.add_argument("--workspace", help="Path to the .evolution workspace.")
    evaluate_parser.add_argument("--subject", required=True, help="Record id to evaluate.")
    evaluate_parser.set_defaults(func=handle_evaluate)

    rebuild_parser = subparsers.add_parser("rebuild-index", help="Regenerate manifest and human-facing ledgers.")
    rebuild_parser.add_argument("--workspace", help="Path to the .evolution workspace.")
    rebuild_parser.set_defaults(func=handle_rebuild_index)

    return parser


def main(argv: list[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
