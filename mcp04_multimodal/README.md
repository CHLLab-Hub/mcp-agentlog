# mcp04_multimodal

## Data Notes

`data/` and `model/` are not included in this repository (see `.gitignore`). To reproduce each notebook, prepare the datasets below.

- **VOC2007** (used in [03_object detection.ipynb](03_object%20detection.ipynb))
  Download from the [official PASCAL VOC site](http://host.robots.ox.ac.uk/pascal/VOC/voc2007/) and place it under `data/VOCdevkit/VOC2007`.

- **Rip Current CCTV dataset** (used in [04_이안류 CCTV 데이터셋.ipynb](04_이안류%20CCTV%20데이터셋.ipynb))
  Download from [AI Hub](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=71297) (login/approval required) and place it under `data/Sample/` as referenced by `BASE_DIR` in the notebook.

- **K-MHaS** (used in [09_PLM.ipynb](09_PLM.ipynb))
  Cloned automatically by the notebook itself (`git clone https://github.com/adlnlp/K-MHaS.git`) into `data/K-MHaS`. No manual download needed.

- **License plate dataset** (used in [10_ViT.ipynb](10_ViT.ipynb))
  Download from [AI Hub](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=172) (login/approval required) and place `annotations.json` and the `images/` folder under `data/ViT/`.

> AI Hub datasets require a registered account and individual approval, and their terms of use restrict redistribution — they are not bundled or mirrored in this repository.

- **ImageNetV2** (used in [11_멀티모달.ipynb](11_멀티모달.ipynb))
  Downloaded automatically via Hugging Face `datasets.load_dataset("clip-benchmark/wds_imagenetv2")`. No manual download needed.

- **Model weights** (`model/`)
  `yolo11s.pt` is downloaded automatically by Ultralytics on first use. Trained checkpoints (e.g. `best.pt`, `best_vit_multihead.pth`) are produced by running the training cells and are not included here.
