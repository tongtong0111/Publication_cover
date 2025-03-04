from flask import Flask, request, send_file, render_template_string
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)

# 出版社名称
publisher = "北京中电出版社"

# 著作权方，默认为有道（广州）计算机系统有限公司
copyright_holder = "有道（广州）计算机系统有限公司"

# 图片文件路径
image_path = "C:\\Users\\tongkw\\Cover\\text_img.png"

# 生成处理后的图片
def generate_image(edition_number, publication_name):
    # 打开图片
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # 设置字体和字体大小
    try:
        font = ImageFont.truetype("simhei.ttf", 40)
    except OSError:
        print("黑体字体文件未找到，使用默认字体")
        font = ImageFont.load_default()

    # 计算文字位置
    width, height = image.size
    # 纵向靠下三分之一处
    y_position = height * (4 / 5)

    # 获取文字的宽度
    publication_text_width = draw.textlength(publication_name, font=font)
    edition_text_width = draw.textlength(f"版号: {edition_number}", font=font)
    copyright_text_width = draw.textlength(copyright_holder, font=font)
    publisher_text_width = draw.textlength(publisher, font=font)

    # 第一行（出版物名称）居中
    publication_x = (width - publication_text_width) / 2

    # 后续行左对齐，与第一行的起始位置相同
    edition_x = publication_x
    copyright_x = publication_x
    publisher_x = publication_x

    # 添加出版物名称
    dot_font = ImageFont.truetype("simhei.ttf", 20)  # 调整圆点字体大小
    draw.text((publication_x, y_position + 10), "●", fill=(255, 165, 0), font=dot_font)  # 橙色圆点
    draw.text((publication_x + 30, y_position), publication_name, fill=(0, 0, 0), font=font)

    # 版号在出版物名称下方，留出一定间距，这里假设间距为 45 像素
    edition_y = y_position + 45
    dot_font = ImageFont.truetype("simhei.ttf", 20)  # 调整圆点字体大小
    draw.text((edition_x, edition_y + 10), "●", fill=(255, 165, 0), font=dot_font)  # 橙色圆点
    draw.text((edition_x + 30, edition_y), f"ISBN {edition_number}", fill=(0, 0, 0), font=font)

    # 著作权方在版号下方，留出一定间距，这里假设间距为 45 像素
    copyright_y = edition_y + 45
    draw.text((copyright_x, copyright_y + 10), "●", fill=(255, 165, 0), font=dot_font)  # 橙色圆点
    draw.text((copyright_x + 30, copyright_y), copyright_holder, fill=(0, 0, 0), font=font)

    # 出版社名称在著作权方下方，留出一定间距，这里假设间距为 45 像素
    publisher_y = copyright_y + 45
    draw.text((publisher_x, publisher_y + 10), "●", fill=(255, 165, 0), font=dot_font)  # 橙色圆点
    draw.text((publisher_x + 30, publisher_y), publisher, fill=(0, 0, 0), font=font)

    # 保存处理后的图片
    output_filename = f"封面-{publication_name}-ISBN {edition_number}.png"
    output_path = os.path.join("C:\\Users\\tongkw\\Cover", output_filename)
    image.save(output_path)

    return output_path

# 主页路由
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 获取用户输入的版号
        edition_number = request.form.get('edition_number')
        # 获取用户输入的出版物名称
        publication_name = request.form.get('publication_name')

        # 生成处理后的图片
        output_path = generate_image(edition_number, publication_name)

        # 发送处理后的图片供用户下载
        return send_file(output_path, as_attachment=True)

    # 渲染 HTML 模板
    html_template = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>出版物送审封面制作📔</title>
    <style>
        /* 整体页面背景和布局 */
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #f6f8f9 0%, #e5ebee 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }

        /* 主容器样式 */
        .container {
            background-color: #fff;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
            width: 400px;
        }

        /* 标题样式 */
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }

        /* 表单样式 */
        form {
            display: flex;
            flex-direction: column;
        }

        /* 标签样式 */
        label {
            margin-bottom: 8px;
            color: #555;
            font-size: 16px;
        }

        /* 输入框样式 */
        input {
            padding: 12px;
            margin-bottom: 20px;
            border: 1px solid #ccc;
            border-radius: 6px;
            font-size: 16px;
        }

        /* 出版物名称输入框特殊样式，设置更长 */
        #publication_name {
            width: 100%;
        }

        /* 按钮样式 */
        button {
            padding: 12px;
            background: linear-gradient(to right, #FFD700, #FFA500); /* 渐变金黄色 */
            color: #fff;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.2s ease;
            font-size: 16px;
        }

        /* 按钮悬停效果 */
        button:hover {
            background: linear-gradient(to right, #FFA500, #FFD700); /* 渐变金黄色（反向） */
            transform: scale(1.02);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>出版物送审封面制作📔</h1>
        <form method="post">
            <label for="publication_name">请输入出版物名称:</label>
            <input type="text" id="publication_name" name="publication_name" required>
            <label for="edition_number">请输入版号:</label>
            <input type="text" id="edition_number" name="edition_number" required>
            <button type="submit">下载图片</button>
        </form>
    </div>
</body>
</html>
    """
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True)