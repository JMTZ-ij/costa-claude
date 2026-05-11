#!/bin/bash
# Costanera AI Sales Studio — Uninstaller
set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SKILLS_DIR="$HOME/.claude/skills"
AGENTS_DIR="$HOME/.claude/agents"

echo "Removing Costanera skills, agents, and scripts..."

# Skills
SKILLS=(costa costa-prospect costa-quick costa-audit costa-proposal costa-outreach costa-icp)
for s in "${SKILLS[@]}"; do
    if [ -d "$SKILLS_DIR/$s" ]; then
        rm -rf "$SKILLS_DIR/$s"
        echo -e "  ${GREEN}✓${NC} removed $s"
    fi
done

# Agents
AGENTS=(costa-ops-audit costa-data-stack costa-automation costa-ai-fit costa-decision-maker)
for a in "${AGENTS[@]}"; do
    if [ -f "$AGENTS_DIR/$a.md" ]; then
        rm "$AGENTS_DIR/$a.md"
        echo -e "  ${GREEN}✓${NC} removed $a"
    fi
done

echo ""
echo -e "${GREEN}Uninstall complete.${NC}"
echo -e "${YELLOW}Note:${NC} Python packages installed (if any) were not removed."
