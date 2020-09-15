# 一，消息队列

​	1，使用消息队列有点

​			1.1解耦
​			1.2可恢复性-
​				系统挂了，重启系统后消息继续消费
​			1.3缓冲
​				优化生产跟消费不对称的情况
​			1.4灵活性&峰值处理
​				灵活的上机器

​	2，消息队列俩种模式
​		1，点对点		
​			消费完，消息会被从queue中取出来
​		2，发布订阅（kafka）

​				<img src="D:\文档\学习\kafka\imgs\1.jpg" style="zoom: 50%; margin-left:10%" />

​				消费完，不会消息依然会在队列中，消息会有期限；

​				消费方式：1，消费者主动拉去消费(kafka使用方式)
​										缺点会维持一个长连接	
​								 2，消息队列Topic主动推送（这样会有一个缺点，消费者的消费能力是不一样的）

# 二，kafka基础架构

# <img src="D:\文档\学习\kafka\imgs\2.jpg" style="zoom: 33%;" />

​		Broker:一台主机，也叫分区,一个集群就是由多个broker组成
​		Topic:消息类别，可以理解为一个队列，一个主题可以有多个分区，生产者消费者都是面向一个topic
​		Leader:生产者提供数据的对象，消费者消费的对象
​		Follower:同步leader消息，写入磁盘(一个分区分为分为一个leader和一个Follower)，实时同步Leader
​						的数据，leader挂了，某个follower会成为一个leader
​		Partition:为了实现扩展，一个topic 可以分配到多个broker（服务器）上，一个topic可以分成多个
​						parttion,每个parttiton都是一个有序队列
​		Replication:副本，为了保证集群中某个节点发生故障时，该节点上的partition数据不会丢失，且kafka
​							仍然可以继续工作，fafka提供了副本机制，一个topic的每个分区上都有若干个副本，一个
​							leader若干个follower
​		ConsumerGroup(CG):消费者组，多个consumer组成，每个消费者负责消费不同分区的数据，一个分区
​							只能由一个组内消费者消费；消费组直接互不影响，所有的消费者都属于某个组，消费者逻辑上
​							是一个订阅者

​	  说明(一个消费组group中，一个消费者只能消费一个分区中的一个生产者leader
​		一个主题Topic可以有多个分区，一个分区Broker在一个机器上
​		一个机器上一个分区分成一个leader(作用是提供给消费者消费)一个follower（作用是将消息写在本地，重启消息队列使用）
​		一般消费组中消费者个数跟分区数是相等的)

​		消费者挂了，0.9消费offset被记录在zookeeper中，0.9之后是存在主题中

​			

