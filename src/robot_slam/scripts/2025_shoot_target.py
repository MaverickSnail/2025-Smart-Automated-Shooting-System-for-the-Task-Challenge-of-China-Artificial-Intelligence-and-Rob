#!/home/abot/anaconda3/envs/py38/bin/python
#coding: utf-8
import rospy
from std_msgs.msg import String, Int32


# 全局发布器与目标ID存储
arrive_pub = None               # 语音反馈发布器
target_id_rotating_pub = None   # 旋转靶ID发布器
target_id_moving_pub = None     # 移动靶ID发布器
target_id_rotating = None       # 存储检测到的旋转靶ID
target_id_moving = None         # 存储检测到的移动靶ID

# 旋转靶ID映射（中文数字 -> 数字ID）
target_id_rotating_mapping = {
    "一": 1,  # 旋转靶一号
    "二": 2,  # 旋转靶二号
    "三": 3,  # 旋转靶三号
    "四": 4,  # 旋转靶四号
    "五": 5   # 旋转靶五号
    # 可扩展：添加更多旋转靶映射
}

# 移动靶ID映射（中文数字 -> 数字ID）
target_id_moving_mapping = {
    "六": 6,  # 移动靶六号
    "七": 7,  # 移动靶七号
    "八": 8   # 移动靶八号
    # 可扩展：添加更多移动靶映射
}

def chinese_callback(msg):
    """
    ROS消息回调函数 - 处理接收到的中文语音指令
    参数:
        msg: 包含语音识别文本的ROS消息
    """
    global arrive_pub, target_id_rotating, target_id_moving, arrive_str
    
    # 记录接收到的指令
    rospy.loginfo(f"接收到语音指令: {msg.data}")
    arrive_str = ""
    # === 旋转靶检测模块 ===
    # 遍历旋转靶关键词映射表
    for keyword, value in target_id_rotating_mapping.items():
        if keyword in msg.data:  # 检测指令中是否包含关键词
            # 设置旋转靶ID
            target_id_rotating = value
            
            # 记录检测到的旋转靶信息
            rospy.loginfo(f"检测到旋转靶关键词：{keyword}，设置 target_id_rotating={target_id_rotating}")
            
            # 生成语音反馈信息并发布
            arrive_str = arrive_str + "旋转靶为{}号".format(keyword)
            # arrive_pub.publish(arrive_str)
            
            # 尝试发布旋转靶ID到指定话题
            try:
                target_id_rotating_pub.publish(target_id_rotating)
                rospy.loginfo(f"已发布旋转靶：target_id_rotating={target_id_rotating}到话题target_id_rotating")
            except Exception as e:
                rospy.logerr(f"发布旋转靶 target_id 时出错：{e}")
            
            break  # 找到一个关键词即结束循环

    # === 移动靶检测模块 ===
    # 遍历移动靶关键词映射表
    for keyword, value in target_id_moving_mapping.items():
        if keyword in msg.data:  # 检测指令中是否包含关键词
            # 设置移动靶ID
            target_id_moving = value
            
            # 记录检测到的移动靶信息
            rospy.loginfo(f"检测到移动靶关键词：{keyword}，设置 target_id_moving={target_id_moving}")
            
            # 生成语音反馈信息并发布
            arrive_str = arrive_str + "移动靶为{}号".format(keyword)
            arrive_pub.publish(arrive_str)
            # arrive_pub.publish(arrive_str)
            
            # 尝试发布移动靶ID到指定话题
            try:
                target_id_moving_pub.publish(target_id_moving)
                rospy.loginfo(f"已发布移动靶：target_id_moving={target_id_moving}到话题target_id_moving")
            except Exception as e:
                rospy.logerr(f"发布移动靶 target_id 时出错：{e}")
            
            break  # 找到一个关键词即结束循环

def chinese_subscriber():
    """
    ROS节点初始化函数
    功能:
      1. 初始化ROS节点
      2. 创建发布者/订阅者
      3. 启动消息循环
    """
    global arrive_pub, target_id_rotating_pub, target_id_moving_pub
    
    # 节点初始化
    rospy.init_node('chinese_subscriber', anonymous=True)
    rospy.loginfo("正在启动射击目标识别节点...")
    
    # 创建发布者
    # 语音反馈发布到/voiceWords话题
    arrive_pub = rospy.Publisher('/voiceWords_tts', String, queue_size=10)
    
    # 旋转靶ID发布到target_id_rotating话题
    target_id_rotating_pub = rospy.Publisher('target_id_rotating', Int32, queue_size=10)
    
    # 移动靶ID发布到target_id_moving话题
    target_id_moving_pub = rospy.Publisher('target_id_moving', Int32, queue_size=10)
    
    # 创建订阅者 - 订阅chinese_topic话题（接收语音识别结果）
    rospy.Subscriber("chinese_topic", String, chinese_callback)
    
    rospy.loginfo("射击目标识别节点已成功启动")
    rospy.loginfo("等待语音指令识别射击目标...")
    
    # 启动消息循环
    rospy.spin()

# === 主程序入口 ===
if __name__ == '__main__':
    try:
        chinese_subscriber()
    except rospy.ROSInterruptException:
        rospy.loginfo("ROS 节点被中断")
        



    
