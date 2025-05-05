import os
import ast
import argparse
import datetime
import webbrowser

class CodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.issues = []

    def visit_Call(self, node):
        func_name = ""
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            func_name = node.func.attr

        if func_name in ['eval', 'exec', 'input']:
            self.issues.append((node.lineno, f"Use of dangerous function: {func_name}()"))
        elif func_name == 'system':
            self.issues.append((node.lineno, "Use of os.system()"))

        self.generic_visit(node)

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name) and "pass" in target.id.lower():
                self.issues.append((node.lineno, "Hardcoded password detected"))
        self.generic_visit(node)

def scan_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read(), filename=file_path)
        except SyntaxError as e:
            return [(e.lineno, f"SyntaxError: {e.msg}")]
    visitor = CodeVisitor()
    visitor.visit(tree)
    return visitor.issues

def generate_html_report(results, output_path="report.html"):
    html = "<html><head><title>CodeGuard Report</title></head><body>"
    html += f"<h2>CodeGuard Scan Report</h2><p>Generated on: {datetime.datetime.now()}</p><ul>"

    if not results:
        html += "<li>✅ No issues found.</li>"
    else:
        for file, issues in results.items():
            html += f"<li><b>{file}</b><ul>"
            for line, issue in issues:
                html += f"<li>Line {line}: {issue}</li>"
            html += "</ul></li>"

    html += "</ul></body></html>"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    webbrowser.open(output_path)

def main():
    parser = argparse.ArgumentParser(description="CodeGuard - AST-based Bug Scanner")
    parser.add_argument("path", help="File or directory to scan")
    parser.add_argument("--html", action="store_true", help="Generate HTML report")
    args = parser.parse_args()

    path = args.path
    results = {}

    if os.path.isfile(path) and path.endswith(".py"):
        results[path] = scan_file(path)
    elif os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    issues = scan_file(full_path)
                    if issues:
                        results[full_path] = issues
    else:
        print("❌ Invalid path.")
        return

    if args.html:
        generate_html_report(results)
    else:
        if not results:
            print("✅ No issues found.")
        else:
            for file, issues in results.items():
                print(f"\n📄 File: {file}")
                for line, issue in issues:
                    print(f"  Line {line}: {issue}")
                    print("Checking path:", os.path.abspath(path))

if __name__ == "__main__":
    main()
