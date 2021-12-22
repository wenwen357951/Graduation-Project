cnf ?= config.env
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

.PHONY: help
.DEFAULT_GOAL := help

help: ## This help message
ifeq ($(DETECTED_OS), Windows)
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "%-30s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
else
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
endif

training: ## MaskRCNN Training
	docker run $(DOCKER_RUN_PARM) $(DOCKER_IMAGE) sh -c 'cd $(PROJECT_MASKRCNN_TRAINING) && python training.py --name=Peritoneal_A_coco --dataset=/GraduationProject/resources/k-fold/B --weights=coco'

splash: ## MaskRCNN Splash
	docker run $(DOCKER_RUN_PARM) $(DOCKER_IMAGE) sh -c 'cd $(PROJECT_MASKRCNN_SPLASH) && python splash.py --name=COCO_A_TEST_B --images=/GraduationProject/resources/k-fold/B/val --weights=/GraduationProject/logs/Weights/coco/peritoneal_a_coco20211104T2156/mask_rcnn_peritoneal_a_coco_0100.h5'
	docker run $(DOCKER_RUN_PARM) $(DOCKER_IMAGE) sh -c 'cd $(PROJECT_MASKRCNN_SPLASH) && python splash.py --name=COCO_A_TEST_C --images=/GraduationProject/resources/k-fold/C/val --weights=/GraduationProject/logs/Weights/coco/peritoneal_a_coco20211104T2156/mask_rcnn_peritoneal_a_coco_0100.h5'
	docker run $(DOCKER_RUN_PARM) $(DOCKER_IMAGE) sh -c 'cd $(PROJECT_MASKRCNN_SPLASH) && python splash.py --name=COCO_A_TEST_D --images=/GraduationProject/resources/k-fold/D/val --weights=/GraduationProject/logs/Weights/coco/peritoneal_a_coco20211104T2156/mask_rcnn_peritoneal_a_coco_0100.h5'
	docker run $(DOCKER_RUN_PARM) $(DOCKER_IMAGE) sh -c 'cd $(PROJECT_MASKRCNN_SPLASH) && python splash.py --name=COCO_A_TEST_E --images=/GraduationProject/resources/k-fold/E/val --weights=/GraduationProject/logs/Weights/coco/peritoneal_a_coco20211104T2156/mask_rcnn_peritoneal_a_coco_0100.h5'

	docker run $(DOCKER_RUN_PARM) $(DOCKER_IMAGE) sh -c 'cd $(PROJECT_MASKRCNN_SPLASH) && python splash.py --name=COCO_B_TEST_A --images=/GraduationProject/resources/k-fold/A/val --weights=/GraduationProject/logs/Weights/coco/peritoneal_b_coco20211217T0432-retrain/mask_rcnn_peritoneal_b_coco_0100.h5'
	docker run $(DOCKER_RUN_PARM) $(DOCKER_IMAGE) sh -c 'cd $(PROJECT_MASKRCNN_SPLASH) && python splash.py --name=COCO_B_TEST_C --images=/GraduationProject/resources/k-fold/C/val --weights=/GraduationProject/logs/Weights/coco/peritoneal_b_coco20211217T0432-retrain/mask_rcnn_peritoneal_b_coco_0100.h5'
	docker run $(DOCKER_RUN_PARM) $(DOCKER_IMAGE) sh -c 'cd $(PROJECT_MASKRCNN_SPLASH) && python splash.py --name=COCO_B_TEST_D --images=/GraduationProject/resources/k-fold/D/val --weights=/GraduationProject/logs/Weights/coco/peritoneal_b_coco20211217T0432-retrain/mask_rcnn_peritoneal_b_coco_0100.h5'
	docker run $(DOCKER_RUN_PARM) $(DOCKER_IMAGE) sh -c 'cd $(PROJECT_MASKRCNN_SPLASH) && python splash.py --name=COCO_B_TEST_E --images=/GraduationProject/resources/k-fold/E/val --weights=/GraduationProject/logs/Weights/coco/peritoneal_b_coco20211217T0432-retrain/mask_rcnn_peritoneal_b_coco_0100.h5'

	docker run $(DOCKER_RUN_PARM) $(DOCKER_IMAGE) sh -c 'cd $(PROJECT_MASKRCNN_SPLASH) && python splash.py --name=COCO_C_TEST_A --images=/GraduationProject/resources/k-fold/A/val --weights=/GraduationProject/logs/Weights/coco/peritoneal_c_coco20211115T1430/mask_rcnn_peritoneal_c_coco_0100.h5'
	docker run $(DOCKER_RUN_PARM) $(DOCKER_IMAGE) sh -c 'cd $(PROJECT_MASKRCNN_SPLASH) && python splash.py --name=COCO_C_TEST_B --images=/GraduationProject/resources/k-fold/B/val --weights=/GraduationProject/logs/Weights/coco/peritoneal_c_coco20211115T1430/mask_rcnn_peritoneal_c_coco_0100.h5'
	docker run $(DOCKER_RUN_PARM) $(DOCKER_IMAGE) sh -c 'cd $(PROJECT_MASKRCNN_SPLASH) && python splash.py --name=COCO_C_TEST_D --images=/GraduationProject/resources/k-fold/D/val --weights=/GraduationProject/logs/Weights/coco/peritoneal_c_coco20211115T1430/mask_rcnn_peritoneal_c_coco_0100.h5'
	docker run $(DOCKER_RUN_PARM) $(DOCKER_IMAGE) sh -c 'cd $(PROJECT_MASKRCNN_SPLASH) && python splash.py --name=COCO_C_TEST_E --images=/GraduationProject/resources/k-fold/E/val --weights=/GraduationProject/logs/Weights/coco/peritoneal_c_coco20211115T1430/mask_rcnn_peritoneal_c_coco_0100.h5'

	docker run $(DOCKER_RUN_PARM) $(DOCKER_IMAGE) sh -c 'cd $(PROJECT_MASKRCNN_SPLASH) && python splash.py --name=COCO_D_TEST_A --images=/GraduationProject/resources/k-fold/A/val --weights=/GraduationProject/logs/Weights/coco/peritoneal_d_coco20211105T1545/mask_rcnn_peritoneal_d_coco_0100.h5'
	docker run $(DOCKER_RUN_PARM) $(DOCKER_IMAGE) sh -c 'cd $(PROJECT_MASKRCNN_SPLASH) && python splash.py --name=COCO_D_TEST_B --images=/GraduationProject/resources/k-fold/B/val --weights=/GraduationProject/logs/Weights/coco/peritoneal_d_coco20211105T1545/mask_rcnn_peritoneal_d_coco_0100.h5'
	docker run $(DOCKER_RUN_PARM) $(DOCKER_IMAGE) sh -c 'cd $(PROJECT_MASKRCNN_SPLASH) && python splash.py --name=COCO_D_TEST_C --images=/GraduationProject/resources/k-fold/C/val --weights=/GraduationProject/logs/Weights/coco/peritoneal_d_coco20211105T1545/mask_rcnn_peritoneal_d_coco_0100.h5'
	docker run $(DOCKER_RUN_PARM) $(DOCKER_IMAGE) sh -c 'cd $(PROJECT_MASKRCNN_SPLASH) && python splash.py --name=COCO_D_TEST_E --images=/GraduationProject/resources/k-fold/E/val --weights=/GraduationProject/logs/Weights/coco/peritoneal_d_coco20211105T1545/mask_rcnn_peritoneal_d_coco_0100.h5'

	docker run $(DOCKER_RUN_PARM) $(DOCKER_IMAGE) sh -c 'cd $(PROJECT_MASKRCNN_SPLASH) && python splash.py --name=COCO_E_TEST_A --images=/GraduationProject/resources/k-fold/A/val --weights=/GraduationProject/logs/Weights/coco/peritoneal_e_coco20211220T0810-retrain/mask_rcnn_peritoneal_e_coco_0100.h5'
	docker run $(DOCKER_RUN_PARM) $(DOCKER_IMAGE) sh -c 'cd $(PROJECT_MASKRCNN_SPLASH) && python splash.py --name=COCO_E_TEST_B --images=/GraduationProject/resources/k-fold/B/val --weights=/GraduationProject/logs/Weights/coco/peritoneal_e_coco20211220T0810-retrain/mask_rcnn_peritoneal_e_coco_0100.h5'
	docker run $(DOCKER_RUN_PARM) $(DOCKER_IMAGE) sh -c 'cd $(PROJECT_MASKRCNN_SPLASH) && python splash.py --name=COCO_E_TEST_C --images=/GraduationProject/resources/k-fold/C/val --weights=/GraduationProject/logs/Weights/coco/peritoneal_e_coco20211220T0810-retrain/mask_rcnn_peritoneal_e_coco_0100.h5'
	docker run $(DOCKER_RUN_PARM) $(DOCKER_IMAGE) sh -c 'cd $(PROJECT_MASKRCNN_SPLASH) && python splash.py --name=COCO_E_TEST_D --images=/GraduationProject/resources/k-fold/D/val --weights=/GraduationProject/logs/Weights/coco/peritoneal_e_coco20211220T0810-retrain/mask_rcnn_peritoneal_e_coco_0100.h5'

label-gen: ## Generator MaskRCNN Training Label
	docker run $(DOCKER_RUN_PARM) $(DOCKER_IMAGE) sh -c 'cd $(PROJECT_MASKRCNN_GEN_LABEL) && python generator.py \
 	--label="/GraduationProject/resources/k-fold/peritoneal_cavity.txt" \
 	--segmentation="/GraduationProject/assets/vhp/(VKH) Segmented Images (1000 X 570)" \
 	--target="/GraduationProject/assets/alignment/CT Image Resize (1000 x 570)" \
 	--output="normal.json"'

version: ## current version
	@echo $(APP_VERSION)