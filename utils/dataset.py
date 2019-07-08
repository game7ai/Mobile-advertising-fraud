from pathlib import Path
import zipfile
import pandas as pd


def unzip(root):
    '''
    将 root/'raw' 下的 zip 文件解压到 root 之下
    '''
    root = Path(root)
    Z = zipfile.ZipFile(list((root/'raw').glob('*.zip'))[0])
    for fn in Z.namelist():
        extract_path = Path(Z.extract(fn, root))
        dirt = root/extract_path.parts[1]  # 重命名之后的空目录
        # 防止解压后的数据中文名称乱码
        extract_path.rename(root/fn.encode('cp437').decode('gbk'))
    dirt.rmdir()  # 删除空目录
    return [x for x in root.iterdir() if x != root/'raw'][0]


class toCSV:
    def __init__(self, root):
        '''
        按照 dataType 获取数据集
        '''
        self.root = Path(root)

    def get_df(self, dataType, sep='\t'):
        path = list(self.root.glob(f'*{dataType}*'))[0]
        df = pd.read_csv(path, sep=sep, index_col='sid')
        return df