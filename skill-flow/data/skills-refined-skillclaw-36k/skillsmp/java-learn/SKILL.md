---
name: java-learn
description: Java 架构师学习资料（含可运行 Demo）
---

# 学习总索引（以 skills/*.md 为准）

> 说明：仓库内容分两层：
> 1）`skills/*.md`：模块级“总纲 + 方法论 + 面试/踩坑”
> 2）各模块目录（如 `java-thread/`、`jvm/` 等）：按文件拆分的深入文章
> 3）`src/main/java`：与知识点对应的可运行 Demo

## Java 基础（java-basics）
- 入口：`skills/java-basics.md`
- Demo：`src/main/java/com/example/basics/`

## 设计模式（design-patterns）
- 总纲：`skills/desgin-learn.md`
- 文章：`design-patterns/01-Singleton.md` ~ `design-patterns/06-Delegate.md`
- Demo：`src/main/java/com/example/designpatterns/`

## Spring（spring-learn）
- 总纲：`skills/spring-learn.md`
- 文章：`spring-learn/01-SpringBean.md` ~ `spring-learn/10-SpringInterview.md`
- Demo：`src/main/java/com/example/spring/`

## Java 并发（java-thread）
- 总纲（现状为设计模式提纲，后续可再拆分完善）：`skills/java-thread.md`
- 文章：`java-thread/01-ThreadBasics.md` ~ `java-thread/06-ThreadPool.md`
- Demo：`src/main/java/com/example/thread/`

## JVM（jvm）
- 总纲：`skills/JVM.md`
- 文章：`jvm/01-ClassLifecycle.md` ~ `jvm/07-JVM_Tuning.md`
- Demo：`src/main/java/com/example/jvm/`

## MySQL（mysql）
- 总纲：`skills/Mysql.md`
- 文章：`mysql/01-ExecutionFlow.md` ~ `mysql/04-Transaction_Lock.md`

## Redis（redis）
- 总纲：`skills/Redis.md`

## MQ（mq）
- 总纲：`skills/MQ.md`

## Netty（netty）
- 入口：`skills/netty.md`
- 文章：`spring-learn/09-Netty.md`

# 推荐学习路径
1. Java 基础 → 设计模式
2. 并发（线程/锁/线程池）→ JVM（内存/GC/排错）
3. Spring（IOC/AOP/事务）
4. MySQL/Redis/MQ（结合业务场景）

# 运行 Demo（JDK8 兼容）
- 编译命令示例：`javac -encoding UTF-8 src/main/java/.../Demo.java`
- 建议用 IDEA 直接运行各 `main` 方法

# desgin-learn

[常用设计模式]

## 单例模式
- 所有单例模式
- 单例模式对应的应用

## 工厂模式
- 简单工厂，工厂方法，抽象工厂
- 工厂模式常用案例以及代码
## 策略模式
- 常用策略模式
- 策略模式常用案例以及代码
## 模版模式
- 常用模版模式
- 模版模式常用案例以及代码
## 单例模式
- 静态代理
- 动态代理
- jdk代理 CGLB代理 案例以及底层原理
## 委派模式
- 常用委派模式
- 委派模式常用案例以及代码
## 策略模式
- 策略模式常用案例
- 策略模式案例代码
# spring-learn
[Spring学习资料]
## Spring Bean
- Spring Bean生命周期，扩展点
- Spring Bean源码分析 

## Spring注解
- Spring常用注解，以及使用方法
- 针对架构师使用注解
- Spring注解扩展点 
## Spring Aop
- Aop核心功能
- Aop流程
- Aop源码分析

## Spring Mvc
- Mvc核心功能
- Mvc流程
- Mvc源码分析
## Spring IOC DI
- 核心功能
- 流程
- 源码分析
## Spring 三级缓存与循环依赖
- 主要流程
- 源码分析

## Spring 事物
- Spring事物传播机制
- Spring事物失效机制
- Spring事物源码分析

## Spring 常用面试点
- 常用面试题以及答案

## netty
- 网络分成
- TCP/UDP
- Netty常用案例
- Netty源码分析
## SpringBoot
- 启动流程
- 自动装配
- SPI机制Java Dubbo SpringBoot
# java-thread
[Java线程池学习]
## 线程基础
- 生命周期
- 多线程创建方式
- 线程的启动和停止
- 线程的通信
- 线程安全问题
- synchronized 使用方式
- synchronized 锁状态及锁升级
- volatile 的作用
- volatile 底层原理
- happens-before 模型
## ThreadLocal
- ThreadLocal 它是什么
- ThreadLocal 是干什么的
- ThreadLocal 底层数据结构
- ThreadLocal 如何解决 hash 冲突
- ThreadLocal 扩容因子是 2/3，hashmap 的扩容因子是 0.75
- java 中有哪几种引用
- ThreadLocalMap 中的 key 是什么引用，为什么要用这种引用类型
- 怎么解决内存泄漏呢？
## ReentrantLock
- ReentrantLock（重入锁）
- ReentrantReadWriteLock（重入读写锁）
- 源码解读
## CHM 底层详解
- 数据结构
- 源码分析
## 线程池
- 线程的问题
- 线程池的概念及作用
- 核心思想
- 源码分析
# JVM
[JVM学习资料]
##  class类的生命周期
- 加载
- 验证
- 准备
- 解析
- 初始化
- 使用
- 卸载
## JVM 的内存结构
- 程序计数器
- 本地方法栈
- 虚拟机栈
- 堆
- 方法区：永久代
- 堆内存溢出
- 虚拟机栈内存溢出
- 字节码指令
## GC 垃圾回收
- 如何确定一个对象是垃圾(引用计数法,可达性分析)
- 常用垃圾收集算法 标记-清除(Mark-Sweep) 标记-整理(Mark-Compact)
- 分代收集算法
## 垃圾收集算法
- 标记清除算法
- 复制算法
- 标记整理算法
- 分代收集算法
## 垃圾收集器 
- Serial 收集器
- ParNew 收集器 
- Parallel Scavenge 收集器 
- Serial Old 收集器
- Parallel Old 收集器
- CMS 收集器
- G1 收集器
## JVM参数
- 标准参数
- -X参数
- -XX参数
- 其他参数
- 如何查看参数
- 设置参数的方式
- 常用的参数
## 常用命令
- JPS
- jinfo
- jstat
- jstack
- jmap
## 常用工具
- jconsole 使用教程
- jvisualvm 使用教程
## JVM调优步骤
- 一般步骤
- 生产实例
# Mysql
[Mysql学习资料]
## 框架执行流程
- 一条SQL语句是如何执行的
- Buffer pool
- 修改内存已有数据逻辑
- Double Write机制
- RedoLog
- BinLog
- undoLog
## Mysql索引剖析
- Page页
- 主键索引
- 二级索引
- 联合索引
- 一条sql是怎么走索引的
## mysql语句分析以及优化
- 怎么去判断 explain各个字段的含义
- select_type
- table
- partitions
- type
- possible_keys
- key
- ref
- rows
- Extra
## Mysql的事务与锁机制分析
- 事务简单的操作
- 事务的特性
- 事务并发产生的问题
- 怎么实现事务的隔离级别的
- MVCC（Multi-Version Concurrent Control ）多版本并发控制
- LBCC（Lock-Based Concurrent Control） 锁并发控制

# MQ
[MQ学习资料]
## Kafka
- 使用手册
- 部署方案
- 集群部署
- 源码分析
- 常见问题
## RocketMQ
- 使用手册
- 部署方案
- 集群部署
- 源码分析
- 常见问题
## Pulsar
- 使用手册
- 部署方案
- 集群部署
- 源码分析
- 常见问题
# Redis
[Redis学习资料]
## Redis 基础
- 使用手册
- 数据结构，底层原理，常见应用
- Redis为什么这么快
## Redis应用
- 持久化
- 缓存一致性
- 内存淘汰策略
- 分布式锁
##  集群部署
- 哨兵
- 主从复杂
- Redis Cluster

