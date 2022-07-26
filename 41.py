from time import sleep, perf_counter
import os
import shutil
import threading
import time
import argparse


files_expansion = {
    'images':('.jpeg', '.png', '.jpg', '.svg'),
    'video':('.avi', '.mp4', '.mov', '.mkv'),
    'documents':('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'),
    'music':('.mp3', '.ogg', '.wav', '.amr'),
    'archives':('.zip', '.gz', '.tar')}

need_files = {}
parser = argparse.ArgumentParser(description='Сортировка папки')
parser.add_argument('path', type=str, help='Путь к папке,можно без кавычек' )
args = parser.parse_args()

def normalize(name_dir):
    TRANS = {1072: 'a', 1040: 'A', 1073: 'b', 1041: 'B', 1074: 'v', 1042: 'V', 1075: 'g',
         1043: 'G', 1076: 'd', 1044: 'D', 1077: 'e', 1045: 'E', 1105: 'e', 1025: 'E',
         1078: 'j', 1046: 'J', 1079: 'z', 1047: 'Z', 1080: 'i', 1048: 'I', 1081: 'j',
         1049: 'J', 1082: 'k', 1050: 'K', 1083: 'l', 1051: 'L', 1084: 'm', 1052: 'M',
         1085: 'n', 1053: 'N', 1086: 'o', 1054: 'O', 1087: 'p', 1055: 'P', 1088: 'r',
         1056: 'R', 1089: 's', 1057: 'S', 1090: 't', 1058: 'T', 1091: 'u', 1059: 'U',
         1092: 'f', 1060: 'F', 1093: 'h', 1061: 'H', 1094: 'ts', 1062: 'TS',
         1095: 'ch', 1063: 'CH', 1096: 'sh', 1064: 'SH', 1097: 'sch', 1065: 'SCH',
         1098: '', 1066: '', 1099: 'y', 1067: 'Y', 1100: '', 1068: '', 1101: 'e',
         1069: 'E', 1102: 'yu', 1070: 'YU', 1103: 'u', 1071: 'U',
         1108: 'ja', 1028: 'JA', 1110: 'je', 1030: 'JE', 1111: 'ji', 1031: 'JI', 1169: 'g', 1168: 'G'}
    
    expansion = '.'+os.path.splitext(name_dir)[1][1:].strip()
    verif_name = name_dir.translate(TRANS).replace(expansion,'')
    
    for i in verif_name:
        if not i.isdigit() and not i.isalpha():
            verif_name = verif_name.replace(i,'_')
            
    return(verif_name+expansion)


def search_file(root,dirr,file):
    if len(root.split("\\"))>=3 and root.split("\\")[2] not in files_expansion.keys():
        need_files[root] = file
    elif len(root.split("\\"))==2:
        need_files[root] = file
    
def check_expansion(root, file):
    for i in file:
        if i.lower().endswith(files_expansion['images']):       #картинки
            sort_files(args.path,os.path.join(root,i), i,'images') 
        elif i.lower().endswith(files_expansion['video']):     #відео
            sort_files(args.path,os.path.join(root,i), i,'video')       
        elif i.lower().endswith(files_expansion['documents']) :  #доки
            sort_files(args.path,os.path.join(root,i), i,'documents')
        elif i.lower().endswith(files_expansion['music']):     #музыка
            sort_files(args.path,os.path.join(root,i), i,'music')   
        elif i.lower().endswith(files_expansion['archives']):    #архивы
            sort_files(args.path,os.path.join(root,i), i,'archives')
        else:
            sort_files(args.path,os.path.join(root,i), i,'')
    if root != args.path:
        os.rmdir(root)
            
            

def sort_files(parent_dir, current_path, current_file,name_dir):
    
    if not (os.path.exists(os.path.join(parent_dir+'\\' + name_dir))):
        os.mkdir(parent_dir + '\\' + name_dir)
    path_replace = os.path.join(parent_dir,name_dir,
                                          normalize(current_file))
    os.replace(current_path, path_replace)
    if name_dir =='archives':
        shutil.unpack_archive(path_replace,path_replace
                              .replace(expanssion,''))

threads_search_file = [threading.Thread(target=search_file, args=(root,dirr,file))
            for root,dirr,file in os.walk(args.path)]
for thread in threads_search_file:
    thread.start()
for thread in threads_search_file:
    thread.join()


threads_sort_file = [threading.Thread(target=check_expansion, args=(root,file))
            for root,file in need_files.items()]
for thread in threads_sort_file:
    thread.start()
for thread in threads_sort_file:
    thread.join()

