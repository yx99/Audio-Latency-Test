import pyaudio
import wave
import numpy as np
from scipy.signal import correlate

def play_and_record(audio_file, fs, channels, frames_per_buffer=1024):
    p = pyaudio.PyAudio()

    # 打开音频文件
    wf = wave.open(audio_file, 'rb')

    # 定义流的参数
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    input=True,
                    frames_per_buffer=frames_per_buffer)

    # 播放和录音数据存储
    frames = []

    # 播放和录音
    data = wf.readframes(frames_per_buffer)
    while len(data) > 0:
        stream.write(data)  # 播放音频
        recorded_data = stream.read(frames_per_buffer)  # 录制音频
        frames.append(recorded_data)
        data = wf.readframes(frames_per_buffer)

    # 停止流
    stream.stop_stream()
    stream.close()
    p.terminate()

    # 将录制的数据转换为numpy数组
    recorded_audio = np.frombuffer(b''.join(frames), dtype=np.int16)

    return recorded_audio, wf.getframerate()

def calculate_delay(play_audio_file, recorded_audio, fs):
    # 打开并读取原始音频文件
    wf = wave.open(play_audio_file, 'rb')
    original_audio = wf.readframes(wf.getnframes())
    original_audio = np.frombuffer(original_audio, dtype=np.int16)

    # 对录制的音频进行归一化处理
    recorded_audio = recorded_audio / np.max(np.abs(recorded_audio))
    original_audio = original_audio / np.max(np.abs(original_audio))

    # 计算相关性以确定延迟
    correlation = correlate(recorded_audio, original_audio, mode='full')
    lag = np.argmax(correlation) - len(original_audio) + 1

    # 处理负延迟
    if lag < 0:
        return np.nan  # 跳过负延迟

    delay = lag / fs
    return delay

def average_delay(audio_file, fs, channels, num_samples):
    delays = []

    for i in range(num_samples):
        print(f"正在进行第 {i+1} 次测试...")
        recorded_audio, fs = play_and_record(audio_file, fs, channels)
        delay = calculate_delay(audio_file, recorded_audio, fs)
        if not np.isnan(delay):
            delays.append(delay)
            print(f"第 {i+1} 次测试延迟时间: {delay:.6f} 秒")
        else:
            print(f"第 {i+1} 次测试的延迟值无效，跳过")

    # 计算平均延迟时间
    if len(delays) > 0:
        average_delay = np.mean(delays)
    else:
        average_delay = float('nan')  # 如果没有有效的测试结果

    return average_delay

# 设置参数
audio_file = './kick.wav'  # 替换为您的音频文件路径
fs = 44100  # 采样率
channels = 1  # 声道数
num_samples = 10  # 测试次数

# 多次测试并计算平均延迟时间
average_delay_value = average_delay(audio_file, fs, channels, num_samples)

if np.isnan(average_delay_value):
    print("没有有效的延迟值可用于计算平均延迟时间。")
else:
    print(f"音频从播放到接收的平均延迟时间: {average_delay_value:.6f} 秒")
