**#1，JUC概述**

​			1.1，java 有俩个线程 main&GC

​       	1.2，new Thread().start();java是没有权限开启线程的，java会通过native调用本地方法

​			1.3，//获取CPU核数//CPU密集型 IO密集型System.out.println(Runtime.getRuntime().availableProcessors());

**#二，常用对象**

​	##1，CopyOnWriteArrayList 并发包线程安全

```java
public static void main(String[] args) {
//        List<String> lists = new ArrayList<>();
		//不使用并发包利用集合转换
//        List<String> lists = Collections.synchronizedList(new ArrayList<>());
        List<String> lists = new CopyOnWriteArrayList<>();

        for (int i = 1; i <= 20; i++) {
            new Thread(() -> {
                lists.add(UUID.randomUUID().toString().substring(0, 6));
                System.out.println(lists);
            }, String.valueOf(i)).start();
        }
    }
```

​	2,CopyOnWriteArraySet

​	

```java
 public static void main(String[] args) {
//        Set<String> sets = new HashSet<>();
//        Set<String> sets = Collections.synchronizedSet(new HashSet<>());
        Set<String> sets = new CopyOnWriteArraySet<>();
        for (int i = 0; i < 200; i++) {
            new Thread(() -> {
                sets.add(UUID.randomUUID().toString().substring(0, 6));
                System.out.println(sets);
            }
            ).start();
        }
    }
```

​	3,ConcurrentHashMap

​	

```java
    public static void main(String[] args) {
//        Map<String,Object> parms=new HashMap<>(16,0.75f);
//        Map<String,Object> parms= Collections.synchronizedMap(new HashMap<>(16,0.75f));
        Map<String, Object> parms = new ConcurrentHashMap<>();
        for (int i = 0; i < 30; i++) {
            new Thread(() -> {
                parms.put(UUID.randomUUID().toString().substring(0, 3), UUID.randomUUID().toString().substring(0, 3));
                System.out.println(parms);
            }).start();

        }
    }
```



**三, Callable**

​	

```java
public class CallableTest {
    public static void main(String[] args) throws ExecutionException, InterruptedException {

        FutureTask<Integer> futureTask=new FutureTask<>(new Data1());
        new Thread(futureTask).start();
        new Thread(futureTask).start();//结果会被缓存，效率高
        Integer integer = futureTask.get();//get()方法可能会出现阻塞，放在最后执行或者执行异步通信
        System.out.println(integer);
    }
}

class Data1 implements Callable<Integer>{

    @Override
    public Integer call()  {
        System.out.println("3214");
        return 123;
    }
}
```



**四，常用辅助类**

​	1,CountDownLatch

​	2,CyclicBarrier

​	3,Semaphore



​	减法计数器CountDownLatch

```java
public static void main(String[] args) throws InterruptedException {
    CountDownLatch countDownLatch=new CountDownLatch(6);
    for (int i = 1; i <= 6; i++) {
        new Thread(()->{
            System.out.println("go out"+Thread.currentThread().getName());
            countDownLatch.countDown();//数量减-1
        }).start();
    }
    countDownLatch.await();//等待计数器归零在向下执行，计数器归0，countDownLatch.await()会被唤醒。
    System.out.println("close open");
}
```

​     加法计数器 CyclicBarrier

```java
public static void main(String[] args) {
  //线程累加到parties时候执行
    CyclicBarrier cyclicBarrier=new CyclicBarrier(7,()->{
        System.out.println("cyclicBarrier");
    });
    for (int i = 1; i <= 7; i++) {
        final int temp=i;
        new Thread(()->{
            System.out.println(Thread.currentThread().getName()+"--"+temp);
            try {
                cyclicBarrier.await();
            } catch (InterruptedException e) {
                e.printStackTrace();
            } catch (BrokenBarrierException e) {
                e.printStackTrace();
            }
        }).start();
    }
}
```

​	Semaphore 线程限流，阈值

```java
public static void main(String[] args) {
    //允许执行线程数量，限流作用,阈值
    Semaphore semaphore=new Semaphore(3);
    for (int i = 0; i < 9; i++) {
        new Thread(()->{
            try {
                //得到
                semaphore.acquire();
                System.out.println(Thread.currentThread().getName()+"抢到车位");
                TimeUnit.SECONDS.sleep(2);
                System.out.println(Thread.currentThread().getName()+"离开车位");
            } catch (InterruptedException e) {
                e.printStackTrace();
            }finally {
                //释放资源
                semaphore.release();
            }
        },"线程->"+i).start();
    }
}
```

**五，读写锁**

​	ReentrantReadWriteLock

​	独占锁（写锁）一次只能有一个线程操作

​	共享锁（读锁）多个线程可以同时操作

​	

```java
public class ReadWriteLock {
    public static void main(String[] args) {
        Data1 data1=new Data1();
        for (int i = 1; i < 20; i++) {
            final int temp=i;
            new Thread(()->{
                data1.setMap(""+temp,"value->"+temp);
            },Thread.currentThread().getName()).start();
        }
        for (int i = 1; i < 20; i++) {
            final int temp=i;
            new Thread(()->{
                data1.getMap(""+temp);
            },Thread.currentThread().getName()).start();
        }
    }
}

class Data1 {
    private volatile Map<String, Object> map = new HashMap<>();
    //读写锁，写入操作要加锁
    java.util.concurrent.locks.ReadWriteLock readWriteLock = new ReentrantReadWriteLock();

    public void setMap(String key,Object value){

        try {
            readWriteLock.writeLock().lock();
            System.out.println(Thread.currentThread().getName()+"--写入操作开始"+key);
            map.put(key,value);
            System.out.println("写入操作结束");
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            readWriteLock.writeLock().unlock();
        }
    }

    public void getMap(String key){
        //读取操作可以多个线程同时操作
        try {
            readWriteLock.readLock().lock();
            System.out.println(Thread.currentThread().getName()+"--读操作开始"+key);
            map.get(key);
            System.out.println("读操作结束ok");
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            readWriteLock.readLock().unlock();
        }

    }

}
```

六，队列

​	1，概述

​			Deque 双边队列，BlockingQueue阻塞队列，AbstractQueue非阻塞队列

<img src="D:\文档\学习\JUC\queue.png" style="zoom:60%;" />

 	2，添加，移除

| 方式         | 抛出异常 | 有返回值,不抛出异常 | 阻塞 等待 | 超时等待                |
| ------------ | -------- | ------------------- | --------- | ----------------------- |
| 添加         | add      | offer               | put       | offer(el,时长,时间级别) |
| 移除         | remove   | poll                | take      | poll（时长,时间级别）   |
| 判断队列首位 | element  | peek                | -         | -                       |

```java
    static void test1(){
        BlockingQueue<Object> arrayBlockingQueue = new ArrayBlockingQueue<>(3);
        arrayBlockingQueue.add("a");
        arrayBlockingQueue.add("b");
        arrayBlockingQueue.add("c");
        System.out.println("-----------------");
        System.out.println(arrayBlockingQueue.remove());
        System.out.println(arrayBlockingQueue.remove());
        System.out.println(arrayBlockingQueue.remove());
//        arrayBlockingQueue.remove();
    }
```

```java
private static void test2() {
    BlockingQueue abq=new ArrayBlockingQueue<String>(3);
    abq.offer("ack");
    abq.offer("ack2");
    abq.offer("ack");
    System.out.println("------------");
    System.out.println(abq.poll());
    System.out.println(abq.poll());
    System.out.println(abq.poll());
    System.out.println(abq.poll());
    System.out.println(abq.peek());
}
```