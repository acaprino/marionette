"""scrolltide-ai-studio: MIT-licensed scrollytelling patterns, house style, handoff and Playwright scroll QA.

Pinned to published release v1.0.0 (`5662f4f2`). Section 1 (MIT) of the upstream dual LICENSE is
verified through `license_section` (ADR-0038); section 2 reserves all rights on the nine `library/*.md`
builds and forbids redistribution, so `library/**` (including `library/INDEX.md`) is excluded and
declared in `omissions` (owner decision of 2026-11-28). Two on-demand capabilities:
`scroll-storytelling` (in `marionette-web-design`) and `scroll-checkpoint-audit` (in `marionette-motion`).
"""
import json
import shutil

import pytest

from muro import parse_capabilities, parse_router
from muro.delivery import validate_delivery
from muro.entries import validate_entries
from muro.runtime import Coordinator
from routing_helpers import ROOT, decision

from project_dir import PACKAGE  # the project file, unpacked

SOURCE = "scrolltide-ai-studio"
RELEASE = "v1.0.0"
COMMIT = "5662f4f20de1398b1b2c6818b4a64d407662d9e2"
SKILL_DIR = "plugins/ai-studio/skills/scrolltide-ai-studio"
STORY = "scroll-storytelling"
AUDIT = "scroll-checkpoint-audit"


def read_json(name):
    return json.loads((PACKAGE / name).read_text(encoding="utf-8"))


def catalog():
    return {cap.id: cap for cap in parse_capabilities(PACKAGE / "capabilities")}


def before_sources(cap):
    return cap.body.split("## Sources", 1)[0]


@pytest.fixture
def coordinator(tmp_path):
    package = tmp_path / "package"
    package.mkdir()
    shutil.copytree(PACKAGE / "capabilities", package / "capabilities")
    shutil.copytree(PACKAGE / "custom-instructions", package / "custom-instructions")
    shutil.copytree(ROOT / "prompts", package / "prompts")
    for name in ("ROUTER.md", "sources.json", "delivery.json"):
        shutil.copy2(PACKAGE / name, package / name)
    return Coordinator(package, tmp_path / "consumer")


def test_manifest_pins_release_v1_with_license_section_and_excludes_proprietary_library():
    manifest = read_json("sources.json")
    src = next(source for source in manifest["sources"] if source["id"] == SOURCE)
    assert src["repo_url"] == "https://github.com/scrolltide/ai-studio-skill"
    assert (src["pin"], src["release"], src["commit"]) == ("release", RELEASE, COMMIT)
    assert src["license"] == "MIT" and "Scrolltide" in src["copyright"]
    assert src["license_section"]["start"] == "MIT License"
    assert src["license_section"]["end"] == "SOFTWARE."
    assert src["license_section"]["reason"].strip()
    assert f"{SKILL_DIR}/SKILL.md" in src["selected_paths"]
    assert f"{SKILL_DIR}/patterns/**" in src["selected_paths"]
    assert f"{SKILL_DIR}/scripts/scrollshot.mjs" in src["selected_paths"]
    assert f"{SKILL_DIR}/library/**" in src["excluded_paths"]
    assert any(f"{SKILL_DIR}/library/**" in entry["paths"] for entry in src["omissions"])
    assert SOURCE in manifest["plugin"]["replaces"]


def test_both_capabilities_match_router_and_keep_relations_and_coexistence():
    caps = catalog()
    rows = {row.id: row for row in parse_router(PACKAGE / "ROUTER.md")}

    story = caps[STORY]
    assert story.role == rows[STORY].role == "scroll-storytelling"
    assert [i["id"] for i in story.intents] == ["ui.scroll-page", "ui.scroll-handoff"] == rows[STORY].intents_list()
    assert story.outputs == ["scroll_moment", "scroll_page", "handoff_prompt"] == rows[STORY].outputs_list()
    assert story.resumable is True
    assert set(story.conflicts) == {"aesthetic-direction", "gsap-scrolltrigger", "css-scroll"}
    assert {"design_file", "offer", "page_outline", "motion-spec", "reduced-motion"} <= set(story.reads)
    assert set(story.intent_checks) == {"ui.scroll-page", "ui.scroll-handoff"}
    assert "handoff_prompt_complete" in story.intent_checks["ui.scroll-handoff"]
    assert "handoff_prompt_complete" not in story.intent_checks["ui.scroll-page"]
    assert f"<package_root>/scripts/{SOURCE}/{SKILL_DIR}" in before_sources(story)
    assert "/SKILL.source.md" in before_sources(story) and "/SKILL.md" not in before_sources(story)
    assert COMMIT in story.body.split("## Sources", 1)[1] and RELEASE in story.body.split("## Sources", 1)[1]
    assert "Changes for coexistence (ADR-0017)" in story.body.split("## Sources", 1)[1]
    assert "- Relations:" in story.body.split("## Sources", 1)[1]

    audit = caps[AUDIT]
    assert audit.role == rows[AUDIT].role == "scroll-verification"
    assert [i["id"] for i in audit.intents] == ["ui.scroll-checkpoint-audit"] == rows[AUDIT].intents_list()
    assert audit.outputs == ["scroll_checkpoints", "scroll_audit_report"] == rows[AUDIT].outputs_list()
    assert audit.conflicts == []
    assert {"scroll_page", "page", "code-patch", "scroll-verified", "design_file", "palette", "typography"} <= set(audit.reads)
    assert f"<package_root>/scripts/{SOURCE}/{SKILL_DIR}" in before_sources(audit)
    assert COMMIT in audit.body.split("## Sources", 1)[1] and RELEASE in audit.body.split("## Sources", 1)[1]


def test_delivery_discovery_examples_and_eval_cases_cover_scrolltide():
    document = read_json("delivery.json")
    mine = [item for item in document["decisions"] if item["source"] == SOURCE]
    assert {item["form"] for item in mine} == {"capability", "dropped"}
    assert {target for item in mine for target in item["targets"]} == {STORY, AUDIT}
    assert validate_delivery({"decisions": mine}, [catalog()[STORY], catalog()[AUDIT]], {SOURCE}) == []
    assert not any(w["capability"] in {STORY, AUDIT} for w in document.get("hooks", []))
    assert "scrolltide" not in document["always_on"].lower()

    entries = read_json("entries.json")
    assert validate_entries(entries, list(catalog().values()), read_json("sources.json")["plugin"]) == []
    by_name = {item["name"]: item for item in entries["entries"]}
    assert STORY in by_name["marionette-web-design"]["capabilities"]
    assert SOURCE in by_name["marionette-web-design"]["absorbs"]
    assert AUDIT in by_name["marionette-motion"]["capabilities"]

    examples = read_json("guide-examples.json")["examples"]
    shown = {(s["capability"], s["intent"]) for example in examples for s in example["selections"]}
    assert {(STORY, "ui.scroll-page"), (STORY, "ui.scroll-handoff"), (AUDIT, "ui.scroll-checkpoint-audit")} <= shown

    expected = {case["id"]: case["expect"] for case in read_json("eval-cases.json")["cases"]}
    assert expected["st-scroll-film-page"]["selections"] == [{"capability": STORY, "intent": "ui.scroll-page"}]
    assert expected["st-handoff-prompt-lovable"]["selections"] == [{"capability": STORY, "intent": "ui.scroll-handoff"}]
    assert expected["st-checkpoint-audit-on-gsap-page"]["selections"] == [{"capability": AUDIT, "intent": "ui.scroll-checkpoint-audit"}]
    assert expected["st-strategy-then-scroll-page"]["capabilities"] == ["visual-direction", STORY]
    assert expected["st-flat-conversion-landing-stays-visual-direction"]["capabilities"] == ["visual-direction"]


def _select(coordinator, task, pairs, stack=None):
    req = coordinator.propose(task, stack or set())
    assert req["mode"] == "classification-required"
    return {
        **req["context"],
        "status": "selected",
        "selections": [{"capability": cap, "intent": intent, "reason": "Fixture selection."} for cap, intent in pairs],
        "reason": "Fixture decision.",
        "questions": [],
    }


def test_synergy_and_conflict_rules_in_runtime(coordinator):
    # Synergy 1: landing strategy feeds scroll-storytelling in one plan.
    task1 = "Define landing offer and outline, then build the scrollytelling canvas film page."
    cls1 = _select(coordinator, task1, [("visual-direction", "ui.landing-strategy"), (STORY, "ui.scroll-page")])
    res1 = coordinator.propose(task1, set(), classification=cls1)
    assert res1["mode"] == "confirm" and res1["plan"] == ["visual-direction", STORY]

    # Synergy 2: gsap-scrolltrigger feeds scroll-checkpoint-audit without conflict.
    task2 = "Implement GSAP ScrollTrigger pinning and verify checkpoints on desktop and mobile."
    cls2 = _select(coordinator, task2, [("gsap-scrolltrigger", "ui.scroll-animation"), (AUDIT, "ui.scroll-checkpoint-audit")], {"stack:gsap"})
    res2 = coordinator.propose(task2, {"stack:gsap"}, classification=cls2)
    assert res2["mode"] == "confirm" and res2["plan"] == ["gsap-scrolltrigger", AUDIT]

    # Conflict: scroll-storytelling cannot share a plan with gsap-scrolltrigger (two scroll engines).
    task3 = "Mix GSAP ScrollTrigger and Scrolltide Lenis loop on the same page."
    cls3 = _select(coordinator, task3, [("gsap-scrolltrigger", "ui.scroll-animation"), (STORY, "ui.scroll-page")], {"stack:gsap"})
    with pytest.raises(ValueError, match="(?i)conflict"):
        coordinator.propose(task3, {"stack:gsap"}, classification=cls3)
