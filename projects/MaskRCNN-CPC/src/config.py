####################
#   訓練模型配置
####################

# 可識別名稱
RECOGNIZABLE_NAME = "Peritoneal"
# GPU 可容納圖片數
# 如果顯示卡記憶體容量12GB，可以剛好使用兩張圖片
IMAGES_PER_GPU = 4
# 訓練的類別數量 (需要包含背景)
# 背景 + 需識別類型數量
NUM_CLASSES = 1 + 1
# 每個迭代的訓練次數
STEPS_PER_EPOCH = 100
# 跳過自信度 < 90% 的偵測辨識
DETECTION_MIN_CONFIDENCE = 0.9
