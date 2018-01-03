# UCAS_CC
国科大刷课脚本。(2017年秋季学期)

## 运行截图
![](./screenshot.png)

## 说明
目前只能在内网使用, 外网需要破解验证码（懒得写了）。

## Environment
Python: 2.7

## Installation
``` sh
pip install -r requirements.txt
```

## Usage
### 修改配置
```
mv config.sample.py config.py      # 配置个人信息
```
### 抢课
``` sh
python main.py                     # 用于选人满的课，请修改config.py中的des_courses字段
```
### 快速选课
``` sh
python fast_cc.py                  # 比main.py速度更快，适合开抢时候用。请修改config.py中的
```

## 快速选课说明
### depId配置
![](./note_deptId.png)
### sids配置
![](./note_sids.png)

## LICENSE
MIT