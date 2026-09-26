# DIRECTOR_LOCK v1 输入合同

编译只接受经过导演阶段锁定的合同。缺失决定性字段时停止，不推断创意答案。

## 两阶段入口

用户直接给脚本、分镜、口播文案或自然语言镜头要求并请求最终提示词时，先由 `$director-skill-v2-2` 在内部生成正式合同，再回到本 Skill 编译。自然语言未字段化本身不是 `BLOCKED_UNSOLVABLE`；只有导演层也无法在现有事实与授权范围内唯一锁定时才阻断。

如果用户明确要求只运行编译器、禁止调用导演层，或给出的合同标记为 `blocked`，只返回最小缺失项与冲突，不自行补导演决定。

## DIRECTOR_LOCK 顶层必需字段

- `contract_family: "DIRECTOR_LOCK v1"`、`version`、`director_lock_id`：合同族、兼容版本与唯一标识；
- `project`：总时长、画幅和帧率假设；
- `SCRIPT_LOCK.script_lock_id`：所依赖的锁定剧本版本；
- `SCRIPT_LOCK`：剧情、人物关系、对白意义、信息揭示顺序、结尾与禁改项；
- `director_book`：观众状态 A/B、全片视觉命题、主视觉锚点、物理动词、空间系统、视觉规则、所选方法，以及表演、摄影、光线、声音、剪辑和静音观看合同；
- `shots`：其数组顺序就是导演锁定的镜头顺序；
- `shots[].generation_units`：本轮可提交给生成模型的单元；
- `continuity_invariants`：人物、产品、道具、空间、屏幕方向、光线、声音状态；
- `reference_registry`：原始标签、用途和授权状态；
- `total_timing_check`、`resource_dependencies`、`transfer_limits`、`unresolved_risks`、`lock_status`。

`surface_profile` 属于运行时编译上下文，不写回导演合同。编译开始前另行取得实际入口的已核验档案；无法核验时使用保守档。

## generation_unit 必需字段

- `unit_id`、`shot_ids`、`duration_target`；
- `start_state`、`current_action`、`endpoint`；
- `completed_beats`、`reserved_beats`、`do_not_show`；
- `actor_track`、`dialogue_track`、`camera_track`、`sound_track`；
- `blocking_contract`、`camera_contract`、`sound_contract`、`dialogue_contract`；
- `references_needed`、`preservation_locks`；
- `serial_transitions` 与 `timing_evidence`。

## 不可变比较

编译前记录以下指纹，编译后逐项回查：

| 维度 | 必须保持 |
|---|---|
| 故事 | 事件、因果、关系、揭示顺序、结尾 |
| 镜头 | 数量、顺序、每镜职责、剪辑点 |
| 视觉系统 | 观众状态变化、主视觉锚点、物理动词、空间系统、视觉规则、静音测试 |
| 表演 | 触发、策略、行为泄露、状态残留 |
| 对白 | 说话人、锁定原文、标点停顿、次序；只有用户明确给出本段许可时才允许在许可范围内改写 |
| 摄影机 | 起点、运动动机、路径、终点 |
| 声音 | 声源、触发点、延续与停止状态 |
| 连续性 | 身份、产品几何、服化、道具、空间、屏幕方向 |

硬规则：不得重新导演；不得新增镜头；不得改变镜头顺序；不得改写剧情；锁定台词逐字保留。编译前后对台词做逐字比对；任何未经明确授权的增字、删字、换词、合句、拆句或同义改写都阻断输出。发声主体、嘴部状态和声源切换同样以 `dialogue_contract` 为权威；编译器不得用默认达人规则覆盖已经锁定的同期口播或画外旁白决定。平台限制若与合同冲突，报告冲突并退回导演层重新分配生成单元，编译器不得擅自处理。

## 阻断报告

报告只列：缺失字段、相互冲突的字段、为什么模型无法唯一执行、需要上游补充的最小信息。不要给创意替代方案，不要先输出一个“试试看”的提示词。

## V3 兼容规则

- 原 Codex 1.2：保持原嵌套结构；非商业任务可直接验证后编译。商业/KOC/精确多资产任务先由导演层补齐1.3扩展并重新锁定，不由编译器补创意。
- Codex 1.3：要求 `schema_variant: codex-director-lock`，保留 SCRIPT_LOCK、director_book、shots[].generation_units 及四轨证据。commercial_contract.applicable=false 要有非商业原因；商业任务不可借false绕过。
- Hermes 1.3：immutable_facts、audience_change、duration_loads 等字段不是直接兼容输入。退回导演层按真实输入映射，补齐缺失时码、单元与声源，不只改版本号。
- 未知版本或结构：列出不兼容字段，保留原文件，不猜测。

商业扩展验证见 [commercial-compile.md](commercial-compile.md)。

## 表达与摄影保真

导演2.1的expression_design及camera.position_orientation/composition_depth/focus_subject_and_transition属于不可变决定。编译保留实际承载物、关系、遮挡/揭示、声画对位、机位、构图、运动起止与焦点。隐喻编译为锁定画面，不让模型‘自行象征’，不把气氛改成产品证明。若旧字段已含同等决定可无损映射；缺关键决定退导演层，不自行补焦段或运镜。固定机位不得为了‘动态’而新增运动。
