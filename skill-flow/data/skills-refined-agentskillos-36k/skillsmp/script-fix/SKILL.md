---
name: script_fix
description: 修复生成的conftest.py和pytest脚本
---

# 脚本修复智能体

## 目标

修复conftest.py和pytest脚本中错误


## 工作流程

### 步骤 1：语法检查修复
目标：确保工作区内conftest.py和pytest脚本（例如test_case_0.py）文件内容符合python语法

1. **检查文件**：conftest.py和pytest脚本（例如test_case_0.py）内容。
2. **语法检查**：逐行分析文件内容，内容要符合python语法规范
3. **脚本修复**：对于不符合python语法规范的地方进行修复
    - **例如**：
    case1: 脚本中字符串使用"""xxxx""需要修复为"""xxxx"""
    case2: 脚本中引用了from .conftest import testFun 但是testFun在conftest中不存在，需要去掉相关引用和调用testFun的相关代码
    case3: 脚本中CheckCommand调用是cmd不能为空
    ```python
   gl.DUT.CheckCommand('检查端口信息，预期链路状态UP，IP地址正确', 
         cmd=f'display interface Ethernet0/1',    -----   不能为cmd=""
         expect=['Line protocol current state: UP', 'Internet Address is 11.91.255.79/24'],
         is_strict=True, 
                  relationship='and',
         stop_max_attempt=3, wait_fixed=2)
   ```

### 步骤2：脚本规范检查
1. 不要使用topox中不存在的设备名或者或者端口, 注意是大小问题和是否存在问题。
   例如一下拓扑的设备名是dut1,端口名是port1。
   ```xml
      <LINK_LIST>
      <LINK>
         <NODE>
         <DEVICE>dut1</DEVICE>
         <PORT>
            <NAME>port1</NAME>
            <TYPE/>
            <IPAddr/>
            <IPv6Addr/>
            <SLOT_TYPE/>
            <TAG/>
         </PORT>
         </NODE>
         <NODE>
         <DEVICE>PC</DEVICE>
         <PORT>
            <NAME>port1</NAME>
            <TYPE/>
            <IPAddr/>
            <IPv6Addr/>
            <SLOT_TYPE/>
            <TAG/>
         </PORT>
         </NODE>
      </LINK>
   </LINK_LIST>
  ```
  。
2. 不要使用atf_check和atf_assert，这种方式是违法的，对于H3C设备相关的检查只可以使用CheckCommand， 例如：
   ```python
   gl.DUT.CheckCommand('检查端口信息，预期链路状态UP，IP地址正确', 
         cmd=f'display interface Ethernet0/1',
         expect=['Line protocol current state: UP', 'Internet Address is 11.91.255.79/24'],
         is_strict=True, 
                  relationship='and',
         stop_max_attempt=3, wait_fixed=2)
   ```
