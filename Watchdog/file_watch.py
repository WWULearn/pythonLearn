import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import schedule

# 分类规则字典（可扩展）
FILE_TYPES = {
    "图片": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "文档": [".pdf", ".docx", ".xlsx", ".pptx", ".txt"],
    "压缩包": [".zip", ".rar", ".7z", ".tar.gz"],
    "视频": [".mp4", ".mkv", ".avi", ".mov"],
    "音乐": [".mp3", ".wav", ".flac"],
    "代码": [".py", ".java", ".html", ".js", ".css"]
}


# 继承文件事件
class FileOrganizerHandler(FileSystemEventHandler):
    def on_modified(self, event):
        """当文件夹内文件发生变化时触发整理"""
        # folder_to_track = event.src_path
        # self.organize_files(folder_to_track)
        # 触发时机，只会在文件夹内文件修改时触发
        folder_to_watch = "F:/PythonProject/pythonLearn/Watchdog/fileText"
        self.organize_files(folder_to_watch)

    @staticmethod
    def organize_files(folder_path):
        """整理指定文件夹内的文件"""
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            # 跳过目录和隐藏文件
            if os.path.isdir(file_path) or filename.startswith('.'):
                continue

            # 获取文件拓展名
            name, ext = os.path.splitext(filename)
            ext = ext.lower()  # 统一小写

            # 匹配分类规则
            target_folder = None
            for category, extensions in FILE_TYPES.items():
                if ext in extensions:
                    target_folder = os.path.join(folder_path, category)
                    break

            # 未匹配的文件放入“其他”文件夹
            if not target_folder:
                target_folder = os.path.join(folder_path, "其他")

            # 创建目标文件夹（如果不存在）
            os.makedirs(target_folder, exist_ok=True)

            # 移动文件(避免覆盖)
            target_path = os.path.join(target_folder, filename)
            if not os.path.exists(target_path):
                shutil.move(file_path, target_path)
                print(f"已移动：{filename} -> {target_path}")
            else:
                # 处理重名文件
                timestamp = time.strftime("%Y%m%d%H%M%S")
                new_name = f"{name}_{timestamp}{ext}"
                target_path = os.path.join(target_folder, new_name)
                shutil.move(file_path, target_path)
                print(f"已重命名并移动: {filename} -> {target_path}")
    

def start_monitoring(foler_path):
    """启动文件夹实时监控"""
    event_handler = FileOrganizerHandler()
    observer = Observer()
    observer.schedule(event_handler, foler_path, recursive=False) # recursive->递归监视子目录事件
    observer.start()
    print(f"开始监控文件夹: {foler_path}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

def scheduled_organization(foler_path):
    FileOrganizerHandler.organize_files(foler_path)

if __name__ == "__main__":
    folder_to_watch = "F:/PythonProject/pythonLearn/Watchdog/fileText"  # 修改为你的监控路径
    # start_monitoring(folder_to_watch)

    # 每天凌晨3点整理一次，定时整理
    schedule.every().day.at("03:00").do(scheduled_organization, folder_to_watch)
    while True:
        schedule.run_pending()
        time.sleep(60)

        