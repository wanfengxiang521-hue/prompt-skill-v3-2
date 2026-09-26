# 提示词 Skill V3.2

调用名：`prompt-skill-v3-2`。

把已锁定的 DIRECTOR_LOCK v1 编译为可直接使用的视频模型提示词，保留导演决定，不擅自新增剧情、镜头、表演或声音。

## 本版内容

- 统一单元时间轴，保留多轨相对偏移、切点和停顿。
- 区分标注分析图和干净生成参考，保护产品包装文字。
- 核对人物、服装、道具与事件前提。
- 独立管理对白、旁白、环境声、动作声和音乐权限。
- 支持静态镜头、隐喻并置与声音主导表达，分通道验收后再检查完整视听关系。

## 安装和调用

下载整个仓库，将其中的 `prompt-skill-v3-2` 文件夹放到 Codex 的 skills 目录（通常是 `~/.codex/skills/`）。保留 agents、references、scripts 子目录。

调用示例：

> 使用 $prompt-skill-v3-2，将这个已锁定的 DIRECTOR_LOCK v1 编译成视频提示词。

没有导演锁时需要配套 [导演 Skill V2.2](https://github.com/wanfengxiang521-hue/director-skill-v2-2)。兼容 Codex 1.2/1.3 结构的 DIRECTOR_LOCK v1。

## 校验与限制

```bash
python3 prompt-skill-v3-2/scripts/validate_prompt_skill_v3.py prompt-skill-v3-2
```

本版通过结构检查及合成场景文档行为复核；未进行真实视频生成，不保证特定模型的成片效果。模型和入口能力使用时核验。

## 来源与许可

保留原始来源、修改说明及上游许可。请阅读 [来源说明](prompt-skill-v3-2/references/provenance.md) 和 [上游许可证](prompt-skill-v3-2/references/upstream-licenses.md)；不要将不同来源的内容一概视作同一许可证。
