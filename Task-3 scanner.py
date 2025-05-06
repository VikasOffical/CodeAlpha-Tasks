import ast
from fpdf import FPDF

class SecurityScanner(ast.NodeVisitor):
    def __init__(self):
        self.issues = []

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in ["eval", "exec", "compile"]:
                self.issues.append((node.lineno, f"Use of dangerous function: {node.func.id}()"))
        elif isinstance(node.func, ast.Attribute):
            if node.func.attr in ["load", "loads"]:
                if hasattr(node.func.value, 'id') and node.func.value.id == "pickle":
                    self.issues.append((node.lineno, f"Insecure deserialization with: pickle.{node.func.attr}()"))
        self.generic_visit(node)

def scan_code(filepath):
    with open(filepath, "r") as f:
        code = f.read()
    tree = ast.parse(code, filename=filepath)
    scanner = SecurityScanner()
    scanner.visit(tree)
    return scanner.issues, code

def generate_pdf(issues, output_path, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Security Scan Report: {filename}", ln=True, align="L")
    if not issues:
        pdf.cell(200, 10, txt="No security issues found.", ln=True, align="L")
    else:
        for lineno, issue in issues:
            pdf.cell(200, 10, txt=f"Line {lineno}: {issue}", ln=True, align="L")
    pdf.output(output_path)
