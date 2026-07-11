## 日常生活

### 健身增肌

* 问题描述：`我想多增长一点肌肉，但是我一周能去健身房的时间太少了。`
* 结果示例：[v260315-opencode-glm5](fitness-for-muscle-growth/v260315-opencode-glm5.md)

### 花粉过敏

* 问题描述：`北京的春天的花粉太多了，害得我眼睛过敏，结膜炎特别痒，现在每次出门都必须戴护目镜才行`
* 结果示例：[v260315-opencode-glm5](pollen-allergy/v260315-opencode-glm5.md)

### 白板磁吸滑落

* 问题描述：`我用磁铁把纸贴在白板上，但是纸掉下来了`
* 结果示例：[v260711-opencode-deepseek-v4-pro-manual-guidance](magnet-paper-whiteboard/v260711-opencode-deepseek-v4-pro-manual-guidance.md)

### 书放包里卷边

* 问题描述：`书本或笔记放在包里久了，页面卷边或折角。`
* 结果示例：[v260315-openclaw-glm5](schoolbag-book-torn/v260315-openclaw-glm5.md)

## 技术工程

### 鱼塘增氧

问题描述：

```
用气泵往鱼塘里注入空气，就可以在相对小的空间里饲养大量的鱼。用这个原理来加强湖泊、池塘的工业化养鱼。这个想法已经存在很久了，问题是这个过程很不经济：只有一小部分空气有机会溶解到水里，大多数空气又回到大气中。对于家庭养鱼来说，这个问题并不重要，一个小电泵就能提供充足的空气。但是对于湖水和池塘而言，规模就完全不同了，它们需要建造大功率的空气泵，安装复杂的管道系统。
这个问题需要一种不同的方法，简单、经济，当然对鱼来说要安全，因此，不要使用产生氧的化学物质。
```

* 问题来源：阿奇舒勒《创新算法》第二章问题 9
* 结果示例：[prompt2-v260315-opencode-glm5](pool-increase-oxygen/prompt2-v260315-opencode-glm5.md)
* 作者补注：让智能体直接分析的结果有些跑偏了，这个是手动追加了关于“初始缺点”的提示之后的结果

### 番茄输送管道

问题描述：

```
有一个气动传送带，形状就像个倾斜的管道。管道底部的空气压力，把小产品从管道下端移到上端。这个案例中，番茄就是用这样的管道运输的。管子延伸到大楼的楼层之间，并在几个地方改变方向。这个系统的缺点是，番茄会彼此摩擦、碰撞，最终坏掉。
需要一个气动传送系统，按照预先设置好的程序运输番茄（或其他产品) ，绝对保证产品运输速度低于某特定速度，并且番茄之间保持安全距离。不能去掉气动传送系统，因为这可能会需要我们目前没有的新设备。
```

* 问题来源：阿奇舒勒《创新算法》第二章问题 12
* 结果示例：[v260711-opencode-deepseek-v4-pro-manual-guidance](tomato-transport-pipe/v260711-opencode-deepseek-v4-pro-manual-guidance.md)

### 陨石撞击模拟

问题描述：

```
陨石撞击模拟器采用3~5mm的钢球高速撞击字宙飞船外壳样本，检测样本的破坏程度。撞击模拟器采用爆炸式加速器可以产生50km/s的高速射流，让其冲击钢球以将它射出。但是当钢球加速到16km/s时，钢球因承受不了过高加速度和高速射流的冲击而解体。已知钢球可承受的最高速度为8km/s，但模拟陨石撞击需要至少16km/s。当前要解决的问题是，如何模拟陨石以16km/s的速度撞击飞船外壳。
已经被证明的不可行方法如下：
* 采用硬度更高或更软的材料制造钢球
* 尝试采用直径更大的钢球；
* 采用缓慢加速的方式。
解决问题必须满足的条件如下：
* 撞击钢球与飞船外壳样本相对速度必须达到16km/s；
* 钢球保持完整；
* 原理解易于实现
```

* 问题来源：檀润华《TRIZ及应用》10.5 节
* 结果示例：[v260315-opencode-glm5](meteoroid-impact/v260315-opencode-glm5.md)

### 软体机器人漏气

问题描述：

```
3D打印软体机器人的基本方法是靠一个很小的喷头往外挤出已经烧热融化的‘TPU’膏状材料，材料一层一层往上叠加成型。在这个过程中，加工路径是不连续的，其中的回抽和快速移动很容易在侧壁上产生缝隙。一旦气从缝隙中漏出去，做成的气动机器人部件肯定就不工作了。
在以往的很多研究中，解决漏气的思路非常直接——把壁加厚。尽管达到了气密效果，但由于TPU材料的硬度本来就比硅胶高一个数量级，这样做出的制动器又厚又硬，甚至难以活动，通常需要加超高的气压才能勉强达到一定的弯曲效果。
```

* 问题来源：https://mp.weixin.qq.com/s/rZkNc1gLx7gq-jdwyr-tKg
* 结果示例：[v260315-opencode-deepseek-v3.2](3d-print-robot-gas-leakage/v260315-opencode-deepseek-v3.2.md)

## AI 工具

### skill 自我改进

问题描述：

```
我为我的 AI 智能体编写了因果链分析的 skill，但是它的表现并不让我满意。具体来说，当我提出"Transformer 注意力计算量太大"这个问题时，智能体生成的分析结果报告里面会出现"序列长度大"这种表述。但是在我的 `SKILL.md` 里面，我明明特别强调了这一点：
- **精确区分**：务必区分非常相似、但实际上不同的概念。比如，`参与注意力计算的元素个数`、`输入数据总 token 数`、`输入文本单词数/图像像素个数/视频帧数`，是三个完全不同的东西，绝不能用笼统的`序列长度`糊弄过去。
即使我特地补充了这一个专门针对当前问题的指令，模型也完全没有遵循。我感到很无奈。
```

* 作者补注：不是所有模型都会出现这个问题
* 结果示例：[v260315-opencode-glm5](skill-self-improvement/v260315-opencode-glm5.md)

### AI 讨好用户

* 问题描述：`比方说一个人。他有一个什么想法。他告诉 AI 我有一个想法，哪怕他那个想法糟糕透顶，AI 很有可能也不会直接告诉他，会顺着他说`
* 问题来源：https://mp.weixin.qq.com/s/mhF6XhgM0Lh3VeNCbwbt0w
* 结果示例：[prompt2-v260315-opencode-glm5.1](ai-sycophancy/prompt2-v260315-opencode-glm5.1.md)

## AI 算法

### Transformer 注意力复杂度

* 问题描述：`Transformer 注意力计算量太大`
* 结果示例：[v260711-opencode-deepseek-v4-pro-manual-guidance](transformer-attention-complexity/v260711-opencode-deepseek-v4-pro-manual-guidance.md)

### fp32 精度不足导致训练 loss spike

* [问题描述](loss-spike-from-nfi/prompt.txt)
* 问题来源：https://mp.weixin.qq.com/s/LS2zK_mD68e653_ao2QeZg
* 结果示例：[v260711-opencode-deepseek-v4-pro-manual-guidance](loss-spike-from-nfi/v260711-opencode-deepseek-v4-pro-manual-guidance.md)

## 其他
### 全球变暖

* 问题描述：`全球变暖`
* 结果示例：[v260315-opencode-glm5](global-warming/v260315-opencode-glm5.md)
