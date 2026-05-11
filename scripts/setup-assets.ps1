# Mnemo — copy the asset source folders to the external mirror paths.
# Run once after cloning the lab repo. Re-run to refresh from upstream.
#
# Default mirror location: $env:USERPROFILE\mnemo-assets\{specs,bugs}
# Override with -Destination.

[CmdletBinding()]
param(
    [string]$Destination = (Join-Path $env:USERPROFILE 'mnemo-assets')
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot

$specsSource = Join-Path $repoRoot 'assets\specs-source'
$bugsSource  = Join-Path $repoRoot 'assets\bugs-source'

$specsTarget = Join-Path $Destination 'specs'
$bugsTarget  = Join-Path $Destination 'bugs'

Write-Host "Mnemo asset setup"
Write-Host "  Source (specs): $specsSource"
Write-Host "  Source (bugs):  $bugsSource"
Write-Host "  Target root:    $Destination"

New-Item -ItemType Directory -Force -Path $specsTarget | Out-Null
New-Item -ItemType Directory -Force -Path $bugsTarget  | Out-Null

Copy-Item -Path (Join-Path $specsSource '*') -Destination $specsTarget -Recurse -Force
Copy-Item -Path (Join-Path $bugsSource  '*') -Destination $bugsTarget  -Recurse -Force

Write-Host ""
Write-Host "Done. Now point your .env at the mirror:"
Write-Host "  MNEMO_SPECS_SOURCE_DIR=$specsTarget"
Write-Host "  MNEMO_BUGS_SOURCE_DIR=$bugsTarget"
