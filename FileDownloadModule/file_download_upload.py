from flask import send_file, jsonify, make_response
import os

TEST_FILE_DOWNLOAD_DIR_NAME = "F://"


class FileDownloadController:
    def __init__(self):
        pass

    def DownloadFile(self, szFileName):
        file_path = TEST_FILE_DOWNLOAD_DIR_NAME + szFileName
        if os.path.isfile(file_path):
            print("file download:{}".format(file_path))
            response = make_response(send_file(file_path, as_attachment=True))
            response.headers["Content-Disposition"] = "attachment; filename={}".format(
                szFileName.encode().decode('latin-1'))
            # return send_file(file_path, as_attachment=True)
            return response
        else:
            return jsonify({"tips": "The downloaded file does not exist"})

    def UploadFile(self):
        pass


DownloadCtrl = FileDownloadController()


