import jieba
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')  # 强制使用非交互式后端
from matplotlib import pyplot as plt
from wordcloud import WordCloud
import os
import glob
import random

MAX_KEEP_FILES = 5  # 最多保留的历史文件数


def getCommentsImage(comments):
    # 生成唯一文件名（添加前缀 "wordcloud_" 便于识别）
    random_suffix = random.randint(1, 1000000)
    save_path = f'./static/wordcloud_{random_suffix}.png'

    # --- 生成词云图（保持原有逻辑） ---
    text = ''.join([i['content'] for i in comments])
    cut = jieba.cut(text)
    string = ' '.join(cut)

    img = Image.open('./static/1.png')
    img_arr = np.array(img)

    wc = WordCloud(
        background_color='#2d3035',
        mask=img_arr,
        font_path='STHUPO.TTF',
        colormap='viridis'
    )
    wc.generate_from_text(string)

    fig = plt.figure(figsize=(10, 8), dpi=100)
    plt.imshow(wc)
    plt.axis('off')

    plt.savefig(
        save_path,
        bbox_inches='tight',
        pad_inches=0,
        transparent=True
    )
    plt.close(fig)
    # --- 生成结束 ---

    # 清理旧文件（保留最多 MAX_KEEP_FILES 个）
    all_wordclouds = glob.glob('./static/wordcloud_*.png')
    all_wordclouds.sort(key=os.path.getmtime, reverse=True)  # 按修改时间排序

    # 删除超出保留数量的旧文件
    for old_file in all_wordclouds[MAX_KEEP_FILES:]:
        try:
            os.remove(old_file)
        except Exception as e:
            print(f"删除旧文件失败: {old_file} - {e}")

    return save_path