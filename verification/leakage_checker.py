#!/usr/bin/env python3
"""
Information Leakage Checker

Verifies that chapter drafts do not reveal information ahead of schedule.
This is the enforcement layer for information architecture discipline.

Usage:
    python leakage_checker.py <chapter_number> <draft_file>

Example:
    python leakage_checker.py 7 drafts/ch07_draft.md
"""

import yaml
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum


class LeakageSeverity(Enum):
    """Severity levels for information leakage"""
    MINOR = "MINOR"      # Small detail leaked, not critical to main suspense
    MAJOR = "MAJOR"      # Key reveal leaked early, damages tension
    CRITICAL = "CRITICAL"  # Central mystery spoiled, destroys story


@dataclass
class LeakageIssue:
    """Represents a detected information leakage"""
    fact_id: str
    fact_description: str
    scheduled_chapter: int
    current_chapter: int
    severity: LeakageSeverity
    evidence: str  # The passage that leaked it
    line_number: int
    explanation: str


class LeakageChecker:
    """Main checker class for information discipline"""

    def __init__(self, story_bible_path: str, tension_curve_path: str):
        """Initialize checker with story bible and tension curve"""
        self.story_bible = self._load_yaml(story_bible_path)
        self.tension_curve = self._load_yaml(tension_curve_path)

    @staticmethod
    def _load_yaml(filepath: str) -> dict:
        """Load YAML file"""
        with open(filepath, 'r') as f:
            return yaml.safe_load(f)

    def check_chapter(self, chapter_num: int, draft_text: str) -> List[LeakageIssue]:
        """
        Check a chapter draft for information leakage.

        Args:
            chapter_num: The chapter number being checked
            draft_text: The full text of the draft

        Returns:
            List of LeakageIssue objects (empty if no leaks detected)
        """
        issues = []
        disclosure_schedule = self.story_bible.get('disclosure_schedule', [])

        for item in disclosure_schedule:
            fact_id = item.get('fact_id')
            scheduled_chapter = item.get('confirmed_to_reader')

            # Only check facts that shouldn't be revealed yet
            if scheduled_chapter > chapter_num:
                leak = self._detect_leak(
                    chapter_num=chapter_num,
                    draft_text=draft_text,
                    fact_item=item
                )
                if leak:
                    issues.append(leak)

        return issues

    def _detect_leak(self, chapter_num: int, draft_text: str, fact_item: dict) -> LeakageIssue | None:
        """
        Detect if a specific fact has leaked in the draft.

        This is a heuristic-based check. For production, you'd want more sophisticated
        NLP analysis, but this provides a useful baseline.
        """
        fact_id = fact_item.get('fact_id')
        fact_description = fact_item.get('fact')
        scheduled_chapter = fact_item.get('confirmed_to_reader')

        # Get the objective reality details for this fact
        objective_fact = self._get_objective_reality_fact(fact_id)
        if not objective_fact:
            return None

        # Define patterns that would constitute leakage for each fact type
        patterns = self._get_leak_patterns(fact_id, objective_fact)

        # Search for these patterns in the text
        for pattern, severity, context in patterns:
            match = re.search(pattern, draft_text, re.IGNORECASE | re.MULTILINE)
            if match:
                # Found potential leak - extract context
                line_num = draft_text[:match.start()].count('\n') + 1
                evidence = self._extract_context(draft_text, match)

                return LeakageIssue(
                    fact_id=fact_id,
                    fact_description=fact_description,
                    scheduled_chapter=scheduled_chapter,
                    current_chapter=chapter_num,
                    severity=severity,
                    evidence=evidence,
                    line_number=line_num,
                    explanation=context
                )

        return None

    def _get_objective_reality_fact(self, fact_id: str) -> dict | None:
        """Get the objective reality entry for a fact ID"""
        for fact in self.story_bible.get('objective_reality', []):
            if fact.get('id') == fact_id:
                return fact
        return None

    def _get_leak_patterns(self, fact_id: str, objective_fact: dict) -> List[Tuple[str, LeakageSeverity, str]]:
        """
        Get regex patterns that would constitute leakage for this fact.

        Returns list of tuples: (pattern, severity, explanation)

        NOTE: This is example-specific for "The Silent Witness" story.
        In production, you'd want a more generalized pattern system or LLM-based detection.
        """
        patterns = []

        if fact_id == "killer_identity":
            # Critical: Direct statement that Marcus killed Elena
            patterns.append((
                r'\bMarcus\b.{0,100}\b(killed|murdered|pushed)\b.{0,100}\bElena\b',
                LeakageSeverity.CRITICAL,
                "Direct statement that Marcus killed Elena"
            ))
            patterns.append((
                r'\bhe\b.{0,50}\b(killed|murdered|pushed)\b.{0,50}\bher\b.*lighthouse',
                LeakageSeverity.CRITICAL,
                "Narrator confirming Marcus killed Elena (in his POV)"
            ))
            patterns.append((
                r'the night (I|he) killed (her|Elena)',
                LeakageSeverity.CRITICAL,
                "Character or narrator referencing the murder as fact"
            ))

        elif fact_id == "sibling_connection":
            # Major: Stating they are siblings
            patterns.append((
                r'\b(brother|sister|sibling|half-sibling)\b.{0,50}\b(Marcus|Elena)\b',
                LeakageSeverity.MAJOR,
                "Explicitly stating sibling relationship"
            ))
            patterns.append((
                r'\bsame (father|mother|parent)\b',
                LeakageSeverity.MAJOR,
                "Revealing shared parentage"
            ))

        elif fact_id == "forged_letter":
            # Major: Confirming note is forged
            patterns.append((
                r'suicide note.{0,50}\b(was|is)\b.{0,30}\b(forged|faked|fabricated)\b',
                LeakageSeverity.MAJOR,
                "Definitively stating suicide note is forged"
            ))
            patterns.append((
                r'\bMarcus\b.{0,50}\b(forged|wrote|created|faked)\b.{0,50}\bnote\b',
                LeakageSeverity.MAJOR,
                "Stating Marcus forged the note"
            ))

        elif fact_id == "witness":
            # Major: Confirming Thomas saw the murder
            patterns.append((
                r'\bThomas\b.{0,50}\b(saw|witnessed)\b.{0,50}\b(murder|killing|Marcus pushing)',
                LeakageSeverity.MAJOR,
                "Confirming Thomas witnessed the murder"
            ))

        elif fact_id == "embezzlement":
            # Major: Confirming embezzlement
            patterns.append((
                r'\bMarcus\b.{0,50}\b(stole|embezzled|took)\b.{0,50}\b(money|million|trust)',
                LeakageSeverity.MAJOR,
                "Confirming Marcus embezzled from trust"
            ))

        # Add more fact-specific patterns as needed

        return patterns

    def _extract_context(self, text: str, match: re.Match, context_chars: int = 150) -> str:
        """Extract surrounding context from a regex match"""
        start = max(0, match.start() - context_chars)
        end = min(len(text), match.end() + context_chars)
        context = text[start:end]

        # Add ellipsis if we're not at the boundaries
        if start > 0:
            context = "..." + context
        if end < len(text):
            context = context + "..."

        return context.strip()

    def generate_report(self, chapter_num: int, issues: List[LeakageIssue]) -> str:
        """Generate human-readable report"""
        if not issues:
            return f"""
╔══════════════════════════════════════════════════════════════╗
║         INFORMATION LEAKAGE CHECK - CHAPTER {chapter_num:02d}              ║
╚══════════════════════════════════════════════════════════════╝

✓ NO LEAKAGE DETECTED

All information is being withheld according to the disclosure schedule.
The chapter maintains appropriate information discipline.
"""

        report_lines = [
            "╔══════════════════════════════════════════════════════════════╗",
            f"║         INFORMATION LEAKAGE CHECK - CHAPTER {chapter_num:02d}              ║",
            "╚══════════════════════════════════════════════════════════════╝",
            "",
            f"❌ {len(issues)} LEAKAGE ISSUE{'S' if len(issues) != 1 else ''} DETECTED",
            ""
        ]

        for i, issue in enumerate(issues, 1):
            severity_symbol = {
                LeakageSeverity.MINOR: "ℹ️",
                LeakageSeverity.MAJOR: "⚠️",
                LeakageSeverity.CRITICAL: "🔴"
            }[issue.severity]

            report_lines.extend([
                f"{'─' * 62}",
                f"Issue #{i}: {severity_symbol} {issue.severity.value}",
                f"{'─' * 62}",
                "",
                f"FACT ID: {issue.fact_id}",
                f"FACT: {issue.fact_description}",
                "",
                f"SCHEDULED REVEAL: Chapter {issue.scheduled_chapter}",
                f"CURRENT CHAPTER: Chapter {issue.current_chapter}",
                f"REVEALED: {issue.scheduled_chapter - issue.current_chapter} chapters too early",
                "",
                f"LINE NUMBER: {issue.line_number}",
                "",
                f"EXPLANATION: {issue.explanation}",
                "",
                "EVIDENCE:",
                f'"{issue.evidence}"',
                ""
            ])

        report_lines.extend([
            "╔══════════════════════════════════════════════════════════════╗",
            "║                    REVISION REQUIRED                          ║",
            "╚══════════════════════════════════════════════════════════════╝",
            "",
            "This chapter leaks information ahead of schedule, which will",
            "damage suspense and undermine the information architecture.",
            "",
            "NEXT STEPS:",
            "1. Review each flagged passage",
            "2. Remove or ambiguate the premature disclosure",
            "3. Re-run this checker until no issues remain",
            ""
        ])

        return "\n".join(report_lines)


def main():
    """Main CLI entry point"""
    if len(sys.argv) != 3:
        print("Usage: python leakage_checker.py <chapter_number> <draft_file>")
        print("Example: python leakage_checker.py 7 drafts/ch07_draft.md")
        sys.exit(1)

    chapter_num = int(sys.argv[1])
    draft_file = sys.argv[2]

    # Paths to story bible and tension curve
    project_root = Path(__file__).parent.parent
    story_bible_path = project_root / "story_bible.yaml"
    tension_curve_path = project_root / "tension_curve.yaml"

    # Check files exist
    if not story_bible_path.exists():
        print(f"Error: story_bible.yaml not found at {story_bible_path}")
        sys.exit(1)

    if not Path(draft_file).exists():
        print(f"Error: Draft file not found at {draft_file}")
        sys.exit(1)

    # Load draft
    with open(draft_file, 'r') as f:
        draft_text = f.read()

    # Run checker
    checker = LeakageChecker(str(story_bible_path), str(tension_curve_path))
    issues = checker.check_chapter(chapter_num, draft_text)

    # Generate and print report
    report = checker.generate_report(chapter_num, issues)
    print(report)

    # Exit with error code if issues found
    if issues:
        # Determine exit code based on severity
        severities = [issue.severity for issue in issues]
        if LeakageSeverity.CRITICAL in severities:
            sys.exit(3)  # Critical leakage
        elif LeakageSeverity.MAJOR in severities:
            sys.exit(2)  # Major leakage
        else:
            sys.exit(1)  # Minor leakage
    else:
        sys.exit(0)  # No issues


if __name__ == "__main__":
    main()
