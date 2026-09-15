import argparse
import shutil
import subprocess
import sys
from pathlib import Path

parser = argparse.ArgumentParser()

parser.add_argument(
    "-a",
    "--acct",
    dest="a_id",
    help="<str> account_id of the client",
)

parser.add_argument(
    "-t",
    "--client-type",
    dest="clientType",
    type=int,
    help="<int> what type of client they are (1, 2, 3, 4)",
)

parser.add_argument(
    "-f",
    "--file",
    dest="stripeExport",
    type=Path,
    help="<path> path to csv file to parse data from",
)

args = parser.parse_args()


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
    print("Checking for necessary scripts...")

    repos = [
        (
            Path("./Stripe-Export-Standardizer"),
            "https://github.com/AutofillMe/Stripe-Export-Standardizer.git",
        ),
        (
            Path("./Stripe-Client-Config-Checker"),
            "https://github.com/AutofillMe/Stripe-Client-Config-Checker.git",
        ),
    ]

    for repoPath, repoUrl in repos:
        try:
            if not repoPath.exists():
                print(f"Cloning {repoPath}...")
                subprocess.run(
                    ["git", "clone", repoUrl, str(repoPath)],
                    check=True,
                )
            else:
                print(f"Updating {repoPath}...")
                subprocess.run(
                    ["git", "-C", str(repoPath), "pull"],
                    check=True,
                )
        except subprocess.CalledProcessError as e:
            print(f"Failed to update {repoPath}: {e}")
            raise SystemExit(e.returncode)

    # Default script paths
    pathToExportStandardizer = Path(
        "./Stripe-Export-Standardizer/stripeExportStandardizer.py"
    )
    pathToConfigChecker = Path("./Stripe-Client-Config-Checker/checkConfig.py")

    return pathToConfigChecker.exists() and pathToExportStandardizer.exists()


def runScripts(recentStripeExport: Path, clientType: int, accountID: str) -> None:
    # First, standardize the export
    subprocess.run(
        [
            sys.executable,
            Path("./Stripe-Export-Standardizer/stripeExportStandardizer.py"),
            "-i",
            recentStripeExport,
            "-o",
            Path("./Stripe-Client-Config-Checker/recentStripeExport-clean.csv"),
            "-c",
            Path("./Stripe-Export-Standardizer/config.txt"),
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
            "-c",
            Path("./Stripe-Client-Config-Checker/clientTypeChart.csv"),
        ],
    )


def main(args: argparse.Namespace) -> int:
    accountID: str = args.a_id
    clientType: str = str(args.clientType)
    recentStripeExport: Path = args.stripeExport or Path("./export.csv")

    if not checkGit() or not checkScripts():
        raise SystemExit(1)

    print("Running config check...")
    runScripts(recentStripeExport, clientType, accountID)
    return 0


if __name__ == "__main__":
    main(args)
