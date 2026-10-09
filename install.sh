#!/usr/bin/env bash
# Install the 12 invention-patent skills.
# Project mode writes only to <dir>/.agents/skills.
# cursor, claude, codex, and all write to the matching user skill directories.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCE_DIR="$SCRIPT_DIR/skills"

EXPECTED_SKILLS=(
  "01-patent-master-control"
  "02-patent-init"
  "03-invention-status-check"
  "04-patent-topic-selector"
  "05-patent-prior-art-search"
  "06-innovation-point-finder"
  "07-abstract-generator"
  "08-claims-writer"
  "09-patent-drawing-generator"
  "10-drawing-consistency-validator"
  "11-description-writer"
  "12-patent-word-generator"
)

usage() {
  cat <<'EOF'
Usage:
  install.sh --target cursor|claude|codex|all [--mode link|copy] [--dry-run]
  install.sh --target project <dir> [--mode link|copy] [--dry-run]
  install.sh -h

Targets:
  cursor    ~/.cursor/skills
  claude    ~/.claude/skills
  codex     ~/.codex/skills
  all       cursor, claude, and codex
  project   <dir>/.agents/skills

--mode copy (default) replaces only these 12 skill directories.
--mode link symlinks each skill directory to this pack.
--dry-run prints the actions and does not write.
EOF
}

TARGET=""
MODE="copy"
DRY_RUN=0
POSITIONALS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --target)
      if [[ $# -lt 2 ]]; then
        echo "error: --target needs a value" >&2
        exit 2
      fi
      TARGET="$2"
      shift 2
      ;;
    --mode)
      if [[ $# -lt 2 ]]; then
        echo "error: --mode needs a value" >&2
        exit 2
      fi
      MODE="$2"
      shift 2
      ;;
    --)
      shift
      while [[ $# -gt 0 ]]; do
        POSITIONALS+=("$1")
        shift
      done
      ;;
    -*)
      echo "error: unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
    *)
      POSITIONALS+=("$1")
      shift
      ;;
  esac
done

if [[ -z "$TARGET" ]]; then
  echo "error: --target is required" >&2
  usage >&2
  exit 2
fi

case "$MODE" in
  link|copy) ;;
  *)
    echo "error: --mode must be link or copy" >&2
    exit 2
    ;;
esac

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "error: skills directory is missing: $SOURCE_DIR" >&2
  exit 1
fi

for skill_name in "${EXPECTED_SKILLS[@]}"; do
  if [[ ! -f "$SOURCE_DIR/$skill_name/SKILL.md" ]]; then
    echo "error: missing skill or SKILL.md: $skill_name" >&2
    exit 1
  fi
done

DEST_PARENTS=()
case "$TARGET" in
  cursor)
    DEST_PARENTS+=("$HOME/.cursor/skills")
    ;;
  claude)
    DEST_PARENTS+=("$HOME/.claude/skills")
    ;;
  codex)
    DEST_PARENTS+=("$HOME/.codex/skills")
    ;;
  all)
    DEST_PARENTS+=(
      "$HOME/.cursor/skills"
      "$HOME/.claude/skills"
      "$HOME/.codex/skills"
    )
    ;;
  project)
    if [[ ${#POSITIONALS[@]} -ne 1 ]]; then
      echo "error: project target needs exactly one directory" >&2
      exit 2
    fi
    PROJECT_DIR="${POSITIONALS[0]}"
    if [[ ! -d "$PROJECT_DIR" ]]; then
      echo "error: project directory does not exist: $PROJECT_DIR" >&2
      exit 1
    fi
    PROJECT_DIR="$(cd "$PROJECT_DIR" && pwd)"
    DEST_PARENTS+=("$PROJECT_DIR/.agents/skills")
    ;;
  *)
    echo "error: unknown target: $TARGET" >&2
    exit 2
    ;;
esac

if [[ "$TARGET" != "project" && ${#POSITIONALS[@]} -gt 0 ]]; then
  echo "error: unexpected extra arguments" >&2
  exit 2
fi

install_one() {
  local parent="$1"
  local skill_name="$2"
  local src="$SOURCE_DIR/$skill_name"
  local dest="$parent/$skill_name"
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "dry-run: mkdir -p $parent"
    echo "dry-run: $MODE $src -> $dest"
    return 0
  fi
  mkdir -p "$parent"
  rm -rf -- "$dest"
  if [[ "$MODE" == "link" ]]; then
    ln -s "$src" "$dest"
  else
    cp -R "$src" "$dest"
  fi
}

installed_count=0
for parent in "${DEST_PARENTS[@]}"; do
  for skill_name in "${EXPECTED_SKILLS[@]}"; do
    install_one "$parent" "$skill_name"
    installed_count=$((installed_count + 1))
  done
done

expected_count=$(( ${#EXPECTED_SKILLS[@]} * ${#DEST_PARENTS[@]} ))
if [[ "$installed_count" -ne "$expected_count" ]]; then
  echo "error: expected $expected_count skill installs, got $installed_count" >&2
  exit 1
fi

if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "dry-run: ${#EXPECTED_SKILLS[@]} skills x ${#DEST_PARENTS[@]} target(s); nothing written"
else
  echo "Installed ${#EXPECTED_SKILLS[@]} invention-patent skills."
  for parent in "${DEST_PARENTS[@]}"; do
    echo "  $parent"
  done
  echo "Mode: $MODE. Only these 12 skill names were replaced."
fi
