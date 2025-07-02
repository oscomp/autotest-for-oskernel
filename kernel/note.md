

# Sifive Unmatched 评测流程

评测服务器环境变量应包含UNMATCHED=1表示应该使用哪块开发板进行评测。

评测机内部可根据此编号找到如下信息：
 + serial='/dev/ttyUSB0'
 + boot_file='boot_file_1.bin'
 + reset_channel='1'

编译学生代码生成os.bin。

将SD卡复位程序复制为boot_file指定的名字。

打开串口，重置开发板，并监控输出内容。

将os.bin根据boot_file重命名并复制到tftp目录。

打开串口，重置开发板，并监控输出内容。
