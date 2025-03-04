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
    return render_template_string(index.html)

if __name__ == '__main__':
    app.run(debug=True)