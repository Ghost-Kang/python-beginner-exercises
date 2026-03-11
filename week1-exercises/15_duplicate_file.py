"""
找出文件夹中重名的文件

"""


__author__ = 'wangxukang'
__date__ = '2026-03-10'

import os
from collections import defaultdict
import hashlib

def get_file_hash(filepath:str,chunk_size:int = 8192)->str:

    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (PermissionError, IOError) as e:
        print(f"无法读取文件{filepath}->{e}")
        return None


def scan_duplicate_files(root_dir:str,check_content:bool = False)->dict:

    scan_maps = defaultdict(list)
    total_files =0

    print(f"\n{"="*60}")
    print(f"扫描文件路径：{os.path.abspath(root_dir)}")
    print(f"{"=" * 60}")

    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.startswith('.'):
                continue
            filepath = os.path.join(root, file)
            scan_maps[file].append(filepath)
            total_files += 1
    print(f"共扫描的文件：{total_files}")
    duplicates={name:paths for name,paths in scan_maps.items() if len(paths)>1}
    if not duplicates:
        print(f"无重复的文件！")
        return {}

    print(f"共发现重复的文件:{len(duplicates)}!")

    result = {}

    for filename,paths in sorted(duplicates.items()):
        print(f"文件：{filename}，共有{len(paths)}处")

        if check_content:
            hash_map = defaultdict(list)
            for path in paths:
                hash_file = get_file_hash(path)
                if hash_file:
                    hash_map[hash_file].append(path)

            for hash_file, hashed_paths in hash_map.items():
                content_tag = "🔴 内容相同" if len(hashed_paths) > 1 else "🟡 内容不同"
                for path in hashed_paths:
                    size = os.path.getsize(path)
                    print(f"     {content_tag} [{size:,} 字节]  {path}")

        else:
            for path in paths:
                size = os.path.getsize(path)
                print(f"     📍 [{size:,} 字节]  {path}")

        print()
        result[filename] = paths

    return result


def  generate_report(result:dict,output_dir:str= '15_output_file.txt'):

    if not result:
        print("nothing to report")
        return

    with open(output_dir,'w',encoding='utf-8') as f:
        f.write(f"\n{60*'='}\n")
        f.write("检测报告！".center(60))
        f.write(f"\n{60*'='}\n")

        for filename,paths in sorted(result.items()):
            f.write(f"文件{filename}：共有{len(paths)}！\n")
            for path in paths:
                size = os.path.getsize(path)
                f.write(f"    [{size:,} 字节]  {path}\n")
            f.write("\n")

    print(f"文件已经保存到{os.path.abspath(output_dir)}!")


if __name__ == '__main__':
    import sys
    target_dir = sys.argv[1] if len(sys.argv)>1 else '.'

    if not os.path.isdir(target_dir):
        print(f"please check the directory:{target_dir}, it is not a directory")
        sys.exit(1)

    dupes = scan_duplicate_files(target_dir,check_content=True)

    if dupes:
        generate_report(dupes)

