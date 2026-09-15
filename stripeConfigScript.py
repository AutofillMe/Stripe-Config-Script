import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def checkGit() -> bool:
    gitFound: bool = False
    gitPath: Path = shutil.which("git")

    if gitPath is None:
        print("Git is not installed or not available in PATH.")
        print("Please download git from https://git-scm.com/ or check your PATH")
        raise SystemExit(1)
    else:
        print(f"Git found: {gitPath}")
        gitFound = True

    return gitFound


def checkScripts() -> bool:
    pathToExportStandardizer: Path = Path(
        "./Stripe-Export-Standarizer/stripeExportStandardizer.py"
    )
    pathToConfigChecker: Path = Path("./Stripe-Config-Checker/checkConfig.py")

    if not pathToExportStandardizer.exists():
        try:
            subprocess.run(
                [
                    "git",
                    "clone",
                    "https://github.com/AutofillMe/Stripe-Export-Standardizer.git",
                    "./Stripe-Export-Standarizer",
                ],
                check=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"git clone export standardizer failed with error {e}")
            raise SystemExit(e.returncode)

    if not pathToConfigChecker.exists():
        try:
            subprocess.run(
                [
                    "git",
                    "clone",
                    "https://github.com/AutofillMe/Stripe-Client-Config-Checker.git",
                    "./Stripe-Client-Config-Checker",
                ],
                check=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"git clone config checker failed with error {e}")
            raise SystemExit(e.returncode)

    return pathToConfigChecker.exists() and pathToExportStandardizer.exists()


def runScripts(recentStripeExport: Path, clientType: int, accountID: str) -> None:
    # First, standardize the export
    subprocess.run(
        [
            sys.executable,
            Path("./Stripe-Export-Standarizer/stripeExportStandardizer.py"),
            "-i",
            recentStripeExport,
            "-o",
            Path("./Stripe-Client-Config-Checker/recentStripeExport-clean.csv"),
        ],
        check=True,
    )

    # Then, run the config check
    subprocess.run(
        [
            sys.executable,
            Path("./Stripe-Client-Config-Checker/checkConfig.py"),
            "-f",
            Path("./Stripe-Client-Config-Checker/recentStripeExport-clean.csv"),
            "-t",
            clientType,
            "-a",
            accountID,
        ],
        check=True,
    )


def main() -> None:
    # TEST: delete later
    clientType: int = 1
    accountID: str = "testing"
    recentStripeExport: Path = "./"
    # TEST: delete later

    if not checkGit() or not checkScripts():
        raise SystemExit(1)
    runScripts(recentStripeExport, clientType, accountID)
    return 0


if __name__ == "__main__":
    main()
