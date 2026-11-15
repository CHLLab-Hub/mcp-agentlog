# mcp-agentlog

A learning repository for an MCP(Model Context Protocol) based AI Agent bootcamp course.

## Folder Structure
```
mcp-agentlog/
├── git_github.ipynb          # Git/GitHub basics
├── mcp03_mldl/               # Machine Learning/Deep Learning basics
│   ├── images/
│   ├── 01_ml.ipynb
│   ├── 02_scikit-learn.ipynb
│   ├── 03_주택 임대료 예측 데이터셋.ipynb        # Housing Rent Prediction Dataset
│   ├── 04_서울 자전거 공유 수요 예측.ipynb       # Seoul Bike Sharing Demand Prediction
│   ├── 05_호텔 예약 수요 데이터셋.ipynb          # Hotel Booking Demand Dataset
│   ├── 06_pytorch 프레임워크.ipynb             # PyTorch Framework basics
│   ├── 07_파이토치로 구현한 선형회귀.ipynb       # Linear Regression with PyTorch
│   ├── 08_파이토치로 구현한 논리회귀.ipynb       # Logistic Regression with PyTorch
│   ├── 09_손 글씨 숫자 데이터셋.ipynb            # Handwritten Digit Dataset(sklearn digits)
│   ├── 10_딥러닝 퍼셉트론과 다층 퍼셉트론.ipynb   # Deep Learning: Perceptron and MLP
│   ├── 11_CNN.ipynb                        # Convolutional Neural Networks(CNN)
│   ├── 12_손글씨 도형 분류하기.ipynb             # Handwritten Shape Classification
│   ├── 13_Alexnet 구현하기.ipynb               # Implementing AlexNet
│   └── 14_에일리언 vs 프레데터.ipynb            # Alien vs Predator Classification
├── mcp04_multimodal/         # Computer Vision, NLP, and Multimodal Learning
│   ├── 02_opencv/                           # OpenCV basics scripts(01–21)
│   ├── images/
│   ├── 01_컴퓨터 비전.ipynb                    # Computer Vision basics
│   ├── 03_object detection.ipynb            # Object Detection(VOC, YOLO)
│   ├── 04_이안류 CCTV 데이터셋.ipynb            # Rip Current CCTV Dataset(YOLO)
│   ├── 05_자연어 처리 기초.ipynb                # NLP basics
│   ├── 06_RNN.ipynb                         # Recurrent Neural Networks(RNN)
│   ├── 07_LSTM.ipynb                        # Long Short-Term Memory(LSTM), GRU
│   ├── 08_Transformer.ipynb                 # Transformer
│   ├── 09_PLM.ipynb                         # Pretrained Language Model(BERT)
│   ├── 10_ViT.ipynb                         # Vision Transformer(ViT)
│   └── 11_멀티모달.ipynb                      # Multimodal Learning(CLIP, DINO, BLIP)
├── mcp05_agent/              # AI Agent
│   └── 01_Agent.ipynb                       # AI Agent basics(LangGraph, Tool Calling, Web Search)
└── mcp06_project/            # Project: MeetMind (AI meeting assistant)
    ├── docs/
    │   └── planning.md                      # Project planning(background, goals, scenarios)
    └── exam/                                # Building-block examples for the project
        ├── 01_gradio1.py                    # Gradio basics(Interface)
        ├── 02_gradio2.py                    # Gradio Blocks and Tabs
        ├── 03_main.py                       # FastAPI memo server
        ├── 03_app.py                        # Gradio UI calling the FastAPI server
        ├── 04_memo_chat.py                  # Memo chatbot server(LangGraph + OpenAI)
        ├── 04_memo_ui.py                    # Gradio chat UI for the memo chatbot
        ├── 05_Qwen3_test.py                 # Speech recognition from a WAV file(Qwen3-ASR)
        ├── 06_Qwen3_live.py                 # Live microphone speech recognition(Qwen3-ASR)
        ├── 07_pyannote.py                   # Speaker enrollment and identification(pyannote)
        ├── 08_mcp.py                        # Sending messages to Slack(Incoming Webhook)
        └── 09_sqlite.py                     # Storing memos in SQLite
```
Folders follow the `mcpN_Topic` naming convention, where "N" is the session number and "Topic" is what I learned in the session. Sessions 01–02 have no material in this repository, so the numbering starts at 03.

Datasets, model weights, `.env` and virtual environments are not tracked (see [.gitignore](.gitignore)). Each folder's README explains how to prepare what its notebooks need.

## Tech Stack

- Python
- Jupyter Notebook
- PyTorch, Ultralytics YOLO, Hugging Face Transformers, timm, scikit-learn, OpenCV, Albumentations
- LangChain, LangGraph, OpenAI API, Tavily
- Gradio, FastAPI, SQLite, Qwen3-ASR, pyannote.audio, Slack Incoming Webhook
