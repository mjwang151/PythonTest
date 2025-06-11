from PIL import Image


def image_to_pdf(image_path, output_pdf_path):
    # 打开图像文件
    img = Image.open(image_path)

    # 将图像转换为 RGB 模式（确保兼容 PDF 格式）
    if img.mode == 'RGBA':
        img = img.convert('RGB')

    # 将图像保存为 PDF
    img.save(output_pdf_path, "PDF", resolution=100.0)

    print(f"图片已成功转换为 PDF：{output_pdf_path}")


# 示例调用
image_path = 'S:/tmp/ct.png'
output_pdf_path = 'S:/tmp/output/output_file.pdf'  # 设置输出 PDF 文件路径
image_to_pdf(image_path, output_pdf_path)
