from moviepy.editor import VideoFileClip
from spleeter.separator import Separator

# import whisper
# from aeneas.executetask import ExecuteTask
# from aeneas.task import Task


def extract_audio_from_video(video_path, output_audio_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(output_audio_path)


def separate_audio(audio_path, output_dir):
    separator = Separator("spleeter:2stems")
    separator.separate_to_file(audio_path, output_dir)


# def transcribe_audio_to_text(audio_path, language="zh"):
#     model = whisper.load_model("base")
#     result = model.transcribe(audio_path, language=language)
#     return result["text"]


# def generate_srt(audio_path, lyrics, output_srt_path):
#     task = Task()
#     task.configuration_string = (
#         "task_language=cmn|is_text_type=plain|os_task_file_format=srt"
#     )
#     task.audio_file_path_absolute = audio_path
#     task.text_file_path_absolute = lyrics
#     task.sync_map_file_path_absolute = output_srt_path
#     ExecuteTask(task).execute()
#     task.output_sync_map_file()


def process_video(video_path, lyrics=None, provided_audio_path=None):
    # Step 1: Extract Audio from Video if no audio provided
    if not provided_audio_path:
        audio_path = "extracted_audio.wav"
        extract_audio_from_video(video_path, audio_path)
    else:
        audio_path = provided_audio_path

    print("finish step 1")

    # Step 2: Separate Vocals and Instrumentals
    output_dir = "separated_audio"
    separate_audio(audio_path, output_dir)

    instrumental_path = f"{output_dir}/accompaniment.wav"
    vocal_path = f"{output_dir}/vocals.wav"

    print("finish step 2")

    # # Step 3: Transcribe Audio to Text if lyrics not provided
    # if not lyrics:
    #     lyrics = transcribe_audio_to_text(vocal_path)

    # # Step 4: Generate Subtitle File
    # output_srt_path = "karaoke.srt"
    # generate_srt(vocal_path, lyrics, output_srt_path)

    return {
        "instrumental_path": instrumental_path,
        "vocal_path": vocal_path,
        # "srt_path": output_srt_path,
    }


result = process_video("music_video.mp4")
print(f"Instrumental: {result['instrumental_path']}")
print(f"Vocal: {result['vocal_path']}")
print(f"Subtitle: {result['srt_path']}")
