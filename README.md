# Audio-Latency-Test
This is a repository for Audio-Latency-Test using your microphone and speaker.

usage:

pip install pyaudio

python test.py

This test file record the whole latency from sending waves to receiving waves, which means you need to prepare a microphone to test your speaker device. The result is effected by your two devices and your computer.


# 中文

这是一个用于相对比较各种耳机延迟的仓库。作者主要使用他验证购买的蓝牙耳机延迟过高的问题。

使用方法：

pip install pyaudio  //安装环境

python test.py  //运行python代码

注意：

本测试给出的延迟数值包括从电脑发送到扬声器播放，再到麦克风接收，直到电脑匹配到波形。这意味着所给出的时间应大于实际扬声器听到的延迟。但如果采用相同的麦克风和不同的扬声器，则可以很好地比较固定的扬声器(如有线耳机)和您所要测试的扬声器(如蓝牙耳机、2.4G连接耳机)的延迟关系。
