# This program removes watermarks from PDF documents
# author name : Pan Fei
# compile time: 2022-1-25
# Wechat:13331062681
# QQ: 200563940

from PIL import Image
from itertools import product
import fitz
import os
import sys
from tqdm import tqdm
import shutil


def pdf2img(path, file, number):
    png_path = os.path.join(path, 'png')
    if not os.path.isdir(png_path):
        os.makedirs(png_path)
    page_num = 0
    pdf_file = os.path.join(path, file)
    pdf = fitz.open(pdf_file)
    for page in tqdm(pdf):
        rotate = int(0)
        zoom_x = 2.0  # horizontal zoom
        zomm_y = 2.0  # vertical zoom
        trans = fitz.Matrix(zoom_x, zomm_y).prerotate(
            rotate
        )  # zoom factor 2 in each dimension
        # pix = page.get_pixmap(matrix=mat) # use 'mat' instead of the identity matrix
        pixmap = page.get_pixmap(matrix=trans, alpha=False)
        # for pos in product(range(pixmap.width), range(pixmap.height)):
        #    rgb = pixmap.pixel(pos[0], pos[1])
        #    if sum(rgb) >= int(number):
        #        pixmap.set_pixel(pos[0], pos[1], (255, 255, 255))
        pixmap.pil_save(f"{png_path}/{page_num}.png")  # , dpi=(300.0, 300.0)
        # print(f"第{page_num}页已转化png格式")
        page_num = page_num + 1


def remove_img(png_path, number):
    pic_dir = png_path
    img_files = sorted(os.listdir(pic_dir))
    deal_png_path = os.path.join(png_path, 'png')
    if not os.path.isdir(deal_png_path):
        os.makedirs(deal_png_path)
    name = []
    page_num = 0
    for i in img_files:
        name.append(i.split(".")[0])
    for x, i in tqdm(enumerate(img_files)):
        png_file_path = os.path.join(pic_dir, i)
        img = Image.open(png_file_path)
        width, height = img.size
        for pos in product(range(width), range(height)):
            if sum(img.getpixel(pos)[:3]) >= int(number):
                img.putpixel(pos, (255, 255, 255))
        img.save(f"{deal_png_path}/{name[x]}.png")


def pic2pdf(png_path, out_name):
    deal_png_path = os.path.join(png_path, 'png')
    pic_dir = deal_png_path
    pdf = fitz.open()
    img_files = sorted(os.listdir(pic_dir), key=lambda x: int(str(x).split('.')[0]))
    for img in img_files:
        imgdoc = fitz.open(pic_dir + '/' + img)
        pdfbytes = imgdoc.convert_to_pdf()
        imgpdf = fitz.open("pdf", pdfbytes)
        pdf.insert_pdf(imgpdf)
    pdf.save(f"{path}/{out_name}.pdf")
    pdf.close()
    print("Watermark removed")


def Help(argv):
    print('->>Description:\nThis program removes watermarks from PDF documents')
    print('Usage:\n\t./%s  xxx.pdf number out_name\n' % (argv))
    exit(-1)


path = os.getcwd()
png_path = os.path.join(path, 'png')
if not os.path.isdir(png_path):
    os.makedirs(png_path)
if len(sys.argv) < 2:
    Help(sys.argv[0])
file = sys.argv[1]
number = sys.argv[2]
out_name = sys.argv[3]
pdf2img(path, file, number)
png_path = os.path.join(path, 'png')
remove_img(png_path, number)
pic2pdf(png_path, out_name)
shutil.rmtree(png_path, ignore_errors=True)
