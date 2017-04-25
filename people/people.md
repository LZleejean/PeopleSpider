#人民网解析池分析

#####导语：
>人民网是世界十大报纸之一《人民日报》建设的以新闻为主的大型网上信息交互平台，也是国际互联网上最大的综合性网络媒体之一。而作为一个著名的门户网站，信息量丰富，信息类别多样，网站结构复杂，反爬虫策略严密等特点使得结构化爬取该网站变得异常困难，本篇文章则重点讨论人民网网站结构以及给出一种较为有效的爬取策略。

##一，网站整体结构

人民网的网站结构如下所示，该网站内部链接比较清晰，首页与频道页，专题页以及内容页之间都是互相链接的，所以这势必会造成很多的重复url，不过庆幸地是我们的框架可以很轻松地完成上亿条数据的去重，所以这就大大减轻了解析模块的负担。
![](https://www.processon.com/chart_image/58f4ad26e4b02e95ec5052ee.png)

##二，页面内部结构

####首页结构

经分析人民网首页结构整体如下，s代表多个标签
![](https://www.processon.com/chart_image/58f4b2b8e4b0f563a7d8170d.png)

body顶部有两个div标签广告以及一个section标签广告。之后则是十几个section，中间掺杂着若干个div标签的广告，底部则是分站与友情链接模块。
很明显首页的所有新闻相关类链接全存在与section标签中（除去第一个），如此我们则可以通过这个特点来提取我们想要的url，比如通过xpath(“//section[position()>1 and position()<12]//a/@href”)。

获取url数据库展示：

![](http://a2.qpic.cn/psb?/V14gFyih05ucmO/1NNY1nZDiQU6DxCE9rCT.2UlhN24WcnEMQWe3eJ97os!/b/dCUAAAAAAAAA&bo=NQPvAQAAAAADAP0!&rf=viewer_4&t=5)

####频道页结构

由于人民网频道种类的繁多，经验证发现频道间结构有较大差异，只有个别频道（如时政，财经等）结构大致相同，而大多频道差异性很大，这就造成了无法通过分析结构来写一个通用的频道页解析方法。还有一个较为尴尬的问题--有些新闻的url是相对路径。考虑到这些特殊性，所以最终决定通过暴力获取所有url，然后过滤掉不满足要求的url并为相对路径补充父亲节点。

我们需要的url具有如下特点：
* 字符串中包含n1--对应内容页
* 字符串中包含GB--对应内专题页
* 字符串中包含index--对应内频道页的翻页
* 字符串以.people.com.cn结尾

具体代码如下：

		self.links.append(selector.xpath(
            '//a/@href'
        ))
        parent = url.split('/')[0]
        self.links = filter(lambda x: '/n1' not in x and '/GB' not in x and 'index' not in x, self.links)
        for i in range(0, len(self.links)):
            if self.links[i].startswith('/n1') or self.links[i].startswith('index'):
                self.links[i] = parent + '/' + self.links[i]

####专题页结构

专题页面和频道页面差不多，甚至具有更大的差异性，所以我们采取和频道页面相同的处理方式。

####内容页结构

内容页结构如下所示，标题都在class= text_title的div标签的h1标签下，而新闻正文则是在id=rwb_zw的div标签的p标签下。所以我们可以分别通过这两个xpath来获取相应的新闻标题和正文。

即xpath("//h1/text()")--标题,xpath("//*[@id="rwb_zw"]/p/text()")--正文
![](https://www.processon.com/chart_image/58f4d2d9e4b02e95ec5246c9.png)

数据库结果展示：

![](http://a1.qpic.cn/psb?/V14gFyih05ucmO/WcOf3MolXp.Il1fNM*WoW7A2HFcpifnFGQpfC*6y02k!/b/dG4BAAAAAAAA&bo=IQPlAQAAAAADAOM!&rf=viewer_4&t=5)