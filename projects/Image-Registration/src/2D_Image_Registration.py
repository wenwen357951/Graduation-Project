import os
import sys
import glob
import itk
import cv2
import numpy as np
from matplotlib import pyplot as plt

plt.ion()
from PIL import Image
import math
from distutils.version import StrictVersion as VS

ROOT_DIR = os.path.abspath("..")
RESOURCES_DIR = os.path.join(ROOT_DIR, "resources")
OUTPUT_DIR = os.path.join(ROOT_DIR, "output")

IMAGE_DIR = os.path.join(RESOURCES_DIR, "images")
IMAGE_DIR_ANN = os.path.join(IMAGE_DIR, "ann")
IMAGE_DIR_CT = os.path.join(IMAGE_DIR, "ct")
IMAGE_DIR_MRI = os.path.join(IMAGE_DIR, "mr")
IMAGE_DIR_SEG = os.path.join(IMAGE_DIR, "seg")

print(RESOURCES_DIR)


def main(dir, type):
    PixelType = itk.ctype('float')
    image_files = glob.glob(dir + "/*.jpg", recursive=True)
    for filename in image_files:

        basename = os.path.basename(filename)
        filename_ann = os.path.join(IMAGE_DIR_ANN, basename)  # CRYO切片
        filename_seg = os.path.join(IMAGE_DIR_SEG, basename[:-4] + ".bmp")  # 標記圖片
        outputImageDir = os.path.join(OUTPUT_DIR, basename[:-4])  # 輸出位置
        if not os.path.exists(outputImageDir):
            os.mkdir(outputImageDir)  # 創資料夾

        img = cv2.imread(filename, 0)
        x = cv2.Sobel(img, cv2.CV_16S, 1, 0)  # 邊緣檢測
        y = cv2.Sobel(img, cv2.CV_16S, 0, 1)
        absX = cv2.convertScaleAbs(x)
        absY = cv2.convertScaleAbs(y)
        dst = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
        cv2.imwrite('temp.jpg', dst, [cv2.IMWRITE_JPEG_QUALITY, 100])
        img = cv2.imread('temp.jpg')
        dstt = cv2.fastNlMeansDenoisingColored(img, None, 30, 10, 7, 21)  # 去噪
        retval, dstt = cv2.threshold(dstt, 100, 255, cv2.THRESH_BINARY_INV)  # 二質化
        cv2.imwrite('temp.jpg', dstt, [cv2.IMWRITE_JPEG_QUALITY, 100])

        img = cv2.imread(filename_seg, 0)
        x = cv2.Sobel(img, cv2.CV_16S, 1, 0)
        y = cv2.Sobel(img, cv2.CV_16S, 0, 1)
        absX = cv2.convertScaleAbs(x)
        absY = cv2.convertScaleAbs(y)
        dst = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
        cv2.imwrite('ann_temp.jpg', dst, [cv2.IMWRITE_JPEG_QUALITY, 100])
        img = cv2.imread('ann_temp.jpg')
        dstt = cv2.fastNlMeansDenoisingColored(img, None, 30, 10, 7, 21)
        retval, dstt = cv2.threshold(dstt, 100, 255, cv2.THRESH_BINARY_INV)
        dstt = cv2.resize(dstt, (494, 281), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite('ann_temp.jpg', dstt, [cv2.IMWRITE_JPEG_QUALITY, 100])

        fixedImage = itk.imread('ann_temp.jpg', PixelType)  #
        movingImage = itk.imread("temp.jpg", PixelType)
        Dimension = fixedImage.GetImageDimension()
        FixedImageType = itk.Image[PixelType, Dimension]
        MovingImageType = itk.Image[PixelType, Dimension]

        TransformType = itk.TranslationTransform[itk.D, Dimension]
        initialTransform = TransformType.New()

        optimizer = itk.RegularStepGradientDescentOptimizerv4.New(
            LearningRate=4,
            MinimumStepLength=0.001,
            RelaxationFactor=0.5,
            NumberOfIterations=200)

        metric = itk.MeanSquaresImageToImageMetricv4[
            FixedImageType, MovingImageType].New()

        registration = itk.ImageRegistrationMethodv4.New(FixedImage=fixedImage,
                                                         MovingImage=movingImage,
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

        resampler = itk.ResampleImageFilter.New(Input=movingImage,
                                                Transform=outputCompositeTransform,
                                                UseReferenceImage=True,
                                                ReferenceImage=fixedImage)
        resampler.SetDefaultPixelValue(100)

        # 圖片移位----------------------------------------------------------------------
        img = cv2.imread(filename, flags=1)  # flags=1讀取為彩色，flags=0讀取為灰度
        img = cv2.resize(img, (494, 281), interpolation=cv2.INTER_CUBIC)  # 變更解析度
        h, w = img.shape[:2]
        mat_shift = np.float32([[1, 0, -translationAlongX], [0, 1, -translationAlongY]])  # 移位矩陣，相當於沿x軸平移100，沿y軸平移200
        dst = cv2.warpAffine(img, mat_shift, (w, h))

        cv2.imwrite(os.path.join(outputImageDir, "final_Align_output" + type + ".jpg"), dst)  # 對齊後結果輸出

        img = cv2.imread(filename_seg[:-4] + ".bmp", flags=1)  # flags=1讀取為彩色，flags=0讀取為灰度
        img = cv2.resize(img, (494, 281), interpolation=cv2.INTER_CUBIC)  # 變更解析度
        cv2.imwrite("filename_seg.jpg", img)

        # 疊圖------
        img1 = Image.open(os.path.join(outputImageDir, "final_Align_output" + type + ".jpg"))  # CT
        img2 = Image.open("filename_seg.jpg")  # 標記原圖
        final_img2 = Image.blend(img1, img2, ((math.sqrt(5) - 1) / 2))

        final_img2.save(os.path.join(outputImageDir, "afterAlign_combine_" + type + ".jpg"))
        print(type + basename + " 對齊完成")
        print(os.path.join(outputImageDir, "afterAlign_combine_" + type + ".jpg"))


if __name__ == '__main__':
    if VS(itk.Version.GetITKVersion()) < VS("4.9.0"):
        print("ITK 4.9.0 is required.")
        sys.exit(1)

    fixedImageDir = IMAGE_DIR_ANN
    movingImageDir = IMAGE_DIR_CT
    main(IMAGE_DIR_CT, "ct")
