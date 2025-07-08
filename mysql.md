## MySQL 新建数据库

### 1. 基本语法
```sql
CREATE DATABASE database_name;
```

### 2. 指定字符集
```sql
CREATE DATABASE database_name CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. 检查数据库是否已存在
```sql
CREATE DATABASE IF NOT EXISTS database_name;
```

### 4. 完整示例
```sql
-- 创建一个名为 myapp 的数据库，使用 utf8mb4 字符集
CREATE DATABASE IF NOT EXISTS myapp 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;
```

### 5. 查看所有数据库
```sql
SHOW DATABASES;
```

### 6. 使用数据库
```sql
USE database_name;
```

### 7. 删除数据库（谨慎使用）
```sql
DROP DATABASE database_name;
```

### 常见字符集选项
- `utf8mb4`：支持完整的 UTF-8 字符集，包括 emoji
- `utf8`：MySQL 的 utf8 实际上是 utf8mb3，不完整
- `latin1`：默认字符集，不推荐用于中文

### 注意事项
1. 数据库名称不能包含特殊字符
2. 推荐使用 `utf8mb4` 字符集
3. 创建前最好检查是否已存在
4. 删除数据库会永久删除所有数据，请谨慎操作

## 连接远程数据库

### 1. 基本连接语法
```bash
mysql -h hostname -P port -u username -p
```

### 2. 完整连接示例
```bash
# 连接远程 MySQL 服务器
mysql -h 192.168.1.100 -P 3306 -u myuser -p

# 直接指定数据库
mysql -h 192.168.1.100 -P 3306 -u myuser -p mydatabase
```

### 3. 连接参数说明
- `-h` 或 `--host`：指定主机名或 IP 地址
- `-P` 或 `--port`：指定端口号（默认 3306）
- `-u` 或 `--user`：指定用户名
- `-p` 或 `--password`：提示输入密码（推荐）
- `-D` 或 `--database`：指定默认数据库

### 4. 其他连接选项
```bash
# 指定密码（不推荐，安全风险）
mysql -h hostname -u username -ppassword

# 使用 SSL 连接
mysql -h hostname -u username -p --ssl-mode=REQUIRED

# 指定字符集
mysql -h hostname -u username -p --default-character-set=utf8mb4
```

### 5. 配置文件连接（推荐）
创建 `~/.my.cnf` 文件：
```ini
[client]
host=your-remote-host
port=3306
user=your-username
password=your-password
default-character-set=utf8mb4
```

然后直接连接：
```bash
mysql
```

### 6. 常见连接问题排查

#### 权限问题
```sql
-- 检查用户权限
SHOW GRANTS FOR 'username'@'%';

-- 创建远程用户
CREATE USER 'username'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON database_name.* TO 'username'@'%';
FLUSH PRIVILEGES;
```

#### 防火墙设置
```bash
# 检查端口是否开放
telnet hostname 3306

# 或使用 nc 命令
nc -zv hostname 3306
```

#### MySQL 配置
检查 MySQL 配置文件 `my.cnf`：
```ini
[mysqld]
bind-address = 0.0.0.0  # 允许远程连接
port = 3306
```

### 7. 安全最佳实践
1. **不要在命令行中直接输入密码**
2. **使用 SSL 连接加密数据传输**
3. **限制用户访问权限和 IP 范围**
4. **定期更换密码**
5. **使用防火墙限制访问端口**

### 8. 测试连接
```sql
-- 连接成功后测试
SELECT VERSION();
SELECT USER();
SELECT DATABASE();
SHOW DATABASES;
```

## Docker MySQL 容器配置

### 1. 基本 Docker 运行命令
```bash
docker run -d \
  --name xiaozhi-esp32-server-db \
  -e MYSQL_ROOT_PASSWORD=123456 \
  -p 3306:3306 \
  -e MYSQL_DATABASE=xiaozhi_esp32_server \
  -e MYSQL_INITDB_ARGS="--character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci" \
  -e TZ=Asia/Shanghai \
  mysql:8.0
```

### 2. 环境变量说明

#### 时区设置
- `-e TZ=Asia/Shanghai`：设置容器的时区为上海时区（东八区）
  - **作用**：确保 MySQL 容器内的时间与本地时间一致
  - **重要性**：避免时间戳记录错误，特别是在日志记录和数据分析时

#### MySQL 配置变量
- `-e MYSQL_ROOT_PASSWORD=123456`：设置 root 用户密码
- `-e MYSQL_DATABASE=xiaozhi_esp32_server`：自动创建指定名称的数据库
- `-e MYSQL_INITDB_ARGS`：MySQL 初始化参数
  - `--character-set-server=utf8mb4`：设置服务器默认字符集
  - `--collation-server=utf8mb4_unicode_ci`：设置服务器默认排序规则

#### 端口映射
- `-p 3306:3306`：将容器的 3306 端口映射到主机的 3306 端口

### 3. 常用时区设置
```bash
# 中国时区
-e TZ=Asia/Shanghai

# 美国东部时间
-e TZ=America/New_York

# 欧洲伦敦时间
-e TZ=Europe/London

# UTC 时间
-e TZ=UTC
```

### 4. 验证时区设置
连接到容器后执行：
```sql
-- 查看当前时区
SELECT @@global.time_zone, @@session.time_zone;

-- 查看当前时间
SELECT NOW();

-- 查看系统时间
SELECT SYSDATE();
```

### 5. 完整的 Docker Compose 配置
```yaml
version: '3.8'
services:
  mysql:
    image: mysql:8.0
    container_name: xiaozhi-esp32-server-db
    environment:
      MYSQL_ROOT_PASSWORD: 123456
      MYSQL_DATABASE: xiaozhi_esp32_server
      MYSQL_INITDB_ARGS: "--character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci"
      TZ: Asia/Shanghai
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    restart: unless-stopped

volumes:
  mysql_data:
```

### 6. 数据持久化建议
```bash
# 添加数据卷持久化
docker run -d \
  --name xiaozhi-esp32-server-db \
  -e MYSQL_ROOT_PASSWORD=123456 \
  -p 3306:3306 \
  -e MYSQL_DATABASE=xiaozhi_esp32_server \
  -e MYSQL_INITDB_ARGS="--character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci" \
  -e TZ=Asia/Shanghai \
  -v mysql_data:/var/lib/mysql \
  mysql:8.0
```

## 安全删除数据操作

### 1. 基本删除语法
```sql
-- 使用指定数据库
USE database_name;

-- 删除符合条件的记录
DELETE FROM table_name WHERE condition;
```

### 2. Gogs 数据库删除示例
```sql
-- 删除 gogs 数据库中 repository 表 owner_id > 100 的记录
USE gogs;
DELETE FROM repository WHERE owner_id > 100;
```

### 3. 安全删除最佳实践

#### 步骤 1：备份数据
```bash
# 备份整个数据库
mysqldump -u username -p gogs > gogs_backup.sql

# 备份特定表
mysqldump -u username -p gogs repository > repository_backup.sql
```

#### 步骤 2：使用事务安全删除
```sql
USE gogs;
START TRANSACTION;

-- 先查看要删除的记录数量
SELECT COUNT(*) FROM repository WHERE owner_id > 100;

-- 查看具体要删除的记录（可选）
SELECT id, name, owner_id FROM repository WHERE owner_id > 100 LIMIT 10;

-- 执行删除
DELETE FROM repository WHERE owner_id > 100;

-- 检查删除后的结果
SELECT COUNT(*) FROM repository;

-- 如果确认无误，提交事务
COMMIT;

-- 如果有问题，回滚事务
-- ROLLBACK;
```

#### 步骤 3：分批删除（大数据量时推荐）
```sql
-- 分批删除，避免长时间锁表
SET @batch_size = 1000;

REPEAT
  DELETE FROM repository WHERE owner_id > 100 LIMIT @batch_size;
UNTIL ROW_COUNT() = 0 END REPEAT;
```

### 4. 其他实用删除操作

#### 条件删除示例
```sql
-- 删除指定时间范围的记录
DELETE FROM repository 
WHERE owner_id > 100 
AND created_unix < UNIX_TIMESTAMP('2023-01-01');

-- 删除多个条件组合
DELETE FROM repository 
WHERE owner_id > 100 
AND is_private = 1 
AND is_fork = 1;
```

#### 关联删除
```sql
-- 删除没有对应用户的仓库记录
DELETE r FROM repository r
LEFT JOIN user u ON r.owner_id = u.id
WHERE u.id IS NULL;
```

### 5. 删除操作注意事项

#### 重要警告
- ⚠️ **DELETE 操作不可逆**，删除后无法恢复
- ⚠️ **务必先备份**重要数据
- ⚠️ **先在测试环境验证**删除逻辑
- ⚠️ **使用事务**确保可以回滚

#### 性能优化
```sql
-- 查看执行计划
EXPLAIN DELETE FROM repository WHERE owner_id > 100;

-- 确保相关字段有索引
SHOW INDEX FROM repository;

-- 如果没有索引，建议添加
CREATE INDEX idx_owner_id ON repository(owner_id);
```

#### 监控删除进度
```sql
-- 删除前记录总数
SELECT COUNT(*) as total_before FROM repository;

-- 删除过程中检查剩余数量
SELECT COUNT(*) as remaining FROM repository WHERE owner_id > 100;

-- 删除后确认结果
SELECT COUNT(*) as total_after FROM repository;
```

### 6. 数据恢复
如果误删了数据，可以从备份恢复：
```bash
# 从备份文件恢复
mysql -u username -p gogs < gogs_backup.sql

# 或恢复特定表
mysql -u username -p gogs < repository_backup.sql
```