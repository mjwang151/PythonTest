from PIL import Image
import pytesseract

# 如果 Tesseract 没有被添加到系统路径，请手动设置路径
# pytesseract.pytesseract.tesseract_cmd = r'路径到您的Tesseract.exe'

def image_to_text(image_path):
    # 打开图像文件
    img = Image.open(image_path)

    # 使用 pytesseract 进行 OCR 识别
    text = pytesseract.image_to_string(img, lang='chi_sim+eng')  # lang 参数指定中英文混合识别

    # 输出识别结果
    print(text)
    return text

# 示例调用
image_path = 'S:/tmp/1.png'  # 替换为您的图片路径
image_text = image_to_text(image_path)
print(image_text)