# -*- coding: UTF-8 -*- 
import os
import os.path as op

from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
#from redis import Redis
from wtforms import fields, widgets

from sqlalchemy.event import listens_for
from jinja2 import Markup

from flask_admin import Admin, form
from flask_admin.form import rules
#from flask_admin.contrib import sqla, rediscli
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import ModelView
from wtforms.validators import DataRequired

app = Flask(__name__, static_folder='files')
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['DATABASE_FILE'] = 'sample_db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

# Create directory for file fields to use
file_path = op.join(op.dirname(__file__), 'files')
try:
    os.mkdir(file_path)
except OSError:
    pass

def build_sample_db():

    db.drop_all()
    db.create_all()

    images = ["Buffalo", "Elephant", "Leopard", "Lion", "Rhino"]
    for name in images:
        image = Student()
        image.name = name
        image.photopath = name.lower() + ".jpg"
        db.session.add(image)
    db.session.commit()
    return

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64))
    photopath = db.Column(db.Unicode(128))
    studentid = db.Column(db.Unicode(50))
    sex = db.Column(db.String(10))
    birthday = db.Column(db.String(20))
    nationality  = db.Column(db.String(20))
    shenfenid = db.Column(db.String(25))
    political = db.Column(db.String(10))
    nativeplace = db.Column(db.String(100))
    schoolzone = db.Column(db.String(100))
    admissiondate = db.Column(db.String(20))
    academy = db.Column(db.String(50))
    professional = db.Column(db.String(50))
    classname = db.Column(db.String(50))
    domitory = db.Column(db.String(50))
    xueli = db.Column(db.String(50))
    xuezhi = db.Column(db.String(50))
    xuewei = db.Column(db.String(50))
    foreignlanguage = db.Column(db.String(50))
    cultivate = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    qq = db.Column(db.String(50))
    instructorname = db.Column(db.String(50))
    email = db.Column(db.String(100))
    

    def __unicode__(self):
        return self.name

@listens_for(Student, 'after_delete')
def del_image(mapper, connection, target):
    if target.photopath:
        # Delete image
        try:
            os.remove(op.join(file_path, target.photopath))
        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(op.join(file_path,
                              form.thumbgen_filename(target.photopath)))
        except OSError:
            pass


class ImageView(sqla.ModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.photopath:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=form.thumbgen_filename(model.photopath)))

    column_formatters = {
        'photopath': _list_thumbnail
    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'photopath': form.ImageUploadField('Image',
                                      base_path=file_path,
                                      thumbnail_size=(100, 100, True))
    }

    can_export = True
    #export_max_rows = 100000
    export_types = ['csv','excel']

    #how many data in a page
    page_size = 10
    can_set_page_size = True
    #do not want to show a column in a page
    column_exclude_list = ['photopath', ]
    #column_list = ['name','Studentid','sex','shoolzone']
    #column_details_exclude_list = None
    #column_details_list = ['name']

    column_display_actions = True

    #search
    column_searchable_list = ['name','email']
    column_filters = ['name', 'email']
    #can edit on the page
    column_editable_list = ['name','sex']
    #modal window
    #create_modal = True
    edit_modal = True

    ##select choice
    form_choices = { 
        'sex': [
            ('MR', 'Mr'),
            ('MRS', 'Mrs')
        ]   
    }   

    ##remove fields from the create and edit forms
    #form_excluded_columns = ['last_name',]

    #column_labels = { 
    #    'name': '姓名',
    #    'sex': '性别'
    #}   
   
    ##sort 
    column_sortable_list = ('name',)

    ##
    can_view_details = True

    # Rename 'title' column in list view
    column_labels = {
        'name'          : '姓名',
        'photopath'       : '照片',
        'studentid'       : '学号',
        'sex'             : '性别',
        'birthday'        : '出生日期',
        'nationality'     : '民族',
        'shenfenid'       : '身份证号',
        'political'       : '政治面貌',
        'nativeplace'     : '籍贯',
        'schoolzone'      : '所在校区',
        'admissiondate'   : '入学时间',
        'academy'         : '学院',
        'professional'    : '专业',
        'classname'       : '班级',
        'domitory'        : '公寓宿舍号',
        'xueli'           : '学历',
        'xuezhi'          : '学制',
        'xuewei'          : '学位',
        'foreignlanguage' : '主修外语语种',
        'cultivate'       : '培养方式',
        'phone'           : '手机',
        'qq'              : 'QQ',
        'instructorname'  : '辅导员姓名',
        'email'           : 'E-mail'
    }

'''
    column_descriptions = dict(
        name='姓名',
        photopath = '照片',
        studentid = '学号',
        sex = '性别',
        birthday = '出生日期',
        nationality  = '民族',
        shenfenid = '身份证号',
        political = '政治面貌',
        nativeplace = '籍贯',
        schoolzone = '所在校区',
        admissiondate = '入学时间',
        academy = '学院',
        professional = '专业',
        classname = '班级',
        domitory = '公寓宿舍号',
        xueli = '学历',
        xuezhi = '学制',
        xuewei = '学位',
        foreignlanguage = '主修外语语种',
        cultivate = '培养方式',
        phone = '手机',
        qq = 'QQ',
        instructorname = '辅导员姓名',
        email = 'E-mail'
    )
'''

admin = Admin(app, name='学生管理系统', template_mode='bootstrap3')
# Add administrative views here
admin.add_view(ImageView(Student, db.session,name=u'学生管理'))


if __name__ == '__main__':
    app_dir = op.realpath(os.path.dirname(__file__))
    database_path = op.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        build_sample_db()
    app.run(host='0.0.0.0', port=5009, debug=True)
