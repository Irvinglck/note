一，JUC概述

 	1，java 有俩个线程 main&GC

​        2，new Thread().start();java是没有权限开启线程的，java会通过native调用本地方法

​	3，//获取CPU核数//CPU密集型 IO密集型System.out.println(Runtime.getRuntime().availableProcessors());

​        4，