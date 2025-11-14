import json
from pathlib import Path


GROUPS = {
    "ark-core-foundation.toon": [
        "ark-core-system.json",
        "ark-persona-cultural-fit.json",
        "ark-communications.json",
    ],
    "ark-intelligence-engines.toon": [
        "ark-advanced-ai-engine.json",
        "ark-reasoning-intelligence.json",
    ],
    "ark-matching-suite.toon": [
        "ark-advanced-matching.json",
        "ark-resume-analysis.json",
        "ark-jd-intelligence.json",
    ],
    "ark-analytics-compliance.toon": [
        "ark-analytics-insights.json",
        "ark-bias-detection-compliance.json",
    ],
    "ark-boolean-engine.toon": [
        "ark-boolean-engine-v1.json",
    ],
    "ark-context-resilience.toon": [
        "ark-context-awareness.json",
        "ark-fallback-resilience.json",
        "ark-governance-resilience.json",
    ],
    "ark-integrations-search.toon": [
        "ark-integrations-ecosystem.json",
        "ark-web-search-integration.json",
    ],
    "ark-security-feedback.toon": [
        "ark-security-feedback.json",
    ],
    "ark-enhancements-guide.toon": [
        "ENHANCEMENTS-v2.0-README.md",
    ],
    "ark-operational-standards.toon": [
        "ark-master-instructions-v2.md",
        "ark-output-templates.json",
    ],
}


def format_scalar(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def emit_lines(value: object, indent: int = 0) -> list[str]:
    lines: list[str] = []
    prefix = "  " * indent

    if isinstance(value, dict):
        for key, nested in value.items():
            if isinstance(nested, (dict, list)):
                lines.append(f"{prefix}{key}:")
                lines.extend(emit_lines(nested, indent + 1))
            else:
                lines.append(f"{prefix}{key}: {format_scalar(nested)}")
    elif isinstance(value, list):
        for item in value:
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}-")
                lines.extend(emit_lines(item, indent + 1))
            else:
                lines.append(f"{prefix}- {format_scalar(item)}")
    else:
        lines.append(f"{prefix}{format_scalar(value)}")

    return lines


def convert_group(archive_dir: Path, output_name: str, sources: list[str]) -> None:
    output_lines = [f"# {output_name.replace('-', ' ').replace('.toon', '').upper()}"]
    for source in sources:
        source_path = archive_dir / source
        output_lines.append("")
        output_lines.append(f"## SOURCE: {source}")

        if source_path.suffix.lower() == ".json":
            with source_path.open("r", encoding="utf-8") as fp:
                data = json.load(fp)
            output_lines.extend(emit_lines(data, indent=0))
        else:
            output_lines.append("content:")
            with source_path.open("r", encoding="utf-8") as fp:
                for line in fp.read().splitlines():
                    output_lines.append(f"  {line}")

    target_path = archive_dir / output_name
    target_path.write_text("\n".join(output_lines) + "\n", encoding="utf-8")


def main() -> None:
    archive_dir = Path(__file__).resolve().parent.parent / "archive-v2-json"
    for output_name, sources in GROUPS.items():
        convert_group(archive_dir, output_name, sources)


if __name__ == "__main__":
    main()
