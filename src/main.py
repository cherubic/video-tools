from youtube_transcript_api import YouTubeTranscriptApi
import sys
import os
from deepmultilingualpunctuation import PunctuationModel
import spacy
import nltk
from nltk.tokenize import sent_tokenize
import stanza


def main(id: str, gpt_manual: bool = True):

    # 判断文件是否存在
    # 如果存在则直接读取文件
    # 如果不存在则调用YouTube API获取字幕
    # 如果获取字幕失败则返回错误信息
    # 如果获取字幕成功则将字幕写入文件
    if os.path.exists(id + ".txt"):
        print("字幕文件已存在")
    else:
        transcript = YouTubeTranscriptApi.get_transcript(id)
        if transcript is None:
            print("获取字幕失败")
            sys.exit(1)
        else:  
            with open(id + ".txt", "w") as f:
                for line in transcript:
                    f.write(line["text"] + " ")
                    
                print("获取字幕成功,写入文件")

    if (gpt_manual):
        with open(id + ".txt", "r") as file:
            origin_text = file.read()
            prompt_with_text = """
prompt:

please processing the text by step by step as follows:

1. original text start with "original start" and end with "original end",if not meet "original end", then notice the user continue to input. if meet "original end" then continue to step 2
2. add correct punctuation and split sentences according to the original text, don't output this step.
3. correct words and sentences according to the step 2 result then optimize according to context
4. summarize the step 3 result
5. translate the step 3 result into Chinese
6. summarize the step 5 result

output format:
1. step 3 output: optimize-output.txt
2. step 4 output: summarize-output.txt
3. step 5 output: translate-output.txt
4. step 6 output: summarize-translate-output.txt

original text:
original start
""" + origin_text + """
original end
"""

        with open(id + ".gptprompt.txt", "w") as file:
            file.write(prompt_with_text)
        
    else:
        # 调用OpenAI API将字幕整理成文章，并且不要修改原文，只需要添加对应的标点符号以及换行符即可
        # 使用spacy对文章进行分句
        with open(id + ".txt", "r") as file:
            origin_text = file.read()

        model = PunctuationModel()
        result = model.restore_punctuation(origin_text)
        
        spacy_nlp = spacy.load("en_core_web_sm")
        spacy_doc = spacy_nlp(result)

        with open(id + ".spacy.final.txt", "w", encoding="utf-8") as file:
            for sent in spacy_doc.sents:
                file.write(sent.text + "\n")

        nltk.download('punkt')
        nltk_sentences = sent_tokenize(result)

        with open(id + ".nltk.final.txt", "w", encoding="utf-8") as file:
            for sent in nltk_sentences:
                file.write(sent + "\n")

        stanza.download('en')
        stanza_nlp = stanza.Pipeline('en')
        stanza_doc = stanza_nlp(result)

        with open(id + ".stanza.final.txt", "w", encoding="utf-8") as file:
            for sent in stanza_doc.sentences:
                file.write(sent.text + "\n")

        print("done text processing")

        # 调用Google翻译API将文章翻译成中文
    


if __name__ == "__main__":

    # 解析系统传参：id
    youtube_id = sys.argv[1]

    # 如果没有传参数，默认为True
    if len(sys.argv) == 2:
        gpt_manual = True
    else:
        gpt_manual = sys.argv[2]
    
    main(youtube_id, gpt_manual)

