from pytube import YouTube
import os
import ffmpeg

def download_and_convert_to_mp3(video_url, output_path, output_filename):
    try:
        # 創建 YouTube 物件
        yt = YouTube(video_url)

        # 選擇最高品質的音樂串流
        audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()

        # 下載音樂
        audio_file_path = audio_stream.download(output_path)

        # 取得下載的音樂檔案路徑及檔名
        downloaded_filename = os.path.basename(audio_file_path)

        # 設定輸出檔案路徑及檔名
        output_file_path = os.path.join(output_path, output_filename)

        # 使用FFmpeg將音樂串流轉換成MP3格式
        ffmpeg.input(audio_file_path).output(output_file_path, codec='libmp3lame').run()

        # 刪除原始的音樂串流檔案
        os.remove(audio_file_path)

        print(f"音樂下載並轉換成MP3成功，檔案位於：{output_file_path}")

        return output_file_path

    except Exception as e:
        print(f"下載過程中發生錯誤：{e}")
        return None

if __name__ == "__main__":
    # 填入欲下載音樂的 YouTube 連結、欲存放音樂的路徑和檔案名稱
    video_url = "https://www.youtube.com/watch?v=SIY2oMBoEag"
    output_folder = "save"
    output_filename = "output.mp3"

    mp3_file_path = download_and_convert_to_mp3(video_url, output_folder, output_filename)

    if mp3_file_path:
        print(f"MP3檔案名稱：{os.path.basename(mp3_file_path)}")
    else:
        print("MP3檔案下載及轉換失敗")