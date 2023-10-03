from faster_whisper import WhisperModel
# from translate import Translator
from googletrans import Translator
from pytube import YouTube
import os
import ffmpeg
import g4f
video_url = "https://www.youtube.com/watch?v=40dJS_LC6S8"
output_folder = "save"
output_filename = "output.mp3"
# 創建 YouTube 物件
yt = YouTube(video_url)
ytName =yt.title
output_txt_file = "output.txt"  # 指定輸出的 txt 檔案名稱
# 選擇最高品質的音樂串流
audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()

# 下載音樂
audio_file_path = audio_stream.download(output_folder)

# 取得下載的音樂檔案路徑及檔名
downloaded_filename = os.path.basename(audio_file_path)

# 設定輸出檔案路徑及檔名
output_file_path = os.path.join(output_folder, output_filename)

# 使用FFmpeg將音樂串流轉換成MP3格式
ffmpeg.input(audio_file_path).output(output_file_path, codec='libmp3lame').run()

# 刪除原始的音樂串流檔案
os.remove(audio_file_path)

#辨識文字
model = WhisperModel("large-v2", device="cuda", compute_type="float16")
#讀取mp3檔
content=""
start_time_in_minutes=""
end_time_in_minutes=""
segments, info = model.transcribe("save/"+output_filename)

def convert_seconds_to_minutes_seconds(seconds):
  minutes = seconds // 60
  seconds = seconds % 60
  return "%d:%.2f" % (minutes, seconds)
with open(os.path.join(output_folder, output_txt_file), "w", encoding="utf-8") as f:
    for segment in segments:
        start_time_in_minutes =str(int((segment.start)//60))+"分"+str(int((segment.start)) % 60)+"秒"
        end_time_in_minutes =str(int((segment.end)//60))+"分"+str(int((segment.end) % 60))+"秒"
        print("[%s  -> %s ] %s" % (start_time_in_minutes,end_time_in_minutes,segment.text))
        content+=("[%.2fs -> %.2fs] %s\n" % (segment.start, segment.end,segment.text))
        f.write("[%.2fs -> %.2fs] %s\n" % (segment.start, segment.end,segment.text))
# 刪除轉換後的音樂檔案（MP3）
os.remove(output_file_path)
print("===========================================")

# messages = []  # 存储消息的列表
# output_txt_file = "GPToutput.txt"  # 指定輸出的 txt 檔案名稱
# messages.append({"role": "system", "content": ""},)  # 将消息添加到列表
# messages.append({"role": "user", "content": "翻譯以下文字成中文:"+content})  # 将消息添加到列表
# response = g4f.ChatCompletion.create(
#     model="gpt-4",
#     provider=g4f.Provider.DeepAi,
#     messages=messages,
#     stream=True,
# )
# content=""
# for message in response:
#     print(message)
#     content+=message
# print("===========================================")
# print(content)
# with open(os.path.join(output_folder, output_txt_file), "w", encoding="utf-8") as f:
#     f.write(content)