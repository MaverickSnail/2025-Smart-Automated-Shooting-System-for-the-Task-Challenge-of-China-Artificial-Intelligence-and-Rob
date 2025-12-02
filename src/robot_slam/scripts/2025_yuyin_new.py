#!/home/abot/anaconda3/envs/py38/bin/python
# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import os
import rospy
import asyncio
import edge_tts
import subprocess
from std_msgs.msg import String

class SimpleTTSNode:
    def __init__(self):
        rospy.init_node('simple_tts_node')
        
        # 语音配置
        self.voice = rospy.get_param('~voice', 'zh-CN-XiaoxiaoNeural')
        
        # 订阅语音消息
        rospy.Subscriber('voiceWords_tts', String, self.voice_callback, queue_size=10)
        
        rospy.loginfo(f"TTS节点已启动，使用语音模型: {self.voice}")
        rospy.loginfo("等待语音消息...")
        rospy.spin()

    def voice_callback(self, msg):
        """处理接收到的语音消息"""
        text = msg.data.strip()
        if not text:
            rospy.logwarn("收到空消息，跳过处理")
            return
            
        rospy.loginfo(f"合成语音: {text}")
        
        # 在新的线程中运行异步任务
        asyncio.run(self.text_to_speech(text))

    async def text_to_speech(self, text):
        """异步执行文本转语音"""
        try:
            # 创建临时文件路径
            audio_file = "tts_output.mp3"
            
            # 使用 edge_tts 合成语音
            communicate = edge_tts.Communicate(text, self.voice)
            await communicate.save(audio_file)
            
            # 使用 mpg321 播放生成的语音
            self.play_audio(audio_file)
            
        except Exception as e:
            rospy.logerr(f"语音处理失败: {str(e)}")

    def play_audio(self, file_path):
        """使用 mpg321 播放音频"""
        if not os.path.exists(file_path):
            rospy.logerr(f"音频文件不存在: {file_path}")
            return
            
        try:
            # 使用 mpg321 播放音频
            rospy.loginfo("开始播放...")
            subprocess.run(["mpg321", "-q", file_path], check=True)
            
            # 删除临时文件
            os.remove(file_path)
            
        except subprocess.CalledProcessError as e:
            rospy.logerr(f"播放失败: {e}")
        except Exception as e:
            rospy.logerr(f"播放错误: {str(e)}")

if __name__ == '__main__':
    try:
        SimpleTTSNode()
    except rospy.ROSInterruptException:
        pass
    except Exception as e:
        rospy.logfatal(f"节点发生错误: {str(e)}")