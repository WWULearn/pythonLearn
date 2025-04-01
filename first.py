import json
import re
import datetime

class test:
    def load_tasks(user):
        try:
            with open('{user}.json', 'r') as file:
               data = json.load(file)
        except FileNotFoundError:
            return {}
    
    def cmd_list(self):
        for task in self.tasks:
            yield task['name']
    
    def cmd_add(self, name):
        task = {'name': name,
                        'desc': '',
                        'datetime': str(datetime.datetime.now())}
        print(f'已添加任务:{task["name"]}')

    def remove_special_chars(text):
        # 匹配除了字母、数字、_以外的字符
        pattern = r'[^a-zA-Z0-9_]+'
        return re.sub(pattern, '', text)

    def run(self):
        while True:
            command = input("请输入命令(add/update/list/delete/exit)+任务名称").strip().split()
            if not command:
                continue
            
            action = command[0].lower()

            if action == 'add':
                self.cmd_add(command[1])
            elif action == 'list':
                print(list(self.cmd_list()))
            elif action == 'exit':
                exit()

    def __init__(self, user):
        self.tasks = self.load_tasks(user)

if __name__ == '__main__':
    while True:
        user = test.remove_special_chars(input("请输入用户名（数字、字母）").strip())
        if user == '':
            print('请输入数字和字母组合')
            continue
        break
    
    ob = test(user)
    ob.run()


