import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt_tab')

def split_by_comma_if_long(sentence, max_length=100):
    if len(sentence) <= max_length:
        return [sentence]

    midpoint = len(sentence) // 2
    comma_index = sentence.find(',', midpoint - 20, midpoint + 20)

    if comma_index != -1:
        part1 = sentence[:comma_index + 1].strip()
        part2 = sentence[comma_index + 1:].strip()
        return [part1, part2]

    return [sentence]

def fun_find_paragraphs_and_sentences(file):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read().strip()
        paragraphs = [p.strip() for p in content.splitlines() if p.strip()]

    paragraphs_and_sentences = []
    for p in paragraphs:
        sentences = sent_tokenize(p)
        processed_paragraph = []
        for s in sentences:
            processed_paragraph.extend(split_by_comma_if_long(s))
        paragraphs_and_sentences.append(processed_paragraph)
    all_sentences = [sentence for paragraph in paragraphs_and_sentences for sentence in paragraph]

    return paragraphs_and_sentences, all_sentences

