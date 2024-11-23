import requests
import argparse
import subprocess

class Visualizer:
    def __init__(self, package_name, repository_url):
        self.package_name = package_name
        self.repository_url = repository_url


def main():
    parser = argparse.ArgumentParser(description="Dependency Visualizer for .NET packages.")
    parser.add_argument("visualizer_path", help="Path to the visualization program (Mermaid CLI)")
    parser.add_argument("package_name", help="Name of the package to analyze")
    parser.add_argument("repository_url", help="URL of the repository")

    args = parser.parse_args()

    visualizer = Visualizer(args.package_name, args.repository_url)


if __name__ == "__main__":
    main()

