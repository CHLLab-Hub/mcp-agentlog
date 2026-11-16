# mcp03_mldl

## Data Notes

`data/` is not included in this repository except for `data/shape/` (see [.gitignore](.gitignore)). To reproduce each notebook, prepare the datasets below.

- **House Rent Prediction Dataset** (used in [03_주택 임대료 예측 데이터셋.ipynb](03_주택%20임대료%20예측%20데이터셋.ipynb))
  Download `House_Rent_Dataset.csv` from [Kaggle](https://www.kaggle.com/datasets/iamsouravbanerjee/house-rent-prediction-dataset) and place it under `data/`.

- **Seoul Bike Sharing Demand** (used in [04_서울 자전거 공유 수요 예측.ipynb](04_서울%20자전거%20공유%20수요%20예측.ipynb))
  Download `SeoulBikeData.csv` from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/560/seoul+bike+sharing+demand) and place it under `data/`.

- **Hotel Booking Demand** (used in [05_호텔 예약 수요 데이터셋.ipynb](05_호텔%20예약%20수요%20데이터셋.ipynb))
  Download `hotel_bookings.csv` from [Kaggle](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand) and place it under `data/`.

- **CIFAR-10** (used in [13_Alexnet 구현하기.ipynb](13_Alexnet%20구현하기.ipynb))
  Downloaded automatically into `data/` by `torchvision.datasets.CIFAR10(download=True)` in the notebook. No manual download needed ([official site](https://www.cs.toronto.edu/~kriz/cifar.html)).

- **Alien vs. Predator Images** (used in [14_에일리언 vs 프레데터.ipynb](14_에일리언%20vs%20프레데터.ipynb))
  Download from [Kaggle](https://www.kaggle.com/datasets/pmigdal/alien-vs-predator-images) and place it under `data/alien_vs_predator/`.

- **Shape dataset** (used in [12_손글씨 도형 분류하기.ipynb](12_손글씨%20도형%20분류하기.ipynb))
  Included in this repository under `data/shape/` (hand-drawn circles, triangles and X marks; 240 training and 60 test images). No download needed.
