cnf ?= config.env
argv ?= ""
include $(cnf)

ifeq ($(OS), Windows_NT)
	DETECTED_OS := Windows
else
	DETECTED_OS := $(shell sh -c 'uname -s 2>/dev/null || echo not')
	export $(shell sed 's/=.*//' $(cnf))

	ifeq ($(DETECTED_OS), Darwin)
		# MacOS
	endif
endif

$(info Detected OS: $(DETECTED_OS))
$(info Argv: $(argv))

.PHONY: help
.DEFAULT_GOAL := help

help: ## This help message
ifeq ($(DETECTED_OS), Windows)
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "%-30s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
else
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
endif

training: ## MaskRCNN Training
	# ============= Parameter Example =============
	# --name=Peritoneal_A_coco
	# --dataset=/GraduationProject/resources/k-fold/B
	# --weights=coco
	# =============================================
	docker run $(DOCKER_RUN_PARM) $(DOCKER_IMAGE) sh -c 'cd $(PROJECT_MASKRCNN_TRAINING) && python training.py $(argv)'

splash: ## MaskRCNN Splash
	# ============= Parameter Example =============
	# --name=COCO_A_TEST_B
	# --images=/GraduationProject/resources/k-fold/B/val
	# --weights=/GraduationProject/logs/Weights/coco/peritoneal_a_coco20211104T2156/mask_rcnn_peritoneal_a_coco_0100.h5
	# =============================================
	docker run $(DOCKER_RUN_PARM) $(DOCKER_IMAGE) sh -c 'cd $(PROJECT_MASKRCNN_SPLASH) && python splash.py $(argv)'

detect-and-export: ## Export MaskRCNN Detect Data
	# ============= Parameter Example =============
	# --name=IMAGENET_A_TEST_B
	# --dataset=/GraduationProject/resources/k-fold/B
	# --weights=/GraduationProject/logs/Weights/imagenet/peritoneal_a_imagenet20211108T1624/mask_rcnn_peritoneal_a_imagenet_0100.h5
	# =============================================
	docker run $(DOCKER_RUN_PARM) $(DOCKER_IMAGE) sh -c 'cd $(PROJECT_MASKRCNN_EXPORT_DETECT_DATA) && python export_detect_data.py $(argv)'

computed-from-class: ## Computed MaskRCNN Model Detect Result from classes
	# ============= Parameter Example =============
	# --jsondir=/GraduationProject/logs/MaskRCNN-ExportDetectData/IMAGE_A_TEST_B.json
	# =============================================
	docker run $(DOCKER_RUN_PARM) $(DOCKER_IMAGE) sh -c 'cd $(PROJECT_COMPUTED_DETECT_DATA) && \
	python computed_from_classes.py --jsondir=/GraduationProject/logs/MaskRCNN-ExportDetectData'


label-gen: ## Generator MaskRCNN Training Label
	# ============= Parameter Example =============
	# --label="/GraduationProject/resources/k-fold/peritoneal_cavity.txt"
	# --segmentation="/GraduationProject/assets/vhp/(VKH) Segmented Images (1000 X 570)"
	# --target="/GraduationProject/assets/alignment/CT Image Resize (1000 x 570)"
	# --output="normal.json"
	# =============================================
	docker run $(DOCKER_RUN_PARM) $(DOCKER_IMAGE) sh -c 'cd $(PROJECT_MASKRCNN_GEN_LABEL) && python generator.py $(argv)'

label-verify: ## Verify MaskRCNN Training Label
	# ============= Parameter Example =============
	# --dataset="/GraduationProject/resources/k-fold/A"
	# =============================================
	docker run $(DOCKER_RUN_PARM) $(DOCKER_IMAGE) sh -c 'cd $(PROJECT_MASKRCNN_VERIFY_LABEL) && python verify.py $(argv)'

tensorboard: ## Open Tensorboard
	# ============= Parameter Example =============
	# --logdir=/GraduationProject/logs/Weights/coco
	# =============================================
	docker run -p 6006:6006 $(DOCKER_RUN_PARM) $(DOCKER_IMAGE) sh -c 'tensorboard $(argv) --host 0.0.0.0'

version: ## Current version
	@echo $(APP_VERSION)
