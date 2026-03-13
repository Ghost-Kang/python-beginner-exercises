"""
把拍的导出的照片进行重命名

"""

__author__ = 'wangxukang'
__date__ = '2026-03-13'


from pathlib import Path
import argparse
import os

def natural_name_sort(name:str):
    import re
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', name) ]

def rename_photos(pathfile:str, prefix,start =1 , digits = 3, exts = None, dry_run = True):
    path = Path(pathfile)

    if not path.exists():
        raise FileNotFoundError(f'文件不存在{pathfile}请check文件夹！')
    if not path.is_dir():
        raise NotADirectoryError(f'此{pathfile}文件不是一个文件夹')

    if exts is None:
        exts = ['.jpg', '.jpeg', '.png', '.webp','.heic']

    files = [f for f in path.iterdir()
             if f.is_file() and f.suffix.lower() in exts]

    if not files:
        raise FileNotFoundError(f'此文件夹{pathfile}没有可编辑的文件！')

    files.sort(key = lambda f: natural_name_sort(f.name))

    print(f"找到 {len(files)} 个文件")
    print(f"命名格式：{prefix}_001.jpg")
    print("-" * 60)

    index = start
    rename =[]
    for file in files:
        ext = file.suffix.lower()
        new_name = f"{prefix}_{index:0{digits}d}{ext}"
        new_path = path/new_name

        if file.name == new_name:
            print(f"跳过（名称已一致）：{file.name}")
            index += 1
            continue
        while new_path.exists() or any( p[1] ==new_path for p in rename ):
            index = index + 1
            new_name = f"{prefix}_{index:0{digits}d}{ext}"
            new_path = path / new_name

        rename.append((file, new_path))
        index += 1

    if not rename:
        print("没有需要重命名的文件。")
        return

    print("以下是重命名预览：")
    for old_path, new_path in rename:
        print(f"{old_path.name}  ->  {new_path.name}")

    print("-" * 60)

    if dry_run:
        print("当前为预览模式，未实际改名。")
        print("如需真正执行，请加参数: --apply")
        return

    temp_plan = []
    for  i, (old_path, new_path) in enumerate(rename,start=1):
        temp_path = old_path.with_name(f"__rename_temp__{i}__{old_path.suffix.lower()}")
        os.rename(old_path, temp_path)
        temp_plan.append((temp_path, new_path))

    for temp_path, final_path in temp_plan:
        os.rename(temp_path, final_path)
        print(f"已重命名：{temp_path.name} -> {final_path.name}")

    print("全部完成")


def main():
    parser = argparse.ArgumentParser(description="批量重命名图片文件")
    parser.add_argument("folder", help="目标文件夹路径")
    parser.add_argument("prefix", help="新文件名前缀，例如 2024_旅行")
    parser.add_argument("--start", type=int, default=1, help="起始编号，默认 1")
    parser.add_argument("--digits", type=int, default=3, help="编号位数，默认 3")
    parser.add_argument("--apply", action="store_true", help="真正执行重命名")
    args = parser.parse_args()

    rename_photos(
        pathfile=args.folder,
        prefix=args.prefix,
        start=args.start,
        digits=args.digits,
        dry_run=not args.apply
    )
if __name__ == '__main__':
    main()
