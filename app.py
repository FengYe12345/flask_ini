from flask import Flask, request, render_template, redirect, url_for
import configparser

app = Flask(__name__)
app.secret_key = 'iii'

class ConfHadndle:
    def __init__(self, conf_name):
        self.conf_name = conf_name
        self.config = configparser .ConfigParser()
        self.config.read(conf_name)

    # 获取所有节点
    def get_sections(self):
        return self.config.sections()

    # 获取一个节点下所有键值对,返回字典形式
    def get_items(self,section):
        return dict(self.config.items(section))

    # 获取某个value
    def get_value(self,section, option):
        return self.config.get(section, option)

#增加节点
    def add_sections(self,section,enable,cloud_id,ip,type,sleep,api_type):
        self.config.add_section(section)
        self.config.set(section, "enable", enable)
        self.config.set(section, "cloud_id", cloud_id)
        self.config.set(section, "ip", ip)
        self.config.set(section, "type", type)
        self.config.set(section, "sleep", sleep)
        self.config.set(section, "api_type", api_type)
        self.config.write(open("machine.ini", "w"))
# 修改option,如果不存在则会出创建
    def set_section(self,section,key,value):
        self.config.set(section,key,value)
        self.config.write(open('machine.ini','w'))
# 删除section和option
    def delete_section(self,section):
        self.config.remove_section(section)
        self.config.write(open('machine.ini','w'))



# test
# 创建配置文件类对象
conf = ConfHadndle("./machine.ini")


# 添加节点
@app.route('/add_section',methods=['POST','GET'])
def add_section():
    if request.method == 'POST':
        conf.add_sections(request.form['section'],request.form['enable'],request.form['cloud_id'],request.form['ip'],request.form['type'],request.form['sleep'],request.form['api_type'])
        return redirect(url_for('index'))
    return render_template('add_view.html')
# 主菜单
@app.route('/index',methods=['POST','GET'])
def index():
    return render_template('index.html')


# 修改option
@app.route('/set_option',methods=['POST','GET'])
def set_option():
    if request.method =='POST':
        conf.set_section(request.form['section'],request.form['key'],request.form['value'])
        return redirect(url_for('index'))
    return render_template('set_view.html')

# 删除section
@app.route('/delete_section',methods=['POST','GET'])
def delete_section():
    if request.method=='POST':
        conf.delete_section(request.form['section'])
        return redirect(url_for('index'))
    return render_template('delete_section.html')
# print (conf)
# print(conf.get_sections())
# items_value = conf.get_items("1901010101001")
# print (items_value)
# print(items_value["ip"])
#
# items_value = conf.get_value("1901010101001", "ip")
# print (items_value)



if __name__ == '__main__':
    app.run()
