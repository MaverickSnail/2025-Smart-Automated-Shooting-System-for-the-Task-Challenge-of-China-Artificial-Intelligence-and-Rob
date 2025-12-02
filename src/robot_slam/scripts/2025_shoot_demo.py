#!/home/abot/anaconda3/envs/py38/bin/python
# -*- coding: utf-8 -*-
import rospy
import pyaudio
import wave
import os
from pathlib import Path  # 添加Path对象处理路径[2,4](@ref)
from funasr import AutoModel
from std_msgs.msg import String

# 获取当前脚本所在目录的Path对象[2,3,4](@ref)
SCRIPT_DIR = Path(__file__).parent.resolve()

# 使用相对路径定义资源文件[1,3,4](@ref)
music_path = SCRIPT_DIR / "start_record.mp3"
music1_path = SCRIPT_DIR / "end_record.mp3"
MODEL_DIR = SCRIPT_DIR / "paraformer-zh"  # 模型目录

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

def audio_callback(msg):
    rospy.loginfo("收到录音指令，开始录音识别")
    start_audio()
    rospy.loginfo("录音识别完成")

def start_audio(time=5, save_file = SCRIPT_DIR / "test.wav"):
    global model
    
    # 音频参数
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 16000
    RECORD_SECONDS = time
    
    # 初始化音频设备
    p = pyaudio.PyAudio()
    rospy.loginfo("录音开始")
    os.system(f'mplayer "{music_path}"')
    
    # 清理旧文件
    if os.path.exists(save_file):
        os.remove(save_file)

    # 开始录音
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    # 结束录音
    rospy.loginfo("录音结束")
    os.system(f'mplayer "{music1_path}"')
    stream.stop_stream()
    stream.close()
    p.terminate()

    # 保存录音文件
    with wave.open(str(save_file), 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    # wf = wave.open(save_file, 'wb')
    # wf.setnchannels(CHANNELS)
    # wf.setsampwidth(p.get_sample_size(FORMAT))
    # wf.setframerate(RATE)
    # wf.writeframes(b''.join(frames))
    # wf.close()
    
    # 语音识别
    rospy.loginfo("开始语音识别")
    res = model.generate(input=str(save_file))
    result = res[0].get('text', '识别失败')
    print("识别结果:", result)

    # 发布识别结果
    rospy.loginfo("等待发布器注册")
    while pub1.get_num_connections() == 0 and not rospy.is_shutdown():
        rospy.sleep(0.1)
    #while pub2.get_num_connections() == 0 and not rospy.is_shutdown():
    #    rospy.sleep(0.1)

    pub1.publish(result)
    #pub2.publish(result)
    rospy.loginfo(f"已发布识别结果: {result}")
    rospy.sleep(0.5)

def audio_subscriber():
    global pub1
    global pub2
    rospy.init_node('audio_subscriber', anonymous=True)
    rospy.Subscriber("audio_topic", String, audio_callback)
    pub1 = rospy.Publisher('chinese_topic', String, queue_size=10)
    #pub2 = rospy.Publisher('chinese_topic1', String, queue_size=10)
    rospy.loginfo("语音识别节点已启动")
    rospy.spin()

if __name__ == '__main__':
    model = AutoModel(
        model=str(MODEL_DIR),
        disable_update=True
    )
    audio_subscriber()
