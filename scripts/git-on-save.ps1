$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

function Invoke-Git {
    param([Parameter(Mandatory = $true)][string[]]$Arguments)

    & git @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "git $($Arguments -join ' ') failed with exit code $LASTEXITCODE"
    }
}

$branch = (& git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($branch)) {
    Write-Warning "[STOP] Could not determine the current Git branch."
    exit 1
}

if ($branch -eq "main") {
    Write-Warning "[STOP] Automatic commit and push are disabled on main."
    exit 0
}

$changedPaths = @(
    (& git diff --name-only)
    (& git diff --cached --name-only)
    (& git ls-files --others --exclude-standard)
) | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Sort-Object -Unique

if ($changedPaths.Count -eq 0) {
    exit 0
}

try {
    $addArguments = @("add", "--") + $changedPaths
    Invoke-Git $addArguments
    Invoke-Git @("commit", "-m", "update: latest changes")
    Invoke-Git @("push", "origin", $branch)

    Invoke-Git @("fetch", "origin", "main", "--quiet")
    & git merge-base --is-ancestor "HEAD" "origin/main"
    $isMergedIntoMain = $LASTEXITCODE -eq 0

    if ($isMergedIntoMain) {
        Write-Host "[OK] '$branch' is merged into main."
    } else {
        Write-Host "[OK] '$branch' was committed and pushed; it is not merged into main yet."
    }
} catch {
    Write-Error "[STOP] $($_.Exception.Message)"
    exit 1
}