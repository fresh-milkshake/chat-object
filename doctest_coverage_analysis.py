"""
usage: doctest_coverage_analysis.py [-h] [--recursive] [--no-recursive] [--format {text,summary,json,csv}] [--verbose] [--output OUTPUT] targets [targets ...]

Doctest coverage analysis tool

positional arguments:
  targets               Files or directories to analyze

options:
  -h, --help            show this help message and exit
  --recursive, -r       Recursively search directories for Python files (default: True)
  --no-recursive        Disable recursive directory search
  --format {text,summary,json,csv}, -f {text,summary,json,csv}
                        Output format (default: text)
  --verbose, -v         Enable verbose output
  --output OUTPUT, -o OUTPUT
                        Output file (for JSON/CSV formats)

Examples:
  doctest_coverage_analysis.py some_src_dir/
  doctest_coverage_analysis.py file1.py file2.py
  doctest_coverage_analysis.py . --recursive --format json
  doctest_coverage_analysis.py src/ --format summary
  doctest_coverage_analysis.py . --format csv > results.csv
"""

import re
import io
import ast
import json
import argparse
import contextlib

from pathlib import Path


class DetailedDoctestAnalyzer:
    """Detailed analyzer for doctest coverage with enhanced statistics."""

    def __init__(self, verbose: bool = False, output_format: str = "text"):
        self.results = {}
        self.verbose = verbose
        self.output_format = output_format

    def analyze_file_detailed(self, file_path: Path) -> dict:
        """Analyze doctest coverage for a single file with detailed breakdown."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except (FileNotFoundError, PermissionError, UnicodeDecodeError) as e:
            return {"error": f"Error reading file: {e}"}

        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            return {"error": f"Syntax error in file: {e}"}

        analysis = {
            "file": str(file_path),
            "classes": {},
            "functions": {},
            "total_functions": 0,
            "total_classes": 0,
            "covered_functions": 0,
            "covered_classes": 0,
            "total_methods": 0,
            "covered_methods": 0,
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_info = self._analyze_class(node, content)
                analysis["classes"][node.name] = class_info
                analysis["total_classes"] += 1
                if class_info["has_doctest"]:
                    analysis["covered_classes"] += 1

                analysis["total_methods"] += class_info["total_methods"]
                analysis["covered_methods"] += class_info["covered_methods"]

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not self._is_inside_class(node, tree):  # type: ignore
                    func_info = self._analyze_function(node, content)  # type: ignore
                    analysis["functions"][node.name] = func_info
                    analysis["total_functions"] += 1
                    if func_info["has_doctest"]:
                        analysis["covered_functions"] += 1

        return analysis

    def _is_inside_class(self, node: ast.FunctionDef, tree: ast.AST) -> bool:
        """Check if a function is defined inside a class."""
        for parent in ast.walk(tree):
            if isinstance(parent, ast.ClassDef):
                for child in ast.walk(parent):
                    if child is node:
                        return True
        return False

    def _analyze_class(self, node: ast.ClassDef, content: str) -> dict:
        """Analyze a class for doctest coverage."""
        class_info = {
            "name": node.name,
            "has_doctest": False,
            "methods": {},
            "total_methods": 0,
            "covered_methods": 0,
        }

        if node.body and isinstance(node.body[0], ast.Expr):
            if isinstance(node.body[0].value, ast.Constant):
                docstring = node.body[0].value.value
                class_info["has_doctest"] = self._has_doctests([docstring])

        for child in node.body:
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                method_info = self._analyze_function(child, content)  # type: ignore
                class_info["methods"][child.name] = method_info
                class_info["total_methods"] += 1
                if method_info["has_doctest"]:
                    class_info["covered_methods"] += 1

        return class_info

    def _analyze_function(self, node: ast.FunctionDef, content: str) -> dict:
        """Analyze a function for doctest coverage."""
        func_info = {
            "name": node.name,
            "has_doctest": False,
            "lineno": node.lineno if hasattr(node, "lineno") else 0,
        }

        if node.body and isinstance(node.body[0], ast.Expr):
            if isinstance(node.body[0].value, ast.Constant):
                docstring = node.body[0].value.value
                func_info["has_doctest"] = self._has_doctests([docstring])

        return func_info

    def _has_doctests(self, lines: list[str]) -> bool:
        """Check if lines contain doctest examples."""
        content = "".join(lines)
        patterns = [
            r">>>\s+",
            r"\.\.\.\s+",
            r"Expecting:",
        ]

        for pattern in patterns:
            if re.search(pattern, content):
                return True
        return False

    def find_python_files(self, path: Path, recursive: bool = True) -> list[Path]:
        """Find all Python files in the given path."""
        python_files = []

        if path.is_file():
            if path.suffix == ".py":
                python_files.append(path)
        elif path.is_dir():
            if recursive:
                python_files.extend(path.rglob("*.py"))
            else:
                python_files.extend(path.glob("*.py"))

        return python_files

    def run_analysis(self, targets: list[str], recursive: bool = True) -> dict:
        """Run analysis on specified targets (files or directories)."""
        all_files = []

        for target in targets:
            target_path = Path(target)
            if not target_path.exists():
                if self.verbose:
                    print(f"Warning: Target not found: {target}")
                continue

            files = self.find_python_files(target_path, recursive)
            all_files.extend(files)

        if not all_files:
            print("No Python files found in the specified targets.")
            return {}

        if self.verbose:
            print(f"Found {len(all_files)} Python files to analyze")

        results = {
            "files": {},
            "summary": {
                "total_files": 0,
                "total_classes": 0,
                "total_functions": 0,
                "total_methods": 0,
                "covered_classes": 0,
                "covered_functions": 0,
                "covered_methods": 0,
                "missing_doctests": [],
            },
        }

        for file_path in all_files:
            analysis = self.analyze_file_detailed(file_path)

            if "error" in analysis:
                if self.verbose:
                    print(f"Error analyzing {file_path}: {analysis['error']}")
                continue

            results["files"][str(file_path)] = analysis
            results["summary"]["total_files"] += 1

            results["summary"]["total_classes"] += analysis["total_classes"]
            results["summary"]["total_functions"] += analysis["total_functions"]
            results["summary"]["total_methods"] += analysis["total_methods"]
            results["summary"]["covered_classes"] += analysis["covered_classes"]
            results["summary"]["covered_functions"] += analysis["covered_functions"]
            results["summary"]["covered_methods"] += analysis["covered_methods"]

            self._collect_missing_doctests(
                analysis, results["summary"]["missing_doctests"]
            )

        return results

    def print_results(self, results: dict) -> None:
        """Print analysis results in the specified format."""
        if self.output_format == "json":
            print(json.dumps(results, indent=2, ensure_ascii=False))
            return

        if not results:
            print("No results to display.")
            return

        summary = results["summary"]

        if self.output_format == "text":
            self._print_text_results(results)
        elif self.output_format == "summary":
            self._print_summary_only(summary)
        elif self.output_format == "csv":
            self._print_csv_results(results)

    def _print_text_results(self, results: dict) -> None:
        """Print detailed text results."""
        summary = results["summary"]

        print("DOCTEST COVERAGE ANALYSIS")
        print("=" * 60)

        for file_path, analysis in results["files"].items():
            print(f"\n📁 {file_path}:")
            print("-" * 40)

            if analysis["classes"]:
                print(
                    f"📦 CLASSES ({analysis['covered_classes']}/{analysis['total_classes']} with doctest):"
                )
                for class_name, class_info in analysis["classes"].items():
                    status = "✅" if class_info["has_doctest"] else "❌"
                    print(f"   {status} {class_name}")

                    if class_info["methods"]:
                        print(
                            f"      Methods ({class_info['covered_methods']}/{class_info['total_methods']} with doctest):"
                        )
                        for method_name, method_info in class_info["methods"].items():
                            method_status = "✅" if method_info["has_doctest"] else "❌"
                            print(f"         {method_status} {method_name}")
                    print()

            if analysis["functions"]:
                print(
                    f"🔧 FUNCTIONS (top-level) ({analysis['covered_functions']}/{analysis['total_functions']} with doctest):"
                )
                for func_name, func_info in analysis["functions"].items():
                    status = "✅" if func_info["has_doctest"] else "❌"
                    print(f"   {status} {func_name}")
                print()

        self._print_summary_only(summary)

    def _print_summary_only(self, summary: dict) -> None:
        """Print only summary statistics."""
        print("=" * 60)
        print("📊 SUMMARY STATISTICS:")

        print(f"   Files processed: {summary['total_files']}")
        print()

        class_coverage = (
            (summary["covered_classes"] / summary["total_classes"] * 100)
            if summary["total_classes"] > 0
            else 0
        )
        print("   CLASSES:")
        print(f"      Total: {summary['total_classes']}")
        print(f"      With doctest: {summary['covered_classes']}")
        print(f"      Coverage: {class_coverage:.1f}%")

        func_coverage = (
            (summary["covered_functions"] / summary["total_functions"] * 100)
            if summary["total_functions"] > 0
            else 0
        )
        print("\n   FUNCTIONS (top-level):")
        print(f"      Total: {summary['total_functions']}")
        print(f"      With doctest: {summary['covered_functions']}")
        print(f"      Coverage: {func_coverage:.1f}%")

        method_coverage = (
            (summary["covered_methods"] / summary["total_methods"] * 100)
            if summary["total_methods"] > 0
            else 0
        )
        print("\n   CLASS METHODS:")
        print(f"      Total: {summary['total_methods']}")
        print(f"      With doctest: {summary['covered_methods']}")
        print(f"      Coverage: {method_coverage:.1f}%")

        total_elements = (
            summary["total_classes"]
            + summary["total_functions"]
            + summary["total_methods"]
        )
        covered_elements = (
            summary["covered_classes"]
            + summary["covered_functions"]
            + summary["covered_methods"]
        )
        overall_coverage = (
            (covered_elements / total_elements * 100) if total_elements > 0 else 0
        )

        print("\n   OVERALL COVERAGE (classes + functions + methods):")
        print(f"      Total elements: {total_elements}")
        print(f"      Covered with doctest: {covered_elements}")
        print(f"      Coverage percentage: {overall_coverage:.1f}%")

        print("\n💡 RECOMMENDATIONS:")
        if overall_coverage >= 80:
            print("   🟢 Excellent coverage! Project is well documented with examples.")
        elif overall_coverage >= 60:
            print(
                "   🟡 Good coverage. Consider adding doctest for remaining elements."
            )
        elif overall_coverage >= 40:
            print(
                "   🟠 Average coverage. Recommended to add doctest for the following elements:"
            )
        else:
            print(
                "   🔴 Low coverage. Critical to add doctest for the following elements:"
            )

        if summary["missing_doctests"]:
            print("\n   📌 ELEMENTS WITHOUT DOCTEST:")
            for item_type, item_name in summary["missing_doctests"][:5]:
                print(f"      • {item_type}: {item_name}")
            if len(summary["missing_doctests"]) > 5:
                print(
                    f"      • and {len(summary['missing_doctests']) - 5} more elements..."
                )
        else:
            print("\n   ✅ All elements have doctest coverage!")

    def _print_csv_results(self, results: dict) -> None:
        """Print results in CSV format."""
        print("file,element_type,element_name,has_doctest")

        for file_path, analysis in results["files"].items():
            for class_name, class_info in analysis["classes"].items():
                print(f"{file_path},class,{class_name},{class_info['has_doctest']}")

                for method_name, method_info in class_info["methods"].items():
                    print(
                        f"{file_path},method,{class_name}.{method_name},{method_info['has_doctest']}"
                    )

            for func_name, func_info in analysis["functions"].items():
                print(f"{file_path},function,{func_name},{func_info['has_doctest']}")

    def _collect_missing_doctests(
        self, analysis: dict, missing_list: list[tuple[str, str]]
    ) -> None:
        """Collect elements missing doctests for recommendations."""

        for class_name, class_info in analysis["classes"].items():
            if not class_info["has_doctest"]:
                missing_list.append(("Class", class_name))

            for method_name, method_info in class_info["methods"].items():
                if not method_info["has_doctest"]:
                    missing_list.append(("Method", f"{class_name}.{method_name}"))

        for func_name, func_info in analysis["functions"].items():
            if not func_info["has_doctest"]:
                missing_list.append(("Function", func_name))


def main():
    """Main entry point with CLI interface."""
    parser = argparse.ArgumentParser(
        description="Doctest coverage analysis tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s some_src_dir/                    
  %(prog)s file1.py file2.py              
  %(prog)s . --recursive --format json    
  %(prog)s src/ --format summary          
  %(prog)s . --format csv > results.csv   
        """,
    )

    parser.add_argument("targets", nargs="+", help="Files or directories to analyze")

    parser.add_argument(
        "--recursive",
        "-r",
        action="store_true",
        default=True,
        help="Recursively search directories for Python files (default: True)",
    )

    parser.add_argument(
        "--no-recursive", action="store_true", help="Disable recursive directory search"
    )

    parser.add_argument(
        "--format",
        "-f",
        choices=["text", "summary", "json", "csv"],
        default="text",
        help="Output format (default: text)",
    )

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )

    parser.add_argument(
        "--output", "-o", type=str, help="Output file (for JSON/CSV formats)"
    )

    args = parser.parse_args()

    recursive = args.recursive and not args.no_recursive
    analyzer = DetailedDoctestAnalyzer(verbose=args.verbose, output_format=args.format)
    results = analyzer.run_analysis(args.targets, recursive)

    if args.output and args.format in ["json", "csv"]:
        with open(args.output, "w", encoding="utf-8") as f:
            if args.format == "json":
                json.dump(results, f, indent=2, ensure_ascii=False)
            else:
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    analyzer.print_results(results)

                f.write(output.getvalue())
        if args.verbose:
            print(f"Results saved to {args.output}")
    else:
        analyzer.print_results(results)


if __name__ == "__main__":
    main()
