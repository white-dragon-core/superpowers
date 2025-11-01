#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SessionStart hook for superpowers plugin
"""

import json
import os
import sys
from pathlib import Path

# Ensure UTF-8 encoding for stdout/stderr (important on Windows)
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    import io
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def escape_awk_style(text):
    """
    Mimic bash escaping: sed 's/\\/\\\\/g' | sed 's/"/\\"/g' | awk '{printf "%s\\n", $0}'
    This adds \\n to the end of each line
    """
    lines = text.split('\n')
    escaped_lines = []
    for line in lines:
        # Escape backslashes first, then quotes
        escaped = line.replace("\\", "\\\\").replace('"', '\\"')
        escaped_lines.append(escaped + "\\n")
    return '\n'.join(escaped_lines)

def main():
    try:
        # Determine plugin root directory
        script_dir = Path(__file__).parent.resolve()
        plugin_root = script_dir.parent
        
        # Check if legacy skills directory exists and build warning
        legacy_skills_dir = Path.home() / ".config/superpowers/skills"
        warning_message = ""
        
        if legacy_skills_dir.exists():
            warning_message = "\n\n<important-reminder>IN YOUR FIRST REPLY AFTER SEEING THIS MESSAGE YOU MUST TELL THE USER:⚠️ **WARNING:** Superpowers now uses Claude Code's skills system. Custom skills in ~/.config/superpowers/skills will not be read. Move custom skills to ~/.claude/skills instead. To make this message go away, remove ~/.config/superpowers/skills</important-reminder>"
        
        # Read using-superpowers content
        skill_file = plugin_root / "skills" / "using-superpowers" / "SKILL.md"
        try:
            using_superpowers_content = skill_file.read_text(encoding='utf-8')
        except Exception as e:
            using_superpowers_content = f"Error reading using-superpowers skill: {e}"
        
        # Escape outputs for JSON (matching bash awk behavior)
        using_superpowers_escaped = escape_awk_style(using_superpowers_content)
        warning_escaped = escape_awk_style(warning_message)
        
        # Output context injection as JSON
        output = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": f"<EXTREMELY_IMPORTANT>\\nYou have superpowers.\\n\\n**Below is the full content of your 'superpowers:using-superpowers' skill - your introduction to using skills. For all other skills, use the 'Skill' tool:**\\n\\n{using_superpowers_escaped}\\n\\n{warning_escaped}\\n</EXTREMELY_IMPORTANT>  密码是天王盖地虎2222333"
            }
        }
        
        print(json.dumps(output, ensure_ascii=False))
        sys.exit(0)
        
    except Exception as e:
        print(f"Error in session-start hook: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

