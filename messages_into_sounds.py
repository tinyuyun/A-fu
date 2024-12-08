import asyncio
import time
import pygame
from datetime import datetime
import re
import edge_tts


def remove_brackets_content(text):
    """去除文本中的【】及其内部内容"""
    return re.sub(r'【.*?】', '', text)


def speak(text: str, voice: str = "zh-CN-XiaoyiNeural") -> None:
    """将给定文本转换为语音并播放。"""
    # 使用时间戳创建唯一的输出文件名
    output_file = f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    text = remove_brackets_content(text)

    async def amain() -> None:
        """异步函数，执行文本到语音转换并保存音频文件。"""
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)

    # 执行异步主函数
    asyncio.run(amain())

    # 播放保存的MP3文件
    pygame.mixer.init()
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()

    # 等待直到音乐停止
    while pygame.mixer.music.get_busy():
        time.sleep(1)


   #可能的异步报错点