# extract_and_generate.py
import re
from bs4 import BeautifulSoup
import json

def extract_mathml_from_html(input_html_path, output_html_path):
    with open(input_html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    math_entries = []

    # Find all inline math spans that contain hidden <mathml>
    for span in soup.find_all('span', class_=re.compile(r'math-inline|math-display')):
        mathml_tag = span.find('mathml', style="display: none;")
        if not mathml_tag:
            continue

        # Extract the raw MathML string
        mathml_str = str(mathml_tag.find('math'))  # get the <math>...</math> part

        # Optional: get LaTeX if available
        latex_tag = span.find('latex', style="display: none;")
        latex = latex_tag.text.strip() if latex_tag else None

        # Optional: get AsciiMath
        asciimath_tag = span.find('asciimath', style="display: none;")
        asciimath = asciimath_tag.text.strip() if asciimath_tag else None

        math_entries.append({
            "id": f"math-{len(math_entries)+1}",
            "mathml": mathml_str,
            "latex": latex,
            "asciimath": asciimath
        })

        # Replace the entire span with a placeholder <div> for dynamic loading
        placeholder = soup.new_tag('div')
        placeholder['id'] = f"math-{len(math_entries)}"
        placeholder['class'] = 'dynamic-math'
        span.replace_with(placeholder)

    # Generate JavaScript data
    js_data = f"const mathData = {json.dumps(math_entries, indent=2)};\n"

    # Create new standalone HTML with dynamic loading
    new_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dynamic MathML Loading</title>
    <style>
        .dynamic-math {{ min-height: 30px; margin: 10px 0; padding: 8px; border: 1px dashed #ccc; }}
        .math-loaded {{ border: none; }}
        mjx-container {{ display: inline-block; }}
    </style>
    <!-- Optional: MathJax fallback for browsers without MathML support -->
    <script>
        // Check if browser has good MathML support (most don't — Firefox does, Chrome doesn't)
        function hasNativeMathML() {{
            const div = document.createElement('div');
            div.innerHTML = '<math><mi>x</mi></math>';
            document.body.appendChild(div);
            const rendered = div.firstChild.firstChild.getBoundingClientRect().height > 0;
            document.body.removeChild(div);
            return rendered;
        }}
        const useNativeMathML = hasNativeMathML();
    </script>
</head>
<body>
    <h1>Dynamic MathML Expressions</h1>
    <p>Loading math expressions from parsed MathML using JavaScript:</p>

    {soup.body.decode_contents() if soup.body else ""}

    <script>
        {js_data}

        // Dynamically render all math expressions
        function renderAllMath() {{
            mathData.forEach(item => {{
                const el = document.getElementById(item.id);
                if (!el) return;

                if (useNativeMathML) {{
                    // Use native MathML
                    el.innerHTML = item.mathml;
                    el.classList.add('math-loaded');
                }} else {{
                    // Fallback: use MathJax
                    el.innerHTML = '`' + (item.latex || item.asciimath || '') + '`';
                    el.classList.add('math-loaded');
                    if (window.MathJax) {{
                        MathJax.typesetPromise([el]);
                    }}
                }}
            }});
        }}

        // Load MathJax only if needed (lazy load)
        function loadMathJax() {{
            if (window.MathJax) return;
            const script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js';
            script.async = true;
            script.onload = () => {{
                MathJax.typesetPromise();
            }};
            document.head.appendChild(script);
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            if (useNativeMathML) {{
                renderAllMath();
            }} else {{
                loadMathJax();
                // Re-render when MathJax is ready
                document.addEventListener('mathjax-ready', renderAllMath, {{ once: true }});
                // Or fallback timeout
                setTimeout(renderAllMath, 3000);
            }}
        }});
    </script>

    <!-- Signal MathJax is ready -->
    <script>
        if (!useNativeMathML) {{
            window.addEventListener('load', () => {{
                setTimeout(() => document.dispatchEvent(new Event('mathjax-ready')), 1000);
            }});
        }}
    </script>
</body>
</html>
"""

    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(new_html)

    print(f"Generated {output_html_path} with {len(math_entries)} math expressions.")

# Usage
if __name__ == "__main__":
    extract_mathml_from_html("input.html", "dynamic_math_page.html")
