from faster_whisper import WhisperModel
# from translate import Translator
from googletrans import Translator
from pytube import YouTube
import os
import ffmpeg
import g4f
video_url = "https://www.youtube.com/watch?v=SIY2oMBoEag"
output_folder = "save"
output_filename = "output.mp3"
output_txt_file = "output.txt"  # 指定輸出的 txt 檔案名稱
# 創建 YouTube 物件
yt = YouTube(video_url)

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
segments, info = model.transcribe("save/"+output_filename)
with open(os.path.join(output_folder, output_txt_file), "w", encoding="utf-8") as f:
    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end,segment.text))
        f.write("[%.2fs -> %.2fs] %s\n" % (segment.start, segment.end,segment.text))
# 刪除轉換後的音樂檔案（MP3）
os.remove(output_file_path)
