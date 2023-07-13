from youtube_transcript_api import YouTubeTranscriptApi
import sys


def main(id: str):

    # 获取字幕后输入到文件中
    transcript = YouTubeTranscriptApi.get_transcript(id)
    with open(id + ".txt", "w") as f:
        for line in transcript:
            f.write(line["text"] + "\n")

    # 调用OpenAI API将字幕整理成文章，并且不要修改原文，只需要添加对应的标点符号以及换行符即可

    # 调用Google翻译API将文章翻译成中文


if __name__ == "__main__":

    # 解析系统传参：id
    youtube_id = sys.argv[1]
    
    main(youtube_id)

