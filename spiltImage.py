from PIL import Image

def split_image(image_path, output_dir, split_height):
    # 打开图像
    img = Image.open(image_path)
    img_width, img_height = img.size

    # 计算切分的次数
    num_splits = (img_height // split_height) + (1 if img_height % split_height > 0 else 0)

    for i in range(num_splits):
        # 计算每个切分部分的起始和结束位置
        upper = i * split_height
        lower = min((i + 1) * split_height, img_height)

        # 切割图像
        split_img = img.crop((0, upper, img_width, lower))

        # 保存切割后的图像
        split_img.save(f"{output_dir}/split_{i + 1}.png")

    print(f"图片已成功分成 {num_splits} 部分，并保存到 {output_dir} 文件夹中。")

# 示例调用
image_path = 'S:/tmp/ct.png'
output_dir = 'S:/tmp/output'
split_height = 780  # 每部分的高度（可根据需要调整）
split_image(image_path, output_dir, split_height)