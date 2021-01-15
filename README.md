# TangSpiderFrame

## 介绍
    新爬虫框架
## 新框架修改
    1.将原来框架中的根据spider判断item来源改为使用item自身字段判断。优点是避免了大量导包
    2.修改pipline，为content自动建表
    3.添加本地pipline，结果json格式导出到result.json
##  命名规范
    1.抓取类型（text, image, video）+ _ + 源国家（国家或者语言）+ _ + 源名称 + 功能（link, content） 
    国家如果是中文或者英文可以不写
    
       
