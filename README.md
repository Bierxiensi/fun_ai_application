# 项目介绍
快速体验各种 AI Application，无需搭建环境，无需配置，无需部署，即可体验AI Application的功能。

# list
- [✅] llamaIndex_toy_rag - 极简 RAG 功能，支持本地各种常用格式数据，填写自己的 API Key 即可体验
- [✅] rag_factory（动态完善ing） - 基于 Qwen 模型、faiss 向量数据库的 RAG 框架，填写自己的 API Key 即可体验
  - 基于`内容哈希`判断文件是否已被处理过，`避免重复处理`
  - `意图识别`来判断用户的查询意图，根据意图来确定大模型生成还是根据本地数据生成
  - 内置了三个 `extractor`，分别提取 `pdf、word、excel` 文件中的内容，后续可根据文件类型来在 extract_processor 追加要支持的文件类型（这里参考了[dify](https://github.com/langgenius/dify/tree/main/api/core/rag/extractor)的实现）
- [✅] local_rag_factory - 基于 rag_factory 实现的本地 RAG 框架，无需填写 API Key，即可体验
  - 模型目录：`local_rag_factory/models/Qwen-4B-Instruct`
  - embeddings 模型目录：`local_rag_factory/models/Qwen-Embedding-0.6B`
- comfyUI API server - 基于 comfyUI 实现的 API 服务器，支持调用 comfyUI 的功能，目前支持以下模型
  - z_image_turbo