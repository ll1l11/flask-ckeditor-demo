# -*- coding: utf-8 -*-
import random
from datetime import datetime
import os.path
from flask import (
    Blueprint, render_template, request, url_for, make_response, current_app,
    jsonify)
from flask.views import MethodView

from logic import CkFinder

bp = Blueprint('general', __name__)


def gen_rnd_filename():
    filename_prefix = datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/upload', methods=['post'])
def upload():
    """CKEditor file upload"""
    error = ''
    url = ''
    callback = request.args.get("CKEditorFuncNum")
    if request.method == 'POST' and 'upload' in request.files:
        fileobj = request.files['upload']
        fname, fext = os.path.splitext(fileobj.filename)
        rnd_name = '%s%s' % (gen_rnd_filename(), fext)
        filepath = os.path.join(current_app.static_folder, 'upload', rnd_name)
        # 检查路径是否存在，不存在则创建
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                error = 'ERROR_CREATE_DIR'
        elif not os.access(dirname, os.W_OK):
            error = 'ERROR_DIR_NOT_WRITEABLE'
        if not error:
            fileobj.save(filepath)
            url = url_for('static', filename='%s/%s' % ('upload', rnd_name))
    else:
        error = 'post error'
    res = """<script type="text/javascript">
  window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
</script>""" % (callback, url, error)
    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response


class GetInfoView(MethodView):
    def post(self):
        ckfinder = CkFinder()
        upload_path = request.form.get('currentpath', '')
        new_file = request.files['newfile']
        return ckfinder.upload(upload_path, new_file)

    def get(self):
        ckfinder = CkFinder()
        action = request.args.get('mode', '')
        if "getinfo" == action:
            info = ckfinder.get_info(request.args.get("path", ""))
            return jsonify(info)

        elif "getfolder" == action:
            return jsonify(ckfinder.get_dir_file(request.args.get("path", "")))

        elif "rename" == action:
            old_name = request.args.get("old", "")
            new_name = request.args.get("new", "")
            return ckfinder.rename(old_name, new_name)

        elif "delete" == action:
            path = request.args.get("path", "")
            return ckfinder.delete(path)

        elif "addfolder" == action:
            path = request.args.get("path", "")
            name = request.args.get("name", "")
            return ckfinder.addfolder(path, name)

        else:
            return "fail"


bp.add_url_rule('/filemanager/',
                view_func=GetInfoView.as_view('get_info'),
                endpoint='get_info')
