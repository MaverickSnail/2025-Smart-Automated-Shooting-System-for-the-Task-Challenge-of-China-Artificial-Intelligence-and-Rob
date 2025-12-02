#!/home/abot/anaconda3/envs/py38/bin/python
# -*- coding: utf-8 -*-
import rospy
import pyaudio
import wave
import os
import sys
from pathlib import Path  # 添加Path对象处理路径[2,4](@ref)
from funasr import AutoModel
import soundfile
from std_msgs.msg import String

# 获取当前脚本所在目录的Path对象[2,3,4](@ref)
SCRIPT_DIR = Path(__file__).parent.resolve()

# 使用相对路径定义资源文件[1,3,4](@ref)
music_path = SCRIPT_DIR / "start_record.mp3"
music1_path = SCRIPT_DIR / "end_record.mp3"
MODEL_DIR = SCRIPT_DIR / "paraformer-zh"  # 模型目录

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

def audio_callback(msg):
    rospy.loginfo("Received audio message, starting recording and recognition")
    start_audio()
    rospy.loginfo("Recording and recognition completed")

def start_audio(time=5, save_file=SCRIPT_DIR / "test.wav"):
    global model
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 16000
    RECORD_SECONDS = time
    # 使用相对路径保存录音文件[1,3](@ref)
    WAVE_OUTPUT_FILENAME = SCRIPT_DIR / save_file

    p = pyaudio.PyAudio()
    rospy.loginfo("ON")
    # 使用系统无关的路径格式[2,4](@ref)
    os.system(f'mplayer "{music_path}"')
    
    # 使用Path对象检查文件存在性[2,4](@ref)
    if WAVE_OUTPUT_FILENAME.exists():
        os.remove(str(WAVE_OUTPUT_FILENAME))

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    rospy.loginfo("OFF")
    os.system(f'mplayer "{music1_path}"')

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(str(WAVE_OUTPUT_FILENAME), 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    rospy.loginfo("Starting recognition")
    # 使用相对路径读取录音文件[1,3](@ref)
    res = model.generate(input=str(WAVE_OUTPUT_FILENAME))
    
    result = res[0].get('text','默认值')
    print(result)
    
    # 等待发布者注册
    rospy.loginfo("Waiting for publisher to register...")
    while pub1.get_num_connections() == 0 and not rospy.is_shutdown():
        rospy.sleep(0.1)
    while pub2.get_num_connections() == 0 and not rospy.is_shutdown():
        rospy.sleep(0.1)

    # 发布消息
    message = str(result)
    rospy.loginfo("Publishing message: " + message)
    pub1.publish(message)
    pub2.publish(message)
    rospy.sleep(0.5)

def audio_subscriber():
    rospy.init_node('audio_subscriber', anonymous=True)
    rospy.Subscriber("audio_topic", String, audio_callback)
    global pub1
    global pub2
    pub1 = rospy.Publisher('chinese_topic', String, queue_size=10)
    pub2 = rospy.Publisher('chinese_topic1', String, queue_size=10)
    rospy.loginfo("Audio subscriber node started")
    rospy.spin()

if __name__ == '__main__':
    # 使用相对路径加载模型[1,3,4](@ref)
    model = AutoModel(model=str(MODEL_DIR), disable_update=True)
    audio_subscriber()
