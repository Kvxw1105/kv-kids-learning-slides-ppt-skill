# 参考来源与许可边界

本 Skill 的独立实现参考了以下公开项目的架构经验：

- `hugohe3/ppt-master`：路线治理、受限 SVG 中间语言、源/派生工件与质量门。MIT。
- `zarazhangrui/frontend-slides`：固定舞台、视觉样页发现、浏览器编辑。MIT。
- `alchaincyf/huashu-design`：受约束 HTML→PPTX 与可编辑性合约。MIT。
- `lewislulu/html-ppt-skill`：主题 Token、布局库、演讲者模式。MIT。
- `op7418/guizang-ppt-skill`：视觉语法锁定与验证思想。AGPL；未复制其代码。
- `GordenSun/GordenPPTSkill`：模板槽位与容量检查思想；其内置模板限制非商业，未复制模板或受限资产。
- `chuspeeism/dashi-ppt-skill`：布局查询与逐节点回退思想；当前高保真导出引擎为专有许可，未复制。
- `anthropics/skills` PPTX：OOXML 验证和文件治理思想；其专有材料未复制。

本 Skill 附带脚本均为独立实现。若未来直接引入 MIT 代码，必须将上游许可证、版权声明和修改说明随包保留。不要将 AGPL、专有或仅限个人使用的代码/模板混入默认分发包。


## v0.8 新增研究来源

- `gitbrent/PptxGenJS`：母版、SVG、形状、亚洲字体、动画媒体与 75+ 演示页。MIT。
- `facebook/yoga`：内容测量、主轴/交叉轴、伸缩分配与测试夹具思想。MIT；未捆绑代码。
- `opentypejs/opentype.js`：字距、字形边界、kerning 与 advance width。MIT；仅作为可选精确测量方向。
- `rough-stuff/rough`：手绘线条、填充和 SVG 路径。MIT；默认组件为独立实现。
- `svgdotjs/svg.js`：轻量 SVG 操作与动画。MIT；默认组件不依赖该库。
- `Book Dash`：公开儿童绘本电子版、印刷版与 working source files，用于研究图文关系、镜头节奏和翻译排版。内容 CC BY 4.0；默认不打包其插画。
- `scribusproject/scribus`：桌面出版、文本框、双向语言与印刷布局经验；未捆绑代码。
- `hfg-gmuend/openmoji`：统一图标风格、中央数据表、导出脚本和一致性测试。图形 CC BY-SA 4.0、代码 LGPL-3.0；默认不打包。
