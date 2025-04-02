import json
import re
import datetime

class NoteManager:
    def load_tasks(self, user):
        try:
            with open(f'{user}.json', 'r') as file:
               data = json.load(file)
            return data
        except FileNotFoundError:
            return []
        
    def save_tasks(self):
        with open(f'{self.user}.json', 'w') as file:
            json.dump(self.tasks, file, indent=4, ensure_ascii=False)
    
    def cmd_list(self):
        for task in self.tasks:
            yield task['name']
    
    def cmd_add(self, name):
        task = {
            'name': name,
            'desc': '',
            'status': '待完成',
            'dateTime': str(datetime.datetime.now()),
            'lastDateTime': str(datetime.datetime.now())
        }
        self.tasks.append(task)
        print(f'已添加任务:{task["name"]}')

        self.cmd_update(name)

    def _find_task(self, name):
        """通过名称查找任务，返回字典或 None"""
        for task in self.tasks:
            if task["name"] == name:
                return task
        return {}

    def cmd_update(self, name):
        # 遍历所有任务，查找名称匹配的任务
        task = self._find_task(name)
        print(type(task))

        if not task:
            print(f"错误：任务 '{name}' 不存在！")
            return

        while True:
            cmd = input(f'任务：{name},请输入需要执行的操作(update+key+value/look/exit) ').strip().split()
            
            action = cmd[0]

            if action == 'update':
                try:
                    key, value = cmd[1], " ".join(cmd[2:])
                    task[key] = value
                    task['lastDateTime'] = str(datetime.datetime.now())
                    name = value if key == 'name' else name
                    print('更新成功')
                    print(task)
                except Exception:
                    print('输入错误')
            elif action == 'look':
                print(task)
            elif action == 'exit':
                break
            else:
                print('输入错误')

    def cmd_del(self, name):
        task = self._find_task(name)

        if not task:
            print(f"错误：任务 '{name}' 不存在！")
            return
        else:
            self.tasks.remove(task)
            print('已删除')

    @staticmethod
    def remove_special_chars(text):
        # 匹配除了字母、数字、_以外的字符
        pattern = r'[^a-zA-Z0-9_]+'
        return re.sub(pattern, '', text)

    def run(self):
        while True:
            command = input("请输入命令(add/update/list/delete/exit)+任务名称 ").strip().split()
            if not command:
                continue
            
            action = command[0].lower()

            # 需要任务名称的命令（add/update/del）必须检查参数长度
            if action in ("add", "update", "del"):
                if len(command) < 2:
                    print("错误：缺少任务名称！")
                    continue
                name = " ".join(command[1:])  # 合并名称中的空格（如"学习 Python"）
            else:
                name = None  # 不需要名称的命令

            if action == 'add':
                self.cmd_add(name)
            elif action == 'update':
                self.cmd_update(name)
            elif action == 'delete':
                self.cmd_del(name)
            elif action == 'list':
                print(list(self.cmd_list()))
            elif action == 'exit':
                self.save_tasks()
                print("任务已保存，程序退出！")
                exit()
            else:
                print('命令错误')

    def __init__(self, user):
        self.user = user
        self.tasks = self.load_tasks(user)

if __name__ == '__main__':
    while True:
        user_input = input("请输入用户名（数字、字母） ").strip()
        user = NoteManager.remove_special_chars(user_input)
        if not user:
            print('请输入数字和字母_组合 ')
            continue
        break

    print(f'*****{user}*****')
    ob = NoteManager(user)
    ob.run()
    


