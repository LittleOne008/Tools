import re
from difflib import SequenceMatcher


def extract_data(file_path):
    ref_lines = []
    hyp_lines = []
    file_names = []

    with open(file_path, "r", encoding="utf-8") as file:
        ref, hyp, filename = None, None, None
        for line in file:
            if ".wav" in line:
                # 提取文件名（最后一个斜杠后的部分）
                filename = line.strip().split('/')[-1]
                file_names.append(filename)
            elif line.startswith("ref:"):
                ref = line.replace("ref:", "").strip()
                ref_lines.append(ref)
            elif line.startswith("hyp:"):
                hyp = line.replace("hyp:", "").strip()
                hyp_lines.append(hyp)

    return file_names, ref_lines, hyp_lines


def highlight_differences(ref, hyp):
    matcher = SequenceMatcher(None, ref, hyp)
    highlighted_ref = []
    highlighted_hyp = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        ref_text = ref[i1:i2]
        hyp_text = hyp[j1:j2]

        if tag == "equal":
            highlighted_ref.append(ref_text)
            highlighted_hyp.append(hyp_text)
        elif tag == "replace" or tag == "delete":
            highlighted_ref.append(f'<span style="background-color: #ffcccc;">{ref_text}</span>')
        if tag == "replace" or tag == "insert":
            highlighted_hyp.append(f'<span style="background-color: #ccffcc;">{hyp_text}</span>')

    return ''.join(highlighted_ref), ''.join(highlighted_hyp)


def generate_html_diff(file_names, ref_lines, hyp_lines, output_file="diff_output.html"):
    html_content = "<html><body><h2>Text Comparison</h2>"

    for i, (filename, ref, hyp) in enumerate(zip(file_names, ref_lines, hyp_lines), 1):
        highlighted_ref, highlighted_hyp = highlight_differences(ref, hyp)

        # HTML内容按文件名、参考文本和比较文本顺序显示
        html_content += f"""
        <div style="margin-bottom: 20px;">
            <h3>File: {filename}</h3>
            <div><strong>Reference:</strong><br>{highlighted_ref}</div>
            <div><strong>Hypothesis:</strong><br>{highlighted_hyp}</div>
        </div>
        <hr>
        """

    html_content += "</body></html>"

    # 将 HTML 内容写入文件
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(html_content)


# 使用示例
file_path = "test.txt"  # 输入包含 'ref:'、'hyp:' 和文件名的行
file_names, ref_lines, hyp_lines = extract_data(file_path)
generate_html_diff(file_names, ref_lines, hyp_lines)
