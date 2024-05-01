# process_document.py
import re
from docx import Document

def process_document(input_file, max_length=400, min_length=50):
    doc_input = Document(input_file)
    sentences = []
    grouped_sentences = []
    current_length = 0

    for para in doc_input.paragraphs:
        # 使用正则表达式分割句子
        sentences_in_para = re.split('(?<=[.。！？])(?![0-9])', para.text)
        sentences_in_para = [sentence.strip() for sentence in sentences_in_para if sentence.strip() != '']
        for sentence in sentences_in_para:
            # 如果添加这个句子会超过 max_length 字，就开始新的一组
            if current_length + len(sentence) > max_length:
                group = ' '.join(sentences)
                # 检查字数是否大于等于 min_length
                if len(group) >= min_length:
                    grouped_sentences.append(group)
                sentences = []
                current_length = 0
            sentences.append(sentence)
            current_length += len(sentence)
    # 添加最后一组句子
    if sentences:
        group = ' '.join(sentences)
        if len(group) >= min_length:
            grouped_sentences.append(group)

    return grouped_sentences

# 可选：如果作为主程序运行，处理指定的文档
if __name__ == "__main__":
    input_file = 'input.docx'  # 指定要处理的文件名
    max_length = 400  # 可以根据需要调整
    min_length = 50  # 可以根据需要调整
    grouped_sentences = process_document(input_file, max_length, min_length)
    
    total = len(grouped_sentences)  # 获取组的总数
    print(f"=====总组个数：【{total}】=====")
    print(f"=====文本预览如下：=====")
    for i in range(min(4, len(grouped_sentences))):  # 预览前 4 组，或者少于 4 组的全部
        print(grouped_sentences[i])
    
    # play_beep()  # 根据需要调用 play_beep，这里需要你自行定义 play_beep 函数或导入相关库
