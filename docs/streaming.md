# 流式与实时推理

一次性合成会等整段音频渲染完才返回，长文本的**首包延迟**很高。流式引擎把文本切成小块，
每合成完一块就产出，让下游可以立刻开始播放。

## 基本用法

```python
from prosodia import ExpressiveTTS

tts = ExpressiveTTS()
for chunk in tts.stream("第一句。第二句稍长一点。第三句。"):
    play(chunk)          # 边合成边消费
```

要一次拿到全部音频和实时指标：

```python
stats = tts.stream_to_wav("……", "out.wav")
print(stats.summary())
# 3 chunks, audio=8.25s, wall=0.03s, RTF=0.003, first_audio=0.007s
```

## 切块策略

`chunk_text(text, max_chars=60)` 的规则：

1. 先在**句末标点**（。！？!?…）切；
2. 每个句子若超过 `max_chars`，再在**短语标点**（，、；:）处贪心打包；
3. 仍然超长的无标点串按字数硬切兜底。

单块字数由 `StreamingConfig.max_chunk_chars` 控制：越小首包越快，但块与块之间的韵律连贯性
越弱，需要权衡。

## 指标

`StreamStats` 提供：

| 字段 / 属性 | 含义 |
|------|------|
| `audio_seconds`       | 产出的音频总时长 |
| `wall_seconds`        | 实际墙钟耗时 |
| `first_chunk_seconds` | 首包延迟 |
| `rtf`                 | 实时率 = 墙钟 / 音频；`< 1` 表示快于实时 |
| `is_realtime`         | `rtf <= 1` |
| `throughput`          | 每秒墙钟产出多少秒音频 |

时间测量走可注入的 `clock`，因此单元测试可以用确定性的假时钟，不依赖真实耗时。

## 自定义消费端

`streaming/sink.py` 提供两种 sink：

```python
from prosodia.streaming.sink import WavSink, CallbackSink

with WavSink("out.wav") as sink:      # 累积后一次写文件
    for c in tts.stream(text):
        sink.write(c)

CallbackSink(lambda c: device.play(c))  # 每块回调——实时播放/WebSocket 推流的接入点
```

## 用参考后端跑基准

```bash
prosodia bench "你好，世界。今天天气不错。" --repeat 10
```

参考声码器很轻，在普通 CPU 上 RTF 远小于 1；换成神经后端后，这里就是评估是否满足实时的地方。
