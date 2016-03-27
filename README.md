配置:

    config.language = 'zh-cn';
    config.filebrowserBrowseUrl = '/static/filemanager/index.html';
    config.filebrowserUploadUrl = '/uploader';

制作过程可以参考:
https://segmentfault.com/a/1190000002436865

工程可以参考:
https://github.com/zrq495/flask-ckfinder

配置参考:

http://docs.ckeditor.com/#!/guide/dev_file_browse_upload

上传图片后返回:
<script type="text/javascript">
    window.parent.CKEDITOR.tools.callFunction("0", "\/userfiles\/images\/Public%20Folder\/akgk451.png", "");
</script>
