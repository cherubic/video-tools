from youtube_transcript_api import YouTubeTranscriptApi
import sys
import spacy
import os
import stanza


def main(id: str):

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
                    f.write(line["text"] + "\n")
                    
                print("获取字幕成功,写入文件")

    # 调用OpenAI API将字幕整理成文章，并且不要修改原文，只需要添加对应的标点符号以及换行符即可
    # 使用spacy对文章进行分句
    # nlp = spacy.load("en_core_web_sm")
    with open(id + ".txt", "r") as file:
        text = file.read()

    # doc = nlp(text)

    # sentences = [sent.text for sent in doc.sents]

    stanza.download('en')
    nlp = stanza.Pipeline('en')
    doc = nlp(text)

    
    with open(id + "final.txt", "w", encoding="utf-8") as file:
        for sentence in doc.sentences:
            file.write(sentence.text + "\n")

    print("done")

    # 调用Google翻译API将文章翻译成中文


if __name__ == "__main__":

    # 解析系统传参：id
    youtube_id = sys.argv[1]
    
    main(youtube_id)

