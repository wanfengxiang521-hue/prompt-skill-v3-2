#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_REFERENCES = (
    "compiler-director-lock-input.md",
    "compiler-mode-and-compile.md",
    "compiler-reference-contract.md",
    "compiler-continuity-and-density.md",
    "compiler-model-mechanics-and-repair.md",
    "compiler-production-gates.md",
    "compiler-evaluation.md",
    "v3-output-contract.md",
    "x-prompt-methods.md",
)


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_prompt_skill_v3.py <skill-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).expanduser().resolve()
    skill_path = root / "SKILL.md"
    ui_path = root / "agents" / "openai.yaml"
    skill = read(skill_path)
    ui = read(ui_path)
    references = {
        name: read(root / "references" / name) for name in REQUIRED_REFERENCES
    }
    corpus = "\n".join([skill, ui, *references.values()])

    checks: list[tuple[str, bool, str]] = [
        (
            "P001",
            bool(re.search(r"(?m)^name:\s*prompt-skill-v3-2\s*$", skill)),
            "SKILL.md uses the unique name prompt-skill-v3-2",
        ),
        (
            "P002",
            "display_name:" in ui and "V3" in ui,
            "agents/openai.yaml exposes the V3 display name",
        ),
        (
            "P003",
            all(references.values())
            and all(f"references/{name}" in skill for name in REQUIRED_REFERENCES),
            "all required V3 references exist and are discoverable from SKILL.md",
        ),
        (
            "P004",
            "不得新增任何导演决定" in corpus,
            "compile-only director boundary is explicit",
        ),
        (
            "P005",
            "锁定台词逐字保留" in corpus or "锁定对白逐字不变" in corpus,
            "locked dialogue remains verbatim",
        ),
        (
            "P006",
            "默认最终交付只输出可直接复制给生成模型的纯提示词" in corpus,
            "default delivery is copy-ready prompt only",
        ),
        (
            "P007",
            "默认禁止第三方动态视频参考" in corpus
            or "第三方动态视频" in corpus and "禁止" in corpus,
            "third-party dynamic video references are excluded",
        ),
        (
            "P008",
            all(term in corpus for term in ("参考权限矩阵", "允许控制", "禁止控制", "优先级")),
            "reference permissions and conflict priority are defined",
        ),
        (
            "P009",
            "纯净母版" in corpus
            and all(
                term in corpus
                for term in ("must-preserve", "illegible", "forbidden", "add-in-post")
            ),
            "clean-master and text-disposition contracts are defined",
        ),
        (
            "P010",
            "闭合终态" in corpus,
            "runtime holds require a closed endpoint",
        ),
        (
            "P011",
            "显式替换" in corpus and "删除 Y" in corpus,
            "repairs replace and remove old conflicting rules",
        ),
        (
            "P012",
            all(
                term in corpus
                for term in (
                    "SUCCESS",
                    "BLOCKED_UNSOLVABLE",
                    "BLOCKED_MISSING_ASSET",
                    "FAILED",
                )
            ),
            "solvability outcomes are explicit",
        ),
        (
            "P013",
            not re.search(r"(?i)\b(TBD|TODO|FIXME)\b|待填写|占位内容", corpus),
            "package contains no unfinished scaffold placeholders",
        ),
        (
            "P014",
            "# 提示词 Skill V3" in skill,
            "entrypoint identifies V3",
        ),
        (
            "P015",
            "控制流外置" in corpus,
            "workflow control is kept outside the generation prompt",
        ),
        (
            "P016",
            "模型原生编译" in corpus and "验证日期" in corpus,
            "model-native compilation uses dated capability evidence",
        ),
    ]

    failed = False
    for check_id, passed, message in checks:
        print(f"{'PASS' if passed else 'FAIL'} {check_id} {message}")
        failed = failed or not passed
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
