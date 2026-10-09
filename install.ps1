# Install the 12 invention-patent skills.
# Project mode writes only to <dir>\.agents\skills.
# cursor, claude, codex, and all write to the matching user skill directories.
$ErrorActionPreference = "Stop"

$ScriptDir = $PSScriptRoot
if (-not $ScriptDir) {
    $ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
}
$SourceDir = Join-Path $ScriptDir "skills"

$ExpectedSkills = @(
    "01-patent-master-control",
    "02-patent-init",
    "03-invention-status-check",
    "04-patent-topic-selector",
    "05-patent-prior-art-search",
    "06-innovation-point-finder",
    "07-abstract-generator",
    "08-claims-writer",
    "09-patent-drawing-generator",
    "10-drawing-consistency-validator",
    "11-description-writer",
    "12-patent-word-generator"
)

function Show-Usage {
    @"
Usage:
  install.ps1 --target cursor|claude|codex|all [--mode link|copy] [--dry-run]
  install.ps1 --target project <dir> [--mode link|copy] [--dry-run]
  install.ps1 -h

Targets:
  cursor    $HOME\.cursor\skills
  claude    $HOME\.claude\skills
  codex     $HOME\.codex\skills
  all       cursor, claude, and codex
  project   <dir>\.agents\skills

--mode copy (default) replaces only these 12 skill directories.
--mode link uses a directory junction or symlink to this pack.
--dry-run prints the actions and does not write.
"@
}

$Target = ""
$Mode = "copy"
$DryRun = $false
$Positionals = @()
$argv = @($args)
for ($i = 0; $i -lt $argv.Count; $i++) {
    $item = [string]$argv[$i]
    switch -Regex ($item) {
        "^(-h|--help|-Help)$" {
            Show-Usage
            exit 0
        }
        "^(--dry-run|-DryRun)$" {
            $DryRun = $true
        }
        "^(--target|-Target)$" {
            if ($i + 1 -ge $argv.Count) { throw "error: --target needs a value" }
            $i++
            $Target = [string]$argv[$i]
        }
        "^(--mode|-Mode)$" {
            if ($i + 1 -ge $argv.Count) { throw "error: --mode needs a value" }
            $i++
            $Mode = [string]$argv[$i]
        }
        "^--" {
            throw "error: unknown option: $item"
        }
        default {
            $Positionals += $item
        }
    }
}

if (-not $Target) {
    Show-Usage
    throw "error: --target is required"
}
if ($Mode -notin @("link", "copy")) {
    throw "error: --mode must be link or copy"
}
if (-not (Test-Path -LiteralPath $SourceDir -PathType Container)) {
    throw "error: skills directory is missing: $SourceDir"
}
foreach ($name in $ExpectedSkills) {
    $skillFile = Join-Path (Join-Path $SourceDir $name) "SKILL.md"
    if (-not (Test-Path -LiteralPath $skillFile -PathType Leaf)) {
        throw "error: missing skill or SKILL.md: $name"
    }
}

$DestParents = @()
switch ($Target) {
    "cursor" { $DestParents += (Join-Path $HOME ".cursor\skills") }
    "claude" { $DestParents += (Join-Path $HOME ".claude\skills") }
    "codex" { $DestParents += (Join-Path $HOME ".codex\skills") }
    "all" {
        $DestParents += (Join-Path $HOME ".cursor\skills")
        $DestParents += (Join-Path $HOME ".claude\skills")
        $DestParents += (Join-Path $HOME ".codex\skills")
    }
    "project" {
        if ($Positionals.Count -ne 1) { throw "error: project target needs exactly one directory" }
        $ProjectDir = $Positionals[0]
        if (-not (Test-Path -LiteralPath $ProjectDir -PathType Container)) {
            throw "error: project directory does not exist: $ProjectDir"
        }
        $ProjectDir = (Resolve-Path -LiteralPath $ProjectDir).Path
        $DestParents += (Join-Path $ProjectDir ".agents\skills")
    }
    default { throw "error: unknown target: $Target" }
}
if ($Target -ne "project" -and $Positionals.Count -gt 0) {
    throw "error: unexpected extra arguments"
}

foreach ($parent in $DestParents) {
    foreach ($name in $ExpectedSkills) {
        $src = Join-Path $SourceDir $name
        $dest = Join-Path $parent $name
        if ($DryRun) {
            Write-Host "dry-run: mkdir $parent"
            Write-Host "dry-run: $Mode $src -> $dest"
            continue
        }
        New-Item -ItemType Directory -Force -Path $parent | Out-Null
        if (Test-Path -LiteralPath $dest) {
            Remove-Item -LiteralPath $dest -Recurse -Force
        }
        if ($Mode -eq "link") {
            New-Item -ItemType SymbolicLink -Path $dest -Target $src | Out-Null
        } else {
            Copy-Item -LiteralPath $src -Destination $dest -Recurse -Force
        }
    }
}

if ($DryRun) {
    Write-Host "dry-run: $($ExpectedSkills.Count) skills x $($DestParents.Count) target(s); nothing written"
} else {
    Write-Host "Installed $($ExpectedSkills.Count) invention-patent skills."
    foreach ($parent in $DestParents) { Write-Host "  $parent" }
    Write-Host "Mode: $Mode. Only these 12 skill names were replaced."
}
