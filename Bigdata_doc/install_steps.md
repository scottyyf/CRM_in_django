## 反洗钱部署使用说明

部署过程包含两个步骤

1. 大数据平台安装
2. 大数据airflow配置

### 大数据平台安装
#### 项目部署总体说明

1. 反洗钱项目部署使用ansible批量执行
2. 安装过程总体分为9个步骤，分别为0到8开头的目录
3. 每个目录中需要修改对应步骤中的文件变量   
4. 除0步骤执行myEL7.sh外，其他每个步骤执行对应目录中main.sh脚本

#### 部署步骤

默认情况下，使用三台服务器进行部署，以下为服务器信息在进行示例，os版本建议rhel7.6及以上:

| 服务器名称 | 服务器直连地址 | 服务器局域网地址 | 操作系统版本 |
| --- | --- | --- | --- |
| bigdata01 | 192.168.122.67 | 21.152.2.67 | redhat7.9 |
| bigdata02 | 192.168.122.68 | 21.152.2.68 | redhat7.9 |
| bigdata03 | 192.168.122.69 | 21.152.2.69 | redhat7.9 |

**附注：**

1. 以下安装过程全部在服务器bigdata01下使用root执行安装
2. 安装过程中提示"Enter yes to continue:"时，需要手动输入yes即可。该断点提示用于用户确认当前的步骤
    是否存在错误，方便进行问题排错
3. 运行过程中，报错的内容后面为...ignoring，则可以忽略错误，否则应该ctrl c中断当前任务，排查完成后，
   重新执行脚本，已经完成的过程请输入n跳过
4. 安装完成后，可将当前环境中的BIGDATA根删除，防止敏感数据暴露   
   
##### 安装ansible环境
该步骤将在0-Build-ansible-env文件夹下的执行

* 前提条件:
    - 当前在BIGDATA安装的根目录下
    - 当前用户为root用户
    - 已配置本地yum源。具体配置过程见**附录**
    
1. 将项目文件拷贝到bigdata01这台机器上。具体步骤略

2. 进入安装目录
    ```
    cd 0-Build-ansible-env
    ```
   
3. 安装ansible环境
    ```
    sh myEL7.sh
    ```
   
##### 系统环境预处理
该步骤在1-Prepare-system-withRoot-ansible文件夹下执行

* 前提条件:
    - 当前在BIGDATA安装的根目录下
    - 当前用户为root用户
    
1. 进入安装目录
    ```
    cd 1-Prepare-system-withRoot-ansible
    ```   

2. 修改hosts-bd文件中的参数。将bigdata01~bigdata03的对应ip修改为当前环境的对应ip。
   修改后对应条目示例如下
   ```
    192.168.122.67  HOSTNAME=bigdata01
    192.168.122.68  HOSTNAME=bigdata02
    192.168.122.69  HOSTNAME=bigdata03
   ```

3. 修改group_vals/bd-all.yml文件中的参数。将文件中的ROOT_USER和ROOT_USER_PASS修改为对应的值
    ```
    ROOT_USER: root
    ROOT_USER_PASS: <填入root的登录密码>
    ```

4. 修改hosts-bda文件中的参数。将bigdata01~bigdata03的对应ip修改为当前环境的对应ip。
   修改后对应条目示例如下
   ```
    192.168.122.67  HOSTNAME=bigdata01
    192.168.122.68  HOSTNAME=bigdata02
    192.168.122.69  HOSTNAME=bigdata03
   ```

5. 修改group_vals/bda-all.yml文件中的参数。将文件中的ROOT_USER和ROOT_USER_PASS修改为对应的值
    ```
    ROOT_USER: root
    ROOT_USER_PASS: <填入root的登录密码>
    ```
   
6. 修改inventory目录下所有文件中参数。这里以hosts-afw为例进行说明，其他文件参照这个文件进行修改。
   将BDAFW下的ip修改为实际ip信息，其他信息不做修改
    ```
    [BDAFW]
    192.168.10.67
    192.168.10.68
    192.168.10.69
    ```
 
7. 修改group_vars/all.yml文件。
    ```
    # Ansible user local
    LOCAL_ANSIBLE_USER: root
    LOCAL_ANSIBLE_HOME: /root
    ROOT_USER: root
    ROOT_USER_PASS: <root用户的密码>
    GATHER_IP: "{{ ansible_facts.eno25.ipv4.address }}" #en025为直连up的网口，可通过ip add命令查看
    GATHER_IP_INNER: "{{ ansible_facts.eno25.ipv4.address }}"
    NTP_MIP_LINUX: <内部ntp服务器地址> # 这个是ntp服务器端的地址，环境将以这个地址为服务端进行时间同步
    NTP_SIP_LINUX: <内部ntp服务器地址>
    ```

8. 修改hosts-root文件中的参数。将对应的ip地址修改为环境中的ip地址。
    - 192.168.1.x网段修改为192.168.10网段对应的ip
    - 10.136.1.x网段修改为21.152.2网段对应的ip
    
9. 运行main.sh
    ```
    sh main.sh
    ```
  
附： 

* 运行过程中，运行到Press [Y/n] to continue/skip running ===== \"ansible-playbook -i hosts-root 08-yum_mnt_with_Centos7.yml -v
，请输入n，因为前面已经配置了本地yum源，跳过该步骤
* 运行到Press [Y/n] to continue/skip running ===== \"ansible-playbook -i hosts-root 09-2-conf_ntp_self_LAN.yml -v\" : " ，
输入n，因为09-1已经配置了ntp同步，跳过该步骤
    
    
##### 安装hadoop多用户
该步骤在2-Hadoop-multiUsers-ansible目录下执行

* 前提条件:
  - 当前在BIGDATA安装的根目录下
  - 当前用户为root用户
    
1. 修改hosts-manager文件中的参数
    - 将对应10.136.1.x网段修改为192.168.10网段对应的ip
    
2. 修改group_vars/all.yml文件中对应的参数
    ```
    HDFS_ROOT_USER: root
    HDFS_ROOT_USER_PASS: <root用户密码>
    ```

3. 修改hosts-install文件中参数
    - 将对应10.136.1.x网段修改为192.168.10网段对应的ip

4. 修改hdfs.yml文件中的参数
   ```
    RM1_outer_ip: 21.152.2.67
    RM2_outer_ip: 21.152.2.68   
    JOBHIS_outer_ip: 21.152.2.69
   ```
 
5. 新建/data目录。如果有数据盘，建议使用数据盘挂载到/data目录,这里以lv的形式挂载data目录
   ```
   mkdir /data
   pvcreate /dev/sdb
   vgcreate vg_bigdata
   lvcreate -L 100G -n lv_bigdata vg_bigdata
   mkfs.xfs /dev/mapper/vg_bigdata_lv_bigdata
   mount /dev/mapper/vg_bigdata_lv_bigdata /data
   echo "/dev/mapper/vg_bigdata_lv_bigdata /data xfs defaults 0 0" >>/etc/fstab
   ```

6. 执行main.sh脚本
    ```
   sh main.sh
   ```
   
##### 安装spk多用户
该步骤在3-Spark-multiUsers-ansible目录中执行

1. 修改hosts-install文件中的参数
    - 将10.136.1.41修改为192.168.10.67
    - 将10.136.1.43修改为192.168.10.68
    - 将10.136.1.48修改为192.168.10.69
    
2. 修改group_vars/all.yml文件中的参数
    - 将10.136.1.41修改为192.168.10.67
    - 将10.136.1.43修改为192.168.10.68
    - 将10.136.1.48修改为192.168.10.69

3. 修改hosts-manager文件中参数
    - 将10.136.1.41修改为192.168.10.67
    - 将10.136.1.43修改为192.168.10.68
    - 将10.136.1.48修改为192.168.10.69
    
4. 修改hosts-spk文件中的参数
    - 将10.136.1.41修改为192.168.10.67
    - 将10.136.1.43修改为192.168.10.68
    - 将10.136.1.48修改为192.168.10.69
    
5. 执行main.sh
    ```
   sh main.sh
   ```
   
##### 安装mariadb
该步骤在4-Mariadb-galera-singleUser-ansible目录下执行

1. 修改hosts-root文件中的参数
    - 将10.136.1.41修改为192.168.10.67
    - 将10.136.1.43修改为192.168.10.68
    - 将10.136.1.48修改为192.168.10.69
    
2. 修改hosts-user文件中参数
    - 将10.136.1.41修改为192.168.10.67
    - 将10.136.1.43修改为192.168.10.68
    - 将10.136.1.48修改为192.168.10.69
    
3. 修改group_vars/all.yml中的参数。需要修改的字段修改如下
    ```
    MARIADB_ROOT: root
    MARIADB_ROOT_PASS: <root用户密码>
    HOST_IP: "{{ ansible_facts.eno25.ipv4.address }}"
    ```

4. 运行main.sh
    ```
    sh main.sh
    ```

* **附注：**
    - 运行过程中，遇到Preinstall lsof/socat/rsync software by sudo user: [Choose one step according ROOT/SUDO user]
    输入n，跳过该步骤

##### 安装hive
该步骤在5-Hive-multiUsers-ansible中执行

1. 修改hosts-install文件中的参数
    - 将10.136.1.41修改为192.168.10.67
    
2. 修改hosts-mysql文件中的参数
    - 将10.136.1.41修改为192.168.10.67
    
3. 修改hosts-manager文件中的参数
    - 将10.136.1.41修改为192.168.10.67
    
4. 执行main.sh
    ```
    sh main.sh
    ```
   
##### 安装redisSentinel
该步骤在6-RedisSentinel-singlerUser-ansible目录下执行

1. 修改hosts文件中的参数
    - 将10.136.1.54修改为192.168.10.67
    - 将10.136.1.55修改为192.168.10.68
    - 将10.136.1.56修改为192.168.10.69    
    
2. 执行main.sh
    ```
    sh main.sh
    ```
   
##### 安装Airflow-singleUser
该步骤在7-Airflow-singleUser-ansible目录下执行

1. 修改hosts.root文件中的参数
    - 将10.136.1.41修改为192.168.10.67
    - 将10.136.1.43修改为192.168.10.68
    - 将10.136.1.48修改为192.168.10.69
    
2. 修改group_vars/airflow.yml中的参数
    ```
    AIRFLOW_ROOT: root
    AIRFLOW_ROOT_PASS: <root用户的密码>
    WEB_SERVER_IP: 21.152.2.67
    BROKER_URL: "sentinel://:{{ REDIS_PASS }}@{{ REDIS_HOSTNAME_1 }}:{{ REDIS_SENTINEL_PORT }}//;sentinel://:{{ REDIS_PASS }}@{{ REDIS_HOSTNAME_2 }}:{{ REDIS_SENTINEL_PORT }}//;sentinel://:{{ REDIS_PASS }}@{{ REDIS_HOSTNAME_3 }}:{{ REDIS_SENTINEL_PORT }}//;"
    #BROKER_URL: "amqp://airflow:airflow123@{{ RMQ_HOSTNAME_1 }}:5672/{{ BROKER_VHOST }};amqp://airflow:airflow123@{{ RMQ_HOSTNAME_2 }}:5672/{{ BROKER_VHOST }};amqp://airflow:airflow123@{{ RMQ_HOSTNAME_3 }}:5672/{{ BROKER_VHOST }};"
    ```
   
3. 修改hosts.user文件中的参数
    - 将10.136.1.41修改为192.168.10.67
    - 将10.136.1.43修改为192.168.10.68
    - 将10.136.1.48修改为192.168.10.69
    
4. 修改hosts.mdb文件中的参数
    - 将10.136.1.41修改为192.168.10.67
    
5. 执行main.sh
    ```
    sh main.sh
    ```

##### 安装Hbase
该步骤在8-Hbase-multiUsers-ansible目录下执行

1. 修改hosts-install文件中的参数
    - 将10.136.1.54修改为192.168.10.67
    - 将10.136.1.55修改为192.168.10.68
    - 将10.136.1.56修改为192.168.10.69 
    
2. 修改group_vars/all.yml文件中的参数
    ```
    HBASE_LOC: /home
    zk_hostname_1: bigdata01
    zk_hostname_2: bigdata02
    zk_hostname_3: bigdata03
    RG_SVR_1: bigdata01
    RG_SVR_2: bigdata02
    RG_SVR_3: bigdata03
    ```

3. 修改hosts-manager文件中的参数
    - 将10.136.1.54修改为192.168.10.67
    - 将10.136.1.55修改为192.168.10.68
    - 将10.136.1.56修改为192.168.10.69 
    
4. 修改hosts-app文件中的参数
    - 将10.136.1.54修改为192.168.10.67
    - 将10.136.1.55修改为192.168.10.68
    - 将10.136.1.56修改为192.168.10.69 
    
5. 执行main.sh
    ```
    sh main.sh
    ```

以上整个安装步骤完成

### 大数据airflow配置

* 前提条件：
   - 已完成airflow配置的文件拷贝到bigdata01

以下步骤如无特殊说明，则在bigdata01上执行即可

#### 配置Spark-server
1. 变更start_sparkserver.sh中的内容。将--master的值改为bigdata01,修改完成后对应行如下
```
-- master spark://bigdata01:7077
```

2. 修改spark-server.jar
   * 直接vim spark-server.jar,然后搜索app.conf，enter进入
      - 将spark的master=条目中的ip更换为bigdata01
      - 将download_data_flight_db的url下ip更改为bigdata01;password更改为airflow123

3. 执行start_sparkser.sh
   ```
   sh start_sparkserver.sh
   ```

#### 配置query-server

1. 修改query_server.jar。
   
   * 直接vim query_server.jar， 然后搜索application.xml,enter进入编辑
      - 将zookeeper下的connectString对应3个IP地址更换为bigdata01, bigdata02, bigdata03
      - 将redis下的nodes字段ip更换为对应bigdata01~03,同时删除6380端口所在的条目
      - 将datasource字段url所在的ip更换为127.0.0.1;username更换为root，password修改为NYroot@123
      - 将sparkserver的rootpath的ip更换为21.152.2.67

2. 在bigdata01上执行
   - mysql -uroot -pNYroot@123 -h127.0.0.1 boc_dh < doc_dh.sql
   - mysql -uroot -pNYroot@123 -h127.0.0.1 AML < AML.sql
   - mysql -uroot -pNYroot@123 -h127.0.0.1 AML < bml_boc_menu.sql
   - mysql -uroot -pNYroot@123 -h127.0.0.1 AML < bml_boc_hdqry_orginfo.sql
   
3. 运行query_server.jar
   - java -jar query_server.jar &
   
#### 配置boc-aml
1. 修改boc_aml.jar
   * 直接vim boc_aml.jar,然后搜索application.conf
      - 将所有ip地址更改为bigdata01
      - mysql条目的url的ip更改为127.0.0.1;user为root，password为NYroot@123
   
2. 运行boc_aml.jar
   - java -jar boc_aml.jar &
   
#### 配置bank_money_laundering

1. 修改bank_money_laundering.jar
   * 修改application.yml。
      - remote条目下所有ip更改为bigdata01
      - redis的nodes条目ip更改为对应的bigdata01~03;password更改为redis123;master更为ylxfmaster
      - datasource下username更为root,password更为NYroot@123, url的ip更改为127.0.0.1
   
2. 启动
   - java -jar bank_money_laundering.jar &
   
#### 配置nginx

* 前提条件
  - 已安装nginx
  - 已进入目录为nginx的安装目录
   
1. 添加nginx配置
```
vim conf/nginx.conf
location=/aml/ {
   index index.html;
   root /data/webapps/bml_web
}

location ^~/aml/api {
   rewirte ~/aml/api(.*)$ $1 break;
   proxy_pass http://21.152.2.67:21001;
}
```

2. 创建目录并拷贝aml
   - mkdir /data/webapps/bml_web -p
   - copy -r aml /data/webapps/bml_web
   
3. 启动nginx
```
./sbin/nginx -c conf/nginx.conf -s start
```

### 附录：

##### 制作本地yum源
1. 拷贝iso中的所有文件到一个固定目录
```
rsync -Aax /mnt/* /home/iso_dir
```

2. 手动增加本地yum源
```angular2html
cat >> eof > /etc/yum.repo.d/local_repo.repo
[local_repo]
name=local repo
baseurl=file:///home/iso_dir
gpgcheck=0
enabled=1
```

