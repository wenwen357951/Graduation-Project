from PIL import Image
from distutils.version import StrictVersion as VS
from matplotlib import pyplot as plt
import os
import sys
import glob
import itk
import cv2
import math
import numpy as np

plt.ion()

sys.path.append("../../../")
from modules.trclab import config as docs

FIXED_IMAGE_DIR = docs.DATASET_VHP_SEG
MOVING_IMAGE_DIR = docs.DATASET_VHP_CT
OUTPUT_DIR = os.path.join(docs.LOGS_DIR, "Image-Registration")
docs.create_folder_if_not_exists(OUTPUT_DIR)


def normalize(moving_image_file):
    # 標記圖片
    moving_image_basename = os.path.basename(moving_image_file)
    fixed_image_file = os.path.join(FIXED_IMAGE_DIR, moving_image_basename[:-4] + ".bmp")

    moving_image = None
    fixed_image = None
    for idx, image_file in enumerate([moving_image_file, fixed_image_file]):
        # Load Image (grayscale)
        image = cv2.imread(image_file, 0)
        # 邊緣檢測
        x = cv2.Sobel(image, cv2.CV_16S, 1, 0)
        y = cv2.Sobel(image, cv2.CV_16S, 0, 1)
        absX = cv2.convertScaleAbs(x)
        absY = cv2.convertScaleAbs(y)
        image = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        # 去噪
        image = cv2.fastNlMeansDenoisingColored(image, None, 30, 10, 7, 21)
        # 二質化
        _, image = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY_INV)
        image = cv2.resize(image, (494, 281), interpolation=cv2.INTER_CUBIC)

        if idx == 0:
            moving_image = image
        else:
            fixed_image = image

    cv2.imwrite(os.path.join(OUTPUT_DIR, "moving_image_tmp.jpg"), moving_image)
    cv2.imwrite(os.path.join(OUTPUT_DIR, "fixed_image_tmp.jpg"), fixed_image)


def image_registration():
    PixelType = itk.ctype('float')
    moving_image_files = glob.glob(os.path.join(MOVING_IMAGE_DIR, "*.jpg"))
    for moving_image_file in moving_image_files:
        normalize(moving_image_file)

        moving_image = itk.imread(os.path.join(OUTPUT_DIR, "moving_image_tmp.jpg"), PixelType)
        fixed_image = itk.imread(os.path.join(OUTPUT_DIR, "fixed_image_tmp.jpg"), PixelType)
        Dimension = fixed_image.GetImageDimension()
        FixedImageType = itk.Image[PixelType, Dimension]
        MovingImageType = itk.Image[PixelType, Dimension]

        TransformType = itk.TranslationTransform[itk.D, Dimension]
        initialTransform = TransformType.New()
        optimizer = itk.RegularStepGradientDescentOptimizerv4.New(
            LearningRate=4,
            MinimumStepLength=0.001,
            RelaxationFactor=0.5,
            NumberOfIterations=200)

        metric = itk.MeanSquaresImageToImageMetricv4[FixedImageType, MovingImageType].New()
        registration = itk.ImageRegistrationMethodv4.New(FixedImage=fixed_image,
                                                         MovingImage=moving_image,
                                                         Metric=metric,
                                                         Optimizer=optimizer,
                                                         InitialTransform=initialTransform)

        movingInitialTransform = TransformType.New()
        initialParameters = movingInitialTransform.GetParameters()
        initialParameters[0] = 0
        initialParameters[1] = 0
        movingInitialTransform.SetParameters(initialParameters)
        registration.SetMovingInitialTransform(movingInitialTransform)

        identityTransform = TransformType.New()
        identityTransform.SetIdentity()
        registration.SetFixedInitialTransform(identityTransform)

        registration.SetNumberOfLevels(1)
        registration.SetSmoothingSigmasPerLevel([0])
        registration.SetShrinkFactorsPerLevel([1])

        registration.Update()

        transform = registration.GetTransform()
        finalParameters = transform.GetParameters()
        translationAlongX = finalParameters.GetElement(0)
        print(" Translation X = " + str(translationAlongX))
        translationAlongY = finalParameters.GetElement(1)
        print(" Translation Y = " + str(translationAlongY))
        numberOfIterations = optimizer.GetCurrentIteration()
        print(" Iterations    = " + str(numberOfIterations))
        bestValue = optimizer.GetValue()
        print(" Metric value  = " + str(bestValue))

        CompositeTransformType = itk.CompositeTransform[itk.D, Dimension]
        outputCompositeTransform = CompositeTransformType.New()
        outputCompositeTransform.AddTransform(movingInitialTransform)
        outputCompositeTransform.AddTransform(registration.GetModifiableTransform())

        resampler = itk.ResampleImageFilter.New(Input=moving_image,
                                                Transform=outputCompositeTransform,
                                                UseReferenceImage=True,
                                                ReferenceImage=fixed_image)
        resampler.SetDefaultPixelValue(100)

        # 圖片移位----------------------------------------------------------------------
        img = cv2.imread(moving_image_file, flags=1)  # flags=1讀取為彩色，flags=0讀取為灰度
        img = cv2.resize(img, (494, 281), interpolation=cv2.INTER_CUBIC)  # 變更解析度
        h, w = img.shape[:2]
        mat_shift = np.float32([[1, 0, -translationAlongX], [0, 1, -translationAlongY]])  # 移位矩陣，相當於沿x軸平移100，沿y軸平移200
        dst = cv2.warpAffine(img, mat_shift, (w, h))

        # 對齊後結果輸出
        cv2.imwrite(os.path.join(OUTPUT_DIR, os.path.basename(moving_image_file)), dst)


if __name__ == '__main__':
    if VS(itk.Version.GetITKVersion()) < VS("4.9.0"):
        print("ITK 4.9.0 is required.")
        sys.exit(1)

    image_registration()
