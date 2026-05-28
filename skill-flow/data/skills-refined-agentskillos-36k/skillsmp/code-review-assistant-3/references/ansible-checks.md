# Ansible 代码审核检查规则

## 审核排除规则

### [ANS-EX001] Roles / Collections 第三方目录

- **描述**: `galaxy_roles/`、`collections/`、`vendor/` 等第三方依赖目录不进行代码审核
- **处理方式**:
  - 不审核通过 Ansible Galaxy 安装的角色
  - 不审核第三方集合
  - 不对依赖目录的变更生成任何审核意见
- **示例**:

```
以下文件路径应被跳过审核:
- galaxy_roles/...
- collections/community/...
- vendor/...
```

### [ANS-EX002] 主机清单文件 (Inventory)

- **描述**: 主机清单文件（`inventory/`、`hosts` 等）包含敏感信息，不进行内容审核
- **处理方式**:
  - 不审核 host.ini、hosts 等清单文件内容
  - 不审核 group_vars/all 中的敏感变量（如密码、密钥）
  - 仅提示文件结构问题，不审核具体主机配置
- **示例**:

```
以下文件路径应被跳过内容审核:
- inventory/*.ini
- inventory/hosts
- group_vars/all/vault.yml
```

---

## 检查规则按严重程度分类

---

## 🔴 Must Fix (-2)

### [ANS-MF001] 明文存储敏感信息

- **描述**: 在 Playbook 或变量文件中明文存储密码、API 密钥等敏感信息
- **影响**: 严重安全风险，敏感信息泄露
- **检测方式**:
  - 搜索变量名包含 `password`、`secret`、`key`、`token` 等关键字
  - 检查值是否为明文字符串
  - 检查是否使用 ansible-vault 加密
- **示例**:

```yaml
# Bad - 明文密码
vars:
  mysql_password: "mysecretpassword123"
  api_key: "sk-1234567890abcdef"
  ssh_private_key: |
    -----BEGIN RSA PRIVATE KEY-----
    ... (明文私钥)
    -----END RSA PRIVATE KEY-----

# Good - 使用 ansible-vault
vars:
  mysql_password: !vault |
    $ANSIBLE_VAULT;1.1;AES256
    663864396539666364636466353361646438383665...
  api_key: !vault |
    $ANSIBLE_VAULT;1.1;AES256
    366163343864326639376263646362663866373139...

# Good - 从外部环境或文件读取
vars:
  mysql_password: "{{ lookup('env', 'MYSQL_PASSWORD') }}"
  api_key: "{{ lookup('file', '/secure/path/api_key') }}"
```

- **建议修改**: 使用 `ansible-vault` 加密敏感变量，或通过环境变量、密钥管理工具动态获取

---

### [ANS-MF002] Shell 模块未使用幂等性检查

- **描述**: 使用 `shell` 或 `command` 模块但未添加 `creates`、`removes` 或条件判断
- **影响**: 每次执行都会运行，可能导致不可预期的副作用
- **检测方式**:
  - 检测 `shell`/`command` 模块没有 `creates`、`removes` 参数
  - 检测模块前缺少 `when` 条件
- **示例**:

```yaml
# Bad - 无条件执行
- name: Install dependencies
  shell: pip install -r requirements.txt

# Good - 使用 creates 参数
- name: Install dependencies
  shell: pip install -r requirements.txt
  args:
    chdir: /opt/app
  creates: /opt/app/venv/bin/python

# Good - 使用 when 条件
- name: Install dependencies
  shell: pip install -r requirements.txt
  when: not venv_exists.stat.exists

# Better - 使用专用模块（幂等）
- name: Install dependencies
  pip:
    requirements: requirements.txt
    virtualenv: /opt/app/venv
```

- **建议修改**: 使用 Ansible 专用模块（如 `yum`、`apt`、`pip`）代替 `shell`，或添加 `creates`/`removes`/`when` 条件

---

### [ANS-MF003] 使用 sudo/su 而非 become

- **描述**: 直接使用 `sudo` 或 `su` 命令而非 Ansible 的 `become` 机制
- **影响**: 违反 Ansible 最佳实践，权限管理混乱
- **检测方式**:
  - 检测 `shell`/`command` 模块命令中包含 `sudo`、`su`
  - 检测未使用 `become` 参数
- **示例**:

```yaml
# Bad - 直接使用 sudo
- name: Install package
  shell: sudo apt-get install -y nginx

# Bad - 使用 su
- name: Run as root
  shell: su - root -c "some command"

# Good - 使用 become
- name: Install package
  apt:
    name: nginx
    state: present
  become: true

# Good - 指定 become_user
- name: Run as specific user
  shell: some command
  become: true
  become_user: appuser
```

- **建议修改**: 使用 `become: true` 和 `become_user` 进行权限提升

---

### [ANS-MF004] 未处理任务失败

- **描述**: 关键任务没有错误处理，失败后继续执行
- **影响**: 可能导致系统处于不一致状态
- **检测方式**:
  - 检测重要操作（如配置文件修改、服务重启）缺少错误处理
  - 检测未使用 `register` + `failed_when` 或 `ignore_errors`（仅用于非关键任务）
- **示例**:

```yaml
# Bad - 无错误检查
- name: Update configuration
  copy:
    src: nginx.conf
    dest: /etc/nginx/nginx.conf

- name: Restart service
  service:
    name: nginx
    state: restarted

# Good - 检查任务结果
- name: Update configuration
  copy:
    src: nginx.conf
    dest: /etc/nginx/nginx.conf
    validate: nginx -t
  notify: reload nginx
  register: config_result

- name: Restart service
  service:
    name: nginx
    state: restarted
  when: config_result is changed

# Good - 使用 block 处理错误
- name: Deploy application
  block:
    - name: Update application
      git:
        repo: https://github.com/example/app.git
        dest: /opt/app
      notify: restart app
  rescue:
    - name: Rollback deployment
      git:
        repo: https://github.com/example/app.git
        dest: /opt/app
        version: "v1.0.0"
```

- **建议修改**: 使用 `register` + `when`、`failed_when` 或 `block/rescue` 进行错误处理

---

### [ANS-MF005] 循环性能问题 - 未使用循环优化

- **描述**: 在循环中使用大量模块调用，性能低下
- **影响**: Playbook 执行时间过长
- **检测方式**:
  - 检测 `with_items` 对大量列表的操作
  - 检测循环中的单个模块调用
- **示例**:

```yaml
# Bad - 逐个创建文件（性能差）
- name: Create multiple files
  file:
    path: "{{ item }}"
    state: touch
  with_items:
    - /tmp/file1.txt
    - /tmp/file2.txt
    - /tmp/file3.txt
    # ... 更多文件

# Good - 使用批量操作
- name: Create multiple files
  file:
    path: "{{ item }}"
    state: touch
  loop:
    - /tmp/file1.txt
    - /tmp/file2.txt
    - /tmp/file3.txt
  loop_control:
    parallel: 0  # 如果模块支持，可以并行

# Better - 使用 copy 模块批量
- name: Create multiple files
  copy:
    dest: "/tmp/{{ item }}"
    content: ""
  loop:
    - file1.txt
    - file2.txt
    - file3.txt
```

- **建议修改**: 考虑使用循环控制参数、批量操作或专用模块

---

### [ANS-MF006] 未检查目标系统支持

- **描述**: 任务未指定目标系统或操作系统，可能在所有主机上执行
- **影响**: 在不支持的系统上执行导致错误
- **检测方式**:
  - 检测缺少 `when: ansible_os_family == ...` 条件
  - 检测系统特定命令未添加平台检查
- **示例**:

```yaml
# Bad - 可能在所有系统执行
- name: Install package
  apt:
    name: nginx
    state: present

- name: Install package
  yum:
    name: nginx
    state: present

# Good - 使用条件判断
- name: Install package (Debian/Ubuntu)
  apt:
    name: nginx
    state: present
  when: ansible_os_family == 'Debian'

- name: Install package (RHEL/CentOS)
  yum:
    name: nginx
    state: present
  when: ansible_os_family == 'RedHat'

# Good - 使用变量映射
- name: Install package
  package:
    name: nginx
    state: present
    use: "{{ ansible_pkg_mgr }}"
```

- **建议修改**: 使用 `ansible_os_family`、`ansible_distribution` 等事实变量进行条件判断

---

### [ANS-MF007] 配置文件修改未备份

- **描述**: 修改关键配置文件时未创建备份
- **影响**: 发生错误时无法快速回滚
- **检测方式**:
  - 检测 `copy`、`template`、`lineinfile` 等模块修改配置文件缺少 `backup: true`
- **示例**:

```yaml
# Bad - 无备份
- name: Update SSH configuration
  lineinfile:
    path: /etc/ssh/sshd_config
    regexp: '^PermitRootLogin'
    line: 'PermitRootLogin no'
  notify: restart sshd

# Good - 启用备份
- name: Update SSH configuration
  lineinfile:
    path: /etc/ssh/sshd_config
    regexp: '^PermitRootLogin'
    line: 'PermitRootLogin no'
    backup: true
  notify: restart sshd
```

- **建议修改**: 修改配置文件时添加 `backup: true` 参数

---

## 🟡 Should Fix (-2)

### [ANS-SF001] 使用弃用的语法或模块

- **描述**: 使用已弃用的 Ansible 模块或语法
- **影响**: 未来版本可能不兼容，升级困难
- **检测方式**:
  - 检测 `with_items`（应使用 `loop`）
  - 检测 `include:`（应使用 `include_tasks:` 或 `import_tasks:`）
  - 检测已弃用的模块
- **示例**:

```yaml
# Bad - 旧语法
- name: Process items
  debug:
    msg: "{{ item }}"
  with_items:
    - item1
    - item2

- include: tasks/main.yml

# Good - 新语法
- name: Process items
  debug:
    msg: "{{ item }}"
  loop:
    - item1
    - item2

- include_tasks: tasks/main.yml  # 动态包含
# 或
- import_tasks: tasks/main.yml  # 静态导入（预解析）
```

- **建议修改**: 使用最新 Ansible 语法和模块

---

### [ANS-SF002] 缺少元数据

- **描述**: Role 缺少 `meta/main.yml` 或 Playbook 缺少描述信息
- **影响**: 难以维护和重用，依赖管理混乱
- **检测方式**:
  - 检查 Role 是否有 `meta/main.yml`
  - 检查 Playbook 是否有 `name` 和描述
- **示例**:

```yaml
# Bad - 缺少元数据
# roles/myrole/tasks/main.yml
- name: Do something
  ...

# Good - 有完整的元数据
# roles/myrole/meta/main.yml
---
dependencies:
  - role: common
galaxy_info:
  role_name: myrole
  author: Your Name
  description: A role description
  company: Your Company
  license: MIT
  min_ansible_version: 2.9
  platforms:
    - name: Ubuntu
      versions:
        - focal
        - jammy
  galaxy_tags: []
```

- **建议修改**: 为 Role 添加完整元数据，Playbook 添加描述性信息

---

### [ANS-SF003] 魔法变量值

- **描述**: 代码中出现未定义的硬编码路径、端口号等
- **影响**: 降低可移植性，难以维护
- **检测方式**: 检测路径、端口号等硬编码值
- **示例**:

```yaml
# Bad - 硬编码
- name: Deploy app
  copy:
    src: app.jar
    dest: /opt/myapp/app.jar

- name: Start service
  systemd:
    name: myapp
    state: started
    enabled: yes
    port: 8080  # 错误参数，但示例展示硬编码问题

# Good - 使用变量
- name: Deploy app
  copy:
    src: app.jar
    dest: "{{ app_install_dir }}/app.jar"

# defaults/main.yml
app_install_dir: /opt/myapp
app_port: 8080
```

- **建议修改**: 在 `defaults/main.yml` 或变量文件中定义配置值

---

### [ANS-SF004] 未使用标签 (Tags)

- **描述**: Playbook 或复杂 Role 未使用 tags 组织任务
- **影响**: 难以选择性执行任务，调试和部署不灵活
- **检测方式**: 检查大型 Playbook 缺少 tags 定义
- **示例**:

```yaml
# Bad - 无 tags
- name: Install dependencies
  apt:
    name: "{{ item }}"
  loop:
    - nginx
    - redis

- name: Configure application
  template:
    src: app.conf.j2
    dest: /etc/app/app.conf

# Good - 使用 tags
- name: Install dependencies
  apt:
    name: "{{ item }}"
    state: present
  loop:
    - nginx
    - redis
  tags:
    - dependencies
    - install

- name: Configure application
  template:
    src: app.conf.j2
    dest: /etc/app/app.conf
  tags:
    - config

# 使用方式
# ansible-playbook site.yml --tags "config"  # 只执行配置任务
# ansible-playbook site.yml --skip-tags "install"  # 跳过安装任务
```

- **建议修改**: 为不同类型的任务添加合理的 tags

---

### [ANS-SF005] 循环或条件变量命名混淆

- **描述**: 在嵌套结构中使用相同的变量名（如 `item`）导致命名冲突
- **影响**: 代码难以理解，可能产生意外行为
- **检测方式**: 检测嵌套循环或 include_tasks 中重复使用 `item`
- **示例**:

```yaml
# Bad - item 冲突
- name: Process users
  include_tasks: process_user.yml
  loop: "{{ users }}"
  vars:
    user_id: "{{ item.id }}"  # 可能与内部 item 冲突

- name: Process users
  include_tasks: process_user.yml
  loop: "{{ users }}"
  loop_control:
    loop_var: user_item  # 重命名

# Good
- name: Process users
  include_tasks: process_user.yml
  loop: "{{ users }}"
  loop_control:
    loop_var: user_item
  vars:
    user_id: "{{ user_item.id }}"
```

- **建议修改**: 使用 `loop_var` 控制循环变量名，避免命名冲突

---

### [ANS-SF006] 未声明依赖关系

- **描述**: Role 或 Task 依赖其他模块但未在 `meta/main.yml` 中声明
- **影响**: 执行顺序不确定，可能导致依赖问题
- **检测方式**: 检查 Role 使用的其他角色但未在 dependencies 中列出
- **示例**:

```yaml
# Bad - 隐式依赖
# role_A/tasks/main.yml
- include_role:
    name: role_B

# Good - 显式声明依赖
# role_A/meta/main.yml
---
dependencies:
  - role: role_B
```

- **建议修改**: 在 `meta/main.yml` 中明确声明 Role 依赖关系

---

### [ANS-SF007] 未使用 Jinja2 过滤器

- **描述**: 使用冗长的 shell 命令处理字符串而非 Jinja2 过滤器
- **影响**: 降低可读性，增加复杂性
- **检测方式**: 检测 shell 模块中的字符串处理可被 Jinja2 替代
- **示例**:

```yaml
# Bad - 使用 shell 处理
- name: Get uppercase username
  shell: echo "{{ username }}" | tr '[:lower:]' '[:upper:]'
  register: upper_username

- name: Set config
  set_fact:
    config_user: "{{ upper_username.stdout }}"

# Good - 使用过滤器
- name: Set config
  set_fact:
    config_user: "{{ username | upper }}"
    config_user_lower: "{{ username | lower }}"
    config_user_title: "{{ username | title }}"
```

- **建议修改**: 使用 Jinja2 内置过滤器处理字符串操作

---

### [ANS-SF008] 注释不够或缺失

- **描述**: 复杂的 Playbook 或缺少解释性注释
- **影响**: 降低可维护性，他人难以理解
- **检测方式**: 检测复杂逻辑缺少注释
- **示例**:

```yaml
# Bad - 无注释
- name: Install and configure
  block:
    - apt: name=nginx state=present
    - debug: msg="{{ groups['webservers'] | length }}"
    - template: src=nginx.conf.j2 dest=/etc/nginx/nginx.conf

# Good - 有注释
- name: Install and configure nginx
  block:
    - name: Install nginx package
      apt:
        name: nginx
        state: present

    - name: Display number of web servers
      debug:
        msg: "Deploying to {{ groups['webservers'] | length }} servers"

    - name: Generate nginx configuration
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
      # Configuration includes upstream backend setting
      notify: reload nginx
```

- **建议修改**: 为重要的任务、block 和复杂逻辑添加注释

---

### [ANS-SF009] 未使用 Handler 实现幂等性

- **描述**: 修改配置后使用 command 模块重启服务而非 Handler
- **影响**: 每次运行都会重启服务，影响可用性
- **检测方式**: 检测配置修改后直接调用 service 模块重启
- **示例**:

```yaml
# Bad - 每次都重启
- name: Update configuration
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf

- name: Restart nginx
  service:
    name: nginx
    state: restarted

# Good - 使用 Handler（仅在配置变化时重启）
- name: Update configuration
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
  notify: reload nginx

# handlers/main.yml
- name: reload nginx
  service:
    name: nginx
    state: reloaded
```

- **建议修改**: 使用 Handler 实现条件性的服务操作

---

## 🔵 Nice to Have (-1)

### [ANS-NH001] 未使用的变量

- **描述**: 定义了变量但未在任何任务中使用
- **影响**: 代码冗余，可能表示逻辑错误
- **检测方式**: 静态分析检测未引用的变量
- **示例**:

```yaml
# Bad - 未使用的变量
vars:
  unused_var: "value"
  another_unused: 123

- name: Use active variable
  debug:
    msg: "{{ active_var }}"

# Good - 删除未使用变量
vars:
  active_var: "value"
```

- **建议修改**: 删除或注释未使用的变量

---

### [ANS-NH002] 可以使用内置模块代替 shell

- **描述**: 使用 shell 模块但有等价的 Ansible 内置模块
- **影响**: 降低可读性和可维护性，可能减少幂等性
- **检测方式**: 检测常见的 shell 操作有对应模块
- **示例**:

```yaml
# Bad - 使用 shell 创建目录
- name: Create directory
  shell: mkdir -p /opt/app/logs

# Good - 使用 file 模块
- name: Create directory
  file:
    path: /opt/app/logs
    state: directory
    mode: '0755'

# Bad - 使用 shell 启动服务
- name: Start service
  shell: systemctl start nginx

# Good - 使用 service/systemd 模块
- name: Start service
  systemd:
    name: nginx
    state: started
    enabled: yes
```

- **建议修改**: 优先使用 Ansible 内置模块

---

### [ANS-NH003] 重复的代码可以提取

- **描述**: 多个 Playbook 或 Task 有相同的代码片段
- **影响**: 维护困难，修改需要多处更新
- **检测方式**: 检测重复的任务序列
- **示例**:

```yaml
# Bad - 重复代码
- name: Setup app server A
  block:
    - name: Install nginx
      apt: name=nginx state=present
    - name: Install redis
      apt: name=redis-server state=present

- name: Setup app server B
  block:
    - name: Install nginx
      apt: name=nginx state=present
    - name: Install redis
      apt: name=redis-server state=present

# Good - 提取为 Role
# roles/common/tasks/main.yml
- name: Install nginx
  apt:
    name: nginx
    state: present

- name: Install redis
  apt:
    name: redis-server
    state: present

- name: Setup app server A
  include_role:
    name: common

- name: Setup app server B
  include_role:
    name: common
```

- **建议修改**: 将重复代码提取为 Role 或 Task 文件

---

### [ANS-NH004] 可以合并相似任务

- **描述**: 多个相同模块的任务可以合并
- **影响**: 简化代码，提高可读性
- **检测方式**: 检测连续的相同模块调用
- **示例**:

```yaml
# Bad - 分离的任务
- name: Create user1
  user:
    name: user1
    state: present

- name: Create user2
  user:
    name: user2
    state: present

- name: Create user3
  user:
    name: user3
    state: present

# Good - 使用循环
- name: Create users
  user:
    name: "{{ item }}"
    state: present
  loop:
    - user1
    - user2
    - user3

# Better - 使用字典（如果需要更多属性）
- name: Create users with home
  user:
    name: "{{ item.name }}"
    home: "{{ item.home }}"
    state: present
  loop:
    - { name: user1, home: /home/user1 }
    - { name: user2, home: /home/user2 }
```

- **建议修改**: 使用循环合并相似任务

---

### [ANS-NH005] YAML 过于冗长

- **描述**: 可以简化但过度展开的 YAML
- **影响**: 降低可读性
- **检测方式**: 检测可以写成单行的简单键值对
- **示例**:

```yaml
# Bad - 过于详细
- name: Copy file
  copy:
    src: /local/path/file.txt
    dest: /remote/path/file.txt
    owner: root
    group: root
    mode: '0644'
    backup: false

# Good - 简洁（必要时可以详细）
- name: Copy file
  copy:
    src: /local/path/file.txt
    dest: /remote/path/file.txt
    owner: root
    group: root
    mode: '0644'
```

- **建议修改**: 在保持清晰的前提下，简化 YAML 结构

---

### [ANS-NH006] 未使用社区集合 (Collections)

- **描述**: 使用旧版模块风格，社区提供了更好的集合版本
- **影响**: 可能错过改进和新功能
- **检测方式**: 检测可以使用 community.general 等集合的操作
- **示例**:

```yaml
# 旧版模块仍在使用
- name: Wait for port
  wait_for:
    port: 8080
    host: localhost

# 如果使用 collections，可以这样引用
- name: Wait for port
  ansible.builtin.wait_for:
    port: 8080
    host: localhost

# 或者使用 community collections 的特定功能
- name: Manage Docker container
  community.docker.docker_container:
    name: myapp
    image: nginx:latest
```

- **建议修改**: 考虑使用社区集合获取更多功能

---

### [ANS-NH007] 可以使用内置 Facts 而非 shell 命令

- **描述**: 使用 shell 获取系统信息而 Ansible 已提供内置事实
- **影响**: 增加执行时间，降低可靠性
- **检测方式**: 检测常见的 info 命令有对应事实变量
- **示例**:

```yaml
# Bad - 使用 shell 获取信息
- name: Get hostname
  shell: hostname
  register: host_name

- name: Get IP address
  shell: ip route get 1 | awk '{print $NF}' | head -n 1
  register: ip_address

# Good - 使用内置事实
- name: Display hostname
  debug:
    msg: "Hostname is {{ ansible_hostname }}"

- name: Display IP address
  debug:
    msg: "Default IP is {{ ansible_default_ipv4.address }}"
```

- **建议修改**: 使用 `ansible_facts` 代替 shell 命令获取系统信息

---

### [ANS-NH008] 变量定义分散

- **描述**: 同一类变量分散在多个文件中
- **影响**: 难以维护和理解变量结构
- **检测方式**: 检测相关变量定义位置分散
- **示例**:

```yaml
# Bad - 变量分散
# group_vars/web/app.yml
app_port: 8080

# group_vars/web/database.yml
db_port: 5432

# roles/myapp/defaults/main.yml
app_version: "1.0.0"

# group_vars/web.yml - 更好的组织方式
---
# Application settings
app:
  port: 8080
  version: "1.0.0"
  install_dir: /opt/app

# Database settings
database:
  host: localhost
  port: 5432
  name: myapp
```

- **建议修改**: 使用嵌套字典结构组织相关变量

---

## 参考资源

- [Ansible Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html)
- [ansible-lint Rules](https://ansible-lint.readthedocs.io/latest/rules/)
- [Ansible Documentation](https://docs.ansible.com/)
- [YAML Syntax](https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html)
- [Jinja2 Filters](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html)
